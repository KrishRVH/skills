"""Preserve-regime accounting: clause-level diff of source and output text.

For each row with `source_text` and `output_text`, both texts are split into
clauses (sentence boundaries first, then commas, semicolons, colons, and
dashes that separate a subject-verb group of at least 4 tokens). Clauses are
normalized (lowercase, punctuation stripped, whitespace collapsed) and each
output clause is matched against the source using a similarity that is the
mean of difflib's SequenceMatcher ratio on token lists and token-set Jaccard.

Classes:
  kept              similarity >= 0.9
  lexically_edited  0.5 <= similarity < 0.9, matched to an unconsumed source clause
  added             best similarity < 0.5
  deleted           source clauses no output clause matched
Matches are assigned greedily by descending similarity so an early output
clause cannot steal a later clause's best match. `reordered` counts matched
output clauses that sit outside the longest in-order run of source matches.

Model-added tokens = tokens of `added` clauses plus output-side tokens of
insert and replace opcodes inside `lexically_edited` clauses.

Per row the output has counts per class, `model_added_tokens` (tokens of
added clauses plus tokens absent from the whole source; the clause-local
count is kept as `model_added_tokens_clause`),
`output_tokens`, `source_tokens`, `model_token_share`, `within_budget`
(share < budget and model_added_tokens < source_tokens), `added_clauses`,
and `violation` (regime is preserve and added_clauses is nonempty or the
row is over budget).

Usage:
  python clause_diff.py --demo
  python clause_diff.py --input outputs.jsonl --out diffs.jsonl --budget 0.15
"""

from __future__ import annotations

import argparse
from collections import Counter
import difflib
import re
import string
from dataclasses import dataclass

from _common import log, read_jsonl, write_jsonl

MIN_CLAUSE_TOKENS = 4
KEPT = 0.9
EDITED = 0.5

# Words that end in "ed" or "ing" without being verbs; keeps "indeed" from
# turning "In the latter, indeed" into a standalone clause.
NOT_VERBS = {
    "indeed", "hundred", "sacred", "ahead", "instead", "wicked", "naked",
    "hatred", "kindred", "morning", "evening", "thing", "nothing", "something",
    "anything", "everything", "during", "ceiling", "sibling", "string", "spring",
    "king", "wing", "ring", "being",
}
VERB_MARKERS = {
    "am", "is", "are", "was", "were", "be", "been", "being", "has", "have", "had",
    "do", "does", "did", "can", "could", "will", "would", "shall", "should", "may",
    "might", "must", "get", "gets", "got", "go", "goes", "went", "make", "makes",
    "made", "say", "says", "said", "know", "knows", "knew", "think", "thinks",
    "thought", "see", "sees", "saw", "take", "takes", "took", "come", "comes",
    "came", "give", "gives", "gave", "find", "finds", "found", "tell", "tells",
    "told", "become", "becomes", "became", "seem", "seems", "seemed", "keep",
    "keeps", "kept", "let", "lets", "need", "needs", "mean", "means", "meant",
    "met", "meet", "sat", "sit", "ran", "run", "led", "lead", "put", "set", "held",
    "hold", "paid", "pay", "left", "leave", "felt", "feel", "built", "build",
    "sent", "send", "spent", "spend", "lost", "lose", "won", "win", "wrote",
    "write", "read", "cut", "hit", "brought", "bring", "bought", "buy", "caught",
    "catch", "taught", "teach", "stood", "stand", "began", "begin", "drew",
    "draw", "grew", "grow", "threw", "throw", "flew", "fly", "chose", "choose",
    "spoke", "speak", "broke", "break", "drove", "drive", "rose", "rise", "fell",
    "fall", "ate", "eat", "sold", "sell", "heard", "hear", "showed", "show",
    "ask", "asks", "asked", "use", "uses", "used", "want", "wants", "wanted",
}
PRONOUN_SUBJECTS = {"i", "we", "you", "they", "he", "she", "it", "who", "which", "that"}

# A sentence ends at terminal punctuation followed by whitespace, regardless
# of the next character's case, so that an exclamation before a lowercase
# continuation splits the same way in source and output (P3 step 1).
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
EM_DASH, EN_DASH = chr(0x2014), chr(0x2013)
CURLY_QUOTES = "".join(chr(c) for c in (0x201C, 0x201D, 0x2018, 0x2019))
SUBCLAUSE_RE = re.compile(r"\s*(?:;|:|,|\s-\s|--|" + EM_DASH + "|" + EN_DASH + r")\s*")
PUNCT_TABLE = str.maketrans("", "", string.punctuation + CURLY_QUOTES + EM_DASH + EN_DASH)


