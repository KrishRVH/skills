"""Score documents with the Open Pangram EditLens models.

  --model roberta  loads pangram/editlens_roberta-large with
                   AutoModelForSequenceClassification.
  --model llama    loads the gated base meta-llama/Llama-3.2-3B in bf16 with
                   num_labels read from the adapter repo (adapter_config.json,
                   then config.json, then the score head shape inside
                   adapter_model.safetensors; never hardcoded), then applies
                   the pangram/editlens_Llama-3.2-3B adapter with PeftModel.

Text is tokenized into 512-token windows with stride 256 and scored in
batches (default 16 for llama, 64 for roberta). A regression head
(num_labels == 1) writes the mean window value as `regression_value` and
`expected_ai_fraction`. A classification head softmaxes each window,
averages the distributions, and computes `expected_ai_fraction` as the
probability-weighted sum of bucket centers from --bucket-map (a JSON list
in label order; the shipped file is a placeholder and the script refuses to
run until it is filled). `argmax_bucket` is the most likely bucket.

Every output row carries `id`, `model`, `model_revision`, `n_windows`, the
scores, and every input metadata field. Documents under 50 words are
skipped and logged. All four Pangram and Llama repos are gated; without
`hf auth login` and accepted terms the script exits with a message naming
that step.

Usage:
  python score_editlens.py --model roberta --input corpus.jsonl --out scores_roberta.jsonl
  python score_editlens.py --model llama --input corpus.jsonl --out scores_llama.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _common import (
    MIN_WORDS,
    WINDOW_STRIDE,
    WINDOW_TOKENS,
    die,
    dtype_kwargs,
    hub_revision,
    iter_windows,
    load_bucket_map,
    log,
    read_jsonl,
    require_hub_file,
    word_count,
    write_jsonl,
)

ROBERTA_REPO = "pangram/editlens_roberta-large"
LLAMA_ADAPTER = "pangram/editlens_Llama-3.2-3B"
LLAMA_BASE = "meta-llama/Llama-3.2-3B"
DEFAULT_BATCH = {"roberta": 64, "llama": 16}


def adapter_head_info(adapter_repo: str) -> tuple[int, dict | None]:
    """Return (num_labels, id2label) for a PEFT sequence-classification adapter."""
    cfg = json.loads(Path(require_hub_file(adapter_repo, "adapter_config.json")).read_text())
    if "num_labels" in cfg:
        return int(cfg["num_labels"]), cfg.get("id2label")
    from huggingface_hub import hf_hub_download

    try:
        cfg_path = hf_hub_download(adapter_repo, "config.json")
        hf_cfg = json.loads(Path(cfg_path).read_text())
        if "id2label" in hf_cfg:
            return len(hf_cfg["id2label"]), hf_cfg["id2label"]
        if "num_labels" in hf_cfg:
            return int(hf_cfg["num_labels"]), None
    except Exception as exc:  # noqa: BLE001
        if type(exc).__name__ not in {"EntryNotFoundError"}:
            log(f"note: could not read config.json from {adapter_repo}: {type(exc).__name__}")
    from safetensors import safe_open

    weights = require_hub_file(adapter_repo, "adapter_model.safetensors")
    with safe_open(weights, framework="pt") as fh:
        for key in fh.keys():
            if "score" in key and key.endswith("weight"):
                shape = fh.get_slice(key).get_shape()
                if len(shape) == 2:
                    log(f"num_labels inferred from {key} shape {shape}")
                    return int(shape[0]), None
    die(f"could not determine num_labels for {adapter_repo}")
    return 0, None  # unreachable


def load_model(which: str):
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    if which == "roberta":
        require_hub_file(ROBERTA_REPO, "config.json")
        tokenizer = AutoTokenizer.from_pretrained(ROBERTA_REPO)
        model = AutoModelForSequenceClassification.from_pretrained(ROBERTA_REPO)
        info = {"model": "editlens_roberta", "model_repo": ROBERTA_REPO, "model_revision": hub_revision(ROBERTA_REPO)}
        id2label = model.config.id2label
    else:
        from peft import PeftModel

        num_labels, id2label = adapter_head_info(LLAMA_ADAPTER)
        require_hub_file(LLAMA_BASE, "config.json")
        try:
            tokenizer = AutoTokenizer.from_pretrained(LLAMA_ADAPTER)
        except Exception:  # noqa: BLE001
            tokenizer = AutoTokenizer.from_pretrained(LLAMA_BASE)
        model = AutoModelForSequenceClassification.from_pretrained(
            LLAMA_BASE, num_labels=num_labels, **dtype_kwargs(torch.bfloat16)
        )
        model = PeftModel.from_pretrained(model, LLAMA_ADAPTER)
        info = {
            "model": "editlens_llama",
            "model_repo": LLAMA_ADAPTER,
            "model_revision": hub_revision(LLAMA_ADAPTER),
            "base_model_repo": LLAMA_BASE,
            "base_model_revision": hub_revision(LLAMA_BASE),
        }
        if id2label is None:
            id2label = {i: f"LABEL_{i}" for i in range(num_labels)}
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    model.config.pad_token_id = tokenizer.pad_token_id
    model = model.to("cuda").eval()
    num_labels = int(getattr(model.config, "num_labels", 1))
    labels = [str(id2label[k]) if k in id2label else str(id2label.get(str(k), k)) for k in range(num_labels)]
    return tokenizer, model, info, num_labels, labels


def main() -> None:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", choices=["roberta", "llama"], required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--batch-size", type=int, help="default 64 for roberta, 16 for llama")
    ap.add_argument("--text-field", default="text")
    ap.add_argument("--bucket-map", default=str(here / "bucket_map.json"))
    ap.add_argument("--max-length", type=int, default=WINDOW_TOKENS)
    ap.add_argument("--stride", type=int, default=WINDOW_STRIDE)
    args = ap.parse_args()
    batch_size = args.batch_size or DEFAULT_BATCH[args.model]

    import torch

    if not torch.cuda.is_available():
        die("CUDA is not available; this script expects the RTX 4090")

    tokenizer, model, info, num_labels, labels = load_model(args.model)
    regression = num_labels == 1
    centers = None if regression else load_bucket_map(args.bucket_map, num_labels)
    log(f"{info['model']}: num_labels={num_labels} head={'regression' if regression else 'classification'} labels={labels}")

    special = tokenizer.num_special_tokens_to_add()
    content = args.max_length - special
    docs = []
    for row in read_jsonl(args.input):
        text = row.get(args.text_field)
        if not text:
            log(f"skip {row.get('id')}: no `{args.text_field}` field")
            continue
        if word_count(text) < MIN_WORDS:
            log(f"skip {row.get('id')}: under {MIN_WORDS} words")
            continue
        ids = tokenizer(text, add_special_tokens=False)["input_ids"]
        wins = [tokenizer.build_inputs_with_special_tokens(w) for w in iter_windows(ids, content, args.stride)]
        docs.append((row, wins))

    pending = [(d, w) for d, (_, wins) in enumerate(docs) for w in wins]
    outputs: dict[int, list] = {d: [] for d in range(len(docs))}
    for start in range(0, len(pending), batch_size):
        chunk = pending[start : start + batch_size]
        batch = tokenizer.pad({"input_ids": [w for _, w in chunk]}, return_tensors="pt").to("cuda")
        with torch.inference_mode():
            logits = model(**batch).logits.float()
        if regression:
            values = logits.squeeze(-1).tolist()
        else:
            values = torch.softmax(logits, dim=-1).tolist()
        for (d, _), v in zip(chunk, values):
            outputs[d].append(v)
        log(f"scored windows {start + len(chunk)}/{len(pending)}")

    out_rows = []
    for d, (row, wins) in enumerate(docs):
        record = {k: v for k, v in row.items() if k != args.text_field}
        record.update(info)
        record["n_windows"] = len(wins)
        vals = outputs[d]
        if regression:
            value = sum(vals) / len(vals)
            record["regression_value"] = value
            record["expected_ai_fraction"] = value
            record["argmax_bucket"] = None
        else:
            probs = [sum(v[k] for v in vals) / len(vals) for k in range(num_labels)]
            record["bucket_probs"] = probs
            record["expected_ai_fraction"] = sum(p * c for p, c in zip(probs, centers))
            arg = max(range(num_labels), key=lambda k: probs[k])
            record["argmax_bucket"] = arg
            record["argmax_label"] = labels[arg]
        out_rows.append(record)
    n = write_jsonl(args.out, out_rows)
    log(f"wrote {n} rows to {args.out}")


if __name__ == "__main__":
    main()
