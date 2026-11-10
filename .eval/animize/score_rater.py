"""Score one rater's reading-room answers against the hidden keys.

The reading-room page exports a JSON object with `pairs`, `reads`, `edit`,
and `closing`. This script unblinds it with `rating_key.json` (which side of
each pair was the skill's output) and `reading_room_key.json` (the class of
each single passage, and the draft the rater edited) and prints Markdown:

  - pairwise preference per cell: how often the rater would publish the
    output, with the strength of each pick, the "more deliberately written"
    pick, the meaning check, and the guess at which side was the original
  - single-passage ratings per class: publish decision, deliberateness, and
    perceived authorship (1 person to 7 machine)
  - the rater's own edit of one defect draft: which injected defects it
    removed and its clause-diff accounting, beside the skill's Preserve
    output on the same draft

Usage:
  python score_rater.py --answers rater_answers.json
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from _common import PRESERVE_BUDGET, read_jsonl
from clause_diff import diff_row

STRENGTHS = ("toss", "slight", "clear", "strong")
DEFECT_LABELS = ("generic opening", "generic closing", "filler phrase", "-ing significance tail", "empty adverb")


def subject(job_id: str) -> str:
    return job_id.split("/")[2].split("__")[0]


def pair_section(answers: dict, key: list[dict]) -> None:
    cells: dict[str, list[dict]] = defaultdict(list)
    for item in key:
        a = answers.get(str(item["item"]))
        if not a:
            continue
        out = "A" if item["A"] == "output" else "B"
        guess = a.get("orig")
        cells[item["cell"]].append(
            {
                "item": item["item"],
                "subject": subject(item["job_id"]),
                "publish": "output" if a["q1"] == out else "source",
                "strength": a["strength"],
                "deliberate": "output" if a["q2"] == out else "source",
                "meaning": "same" if a["q3"] == "same" else ("output changed it" if a["q3"] == out else "source changed it"),
                "original_guess": "none" if guess in (None, "unsure") else ("output" if guess == out else "source"),
                "note": bool(a.get("notes", "").strip()),
            }
        )
    print("### Pairwise preference\n")
    print("| Cell | n | Would publish output | Output more deliberate | Same meaning | Guessed source as original | Strength of output picks | Strength of source picks |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for cell, rows in cells.items():
        n = len(rows)

        def tally(side: str) -> str:
            picks = [r["strength"] for r in rows if r["publish"] == side]
            return ", ".join(f"{picks.count(s)} {s}" for s in STRENGTHS if picks.count(s)) or "none"

        print(
            f"| {cell} | {n} | {sum(r['publish'] == 'output' for r in rows)}/{n} | "
            f"{sum(r['deliberate'] == 'output' for r in rows)}/{n} | {sum(r['meaning'] == 'same' for r in rows)}/{n} | "
            f"{sum(r['original_guess'] == 'source' for r in rows)}/{n} | {tally('output')} | {tally('source')} |"
        )
    print("\n| Item | Cell | Subject | Would publish | Strength | Original guess | Note left |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for cell, rows in cells.items():
        for r in rows:
            print(f"| {r['item']} | {cell} | {r['subject']} | {r['publish']} | {r['strength']} | {r['original_guess']} | {'yes' if r['note'] else 'no'} |")
    print()


def read_section(answers: dict, key: list[dict]) -> None:
    classes: dict[str, list[dict]] = defaultdict(list)
    for item in key:
        a = answers.get(str(item["n"]))
        if a:
            classes[item["class"]].append({**a, "subject": subject(item["ref"])})
    print("### Single passages\n")
    print("| Class | n | Publish as is | With light edits | No | Mean deliberateness (1-7) | Mean authorship (1 person, 7 machine) | Authorship scores |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for cls, rows in classes.items():
        n = len(rows)
        delib = [int(r["deliberate"]) for r in rows]
        auth = [int(r["authorship"]) for r in rows]
        pub = [r["publish"] for r in rows]
        each = ", ".join(r["subject"] + " " + r["authorship"] for r in rows)
        print(
            f"| {cls} | {n} | {pub.count('yes')} | {pub.count('light')} | {pub.count('no')} | "
            f"{sum(delib) / n:.2f} | {sum(auth) / n:.2f} | {each} |"
        )
    print()


def edit_section(edit: dict, ref: str, defects_dir: Path, outputs: list[dict]) -> None:
    stem = ref.split("/")[-1]
    source = (defects_dir / f"{stem}.txt").read_text(encoding="utf-8").strip()
    injected = json.loads((defects_dir / f"{stem}.json").read_text(encoding="utf-8"))["injected"]
    versions = {"rater edit": edit["text"].strip()}
    for o in outputs:
        if o["id"] == ref and o["regime"] == "preserve" and o["budget"] == PRESERVE_BUDGET:
            versions[f"skill, Preserve {PRESERVE_BUDGET:g}"] = o["output_text"]
    print(f"### Edit of `{ref}`\n")
    print("| Version | " + " | ".join(DEFECT_LABELS) + " | Kept | Edited | Deleted | Added | Added-token share |")
    print("| --- | " + " | ".join("---" for _ in DEFECT_LABELS) + " | --- | --- | --- | --- | --- |")
    for name, text in versions.items():
        removed = ["removed" if s.strip(" ,") not in text else "left in" for s in injected]
        summary, _ = diff_row(source, text)
        c = summary["counts"]
        print(
            f"| {name} | " + " | ".join(removed) + f" | {c['kept']} | {c['lexically_edited']} | {c['deleted']} | "
            f"{c['added']} | {summary['model_token_share']:.3f} |"
        )
    print()


def main() -> None:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--answers", required=True, help="JSON exported by the reading-room page")
    ap.add_argument("--pair-key", default=str(here / "rating_key.json"))
    ap.add_argument("--read-key", default=str(here / "reading_room_key.json"))
    ap.add_argument("--outputs", default=str(here / "outputs.jsonl"))
    ap.add_argument("--corpus", default=str(here / "corpus"))
    args = ap.parse_args()

    answers = json.loads(Path(args.answers).read_text(encoding="utf-8"))
    read_key = json.loads(Path(args.read_key).read_text(encoding="utf-8"))
    print(f"## Rater {answers.get('rater', 'unknown')}, exported {answers.get('exported', 'unknown')[:10]}\n")
    pair_section(answers.get("pairs") or {}, json.loads(Path(args.pair_key).read_text(encoding="utf-8")))
    read_section(answers.get("reads") or {}, read_key["read"])
    edit = (answers.get("edit") or {}).get("1")
    if edit and edit.get("text"):
        ref = read_key["edit"]
        cell, source_class, _ = ref.split("/")
        edit_section(edit, ref, Path(args.corpus) / cell / source_class, read_jsonl(args.outputs))


if __name__ == "__main__":
    main()