def normalize(text: str) -> list[str]:
    text = text.lower().translate(PUNCT_TABLE)
    return text.split()


def looks_like_clause(piece: str) -> bool:
    toks = normalize(piece)
    if len(toks) < MIN_CLAUSE_TOKENS:
        return False
    for i, tok in enumerate(toks):
        if tok in VERB_MARKERS:
            return True
        if tok in PRONOUN_SUBJECTS and i + 1 < len(toks):
            return True
        if len(tok) > 4 and (tok.endswith("ed") or tok.endswith("ing")) and tok not in NOT_VERBS:
            return True
    return False


def split_clauses(text: str) -> list[str]:
    clauses: list[str] = []
    for sentence in SENTENCE_RE.split(text.replace("\n", " ").strip()):
        sentence = sentence.strip()
        if not sentence:
            continue
        pieces = [p for p in SUBCLAUSE_RE.split(sentence) if p and p.strip()]
        current = ""
        for piece in pieces:
            if not current:
                current = piece
                continue
            if looks_like_clause(current) and looks_like_clause(piece):
                clauses.append(current.strip())
                current = piece
            else:
                current = f"{current}, {piece}"
        if current.strip():
            clauses.append(current.strip())
    return clauses


def similarity(a: list[str], b: list[str]) -> float:
    if not a or not b:
        return 0.0
    ratio = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
    sa, sb = set(a), set(b)
    jaccard = len(sa & sb) / len(sa | sb)
    return (ratio + jaccard) / 2


def added_tokens_in_edit(source: list[str], output: list[str]) -> int:
    added = 0
    sm = difflib.SequenceMatcher(None, source, output, autojunk=False)
    for tag, _i1, _i2, j1, j2 in sm.get_opcodes():
        if tag in {"insert", "replace"}:
            added += j2 - j1
    return added


