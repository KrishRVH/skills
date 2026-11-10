"""Summarize detector scores, clause-diff accounting, and routing accuracy.

Reads any number of score files (glob), an optional diffs.jsonl from
clause_diff.py, and an optional calibration.json from calibrate.py, and
writes a Markdown report grouped by cell and regime. Per group and per
model it reports the verdict distribution at each calibrated threshold,
the mean and quartiles of the score, clause-diff accounting (added-clauses
zero rate, within-budget rate, violation rate), and routing accuracy where
`regime_expected` and `regime_assigned` both exist. The header lists model
names and revisions, the calibration file and date, and every input or
column that was missing, so the report runs on partial inputs.

Usage:
  python report.py --scores 'scores_*.jsonl' --diffs diffs.jsonl \
      --calibration calibration.json --out report.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
from pathlib import Path

import pandas as pd

from _common import log, read_jsonl

SCORE_FIELDS = {"binoculars": "binoculars_score"}
DEFAULT_SCORE_FIELD = "editlens_score"


def load_scores(pattern: str, missing: list[str]) -> pd.DataFrame:
    files = sorted(glob.glob(pattern))
    if not files:
        missing.append(f"scores: no files match `{pattern}`")
        return pd.DataFrame()
    rows = [r for f in files for r in read_jsonl(f)]
    df = pd.DataFrame(rows)
    for col in ("cell", "regime", "model"):
        if col not in df:
            missing.append(f"scores: column `{col}` absent, filled with `unknown`")
            df[col] = "unknown"
    df["cell"] = df["cell"].fillna("unknown")
    df["regime"] = df["regime"].fillna("source")
    return df


def score_column(model: str, df: pd.DataFrame) -> str | None:
    field = SCORE_FIELDS.get(model, DEFAULT_SCORE_FIELD)
    if field in df and df[field].notna().any():
        return field
    return None


def verdict_rates(values: pd.Series, entry: dict) -> dict[str, str]:
    out = {}
    direction = entry.get("direction", "higher_is_ai")
    thresholds = entry.get("thresholds") or {}
    for name in ("fpr_1pct", "fpr_0_5pct"):
        t = (thresholds.get(name) or {}).get("threshold")
        if t is None:
            out[name] = "n/a"
            continue
        flagged = (values < t) if direction == "lower_is_ai" else (values > t)
        out[name] = f"{flagged.mean():.0%} ai"
    t_h = (thresholds.get("fpr_1pct") or {}).get("threshold")
    t_g = (thresholds.get("macro_f1") or {}).get("threshold")
    if t_h is not None and t_g is not None:
        if direction == "lower_is_ai":
            is_ai = values < t_h
            is_gen = values < t_g
        else:
            is_ai = values > t_h
            is_gen = values > t_g
        human = (~is_ai).mean()
        gen = (is_ai & is_gen).mean()
        assisted = (is_ai & ~is_gen).mean()
        out["three_class"] = f"human {human:.0%} / assisted {assisted:.0%} / generated {gen:.0%}"
    else:
        out["three_class"] = "n/a"
    return out


def score_section(df: pd.DataFrame, calibration: dict, missing: list[str]) -> list[str]:
    lines = ["## Detector scores", ""]
    if df.empty:
        lines += ["No score files were provided.", ""]
        return lines
    models = calibration.get("models") or {}
    for model, part in df.groupby("model"):
        field = score_column(model, part)
        if field is None:
            missing.append(f"scores: model `{model}` has no score column")
            continue
        entry = models.get(model)
        if entry is None:
            missing.append(f"calibration: no thresholds for model `{model}`; verdict columns show n/a")
        lines += [f"### {model} ({field})", ""]
        lines.append("| cell | regime | n | mean | q25 | median | q75 | fpr_1pct | fpr_0_5pct | three_class |")
        lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |")
        for (cell, regime), g in part.groupby(["cell", "regime"]):
            v = g[field].dropna().astype(float)
            if v.empty:
                continue
            verdicts = verdict_rates(v, entry) if entry else {"fpr_1pct": "n/a", "fpr_0_5pct": "n/a", "three_class": "n/a"}
            lines.append(
                f"| {cell} | {regime} | {len(v)} | {v.mean():.4f} | {v.quantile(0.25):.4f} | "
                f"{v.median():.4f} | {v.quantile(0.75):.4f} | {verdicts['fpr_1pct']} | "
                f"{verdicts['fpr_0_5pct']} | {verdicts['three_class']} |"
            )
        lines.append("")
    return lines


def diff_section(path: str | None, missing: list[str]) -> tuple[list[str], pd.DataFrame]:
    lines = ["## Clause-diff accounting (preserve regime)", ""]
    if not path or not Path(path).exists():
        missing.append("diffs: no diffs.jsonl provided")
        lines += ["No clause-diff file was provided.", ""]
        return lines, pd.DataFrame()
    df = pd.DataFrame(read_jsonl(path))
    if df.empty:
        lines += ["diffs.jsonl is empty.", ""]
        return lines, df
    for col in ("cell", "regime"):
        if col not in df:
            df[col] = "unknown"
    df["cell"] = df["cell"].fillna("unknown")
    df["regime"] = df["regime"].fillna("unknown")
    df["added_zero"] = df["added_clauses"].apply(lambda a: len(a) == 0)
    lines.append("| cell | regime | n | added clauses zero | within budget | violations | mean token share | mean added tokens |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for (cell, regime), g in df.groupby(["cell", "regime"]):
        lines.append(
            f"| {cell} | {regime} | {len(g)} | {g['added_zero'].mean():.0%} | {g['within_budget'].mean():.0%} | "
            f"{g['violation'].mean():.0%} | {g['model_token_share'].mean():.3f} | {g['model_added_tokens'].mean():.1f} |"
        )
    lines.append("")
    return lines, df


def routing_section(frames: list[pd.DataFrame], missing: list[str]) -> list[str]:
    lines = ["## Routing accuracy", ""]
    usable = [f for f in frames if not f.empty and {"regime_expected", "regime_assigned"} <= set(f.columns)]
    if not usable:
        missing.append("routing: no rows with both regime_expected and regime_assigned")
        lines += ["No rows carry both `regime_expected` and `regime_assigned`.", ""]
        return lines
    df = pd.concat(usable, ignore_index=True)
    df = df.dropna(subset=["regime_expected", "regime_assigned"])
    if "job_id" in df:
        df = df.drop_duplicates(subset=["job_id"])
    if "cell" not in df:
        df["cell"] = "unknown"
    lines.append("| cell | n | accuracy |")
    lines.append("| --- | ---: | ---: |")
    for cell, g in df.groupby("cell"):
        acc = (g["regime_expected"] == g["regime_assigned"]).mean()
        lines.append(f"| {cell} | {len(g)} | {acc:.0%} |")
    lines.append("")
    return lines


def header(scores: pd.DataFrame, cal_path: str | None, calibration: dict) -> list[str]:
    lines = ["# Animize evaluation report", "", f"Generated {dt.datetime.now().isoformat(timespec='seconds')}", ""]
    if not scores.empty and "model" in scores:
        lines.append("Models:")
        for model, part in scores.groupby("model"):
            revs = sorted({str(r) for r in part.get("model_revision", pd.Series(dtype=str)).dropna()})
            repos = sorted({str(r) for r in part.get("model_repo", pd.Series(dtype=str)).dropna()})
            if model == "binoculars":
                repos = sorted({f"{o} / {p}" for o, p in zip(part.get("observer", []), part.get("performer", []))})
            lines.append(f"- `{model}` {', '.join(repos)} revision {', '.join(revs) or 'unknown'}")
        lines.append("")
    if cal_path and calibration:
        lines.append(f"Calibration: `{cal_path}` dated {calibration.get('date', 'unknown')}")
        for model, entry in (calibration.get("models") or {}).items():
            lines.append(f"- `{model}` split `{entry.get('split')}` on {entry.get('date')}")
    else:
        lines.append("Calibration: none provided")
    lines.append("")
    return lines


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scores", default="scores_*.jsonl", help="glob of score files")
    ap.add_argument("--diffs", help="diffs.jsonl from clause_diff.py")
    ap.add_argument("--calibration", help="calibration.json from calibrate.py")
    ap.add_argument("--out", default="report.md")
    args = ap.parse_args()

    missing: list[str] = []
    calibration = {}
    if args.calibration:
        if Path(args.calibration).exists():
            calibration = json.loads(Path(args.calibration).read_text())
        else:
            missing.append(f"calibration: `{args.calibration}` not found")
    scores = load_scores(args.scores, missing)
    body = header(scores, args.calibration, calibration)
    body += score_section(scores, calibration, missing)
    diff_lines, diffs = diff_section(args.diffs, missing)
    body += diff_lines
    body += routing_section([scores, diffs], missing)
    body += ["## Missing inputs and columns", ""]
    body += [f"- {m}" for m in missing] or ["- none"]
    body.append("")
    Path(args.out).write_text("\n".join(body), encoding="utf-8")
    log(f"wrote {args.out} ({len(missing)} missing items noted)")


if __name__ == "__main__":
    main()
