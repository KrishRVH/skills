"""Score documents with Pangram's live detector through its text API.

This is the benchmark the skill is judged against. The two open EditLens
models are more lenient than the live model: a text they read as human can
read as AI-generated here, so they only rule candidates out.

Each document goes to POST /task once. The result is polled and stored
without any text: the verdict, the class fractions, and each passage's
label, confidence, class probabilities, and humanizer score. Rows already
in --out are skipped, so a rerun never pays twice for one document.

The API bills by the word, so --max-words is required. Documents are taken
in input order until the next one would pass the cap. Keep samples small
and paired: the same documents before and after a change, three at a time,
widened only when a verdict moves.

The key is read from PANGRAM_API_KEY, or from --key-file. Pangram's terms
forbid using the service through anything but its own software, so the web
checker must not be scripted; the API is the supported route.

Usage:
  python score_pangram.py --input outputs.jsonl --text-field output_text \\
      --out scores_pangram_outputs.jsonl --max-words 500 --dry-run
  python score_pangram.py --input corpus.jsonl --ids pilot/ai/darwin-origin \\
      --out scores_pangram_source.jsonl --max-words 300
  python score_pangram.py --summarize scores_pangram_outputs.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

from _common import MIN_WORDS, die, log, read_jsonl, word_count

API = "https://text.external-api.pangram.com"
DEFAULT_KEY_FILE = Path.home() / ".config" / "pangram" / "api_key"
DOLLARS_PER_WORD = 0.0005
POLL_SECONDS = 2
RESULT_FIELDS = (
    "headline",
    "prediction_short",
    "fraction_ai",
    "fraction_ai_assisted",
    "fraction_human",
    "num_ai_segments",
    "num_ai_assisted_segments",
    "num_human_segments",
)
WINDOW_FIELDS = (
    "label",
    "ai_assistance_score",
    "confidence",
    "word_count",
    "start_index",
    "end_index",
    "is_humanized",
    "humanizer_score",
    "class_probabilities",
)
METADATA_FIELDS = ("job_id", "id", "cell", "source_class", "origin", "regime", "budget")
GROUP_FIELDS = ("cell", "source_class", "origin", "regime")


def row_key(row: dict) -> str:
    return row.get("job_id") or row["id"]


def call(method: str, path: str, key: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(API + path, data=data, method=method)
    request.add_header("x-api-key", key)
    request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")[:300]
        die(f"{method} {path} failed with HTTP {error.code}: {detail}")


def detect(text: str, key: str, model: str, wait: float) -> dict:
    task = call("POST", "/task", key, {"text": text, "model": model, "public_dashboard_link": False})
    deadline = time.monotonic() + wait
    while time.monotonic() < deadline:
        result = call("GET", f"/task/{task['task_id']}", key)
        if result.get("stage") == "STAGE_SUCCESS":
            return result
        if result.get("stage") == "STAGE_FAILED":
            die(f"task {task['task_id']} failed: {json.dumps(result)[:300]}")
        time.sleep(POLL_SECONDS)
    die(f"task {task['task_id']} did not finish within {wait:.0f} s")


def text_free(row: dict, result: dict) -> dict:
    record = {field: row[field] for field in METADATA_FIELDS if field in row}
    record["model"] = "pangram_live"
    record["model_version"] = result.get("version")
    record.update({field: result.get(field) for field in RESULT_FIELDS})
    record["windows"] = [
        {field: window[field] for field in WINDOW_FIELDS if field in window}
        for window in result.get("windows", [])
    ]
    return record


def highest_humanizer_score(record: dict) -> float | None:
    scores = [window["humanizer_score"] for window in record["windows"] if "humanizer_score" in window]
    return max(scores) if scores else None


def summarize(records: list[dict]) -> None:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for record in records:
        groups[tuple(record.get(field) for field in GROUP_FIELDS)].append(record)
    print("| " + " | ".join(GROUP_FIELDS) + " | n | verdicts | mean AI | mean assisted | mean human | humanized documents | mean highest humanizer score |")
    print("|" + " --- |" * (len(GROUP_FIELDS) + 7))
    for group, members in sorted(groups.items(), key=lambda item: [str(part) for part in item[0]]):
        verdicts = Counter(member["headline"] for member in members)
        humanized = sum(any(window.get("is_humanized") for window in member["windows"]) for member in members)
        scores = [score for score in map(highest_humanizer_score, members) if score is not None]

        def mean(field: str) -> str:
            return f"{sum(member[field] for member in members) / len(members):.2f}"

        print(
            "| "
            + " | ".join("" if part is None else str(part) for part in group)
            + f" | {len(members)} | "
            + ", ".join(f"{count} {name}" for name, count in sorted(verdicts.items()))
            + f" | {mean('fraction_ai')} | {mean('fraction_ai_assisted')} | {mean('fraction_human')}"
            + f" | {humanized} of {len(members)} | "
            + (f"{sum(scores) / len(scores):.2f}" if scores else "n/a")
            + " |"
        )


def read_key(args: argparse.Namespace) -> str:
    key = os.environ.get("PANGRAM_API_KEY", "").strip()
    if not key and args.key_file.exists():
        key = args.key_file.read_text(encoding="utf-8").strip()
    if not key:
        die(f"no API key: set PANGRAM_API_KEY or save the key to {args.key_file}")
    return key


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--input", help="JSONL file with one document per row")
    ap.add_argument("--text-field", default="text")
    ap.add_argument("--out", help="text-free score rows; appended to, never rewritten")
    ap.add_argument("--ids", help="comma-separated job ids or ids to send; default is every row in input order")
    ap.add_argument("--max-words", type=int, help="stop before the run would send more words than this")
    ap.add_argument("--model", default="pangram-4", help="model selector sent to the API")
    ap.add_argument("--key-file", type=Path, default=DEFAULT_KEY_FILE)
    ap.add_argument("--wait", type=float, default=180, help="seconds to wait for one document")
    ap.add_argument("--dry-run", action="store_true", help="list what would be sent and its cost; send nothing")
    ap.add_argument("--summarize", metavar="SCORES", help="print the verdict table for a scores file and exit")
    args = ap.parse_args()

    if args.summarize:
        summarize(read_jsonl(args.summarize))
        return
    if not (args.input and args.out and args.max_words):
        die("--input, --out, and --max-words are required unless --summarize is given")

    rows = read_jsonl(args.input)
    if args.ids:
        wanted = set(args.ids.split(","))
        unknown = wanted - {row_key(row) for row in rows}
        if unknown:
            die(f"ids not in {args.input}: {sorted(unknown)}")
        rows = [row for row in rows if row_key(row) in wanted]
    done = {row_key(record) for record in read_jsonl(args.out)} if Path(args.out).exists() else set()

    plan, words = [], 0
    for row in rows:
        text = row.get(args.text_field)
        if row_key(row) in done:
            continue
        if not text or word_count(text) < MIN_WORDS:
            log(f"skip {row_key(row)}: under {MIN_WORDS} words or no `{args.text_field}` field")
            continue
        if words + word_count(text) > args.max_words:
            log(f"stopping before {row_key(row)}: it would pass --max-words {args.max_words}")
            break
        plan.append(row)
        words += word_count(text)
    log(f"{len(plan)} documents, {words} words, about ${words * DOLLARS_PER_WORD:.2f}; {len(done)} already scored")

    if args.dry_run:
        for row in plan:
            print(f"{word_count(row[args.text_field]):>5} words  {row_key(row)}")
        return

    if plan:
        key = read_key(args)
        with open(args.out, "a", encoding="utf-8") as handle:
            for row in plan:
                record = text_free(row, detect(row[args.text_field], key, args.model, args.wait))
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                handle.flush()
                log(f"{record['headline']}  {row_key(row)}")
    summarize(read_jsonl(args.out))


if __name__ == "__main__":
    main()
