"""Score documents with the Open Pangram EditLens models.

The procedure follows the reference inference script in
https://github.com/pangramlabs/EditLens (scripts/inference.py):

  - text is cleaned the way the models were trained: emoji demojized, any
    reasoning block and chatbot header paragraph dropped, lowercased, and
    whitespace collapsed
  - the cleaned text is tokenized once and truncated to the model's training
    length (512 tokens for roberta, 1024 for llama); `truncated` records
    whether anything was cut
  - the head is a classifier over n buckets ordered from human (0) to
    AI-generated (n - 1); `editlens_score` is the expected bucket divided by
    n - 1, so it lies in [0, 1], and `bucket` is the most likely bucket

  --model roberta  loads pangram/editlens_roberta-large.
  --model llama    loads the gated base meta-llama/Llama-3.2-3B in 4-bit NF4
                   with the LayerNorm-plus-Linear score head the adapter was
                   trained with, then applies pangram/editlens_Llama-3.2-3B.

Input is either a JSONL file (--input) or a split of the gated
pangram/editlens_iclr dataset (--iclr-split). Dataset rows keep `text_id` as
`id`, carry `label` as human, ai_assisted, or ai_generated, and rename the
dataset's `model` column to `generator` so it cannot collide with the
detector name.

Every output row carries `id`, `model`, `model_revision`, the scores, and
every input metadata field. Documents under 50 words are skipped and logged.
The Pangram and Llama repos are gated; without `hf auth login` and accepted
terms the script exits with a message naming that step.

Usage:
  python score_editlens.py --model roberta --input corpus.jsonl --out scores_roberta_source.jsonl
  python score_editlens.py --model llama --iclr-split val --out scores_llama_iclr_val.jsonl
"""

from __future__ import annotations

import argparse
import re

from _common import (
    MIN_WORDS,
    die,
    gate_message,
    hub_revision,
    is_gate_error,
    log,
    read_jsonl,
    require_hub_file,
    word_count,
    write_jsonl,
)

ROBERTA_REPO = "pangram/editlens_roberta-large"
LLAMA_ADAPTER = "pangram/editlens_Llama-3.2-3B"
LLAMA_BASE = "meta-llama/Llama-3.2-3B"
DATASET = "pangram/editlens_iclr"
MAX_LENGTH = {"roberta": 512, "llama": 1024}
DEFAULT_BATCH = {"roberta": 64, "llama": 8}
LABELS = {"human_written": "human", "ai_edited": "ai_assisted", "ai_generated": "ai_generated"}
HEADER_STARTS = ("Sure", "Here", "Abstract", "Title", "I'm happy to help", "Certainly")


def clean_text(text: str) -> str:
    """Apply the EditLens training-time text normalization."""
    import emoji

    text = emoji.demojize(text)
    if "</think>" in text:
        text = text.split("</think>")[1].strip()
    paragraphs = [p for p in text.split("\n") if p.strip()]
    if len(paragraphs) > 1:
        first = emoji.replace_emoji(re.sub(r"^[^a-zA-Z0-9]*", "", paragraphs[0]), "")
        if first.startswith(HEADER_STARTS):
            text = "\n".join(paragraphs[1:])
    return re.sub(r"\s+", " ", text.lower()).strip()


def score_head_buckets(adapter_repo: str) -> int:
    """Read the bucket count from the adapter's saved score head."""
    from safetensors import safe_open

    with safe_open(require_hub_file(adapter_repo, "adapter_model.safetensors"), framework="pt") as fh:
        for key in fh.keys():
            if "score" in key and key.endswith("linear.weight"):
                return int(fh.get_slice(key).get_shape()[0])
    die(f"no score head weights found in {adapter_repo}")
    return 0  # unreachable


