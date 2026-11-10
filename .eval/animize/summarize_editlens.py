"""Summarize EditLens scores for sources and outputs, with calibrated verdicts.

Reads source scores and output scores from score_editlens.py, the merged
outputs they belong to, and calibration.json, and prints Markdown: one table
of sources per class and one table of outputs per (source class, regime,
budget) cell, each paired with its own sources.

The verdict is the three-class reading of calibrate.py: a score at or below
the 1% false-positive threshold is human, a score beyond the macro-F1
threshold is ai_generated, and anything between is ai_assisted. Verdicts are
EditLens verdicts on an open research model, never production verdicts.

With `--export`, one row per job is also written with scores, verdicts,
word counts, and (given `--diffs`) the clause-diff counts, and with no
document text. That file is safe to track for a corpus whose text may not
be redistributed.

Usage:
  python summarize_editlens.py --outputs outputs.jsonl \
      --source-scores scores_roberta_source.jsonl \
      --output-scores scores_roberta_outputs.jsonl --calibration calibration.json
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path

from _common import die, read_jsonl, word_count, write_jsonl

VERDICTS = ("human", "ai_assisted", "ai_generated")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--source-scores", required=True)
    ap.add_argument("--output-scores", required=True)
    ap.add_argument("--calibration", required=True)
    ap.add_argument("--diffs", help="clause diffs from clause_diff.py, for --export")
    ap.add_argument("--export", help="write one text-free row per job to this JSONL path")
    args = ap.parse_args()

    src_rows = read_jsonl(args.source_scores)
    out_rows = read_jsonl(args.output_scores)
    model = src_rows[0]["model"]
    entry = json.loads(Path(args.calibration).read_text())["models"].get(model)
    if entry is None:
        die(f"{args.calibration} has no thresholds for `{model}`")
    t_human = entry["thresholds"]["fpr_1pct"]["threshold"]
    t_generated = entry["thresholds"]["macro_f1"]["threshold"]

    def verdict(score: float) -> str:
        if score <= t_human:
            return "human"
        return "ai_generated" if score > t_generated else "ai_assisted"

    def tally(scores: list[float]) -> str:
        got = [verdict(s) for s in scores]
        return " / ".join(str(got.count(v)) for v in VERDICTS)

    src = {r["id"]: r["editlens_score"] for r in src_rows}
    out = {r["job_id"]: r["editlens_score"] for r in out_rows}
    print(f"## {model}, revision {src_rows[0].get('model_revision')}\n")
    print(
        f"Thresholds from the `{entry['split']}` split, {entry['date']}: human at or below {t_human:.4f}, "
        f"ai_generated above {t_generated:.4f}. Verdict columns read human / ai_assisted / ai_generated.\n"
    )

    print("### Sources\n")
    print("| Source class | n | Mean | Median | Min | Max | Verdicts |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    by_class: dict[str, list[float]] = defaultdict(list)
    for r in src_rows:
        by_class[r["source_class"]].append(r["editlens_score"])
    for cls, xs in sorted(by_class.items()):
        print(f"| {cls} | {len(xs)} | {statistics.fmean(xs):.3f} | {statistics.median(xs):.3f} | {min(xs):.3f} | {max(xs):.3f} | {tally(xs)} |")

    print("\n### Outputs, paired with their sources\n")
    print("| Source class | Regime | Budget | n | Source mean | Output mean | Mean delta | Outputs scoring lower | Source verdicts | Output verdicts | Verdict changed |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    cells: dict[tuple, list[tuple[float, float]]] = defaultdict(list)
    diffs = {d["job_id"]: d for d in read_jsonl(args.diffs)} if args.diffs else {}
    exported = []
    for o in read_jsonl(args.outputs):
        if o["id"] not in src or o["job_id"] not in out:
            continue
        a, b = src[o["id"]], out[o["job_id"]]
        cells[(o["source_class"], o["regime"], o["budget"])].append((a, b))
        row = {
            "job_id": o["job_id"],
            "source_class": o["source_class"],
            "regime": o["regime"],
            "budget": o["budget"],
            "source_words": word_count(o["source_text"]),
            "output_words": word_count(o["output_text"]),
            "model": model,
            "source_score": a,
            "output_score": b,
            "source_verdict": verdict(a),
            "output_verdict": verdict(b),
        }
        d = diffs.get(o["job_id"])
        if d:
            row.update(counts=d["counts"], reordered=d["reordered"], model_token_share=d["model_token_share"],
                       within_budget=d["within_budget"], violation=d["violation"])
        exported.append(row)
    for (cls, regime, budget), pairs in sorted(cells.items()):
        s = [a for a, _ in pairs]
        t = [b for _, b in pairs]
        changed = sum(verdict(a) != verdict(b) for a, b in pairs)
        print(
            f"| {cls} | {regime} | {budget:g} | {len(pairs)} | {statistics.fmean(s):.3f} | {statistics.fmean(t):.3f} | "
            f"{statistics.fmean(b - a for a, b in pairs):+.3f} | {sum(b < a for a, b in pairs)} | {tally(s)} | {tally(t)} | {changed} |"
        )
    print()
    if args.export:
        write_jsonl(args.export, exported)


if __name__ == "__main__":
    main()
