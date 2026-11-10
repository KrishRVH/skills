"""Write contraction variants of each draft so a detector can score them apart.

A run changes many things at once, so a score that moves after it does not
say which change moved it. This script isolates one change. For each job it
writes four texts: the source, the source with contractions inserted, the
output, and the output with its contractions spelled out. Scoring the four
shows what contractions alone do to a detector's reading.

The substitutions are regular expressions. They cover the common auxiliary
and pronoun forms and nothing else, and they ignore stress, so a variant is
a probe for a detector and never text to deliver.

Usage:
  python contraction_variants.py --outputs idiom/workplace/outputs.jsonl \\
      --out idiom/workplace/contractions.jsonl
  python score_editlens.py --model llama --input idiom/workplace/contractions.jsonl \\
      --out idiom/workplace/scores_llama_contractions.jsonl
"""

from __future__ import annotations

import argparse
import re

from _common import die, log, read_jsonl, write_jsonl

CONTRACTION = re.compile(
    r"\b\w+(?:n't|'re|'ve|'ll|'d|'m)\b|\b(?:it|that|there|here|what|who|he|she|let)'s\b",
    re.IGNORECASE,
)

EXPAND = [
    (r"\bcan't\b", "cannot"),
    (r"\bwon't\b", "will not"),
    (r"\b(\w+)n't\b", r"\1 not"),
    (r"\b(\w+)'re\b", r"\1 are"),
    (r"\b(\w+)'ve\b", r"\1 have"),
    (r"\b(\w+)'ll\b", r"\1 will"),
    (r"\bI'm\b", "I am"),
    (r"\b(it|that|there|here|what|he|she)'s\b", r"\1 is"),
    (r"\blet's\b", "let us"),
]

CONTRACT = [
    (r"\bcannot\b", "can't"),
    (r"\bwill not\b", "won't"),
    (r"\b(do|does|did|is|are|was|were|has|have|had|would|should|could)\s+not\b", r"\1n't"),
    (r"\b(we|you|they)\s+are\b", r"\1're"),
    (r"\b(I|we|you|they)\s+have\b", r"\1've"),
    (r"\b(I|we|you|they|it)\s+will\b", r"\1'll"),
    (r"\bI am\b", "I'm"),
    (r"\b(it|that|there)\s+is\b", r"\1's"),
]


def substitute(text: str, rules: list[tuple[str, str]]) -> str:
    """Apply each rule in order, keeping a capital that opened the match."""

    def replace(match: re.Match, template: str) -> str:
        new = match.expand(template)
        return new[0].upper() + new[1:] if match.group(0)[0].isupper() else new

    for pattern, template in rules:
        text = re.sub(pattern, lambda m, t=template: replace(m, t), text, flags=re.IGNORECASE)
    return text


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--outputs", required=True, help="merged outputs with `source_text` and `output_text`")
    ap.add_argument("--out", required=True, help="JSONL path for the four variants of each job")
    args = ap.parse_args()

    rows = []
    for job in read_jsonl(args.outputs):
        source, output = job.get("source_text"), job.get("output_text")
        if not source or not output:
            die(f"{job.get('job_id', job.get('id'))}: needs both `source_text` and `output_text`")
        variants = {
            "source": source,
            "source_contracted": substitute(source, CONTRACT),
            "output": output,
            "output_expanded": substitute(output, EXPAND),
        }
        for name, text in variants.items():
            rows.append(
                {
                    "id": f"{job['id']}/{name}",
                    "document": job["id"],
                    "variant": name,
                    "contractions": len(CONTRACTION.findall(text)),
                    "text": text,
                }
            )
    log(f"wrote {write_jsonl(args.out, rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