def load_model(which: str):
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    if which == "roberta":
        require_hub_file(ROBERTA_REPO, "config.json")
        tokenizer = AutoTokenizer.from_pretrained(ROBERTA_REPO)
        model = AutoModelForSequenceClassification.from_pretrained(ROBERTA_REPO).to("cuda")
        info = {"model": "editlens_roberta", "model_repo": ROBERTA_REPO, "model_revision": hub_revision(ROBERTA_REPO)}
    else:
        from peft import PeftModel
        from transformers import BitsAndBytesConfig

        class NormedLinear(torch.nn.Module):
            def __init__(self, hidden_size: int, num_labels: int, device) -> None:
                super().__init__()
                self.norm = torch.nn.LayerNorm(hidden_size, device=device)
                self.linear = torch.nn.Linear(hidden_size, num_labels, bias=False, device=device)

            def forward(self, x):
                return self.linear(self.norm(x.to(self.norm.weight.dtype)))

        n_buckets = score_head_buckets(LLAMA_ADAPTER)
        require_hub_file(LLAMA_BASE, "config.json")
        tokenizer = AutoTokenizer.from_pretrained(LLAMA_BASE)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "left"
        base = AutoModelForSequenceClassification.from_pretrained(
            LLAMA_BASE,
            num_labels=n_buckets,
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16
            ),
        )
        base.config.pad_token_id = tokenizer.pad_token_id
        base.score = NormedLinear(base.config.hidden_size, n_buckets, next(base.parameters()).device)
        model = PeftModel.from_pretrained(base, LLAMA_ADAPTER)
        info = {
            "model": "editlens_llama",
            "model_repo": LLAMA_ADAPTER,
            "model_revision": hub_revision(LLAMA_ADAPTER),
            "base_model_repo": LLAMA_BASE,
            "base_model_revision": hub_revision(LLAMA_BASE),
        }
    return tokenizer, model.eval(), info


def iclr_rows(split: str, limit: int | None) -> list[dict]:
    from datasets import load_dataset

    try:
        ds = load_dataset(DATASET, split=split)
    except Exception as exc:  # noqa: BLE001
        if is_gate_error(exc):
            die(gate_message(DATASET, "dataset"))
        raise
    if limit:
        ds = ds.select(range(min(limit, len(ds))))
    rows = []
    for r in ds:
        rows.append(
            {
                "id": r["text_id"],
                "text": r["text"],
                "label": LABELS.get(r["text_type"]),
                "text_type": r["text_type"],
                "generator": r["model"],
                "source": r["source"],
                "split": split,
            }
        )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", choices=["roberta", "llama"], required=True)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--input", help="JSONL file with one document per row")
    src.add_argument("--iclr-split", help=f"split of {DATASET}: val, test, test_enron, test_llama, or train")
    ap.add_argument("--limit", type=int, help="score only the first N rows of the dataset split")
    ap.add_argument("--out", required=True)
    ap.add_argument("--batch-size", type=int, help="default 64 for roberta, 8 for llama")
    ap.add_argument("--text-field", default="text")
    args = ap.parse_args()
    batch_size = args.batch_size or DEFAULT_BATCH[args.model]
    max_length = MAX_LENGTH[args.model]

    import torch

    if not torch.cuda.is_available():
        die("CUDA is not available; this script expects the RTX 4090")

    rows = iclr_rows(args.iclr_split, args.limit) if args.iclr_split else read_jsonl(args.input)
    tokenizer, model, info = load_model(args.model)
    n_buckets = int(model.config.num_labels)
    log(f"{info['model']}: {n_buckets} buckets, max_length={max_length}")

    docs = []
    for row in rows:
        text = row.get(args.text_field)
        if not text:
            log(f"skip {row.get('id')}: no `{args.text_field}` field")
            continue
        if word_count(text) < MIN_WORDS:
            log(f"skip {row.get('id')}: under {MIN_WORDS} words")
            continue
        cleaned = clean_text(text)
        full = len(tokenizer(cleaned)["input_ids"])
        ids = tokenizer(cleaned, truncation=True, max_length=max_length)["input_ids"]
        docs.append((row, ids, full > len(ids)))

    order = sorted(range(len(docs)), key=lambda i: len(docs[i][1]))
    probs: dict[int, list[float]] = {}
    for start in range(0, len(order), batch_size):
        chunk = order[start : start + batch_size]
        batch = tokenizer.pad({"input_ids": [docs[i][1] for i in chunk]}, return_tensors="pt").to("cuda")
        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
            logits = model(**batch).logits
        for i, p in zip(chunk, torch.softmax(logits.float(), dim=-1).tolist()):
            probs[i] = p
        if (start // batch_size) % 20 == 0:
            log(f"scored {start + len(chunk)}/{len(order)}")

    out_rows = []
    for i, (row, _, truncated) in enumerate(docs):
        p = probs[i]
        record = {k: v for k, v in row.items() if k != args.text_field}
        record.update(info)
        record["truncated"] = truncated
        record["bucket_probs"] = p
        record["bucket"] = max(range(n_buckets), key=lambda k: p[k])
        record["editlens_score"] = sum(k * pk for k, pk in enumerate(p)) / (n_buckets - 1)
        out_rows.append(record)
    n = write_jsonl(args.out, out_rows)
    log(f"wrote {n} rows to {args.out}")


if __name__ == "__main__":
    main()
