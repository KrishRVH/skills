"""Shared helpers for the Animize evaluation harness.

Provides JSONL I/O, word counting, token windowing, the job row builder, and
the Hugging Face gate check that turns authentication failures into a short
actionable message instead of a traceback. Every script in this folder
imports it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable, Iterator, NoReturn

MIN_WORDS = 50
WINDOW_TOKENS = 512
WINDOW_STRIDE = 256

# Both mirror the skill's own text: the budget is defined in
# animize/references/procedure.md (P2), and the origin note opens with these
# words in animize/SKILL.md.
PRESERVE_BUDGET = 0.15
ORIGIN_NOTE = "Origin note:"

# The skill takes no settings. What the caller says about who wrote the draft
# is the only thing a job varies, and it fixes the regime the run must select.
CALLER_STATEMENTS = {
    "own": "I wrote this draft myself.",
    "generated": "A model generated this draft.",
    "unstated": None,
}


def make_job(doc: dict, origin: str, budget: float = PRESERVE_BUDGET) -> dict:
    """Build one job row for a corpus document and a caller statement."""
    regime = "preserve" if origin == "own" else "recompose"
    return {
        "job_id": f"{doc['id']}__{origin}__{budget:g}",
        "id": doc["id"],
        "cell": doc.get("cell"),
        "source_class": doc.get("source_class"),
        "origin": origin,
        "caller_statement": CALLER_STATEMENTS[origin],
        "regime": regime,
        "regime_expected": regime,
        "budget": budget,
        "source_text": doc["text"],
    }


def log(msg: str) -> None:
    """Print a status line to stderr."""
    print(msg, file=sys.stderr, flush=True)


def die(msg: str) -> NoReturn:
    """Print an error to stderr and exit with status 2."""
    print(f"error: {msg}", file=sys.stderr, flush=True)
    sys.exit(2)


def word_count(text: str) -> int:
    return len(text.split())


def read_jsonl(path: str | Path) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                die(f"{path}:{n}: invalid JSON ({exc})")
    return rows


def write_jsonl(path: str | Path, rows: Iterable[dict]) -> int:
    n = 0
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n


def iter_windows(
    ids: list[int], size: int = WINDOW_TOKENS, stride: int = WINDOW_STRIDE
) -> Iterator[list[int]]:
    """Yield fixed-size token windows.

    Windows start every `stride` tokens. The final window is right-aligned so
    that every window is full size unless the text is shorter than `size`.
    """
    if len(ids) <= size:
        yield ids
        return
    starts = list(range(0, len(ids) - size, stride))
    last = len(ids) - size
    if starts[-1] != last:
        starts.append(last)
    for start in starts:
        yield ids[start : start + size]


def gate_message(repo: str, repo_type: str = "model") -> str:
    kind = "dataset" if repo_type == "dataset" else "model"
    return (
        f"cannot download gated {kind} `{repo}`.\n"
        "  Missing step: run `hf auth login` with a Hugging Face token, then open\n"
        f"  https://huggingface.co/{'datasets/' if kind == 'dataset' else ''}{repo}\n"
        "  in a browser and accept the access terms. All four gated repos need this:\n"
        "    pangram/editlens_roberta-large, pangram/editlens_Llama-3.2-3B,\n"
        "    meta-llama/Llama-3.2-3B, pangram/editlens_iclr (dataset)."
    )


def is_gate_error(exc: BaseException) -> bool:
    """True when an exception looks like a hub authentication or access error."""
    name = type(exc).__name__
    if name in {"GatedRepoError", "RepositoryNotFoundError", "DatasetNotFoundError"}:
        return True
    text = str(exc)
    return any(
        marker in text
        for marker in ("401 Client Error", "403 Client Error", "gated", "authenticated")
    )


def require_hub_file(repo: str, filename: str, repo_type: str = "model") -> str:
    """Download one small file from the hub or exit with the gate message.

    Returns the local path of the downloaded file.
    """
    from huggingface_hub import hf_hub_download

    try:
        return hf_hub_download(repo, filename, repo_type=repo_type)
    except Exception as exc:  # noqa: BLE001
        if is_gate_error(exc):
            die(gate_message(repo, repo_type))
        raise


def hub_revision(repo: str, repo_type: str = "model") -> str | None:
    """Return the current commit hash of a hub repo, or None when offline."""
    from huggingface_hub import HfApi

    try:
        api = HfApi()
        info = api.dataset_info(repo) if repo_type == "dataset" else api.model_info(repo)
        return info.sha
    except Exception:  # noqa: BLE001
        return None
