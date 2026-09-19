"""Assemble corpus.jsonl from corpus/<cell>/<source_class>/*.txt.

Each document becomes one row with `id`, `cell`, `source_class`, `text`,
`words`, and optional `meta` read from a sibling `.json` file with the same
stem. Documents under 50 words are skipped and logged because Pangram
declares them out of scope.

`--fetch-pilot` also downloads six public-domain pre-1927 English nonfiction
passages from Project Gutenberg into corpus/pilot/human/, one paragraph of
200 to 400 words per book, with the book id recorded in the sibling json.
The AI side of the pilot (corpus/pilot/ai/) is filled by the agent session.

Usage:
  python build_corpus.py --fetch-pilot
  python build_corpus.py --corpus-dir corpus --out corpus.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path

from _common import MIN_WORDS, die, log, word_count, write_jsonl

SOURCE_CLASSES = {"human", "human_defect", "ai", "ai_assisted", "mirror"}

GUTENBERG_URL = "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"

# Each passage is located by the first words of its paragraph so the
# selection is reproducible even if paragraph numbering shifts.
PILOT_PASSAGES = [
    {
        "slug": "thoreau-walden",
        "gutenberg_id": 205,
        "author": "Henry David Thoreau",
        "title": "Walden",
        "year": 1854,
        "start": "I think that we may safely trust a good deal more than we do.",
    },
    {
        "slug": "twain-mississippi",
        "gutenberg_id": 245,
        "author": "Mark Twain",
        "title": "Life on the Mississippi",
        "year": 1883,
        "start": "Now when I had mastered the language of this water",
    },
    {
        "slug": "darwin-origin",
        "gutenberg_id": 1228,
        "author": "Charles Darwin",
        "title": "On the Origin of Species",
        "year": 1859,
        "start": "When we look to the individuals of the same variety or sub-variety",
    },
    {
        "slug": "franklin-autobiography",
        "gutenberg_id": 148,
        "author": "Benjamin Franklin",
        "title": "The Autobiography of Benjamin Franklin",
        "year": 1791,
        "start": "I think you may like to know something of his person and character.",
    },
    {
        "slug": "douglass-narrative",
        "gutenberg_id": 23,
        "author": "Frederick Douglass",
        "title": "Narrative of the Life of Frederick Douglass",
        "year": 1845,
        "start": "I was born in Tuckahoe, near Hillsborough,",
    },
    {
        "slug": "paine-common-sense",
        "gutenberg_id": 147,
        "author": "Thomas Paine",
        "title": "Common Sense",
        "year": 1776,
        "start": "In order to gain a clear and just idea of the design and end of government,",
    },
]

AI_README = """# corpus/pilot/ai

Filled by the agent session, not by build_corpus.py.

Put one `.txt` per document here (at least 50 words each) and an optional
sibling `.json` with the same stem for metadata, for example the model name,
the prompt, and the date. build_corpus.py picks them up as
`cell=pilot`, `source_class=ai`.
"""


def fetch_gutenberg(book_id: int, cache_dir: Path) -> str:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"pg{book_id}.txt"
    if not path.exists():
        url = GUTENBERG_URL.format(id=book_id)
        log(f"downloading {url}")
        with urllib.request.urlopen(url, timeout=60) as resp:
            path.write_bytes(resp.read())
    return path.read_text(encoding="utf-8-sig").replace("\r", "")


def gutenberg_paragraphs(text: str) -> list[str]:
    start = text.find("*** START")
    end = text.find("*** END")
    body = text[text.find("\n", start) + 1 : end] if start >= 0 and end >= 0 else text
    return [re.sub(r"\s+", " ", p).strip() for p in body.split("\n\n") if p.strip()]


def fetch_pilot(corpus_dir: Path, cache_dir: Path) -> None:
    human_dir = corpus_dir / "pilot" / "human"
    ai_dir = corpus_dir / "pilot" / "ai"
    human_dir.mkdir(parents=True, exist_ok=True)
    ai_dir.mkdir(parents=True, exist_ok=True)
    readme = ai_dir / "README.md"
    if not readme.exists():
        readme.write_text(AI_README, encoding="utf-8")
    for spec in PILOT_PASSAGES:
        text = fetch_gutenberg(spec["gutenberg_id"], cache_dir)
        matches = [p for p in gutenberg_paragraphs(text) if p.startswith(spec["start"])]
        if not matches:
            die(f"passage for {spec['slug']} not found in pg{spec['gutenberg_id']}.txt")
        passage = matches[0]
        n = word_count(passage)
        if not 200 <= n <= 400:
            die(f"passage for {spec['slug']} has {n} words, expected 200 to 400")
        (human_dir / f"{spec['slug']}.txt").write_text(passage + "\n", encoding="utf-8")
        meta = {k: v for k, v in spec.items() if k not in {"slug", "start"}}
        meta["source_url"] = GUTENBERG_URL.format(id=spec["gutenberg_id"])
        meta["license"] = "public domain (Project Gutenberg)"
        (human_dir / f"{spec['slug']}.json").write_text(
            json.dumps(meta, indent=2) + "\n", encoding="utf-8"
        )
        log(f"wrote {spec['slug']} ({n} words)")


def build(corpus_dir: Path) -> list[dict]:
    rows = []
    skipped = 0
    for txt in sorted(corpus_dir.glob("*/*/*.txt")):
        cell = txt.parent.parent.name
        source_class = txt.parent.name
        if source_class not in SOURCE_CLASSES:
            log(f"skip {txt}: unknown source class `{source_class}`")
            continue
        text = txt.read_text(encoding="utf-8").strip()
        words = word_count(text)
        if words < MIN_WORDS:
            log(f"skip {txt}: {words} words is under the {MIN_WORDS}-word minimum")
            skipped += 1
            continue
        row = {
            "id": f"{cell}/{source_class}/{txt.stem}",
            "cell": cell,
            "source_class": source_class,
            "text": text,
            "words": words,
        }
        sidecar = txt.with_suffix(".json")
        if sidecar.exists():
            row["meta"] = json.loads(sidecar.read_text(encoding="utf-8"))
        rows.append(row)
    log(f"{len(rows)} documents, {skipped} skipped for length")
    return rows


def main() -> None:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus-dir", default=str(here / "corpus"), help="root of <cell>/<source_class>/*.txt")
    ap.add_argument("--out", default=str(here / "corpus.jsonl"), help="output JSONL path")
    ap.add_argument("--fetch-pilot", action="store_true", help="download the six Gutenberg pilot passages first")
    ap.add_argument(
        "--gutenberg-cache",
        default=str(Path.home() / ".cache" / "animize-eval" / "gutenberg"),
        help="where raw Gutenberg books are cached",
    )
    args = ap.parse_args()
    corpus_dir = Path(args.corpus_dir)
    if args.fetch_pilot:
        fetch_pilot(corpus_dir, Path(args.gutenberg_cache))
    if not corpus_dir.exists():
        die(f"corpus directory `{corpus_dir}` does not exist")
    rows = build(corpus_dir)
    n = write_jsonl(args.out, rows)
    log(f"wrote {n} rows to {args.out}")


if __name__ == "__main__":
    main()
