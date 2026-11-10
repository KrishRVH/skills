"""Compare how often people and models use the constructions a rule targets.

A rule that rewrites a construction on sight assumes readers take it as a
machine default. This script checks that assumption against labeled text:
for each construction it reports the share of documents that contain it and
its rate per 1,000 words, separately for the `human_written` and
`ai_generated` rows of one split of pangram/editlens_iclr. It also reports
sentence-length spread and runs of adjacent sentences of similar length.

The counts are regular-expression matches, so they overcount and undercount
at the edges. The dataset's generated rows come from the models it lists,
which predate the current ones. Read a large ratio as a direction, not a
measurement.

Usage:
  python construction_rates.py --split test --out construction_rates.json
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path

from _common import die, gate_message, is_gate_error, log

DATASET = "pangram/editlens_iclr"
CLASSES = ("human_written", "ai_generated")

CONSTRUCTIONS = {
    "in order to": r"\bin order to\b",
    "the fact that": r"\bthe fact that\b",
    "there is/are/was/were": r"\bthere (?:is|are|was|were|'s)\b",
    "it is important to note": r"\bit(?: is|'s) (?:important|worth) (?:to note|noting)\b",
    "contraction": r"\b\w+(?:n't|'re|'ve|'ll|'d|'m)\b|\b(?:it|that|there|here|what|who|he|she|let)'s\b",
    "rather than": r"\brather than\b",
    "instead of": r"\binstead of\b",
    "not just/only/merely ... but": r"\bnot (?:just|only|merely|simply)\b[^.?!]{0,80}\bbut\b",
    "negation, then correction": r"\b(?:is|are|was|were|does|do|did)(?:n't| not)\b[^.?!]{0,80}[.;]\s+(?:It|They|This|That|He|She|We)(?:'s|'re| is| are| was| were)\b",
    "should not be confused with": r"\b(?:should not|shouldn't|not to) be confused with\b",
    "perhaps/maybe/probably": r"\b(?:perhaps|maybe|probably)\b",
    "tends to": r"\btend(?:s|ed)? to\b",
    "I think/guess/suppose": r"\bI (?:think|guess|suppose|believe)\b",
    "please": r"\bplease\b",
    "just": r"\bjust\b",
    "simply": r"\bsimply\b",
    "because": r"\bbecause\b",
}

SENTENCE_END = re.compile(r"(?<=[.?!])[\"')\]]*\s+(?=[\"'(\[]*[A-Z0-9])")
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’-]*")


def sentence_lengths(text: str) -> list[int]:
    out = []
    for para in text.split("\n"):
        for sent in SENTENCE_END.split(para.strip()):
            n = len(WORD.findall(sent))
            if n:
                out.append(n)
    return out


def longest_similar_run(lengths: list[int], tolerance: float) -> int:
    """Longest run of adjacent sentences each within `tolerance` of the run's first."""
    best = run = 1 if lengths else 0
    start = 0
    for i in range(1, len(lengths)):
        base = lengths[start]
        if abs(lengths[i] - base) <= max(2, tolerance * base):
            run += 1
        else:
            start, run = i, 1
        best = max(best, run)
    return best


def summarize(texts: list[str], tolerance: float) -> dict:
    patterns = {k: re.compile(v, re.IGNORECASE) for k, v in CONSTRUCTIONS.items()}
    patterns["negation, then correction"] = re.compile(CONSTRUCTIONS["negation, then correction"])
    words = 0
    hits = {k: 0 for k in patterns}
    docs_with = {k: 0 for k in patterns}
    spreads, means, runs3, runs4 = [], [], 0, 0
    for text in texts:
        text = text.replace("’", "'")
        words += len(WORD.findall(text))
        for k, pat in patterns.items():
            n = len(pat.findall(text))
            hits[k] += n
            docs_with[k] += bool(n)
        lengths = sentence_lengths(text)
        if len(lengths) >= 5:
            means.append(statistics.mean(lengths))
            spreads.append(statistics.pstdev(lengths) / statistics.mean(lengths))
            run = longest_similar_run(lengths, tolerance)
            runs3 += run >= 3
            runs4 += run >= 4
    n = len(texts)
    return {
        "documents": n,
        "words": words,
        "constructions": {
            k: {"share_of_documents": round(docs_with[k] / n, 4), "per_1000_words": round(1000 * hits[k] / words, 3)}
            for k in patterns
        },
        "sentences": {
            "documents_with_5_or_more": len(means),
            "mean_length": round(statistics.mean(means), 2),
            "mean_spread": round(statistics.mean(spreads), 3),
            "share_with_run_of_3": round(runs3 / len(means), 4),
            "share_with_run_of_4": round(runs4 / len(means), 4),
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="test")
    ap.add_argument("--tolerance", type=float, default=0.2, help="relative length difference that still counts as similar")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    from datasets import load_dataset

    try:
        ds = load_dataset(DATASET, split=args.split)
    except Exception as exc:  # noqa: BLE001
        if is_gate_error(exc):
            die(gate_message(DATASET, "dataset"))
        raise

    result = {"dataset": DATASET, "split": args.split, "tolerance": args.tolerance, "classes": {}}
    for text_type in CLASSES:
        texts = [r["text"] for r in ds if r["text_type"] == text_type]
        result["classes"][text_type] = summarize(texts, args.tolerance)
        log(f"{text_type}: {len(texts)} documents")
    Path(args.out).write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")

    human, model = (result["classes"][c] for c in CLASSES)
    print(f"{'construction':34} {'human docs':>10} {'model docs':>10} {'human /1k':>10} {'model /1k':>10} {'model:human':>11}")
    for k in CONSTRUCTIONS:
        h, m = human["constructions"][k], model["constructions"][k]
        ratio = m["per_1000_words"] / h["per_1000_words"] if h["per_1000_words"] else float("inf")
        print(f"{k:34} {h['share_of_documents']:>10.3f} {m['share_of_documents']:>10.3f} {h['per_1000_words']:>10.3f} {m['per_1000_words']:>10.3f} {ratio:>11.2f}")
    for k in human["sentences"]:
        print(f"{k:34} {human['sentences'][k]:>10} {model['sentences'][k]:>10}")


if __name__ == "__main__":
    main()
