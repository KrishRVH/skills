"""Check local EditLens scores against the scores Pangram published.

The EditLens repository (https://github.com/pangramlabs/EditLens) ships
`data/val.csv`, `data/test.csv`, and other files with one published score
column per detector. This script joins those rows to a local score file on
`text_id` and reports how closely the local scores reproduce them. Run it
before trusting any local score: a large gap means the local loading or
preprocessing differs from the reference.

Usage:
  python compare_reference.py --scores scores_roberta_iclr_val.jsonl \
      --reference ~/EditLens/data/val.csv
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

from _common import die, read_jsonl

COLUMNS = {
    "editlens_roberta": "editlens_roberta-large_score",
    "editlens_llama": "editlens_Llama-3.2-3B_score",
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scores", required=True, help="local scores from score_editlens.py --iclr-split")
    ap.add_argument("--reference", required=True, help="CSV from the EditLens repository's data folder")
    args = ap.parse_args()

    local = pd.DataFrame(read_jsonl(args.scores))
    if local.empty:
        die(f"{args.scores} has no rows")
    ref = pd.read_csv(args.reference)
    for model, part in local.groupby("model"):
        column = COLUMNS.get(model)
        if column is None or column not in ref:
            die(f"no published column for model `{model}` in {args.reference}")
        joined = part.merge(ref[["text_id", column]], left_on="id", right_on="text_id")
        if joined.empty:
            die("no rows share a text_id with the reference file")
        mine = joined["editlens_score"].to_numpy(float)
        theirs = joined[column].to_numpy(float)
        gap = np.abs(mine - theirs)
        print(f"{model} against `{column}`: {len(joined)} rows joined of {len(part)} local")
        print(f"  mean abs gap {gap.mean():.4f}  median {np.median(gap):.4f}  p95 {np.quantile(gap, 0.95):.4f}  max {gap.max():.4f}")
        print(f"  pearson r {np.corrcoef(mine, theirs)[0, 1]:.4f}  rows with gap over 0.05: {int((gap > 0.05).sum())}")


if __name__ == "__main__":
    main()
