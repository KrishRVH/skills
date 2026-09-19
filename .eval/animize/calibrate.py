"""Pick detector thresholds from scored held-out data with ground-truth labels.

Input rows come from score_editlens.py or score_binoculars.py run on a
labeled split, with a class field (default `label`) holding one of
`human`, `ai_assisted`, `ai_generated`. Rows are grouped by their `model`
field. For each model the script records:

  fpr_1pct    the threshold giving at most 1% false positives on human,
              with recall on ai_generated at that threshold
  fpr_0_5pct  the same at 0.5%
  macro_f1    the threshold maximizing macro-F1 between ai_assisted and
              ai_generated (rows of those two classes only)

Comparisons are strict: a document is called AI when its score is beyond
the threshold (above it for EditLens, below it for Binoculars).

Score field and direction: EditLens rows use `expected_ai_fraction`
(higher means AI). Binoculars rows use `binoculars_score` (lower means AI)
and are detected automatically when `expected_ai_fraction` is absent.

The output merges into an existing calibration.json so each model can be
calibrated separately. Each entry records the split name and the date.

Usage:
  python calibrate.py --scores scores_roberta_iclr.jsonl --labels-field label \
      --split test --out calibration.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.metrics import f1_score

from _common import die, log, read_jsonl

CLASSES = ("human", "ai_assisted", "ai_generated")


def pick_score_field(rows: list[dict], requested: str | None) -> tuple[str, str]:
    if requested:
        direction = "lower_is_ai" if requested == "binoculars_score" else "higher_is_ai"
        return requested, direction
    if any("expected_ai_fraction" in r for r in rows):
        return "expected_ai_fraction", "higher_is_ai"
    if any("binoculars_score" in r for r in rows):
        return "binoculars_score", "lower_is_ai"
    die("rows have neither expected_ai_fraction nor binoculars_score")
    return "", ""  # unreachable


def fpr_threshold(oriented: np.ndarray, labels: np.ndarray, target: float) -> dict:
    """Smallest threshold t (AI when oriented > t, strict) with human FPR <= target."""
    human = np.sort(oriented[labels == "human"])
    ai = oriented[labels == "ai_generated"]
    if len(human) < 1 / target:
        log(f"warning: {len(human)} human rows cannot resolve a {target:.1%} FPR; need at least {int(1 / target)}")
    chosen = None
    for t in np.unique(human):
        if float(np.mean(human > t)) <= target:
            chosen = float(t)
            break
    if chosen is None:
        return {"oriented_threshold": None, "fpr_human": None, "recall_ai_generated": None,
                "n_human": int(len(human)), "n_ai_generated": int(len(ai))}
    return {
        "oriented_threshold": chosen,
        "fpr_human": float(np.mean(human > chosen)),
        "recall_ai_generated": float(np.mean(ai > chosen)) if len(ai) else None,
        "n_human": int(len(human)),
        "n_ai_generated": int(len(ai)),
    }


def macro_f1_threshold(oriented: np.ndarray, labels: np.ndarray) -> dict:
    keep = np.isin(labels, ["ai_assisted", "ai_generated"])
    x, y = oriented[keep], labels[keep]
    if len(np.unique(y)) < 2:
        return {"oriented_threshold": None, "macro_f1": None, "n": int(len(x))}
    best_t, best_f1 = None, -1.0
    for t in np.concatenate([[np.min(x) - 1e-9], np.unique(x)]):
        pred = np.where(x > t, "ai_generated", "ai_assisted")
        f1 = f1_score(y, pred, average="macro")
        if f1 > best_f1:
            best_t, best_f1 = float(t), float(f1)
    return {"oriented_threshold": best_t, "macro_f1": best_f1, "n": int(len(x))}


def unorient(entry: dict, direction: str) -> dict:
    t = entry.pop("oriented_threshold")
    entry["threshold"] = None if t is None else (-t if direction == "lower_is_ai" else t)
    return entry


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scores", required=True, nargs="+", help="scored held-out JSONL files")
    ap.add_argument("--labels-field", default="label")
    ap.add_argument("--score-field", help="override the score field (expected_ai_fraction or binoculars_score)")
    ap.add_argument("--split", help="name of the held-out split; defaults to the rows' `split` field or `unknown`")
    ap.add_argument("--out", default="calibration.json")
    args = ap.parse_args()

    rows = [r for path in args.scores for r in read_jsonl(path)]
    by_model: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_model[r.get("model", "unknown")].append(r)

    out_path = Path(args.out)
    calibration = json.loads(out_path.read_text()) if out_path.exists() else {}
    calibration.setdefault("models", {})
    calibration["date"] = dt.date.today().isoformat()

    for model, group in by_model.items():
        score_field, direction = pick_score_field(group, args.score_field)
        usable = [r for r in group if r.get(args.labels_field) in CLASSES and r.get(score_field) is not None]
        unknown = len(group) - len(usable)
        if unknown:
            log(f"{model}: {unknown} rows without a usable label or score were ignored")
        if not usable:
            log(f"{model}: nothing to calibrate")
            continue
        scores = np.array([float(r[score_field]) for r in usable])
        labels = np.array([r[args.labels_field] for r in usable])
        oriented = -scores if direction == "lower_is_ai" else scores
        split = args.split or next((r.get("split") for r in usable if r.get("split")), "unknown")
        entry = {
            "score_field": score_field,
            "direction": direction,
            "split": split,
            "date": calibration["date"],
            "n_rows": int(len(usable)),
            "class_counts": {c: int(np.sum(labels == c)) for c in CLASSES},
            "model_revision": next((r.get("model_revision") for r in usable if r.get("model_revision")), None),
            "thresholds": {
                "fpr_1pct": unorient(fpr_threshold(oriented, labels, 0.01), direction),
                "fpr_0_5pct": unorient(fpr_threshold(oriented, labels, 0.005), direction),
                "macro_f1": unorient(macro_f1_threshold(oriented, labels), direction),
            },
        }
        calibration["models"][model] = entry
        log(f"{model}: {json.dumps(entry['thresholds'])}")

    out_path.write_text(json.dumps(calibration, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {out_path}")


if __name__ == "__main__":
    main()
