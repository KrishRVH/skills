"""Score documents with the Binoculars zero-shot detector.

Implements the Binoculars score in-file (no dependency on the reference
package). For each 512-token window (stride 256):

  observer log-perplexity  = mean over positions of -log p_observer(next token)
  cross-perplexity         = mean over positions of
                             sum_v p_observer(v) * -log p_performer(v)
  window score             = observer log-perplexity / cross-perplexity

The document score is the mean of its window scores. Lower means more
likely AI. The raw score, the two components, and the model revisions are
recorded per document along with every input metadata field.

The default pair is ungated and fits on a 24 GB GPU in bf16:
`Qwen/Qwen2.5-1.5B` (observer) and `Qwen/Qwen2.5-1.5B-Instruct`
(performer). The two tokenizers must be identical; this is asserted.

With `--calibration`, thresholds stored under the `binoculars` model key
are applied and `verdict_*` fields are added.

Usage:
  python score_binoculars.py --input smoke.jsonl --out scores_binoculars_smoke.jsonl
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
    hub_revision,
    is_gate_error,
    gate_message,
    iter_windows,
    log,
    read_jsonl,
    word_count,
    write_jsonl,
)

DEFAULT_OBSERVER = "Qwen/Qwen2.5-1.5B"
DEFAULT_PERFORMER = "Qwen/Qwen2.5-1.5B-Instruct"


def load_pair(observer: str, performer: str, device: str):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    try:
        tok_o = AutoTokenizer.from_pretrained(observer)
        tok_p = AutoTokenizer.from_pretrained(performer)
    except Exception as exc:  # noqa: BLE001
        if is_gate_error(exc):
            die(gate_message(observer))
        raise
    if tok_o.get_vocab() != tok_p.get_vocab():
        die(f"tokenizers of {observer} and {performer} differ; Binoculars needs an identical vocabulary")
    probe = "The quick brown fox, said the observer; the performer agreed."
    if tok_o(probe)["input_ids"] != tok_p(probe)["input_ids"]:
        die("tokenizers produce different ids for the same text; refusing to score")
    if tok_o.pad_token is None:
        tok_o.pad_token = tok_o.eos_token
    tok_o.padding_side = "right"

    try:
        model_o = AutoModelForCausalLM.from_pretrained(observer, dtype=torch.bfloat16).to(device).eval()
        model_p = AutoModelForCausalLM.from_pretrained(performer, dtype=torch.bfloat16).to(device).eval()
    except Exception as exc:  # noqa: BLE001
        if is_gate_error(exc):
            die(gate_message(observer))
        raise
    return tok_o, model_o, model_p


def window_scores(batch_ids, batch_mask, model_o, model_p):
    """Return per-window (log_ppl, x_ppl) tensors for one padded batch."""
    import torch
    import torch.nn.functional as F

    with torch.inference_mode():
        logits_o = model_o(input_ids=batch_ids, attention_mask=batch_mask).logits
        logits_p = model_p(input_ids=batch_ids, attention_mask=batch_mask).logits
    targets = batch_ids[:, 1:]
    mask = batch_mask[:, 1:].to(torch.float32)
    log_ppls, x_ppls = [], []
    for k in range(batch_ids.shape[0]):
        lo = logits_o[k, :-1].float()
        lp = logits_p[k, :-1].float()
        m = mask[k]
        denom = m.sum().clamp(min=1.0)
        nll = F.cross_entropy(lo, targets[k], reduction="none")
        log_ppl = (nll * m).sum() / denom
        p_obs = F.softmax(lo, dim=-1)
        logp_perf = F.log_softmax(lp, dim=-1)
        xent = -(p_obs * logp_perf).sum(dim=-1)
        x_ppl = (xent * m).sum() / denom
        log_ppls.append(log_ppl.item())
        x_ppls.append(x_ppl.item())
        del lo, lp, p_obs, logp_perf
    return log_ppls, x_ppls


def apply_calibration(row: dict, cal: dict | None) -> None:
    if not cal:
        return
    entry = (cal.get("models") or {}).get("binoculars")
    if not entry:
        return
    score = row["binoculars_score"]
    for name, spec in (entry.get("thresholds") or {}).items():
        t = spec.get("threshold")
        if t is None:
            continue
        flagged = score < t if entry.get("direction", "lower_is_ai") == "lower_is_ai" else score > t
        row[f"verdict_{name}"] = "ai" if flagged else "human"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--observer", default=DEFAULT_OBSERVER)
    ap.add_argument("--performer", default=DEFAULT_PERFORMER)
    ap.add_argument("--calibration", help="calibration.json from calibrate.py")
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--text-field", default="text")
    ap.add_argument("--max-length", type=int, default=WINDOW_TOKENS)
    ap.add_argument("--stride", type=int, default=WINDOW_STRIDE)
    args = ap.parse_args()

    import torch

    if not torch.cuda.is_available():
        die("CUDA is not available; this script expects the RTX 4090")
    device = "cuda"
    cal = json.loads(Path(args.calibration).read_text()) if args.calibration else None

    rows = read_jsonl(args.input)
    tok, model_o, model_p = load_pair(args.observer, args.performer, device)
    rev_o, rev_p = hub_revision(args.observer), hub_revision(args.performer)

    docs = []
    for row in rows:
        text = row.get(args.text_field)
        if not text:
            log(f"skip {row.get('id')}: no `{args.text_field}` field")
            continue
        if word_count(text) < MIN_WORDS:
            log(f"skip {row.get('id')}: under {MIN_WORDS} words")
            continue
        ids = tok(text, add_special_tokens=False)["input_ids"]
        wins = list(iter_windows(ids, args.max_length, args.stride))
        docs.append((row, wins))

    pending = [(d, w) for d, (_, wins) in enumerate(docs) for w in wins]
    results: dict[int, list[tuple[float, float]]] = {d: [] for d in range(len(docs))}
    pad_id = tok.pad_token_id
    for start in range(0, len(pending), args.batch_size):
        chunk = pending[start : start + args.batch_size]
        width = max(len(w) for _, w in chunk)
        ids = torch.full((len(chunk), width), pad_id, dtype=torch.long)
        mask = torch.zeros((len(chunk), width), dtype=torch.long)
        for k, (_, w) in enumerate(chunk):
            ids[k, : len(w)] = torch.tensor(w)
            mask[k, : len(w)] = 1
        lp, xp = window_scores(ids.to(device), mask.to(device), model_o, model_p)
        for (d, _), a, b in zip(chunk, lp, xp):
            results[d].append((a, b))
        log(f"scored windows {start + len(chunk)}/{len(pending)}")

    out = []
    for d, (row, wins) in enumerate(docs):
        pairs = results[d]
        scores = [a / b if b else float("nan") for a, b in pairs]
        record = {k: v for k, v in row.items() if k != args.text_field}
        record.update(
            {
                "model": "binoculars",
                "observer": args.observer,
                "performer": args.performer,
                "observer_revision": rev_o,
                "performer_revision": rev_p,
                "model_revision": f"{rev_o}+{rev_p}" if rev_o and rev_p else None,
                "n_windows": len(wins),
                "observer_log_ppl": sum(a for a, _ in pairs) / len(pairs),
                "cross_ppl": sum(b for _, b in pairs) / len(pairs),
                "binoculars_score": sum(scores) / len(scores),
                "window_scores": [round(s, 5) for s in scores],
            }
        )
        apply_calibration(record, cal)
        out.append(record)
    n = write_jsonl(args.out, out)
    log(f"wrote {n} rows to {args.out}")
    for r in out:
        print(f"{r.get('id')}\t{r['binoculars_score']:.4f}")


if __name__ == "__main__":
    main()
