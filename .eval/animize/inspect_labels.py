"""Inspect the EditLens label space and the editlens_iclr dataset.

Downloads only the config files of both Pangram models and prints
num_labels, id2label, and problem_type, then loads pangram/editlens_iclr and
prints its features, splits, and first row. Use the output to fill
bucket_map.json (bucket centers in label order) and to pick a calibration
split for calibrate.py.

All three repos are gated. Without `hf auth login` and accepted terms the
script exits with a message naming that step.

Usage:
  python inspect_labels.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _common import die, gate_message, is_gate_error, require_hub_file

ROBERTA_REPO = "pangram/editlens_roberta-large"
LLAMA_ADAPTER = "pangram/editlens_Llama-3.2-3B"
DATASET = "pangram/editlens_iclr"


def show_config(title: str, cfg: dict) -> None:
    print(f"== {title}")
    id2label = cfg.get("id2label")
    print(f"  num_labels:   {cfg.get('num_labels', len(id2label) if id2label else 'not in config')}")
    print(f"  id2label:     {json.dumps(id2label)}")
    print(f"  problem_type: {cfg.get('problem_type')}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skip-dataset", action="store_true", help="only inspect the model configs")
    args = ap.parse_args()

    cfg = json.loads(Path(require_hub_file(ROBERTA_REPO, "config.json")).read_text())
    show_config(ROBERTA_REPO, cfg)

    adapter_cfg = json.loads(Path(require_hub_file(LLAMA_ADAPTER, "adapter_config.json")).read_text())
    print(f"== {LLAMA_ADAPTER} adapter_config.json")
    for key in ("task_type", "base_model_name_or_path", "modules_to_save", "num_labels", "r", "target_modules"):
        if key in adapter_cfg:
            print(f"  {key}: {adapter_cfg[key]}")
    from huggingface_hub import hf_hub_download

    try:
        show_config(f"{LLAMA_ADAPTER} config.json", json.loads(Path(hf_hub_download(LLAMA_ADAPTER, "config.json")).read_text()))
    except Exception as exc:  # noqa: BLE001
        if is_gate_error(exc):
            die(gate_message(LLAMA_ADAPTER))
        print(f"  no config.json in adapter repo ({type(exc).__name__}); reading the score head shape instead")
        from safetensors import safe_open

        with safe_open(require_hub_file(LLAMA_ADAPTER, "adapter_model.safetensors"), framework="pt") as fh:
            for key in fh.keys():
                if "score" in key:
                    print(f"  {key}: shape {fh.get_slice(key).get_shape()}")

    if args.skip_dataset:
        return
    from datasets import load_dataset

    print(f"== {DATASET}")
    try:
        ds = load_dataset(DATASET)
    except Exception as exc:  # noqa: BLE001
        if is_gate_error(exc):
            die(gate_message(DATASET, "dataset"))
        raise
    for split, part in ds.items():
        print(f"  split {split}: {len(part)} rows")
        print(f"    features: {part.features}")
    first_split = next(iter(ds))
    print("  first row:")
    for key, value in ds[first_split][0].items():
        text = str(value)
        print(f"    {key}: {text[:200]}{'...' if len(text) > 200 else ''}")


if __name__ == "__main__":
    main()
