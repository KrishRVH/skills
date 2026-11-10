"""Plan Animize jobs and merge the outputs an agent session produces.

The Animize skill runs inside an agent session, not in this harness. This
script has two subcommands:

  jobs   Emit jobs.jsonl with one row per document and caller statement.
         Each row carries the source text, the statement the session passes
         to the skill as the caller's own words (`caller_statement`, or null
         for a bare request), and the regime that statement must select.
  merge  Validate agent-produced files (outputs/*.jsonl, rows with job_id,
         output_text, notes, regime_assigned, asked_question), join them to
         their jobs, write outputs.jsonl, and report missing jobs and
         unattended-run failures.

The skill takes no settings, so a job varies one thing: what the caller says
about who wrote the draft. `own` (the caller wrote it) must select the
Preserve regime, and is emitted once per budget, the maximum model-added
token share that clause_diff.py enforces. `generated` and `unstated` must
select Recompose, and an `unstated` run must carry the origin note. A
question put to the caller is a failure for every job.

Usage:
  python run_animize.py jobs --corpus corpus.jsonl \
      --origins own,generated,unstated --budgets 0.05,0.15,0.30 --out jobs.jsonl
  python run_animize.py merge --jobs jobs.jsonl --outputs 'outputs/*.jsonl' \
      --out outputs.jsonl
"""

from __future__ import annotations

import argparse
import glob
from pathlib import Path

from _common import CALLER_STATEMENTS, ORIGIN_NOTE, PRESERVE_BUDGET, die, log, make_job, read_jsonl, write_jsonl

REQUIRED_OUTPUT_FIELDS = ("job_id", "output_text", "notes", "regime_assigned", "asked_question")


def csv_list(value: str) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


def make_jobs(args: argparse.Namespace) -> None:
    origins = csv_list(args.origins)
    budgets = [float(b) for b in csv_list(args.budgets)]
    bad = [o for o in origins if o not in CALLER_STATEMENTS]
    if bad:
        die(f"unknown origin: {', '.join(bad)}")
    docs = read_jsonl(args.corpus)
    jobs = []
    for doc in docs:
        for origin in origins:
            for budget in budgets if origin == "own" else [PRESERVE_BUDGET]:
                jobs.append(make_job(doc, origin, budget))
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
    asked = [r["job_id"] for r in merged.values() if r["asked_question"]]
    wrong = [r["job_id"] for r in merged.values() if r["regime_assigned"] != r["regime"]]
    no_note = [
        r["job_id"] for r in merged.values() if r.get("origin") == "unstated" and ORIGIN_NOTE not in r["notes"]
    ]
    log(f"unattended-run failures: {len(asked)} questions, {len(wrong)} wrong regimes, {len(no_note)} missing origin notes")
    for label, ids in (("asked a question", asked), ("wrong regime", wrong), ("no origin note", no_note)):
        for jid in ids:
            log(f"  {label}: {jid}")
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
    j.add_argument("--origins", default="own,generated,unstated")
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
