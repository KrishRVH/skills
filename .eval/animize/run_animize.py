"""Plan Animize jobs and merge the outputs an agent session produces.

The Animize skill runs inside an agent session, not in this harness. This
script has two subcommands:

  jobs   Emit jobs.jsonl with one row per (document, pass, regime, budget)
         combination. Each row carries the source text and a `controls`
         hint (pass, voice, regime) the session should apply.
  merge  Validate agent-produced files (outputs/*.jsonl, rows with job_id,
         output_text, notes, regime_assigned, asked_question), join them to
         their jobs, write outputs.jsonl, and report missing jobs.

Regimes map to skill controls: `preserve` means voice=preserve (the deep
pass's Preserve regime); `recompose` means voice=rebuild (the Recompose
regime). The budget is the maximum model-added token share
that clause_diff.py enforces under the preserve regime.

Usage:
  python run_animize.py jobs --corpus corpus.jsonl --passes quick,deep \
      --regimes preserve,recompose --budgets 0.05,0.15,0.30 --out jobs.jsonl
  python run_animize.py merge --jobs jobs.jsonl --outputs 'outputs/*.jsonl' \
      --out outputs.jsonl
"""

from __future__ import annotations

import argparse
import glob
from pathlib import Path

from _common import die, log, read_jsonl, write_jsonl

PASSES = {"quick", "deep"}
REGIMES = {
    "preserve": {"voice": "preserve", "regime": "preserve"},
    "recompose": {"voice": "rebuild", "regime": "recompose"},
}
REQUIRED_OUTPUT_FIELDS = ("job_id", "output_text", "notes", "regime_assigned", "asked_question")


def csv_list(value: str) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


def make_jobs(args: argparse.Namespace) -> None:
    passes = csv_list(args.passes)
    regimes = csv_list(args.regimes)
    budgets = [float(b) for b in csv_list(args.budgets)]
    bad = [p for p in passes if p not in PASSES] + [r for r in regimes if r not in REGIMES]
    if bad:
        die(f"unknown pass or regime: {', '.join(bad)}")
    docs = read_jsonl(args.corpus)
    jobs = []
    for doc in docs:
        for p in passes:
            for r in regimes:
                for b in budgets:
                    job = {
                        "job_id": f"{doc['id']}__{p}__{r}__{b:g}",
                        "id": doc["id"],
                        "cell": doc.get("cell"),
                        "source_class": doc.get("source_class"),
                        "pass": p,
                        "regime": r,
                        "budget": b,
                        "controls": {"pass": p, **REGIMES[r]},
                        "source_text": doc["text"],
                    }
                    meta = doc.get("meta") or {}
                    if "regime_expected" in meta:
                        job["regime_expected"] = meta["regime_expected"]
                    elif "regime_expected" in doc:
                        job["regime_expected"] = doc["regime_expected"]
                    jobs.append(job)
    n = write_jsonl(args.out, jobs)
    log(f"wrote {n} jobs for {len(docs)} documents to {args.out}")


def merge(args: argparse.Namespace) -> None:
    jobs = {j["job_id"]: j for j in read_jsonl(args.jobs)}
    files = sorted(glob.glob(args.outputs))
    if not files:
        die(f"no output files match `{args.outputs}`")
    merged: dict[str, dict] = {}
    problems = 0
    for path in files:
        for n, row in enumerate(read_jsonl(path), 1):
            missing = [f for f in REQUIRED_OUTPUT_FIELDS if f not in row]
            if missing:
                log(f"{path}:{n}: missing fields {missing}")
                problems += 1
                continue
            if not isinstance(row["output_text"], str) or not row["output_text"].strip():
                log(f"{path}:{n}: empty output_text")
                problems += 1
                continue
            if not isinstance(row["asked_question"], bool):
                log(f"{path}:{n}: asked_question must be true or false")
                problems += 1
                continue
            jid = row["job_id"]
            if jid not in jobs:
                log(f"{path}:{n}: unknown job_id `{jid}`")
                problems += 1
                continue
            if jid in merged:
                log(f"{path}:{n}: duplicate job_id `{jid}`, keeping the later row")
            record = dict(jobs[jid])
            record.update(row)
            merged[jid] = record
    missing_jobs = [jid for jid in jobs if jid not in merged]
    n = write_jsonl(args.out, (merged[j] for j in jobs if j in merged))
    log(f"wrote {n} merged rows to {args.out}; {problems} invalid rows; {len(missing_jobs)} jobs missing")
    if missing_jobs:
        missing_path = Path(args.out).with_name("missing_jobs.txt")
        missing_path.write_text("\n".join(missing_jobs) + "\n", encoding="utf-8")
        log(f"missing job ids written to {missing_path}")
        for jid in missing_jobs[:20]:
            log(f"  missing: {jid}")
        if len(missing_jobs) > 20:
            log(f"  ... and {len(missing_jobs) - 20} more")
    if args.strict and (missing_jobs or problems):
        die("strict mode: incomplete or invalid outputs")


def main() -> None:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)

    j = sub.add_parser("jobs", help="emit jobs.jsonl")
    j.add_argument("--corpus", default=str(here / "corpus.jsonl"))
    j.add_argument("--passes", default="quick,deep")
    j.add_argument("--regimes", default="preserve,recompose")
    j.add_argument("--budgets", default="0.05,0.15,0.30")
    j.add_argument("--out", default=str(here / "jobs.jsonl"))
    j.set_defaults(func=make_jobs)

    m = sub.add_parser("merge", help="validate and merge agent outputs")
    m.add_argument("--jobs", default=str(here / "jobs.jsonl"))
    m.add_argument("--outputs", default=str(here / "outputs" / "*.jsonl"), help="glob of agent output files")
    m.add_argument("--out", default=str(here / "outputs.jsonl"))
    m.add_argument("--strict", action="store_true", help="exit nonzero when jobs are missing or rows are invalid")
    m.set_defaults(func=merge)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
