"""Shared helpers for the Animize evaluation harness.

Provides JSONL I/O, word counting, token windowing, and the Hugging Face
gate check that turns authentication failures into a short actionable
message instead of a traceback. Every script in this folder imports it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable, Iterator

MIN_WORDS = 50
WINDOW_TOKENS = 512
WINDOW_STRIDE = 256

GATED_REPOS = {
    "pangram/editlens_roberta-large": "model",
    "pangram/editlens_Llama-3.2-3B": "model",
    "meta-llama/Llama-3.2-3B": "model",
    "pangram/editlens_iclr": "dataset",
}


def log(msg: str) -> None:
    """Print a status line to stderr."""
    print(msg, file=sys.stderr, flush=True)


def die(msg: str, code: int = 2) -> None:
    """Print an error to stderr and exit."""
    print(f"error: {msg}", file=sys.stderr, flush=True)
    sys.exit(code)


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


def dtype_kwargs(dtype) -> dict:
    """Return the from_pretrained keyword for a torch dtype.

    transformers 5 renamed `torch_dtype` to `dtype`; older versions only
    accept `torch_dtype`.
    """
    import transformers

    major = int(transformers.__version__.split(".")[0])
    return {"dtype": dtype} if major >= 5 else {"torch_dtype": dtype}


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


def load_bucket_map(path: str | Path, num_labels: int) -> list[float]:
    """Load bucket centers in label order; refuse placeholders."""
    p = Path(path)
    if not p.exists():
        die(f"bucket map `{p}` not found; run inspect_labels.py and fill it")
    data = json.loads(p.read_text(encoding="utf-8"))
    if data is None or not isinstance(data, list) or any(v is None for v in data):
        die(
            f"bucket map `{p}` is still a placeholder. Run inspect_labels.py, read the\n"
            "  id2label mapping, and write a JSON list of bucket centers (0.0 to 1.0)\n"
            "  in label order, for example [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]."
        )
    if len(data) != num_labels:
        die(f"bucket map has {len(data)} entries but the model has {num_labels} labels")
    return [float(v) for v in data]