def longest_increasing_run(seq: list[int]) -> int:
    best: list[int] = []
    for x in seq:
        lo, hi = 0, len(best)
        while lo < hi:
            mid = (lo + hi) // 2
            if best[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(best):
            best.append(x)
        else:
            best[lo] = x
    return len(best)


@dataclass
class ClauseResult:
    index: int
    text: str
    cls: str
    match: int | None
    sim: float
    added_tokens: int


def diff_row(source_text: str, output_text: str) -> tuple[dict, list[ClauseResult]]:
    src = split_clauses(source_text)
    out = split_clauses(output_text)
    src_tok = [normalize(c) for c in src]
    out_tok = [normalize(c) for c in out]

    pairs = []
    for j, o in enumerate(out_tok):
        for i, s in enumerate(src_tok):
            sim = similarity(s, o)
            if sim >= EDITED:
                pairs.append((sim, j, i))
    pairs.sort(key=lambda t: (-t[0], t[1], t[2]))
    match_of: dict[int, tuple[int, float]] = {}
    consumed: set[int] = set()
    for sim, j, i in pairs:
        if j in match_of or i in consumed:
            continue
        match_of[j] = (i, sim)
        consumed.add(i)

    results: list[ClauseResult] = []
    for j, clause in enumerate(out):
        if j in match_of:
            i, sim = match_of[j]
            cls = "kept" if sim >= KEPT else "lexically_edited"
            added = added_tokens_in_edit(src_tok[i], out_tok[j]) if cls == "lexically_edited" else 0
            results.append(ClauseResult(j, clause, cls, i, sim, added))
        else:
            best = max((similarity(s, out_tok[j]) for s in src_tok), default=0.0)
            results.append(ClauseResult(j, clause, "added", None, best, len(out_tok[j])))

    deleted = [src[i] for i in range(len(src)) if i not in consumed]
    order = [r.match for r in results if r.match is not None]
    reordered = len(order) - longest_increasing_run(order)

    counts = {k: 0 for k in ("kept", "lexically_edited", "added", "deleted")}
    for r in results:
        counts[r.cls] += 1
    counts["deleted"] = len(deleted)

    output_tokens = sum(len(t) for t in out_tok)
    source_tokens = sum(len(t) for t in src_tok)
    # Clause-local count (kept for reference): tokens in each output clause with
    # no match in its aligned source clause. It over-counts when a source
    # sentence was split at a stray comma and the output merges the pieces.
    model_added_clause = sum(r.added_tokens for r in results)
    # Policy count: every token of an added clause, plus tokens of kept or
    # edited clauses that do not exist anywhere in the source (multiset).
    src_pool = Counter(tok for clause in src_tok for tok in clause)
    non_added = Counter(
        tok for r in results if r.cls != "added" for tok in out_tok[r.index]
    )
    doc_extra = sum((non_added - src_pool).values())
    model_added = sum(r.added_tokens for r in results if r.cls == "added") + doc_extra
    share = model_added / output_tokens if output_tokens else 0.0
    summary = {
        "counts": counts,
        "reordered": reordered,
        "model_added_tokens": model_added,
        "model_added_tokens_clause": model_added_clause,
        "output_tokens": output_tokens,
        "source_tokens": source_tokens,
        "model_token_share": round(share, 4),
        "added_clauses": [r.text for r in results if r.cls == "added"],
        "deleted_clauses": deleted,
    }
    return summary, results


def finish(summary: dict, regime: str | None, budget: float) -> dict:
    within = summary["model_token_share"] < budget and summary["model_added_tokens"] < summary["source_tokens"]
    summary["budget"] = budget
    summary["within_budget"] = within
    summary["violation"] = bool(regime == "preserve" and (summary["added_clauses"] or not within))
    return summary


def print_table(results: list[ClauseResult], summary: dict) -> None:
    print(f"{'#':>3}  {'class':<17} {'src':>4} {'sim':>5} {'+tok':>4}  clause")
    for r in results:
        m = "" if r.match is None else str(r.match)
        print(f"{r.index:>3}  {r.cls:<17} {m:>4} {r.sim:>5.2f} {r.added_tokens:>4}  {r.text}")
    for d in summary["deleted_clauses"]:
        print(f"{'':>3}  {'deleted':<17} {'':>4} {'':>5} {'':>4}  {d}")
    print()
    for k in (
        "counts", "reordered", "model_added_tokens", "model_added_tokens_clause", "output_tokens", "source_tokens",
        "model_token_share", "budget", "within_budget", "violation",
    ):
        print(f"{k:<20} {summary[k]}")


DEMO_SOURCE = (
    "The committee met on Tuesday, and it approved the revised budget after a short "
    "discussion. Two members asked for a written summary; the chair agreed to circulate "
    "one by Friday. The vote was unanimous. Nobody raised the parking question, which "
    "had been on the agenda for months."
)
DEMO_OUTPUT = (
    "The committee met on Tuesday, and it approved the revised budget after a brief "
    "discussion. The vote was unanimous. The chair agreed to circulate a summary by "
    "Friday, since two members had asked for one. This decision reflects a strong "
    "commitment to fiscal responsibility."
)


def run_demo(budget: float) -> None:
    print("SOURCE:\n  " + DEMO_SOURCE + "\nOUTPUT:\n  " + DEMO_OUTPUT + "\n")
    summary, results = diff_row(DEMO_SOURCE, DEMO_OUTPUT)
    finish(summary, "preserve", budget)
    print_table(results, summary)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", help="JSONL with source_text and output_text per row")
    ap.add_argument("--out", help="output JSONL path")
    ap.add_argument("--budget", type=float, default=0.15, help="default model token share budget")
    ap.add_argument("--demo", action="store_true", help="run the built-in example and print the table")
    args = ap.parse_args()

    if args.demo:
        run_demo(args.budget)
        return
    if not args.input or not args.out:
        ap.error("--input and --out are required unless --demo is given")

    rows_out = []
    skipped = 0
    for row in read_jsonl(args.input):
        src, out = row.get("source_text"), row.get("output_text")
        if not src or not out:
            skipped += 1
            continue
        regime = row.get("regime") or row.get("regime_assigned")
        budget = float(row.get("budget", args.budget))
        summary, _ = diff_row(src, out)
        finish(summary, regime, budget)
        record = {k: v for k, v in row.items() if k not in {"source_text", "output_text", "text"}}
        record.update(summary)
        rows_out.append(record)
    n = write_jsonl(args.out, rows_out)
    log(f"wrote {n} rows to {args.out}; skipped {skipped} rows without source_text/output_text")


if __name__ == "__main__":
    main()
