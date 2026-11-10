"""Draw a seeded sample of the gated EditLens dataset as a second corpus cell.

The pilot corpus is famous public-domain prose and agent-written mirrors of
it. This cell has neither weakness: its human documents are ordinary
unpublished writing, and its generated documents come from the detector's
own labeled data. Rows are drawn at random from one split of
pangram/editlens_iclr among `human_written` and `ai_generated` documents
whose word count falls inside the given range. Nothing is selected on a
detector score.

The corpus (document text) and the job list go under `iclr/`, which is
ignored by git because the dataset is gated and may not be redistributed.
`iclr_sample.json` records the split, seed, and the ids, classes, sources,
and word counts of the drawn rows, so the same sample can be rebuilt by
anyone with dataset access.

Jobs: every generated document gets a job whose caller says a model wrote
it. Every human document gets a job whose caller says they wrote it, which
selects Preserve, and a job with no statement, which measures what the
unstated-origin default costs a human draft.

Usage:
  python sample_iclr.py --split test --per-class 10 --seed 20261109
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from _common import die, gate_message, is_gate_error, log, make_job, word_count, write_jsonl

DATASET = "pangram/editlens_iclr"
CLASSES = {"human_written": "human", "ai_generated": "ai"}


def main() -> None:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="test")
    ap.add_argument("--per-class", type=int, default=10)
    ap.add_argument("--seed", type=int, default=20261109)
    ap.add_argument("--min-words", type=int, default=200)
    ap.add_argument("--max-words", type=int, default=400)
    ap.add_argument("--out-dir", default=str(here / "iclr"))
    ap.add_argument("--sample-file", default=str(here / "iclr_sample.json"))
    args = ap.parse_args()

    from datasets import load_dataset

    try:
        ds = load_dataset(DATASET, split=args.split)
    except Exception as exc:  # noqa: BLE001
        if is_gate_error(exc):
            die(gate_message(DATASET, "dataset"))
        raise

    rng = random.Random(args.seed)
    docs = []
    for text_type, source_class in CLASSES.items():
        pool = [
            r for r in ds
            if r["text_type"] == text_type and args.min_words <= word_count(r["text"]) <= args.max_words
        ]
        pool.sort(key=lambda r: r["text_id"])
        if len(pool) < args.per_class:
            die(f"only {len(pool)} {text_type} rows fit the word range")
        for r in rng.sample(pool, args.per_class):
            docs.append(
                {
                    "id": f"iclr/{source_class}/{r['text_id']}",
                    "cell": "iclr",
                    "source_class": source_class,
                    "text": r["text"],
                    "words": word_count(r["text"]),
                    "meta": {"text_type": text_type, "source": r["source"], "generator": r["model"], "split": args.split},
                }
            )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(exist_ok=True)
    (out_dir / "outputs").mkdir(exist_ok=True)
    write_jsonl(out_dir / "corpus.jsonl", docs)
    jobs = []
    for d in docs:
        if d["source_class"] == "ai":
            jobs.append(make_job(d, "generated"))
        else:
            jobs += [make_job(d, "own"), make_job(d, "unstated")]
    write_jsonl(out_dir / "jobs.jsonl", jobs)

    sample = {
        "dataset": DATASET,
        "split": args.split,
        "seed": args.seed,
        "word_range": [args.min_words, args.max_words],
        "documents": [{"id": d["id"], "words": d["words"], **d["meta"]} for d in docs],
    }
    Path(args.sample_file).write_text(json.dumps(sample, indent=1) + "\n", encoding="utf-8")
    log(f"wrote {len(docs)} documents and {len(jobs)} jobs under {out_dir}; ids in {args.sample_file}")


if __name__ == "__main__":
    main()
