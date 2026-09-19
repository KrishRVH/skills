"""Summarize a pilot run: detector deltas, Preserve accounting, defect repair, routing.

Reads the merged outputs, the Binoculars scores for sources and outputs, the
clause diffs, the routing decisions, and the defect sidecars, and prints a
Markdown summary to stdout. Every table is labeled with its n. Nothing here
calibrates a threshold; the "below lowest strong-human source" column is an
uncalibrated reference line, not a verdict.

Usage:
  python summarize_pilot.py --outputs outputs.jsonl \
      --source-scores scores_binoculars_source.jsonl \
      --output-scores scores_binoculars_outputs.jsonl \
      --diffs diffs.jsonl --routing outputs/routing.jsonl \
      --defects corpus/pilot/human_defect
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import statistics
from collections import defaultdict

DASHES = "\u2013\u2014"
NUM_RE = re.compile(r"\b\d[\d,.]*\b")


def read_jsonl(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def mean(xs):
    return statistics.fmean(xs) if xs else float("nan")


def median(xs):
    return statistics.median(xs) if xs else float("nan")


def fmt(x, nd=3):
    return "n/a" if x != x else f"{x:.{nd}f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--source-scores", required=True)
    ap.add_argument("--output-scores", required=True)
    ap.add_argument("--diffs", required=True)
    ap.add_argument("--routing")
    ap.add_argument("--defects", help="directory of human_defect sidecar json files")
    args = ap.parse_args()

    outputs = read_jsonl(args.outputs)
    src_scores = {r["id"]: r["binoculars_score"] for r in read_jsonl(args.source_scores)}
    out_scores = {r.get("job_id", r["id"]): r["binoculars_score"] for r in read_jsonl(args.output_scores)}
    diffs = {r.get("job_id", r["id"]): r for r in read_jsonl(args.diffs)}

    strong_human = [v for k, v in src_scores.items() if "/human/" in k]
    ref_line = min(strong_human) if strong_human else float("nan")

    print("## Pilot summary\n")
    print(f"Outputs: {len(outputs)}. Source documents scored: {len(src_scores)}. "
          f"Uncalibrated reference line = lowest strong-human source score = {fmt(ref_line)}.\n")

    # 1. Source scores per class
    print("### Binoculars on sources (lower = more model-like)\n")
    print("| Source class | n | mean | median | min | max |")
    print("| --- | --- | --- | --- | --- | --- |")
    by_class = defaultdict(list)
    for k, v in src_scores.items():
        by_class[k.split("/")[1]].append(v)
    for c, xs in sorted(by_class.items()):
        print(f"| {c} | {len(xs)} | {fmt(mean(xs))} | {fmt(median(xs))} | {fmt(min(xs))} | {fmt(max(xs))} |")
    print()

    # 2. Output deltas per cell
    print("### Binoculars on outputs, paired with their sources\n")
    print("| Source class | Regime | Budget | n | source mean | output mean | mean delta | outputs lower than source | outputs below reference line (source below) |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    groups = defaultdict(list)
    for o in outputs:
        groups[(o["source_class"], o["regime"], o["budget"])].append(o)
    for (sc, rg, b), rows in sorted(groups.items()):
        pairs = [(src_scores.get(o["id"]), out_scores.get(o["job_id"])) for o in rows]
        pairs = [(s, t) for s, t in pairs if s is not None and t is not None]
        if not pairs:
            print(f"| {sc} | {rg} | {b} | 0 | | | | | scores missing |")
            continue
        s_m = mean([s for s, _ in pairs]); t_m = mean([t for _, t in pairs])
        d = mean([t - s for s, t in pairs])
        lower = sum(1 for s, t in pairs if t < s)
        below = sum(1 for _, t in pairs if t < ref_line)
        below_src = sum(1 for s, _ in pairs if s < ref_line)
        print(f"| {sc} | {rg} | {b} | {len(pairs)} | {fmt(s_m)} | {fmt(t_m)} | {fmt(d, 4)} | {lower} | {below} ({below_src}) |")
    print()

    # 3. Preserve accounting
    print("### Preserve clause-diff accounting\n")
    print("| Source class | Budget | n | kept | edited | deleted | added | reordered | mean share | max share | within budget | violations |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for (sc, rg, b), rows in sorted(groups.items()):
        if rg != "preserve":
            continue
        ds = [diffs[o["job_id"]] for o in rows if o["job_id"] in diffs]
        if not ds:
            print(f"| {sc} | {b} | 0 | diffs missing |")
            continue
        tot = defaultdict(int)
        for d in ds:
            for k, v in d["counts"].items():
                tot[k] += v
            tot["reordered"] += d.get("reordered", 0)
        shares = [d["model_token_share"] for d in ds]
        wb = sum(1 for d in ds if d["within_budget"])
        viol = sum(1 for d in ds if d["violation"])
        print(f"| {sc} | {b} | {len(ds)} | {tot['kept']} | {tot['lexically_edited']} | {tot['deleted']} | {tot['added']} | {tot['reordered']} | {fmt(mean(shares))} | {fmt(max(shares))} | {wb}/{len(ds)} | {viol} |")
    print()
    added = [(o["job_id"], diffs[o["job_id"]]["added_clauses"]) for o in outputs
             if o["regime"] == "preserve" and o["job_id"] in diffs and diffs[o["job_id"]]["counts"]["added"]]
    if added:
        print("Added clauses under Preserve (each is a violation):\n")
        for jid, cl in added:
            for c in cl:
                print(f"- `{jid}`: {c}")
        print()

    # 4. Defect repair
    if args.defects:
        print("### Injected-defect repair on human_defect drafts\n")
        side = {}
        for p in glob.glob(os.path.join(args.defects, "*.json")):
            with open(p, encoding="utf-8") as fh:
                side[os.path.splitext(os.path.basename(p))[0]] = json.load(fh)["injected"]
        labels = ["generic opening", "generic closing", "filler phrase", "-ing significance tail", "empty adverb"]
        print("| Regime | Budget | n | " + " | ".join(labels) + " | all five |")
        print("| --- | --- | --- | " + " | ".join("---" for _ in labels) + " | --- |")
        for (sc, rg, b), rows in sorted(groups.items()):
            if sc != "human_defect":
                continue
            hits = [0] * 5; allfive = 0
            for o in rows:
                stem = o["id"].split("/")[-1]
                inj = side.get(stem)
                if not inj:
                    continue
                out = o["output_text"]
                rep = [s.strip(" ,") not in out for s in inj]
                for i, r in enumerate(rep):
                    hits[i] += r
                allfive += all(rep)
            print(f"| {rg} | {b} | {len(rows)} | " + " | ".join(f"{h}/{len(rows)}" for h in hits) + f" | {allfive}/{len(rows)} |")
        print()

    # 5. Exact-number preservation and dashes
    print("### Automated fidelity checks\n")
    print("| Source class | Regime | Budget | n | source numbers missing from output | outputs with a generated dash |")
    print("| --- | --- | --- | --- | --- | --- |")
    for (sc, rg, b), rows in sorted(groups.items()):
        miss = 0; dash = 0
        for o in rows:
            src_nums = set(NUM_RE.findall(o["source_text"]))
            out_nums = set(NUM_RE.findall(o["output_text"]))
            miss += len(src_nums - out_nums)
            src_has = any(ch in o["source_text"] for ch in DASHES)
            if any(ch in o["output_text"] for ch in DASHES) and not src_has:
                dash += 1
        print(f"| {sc} | {rg} | {b} | {len(rows)} | {miss} | {dash} |")
    print()

    # 6. Routing
    if args.routing and os.path.exists(args.routing):
        print("### Routing decisions\n")
        rows = read_jsonl(args.routing)
        print("| Hidden class | Caller statement | n | preserve | recompose | ask | wrong guesses |")
        print("| --- | --- | --- | --- | --- | --- | --- |")
        agg = defaultdict(lambda: defaultdict(int))
        for r in rows:
            c = r["id"].split("/")[1]
            agg[c][r["regime_assigned"]] += 1
        stmt = {"human": "says it is their draft", "human_defect": "none", "ai": "none"}
        wrong_total = 0
        for c in ["human", "human_defect", "ai"]:
            d = agg.get(c, {})
            n = sum(d.values())
            if c == "human":
                wrong = n - d.get("preserve", 0)
            else:
                wrong = d.get("preserve", 0)
            wrong_total += wrong
            print(f"| {c} | {stmt[c]} | {n} | {d.get('preserve',0)} | {d.get('recompose',0)} | {d.get('ask',0)} | {wrong} |")
        n_all = len(rows)
        print(f"\nWrong guesses: {wrong_total}/{n_all} (a wrong guess is Preserve without a caller statement, or anything but Preserve with one). "
              f"Routing accuracy without a wrong guess: {fmt(1 - wrong_total / n_all if n_all else float('nan'))}.\n")


if __name__ == "__main__":
    main()
