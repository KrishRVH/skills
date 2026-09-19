# Animize evaluation harness

Local harness for measuring what the `animize` skill does to prose: detector
scores before and after, clause-level fidelity under the preserve regime,
and routing accuracy. It lives under `.eval/` because it is repo
infrastructure, not a skill. Nothing here is committed by the scripts.

## Setup

The Python 3.11 virtualenv already exists. Every command below assumes it:

```sh
source ~/animize-eval/.venv/bin/activate
cd .eval/animize
```

Model weights cache to `~/.cache/huggingface` on the Linux filesystem. The
Qwen pair for Binoculars is ungated. The Pangram EditLens models and dataset
are gated, so once only:

1. `hf auth login` with a Hugging Face token (read scope is enough).
2. In a browser, accept the terms on each of these repos while logged in:
   `pangram/editlens_roberta-large`, `pangram/editlens_Llama-3.2-3B`, and
   `meta-llama/Llama-3.2-3B` (the adapter's base). The dataset
   `pangram/editlens_iclr` has its own contact-info gate; accept that too.
3. On WSL2, give the VM enough RAM to load Llama 3.2 3B in bf16 plus two
   Qwen models: put `memory=32GB` (or more) and `swap=16GB` under
   `[wsl2]` in `%UserProfile%\.wslconfig`, then `wsl --shutdown`.

Until step 1 and 2 are done, `inspect_labels.py` and `score_editlens.py`
exit with a message naming the missing step instead of a traceback.

## Scripts

| Script                | Purpose                                                                                                             |
| --------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `build_corpus.py`     | Assemble `corpus.jsonl` from `corpus/<cell>/<source_class>/*.txt`; `--fetch-pilot` downloads six Gutenberg passages |
| `run_animize.py`      | `jobs` emits `jobs.jsonl` for the agent session; `merge` validates `outputs/*.jsonl` into `outputs.jsonl`           |
| `inspect_labels.py`   | Print EditLens label spaces and the `editlens_iclr` dataset shape so you can fill `bucket_map.json`                 |
| `score_editlens.py`   | Score with `--model roberta` or `--model llama` (gated)                                                             |
| `score_binoculars.py` | Score with the Binoculars ratio using Qwen2.5-1.5B base and Instruct (ungated)                                      |
| `calibrate.py`        | Pick thresholds (1% and 0.5% FPR, macro-F1) from a labeled split into `calibration.json`                            |
| `clause_diff.py`      | Preserve-regime accounting: kept, edited, added, deleted clauses and model token share; `--demo` prints an example  |
| `report.py`           | Markdown report per cell and regime; runs on partial inputs and lists what is missing                               |
| `summarize_pilot.py`  | Pilot summary: paired detector deltas, Preserve accounting, injected-defect repair, routing accuracy                |
| `_common.py`          | Shared JSONL, windowing, and gate-check helpers                                                                     |

Every script accepts `--help`.

## Run order

```sh
python build_corpus.py --fetch-pilot                  # corpus/pilot/human + corpus.jsonl
python run_animize.py jobs --passes quick,deep --regimes preserve,recompose --budgets 0.05,0.15,0.30
# ... the agent session runs the skill and writes outputs/*.jsonl ...
python run_animize.py merge --outputs 'outputs/*.jsonl' --out outputs.jsonl
python clause_diff.py --input outputs.jsonl --out diffs.jsonl
python inspect_labels.py                              # then fill bucket_map.json
python score_editlens.py --model roberta --input corpus.jsonl --out scores_roberta_source.jsonl
python score_editlens.py --model roberta --input outputs.jsonl --text-field output_text --out scores_roberta_outputs.jsonl
python score_binoculars.py --input outputs.jsonl --text-field output_text --out scores_binoculars_outputs.jsonl
python calibrate.py --scores scores_roberta_iclr.jsonl --labels-field label --split test --out calibration.json
python report.py --scores 'scores_*.jsonl' --diffs diffs.jsonl --calibration calibration.json --out report.md
```

`calibrate.py` expects rows scored from a labeled held-out split (for
example `editlens_iclr` after `inspect_labels.py` shows its splits) with a
class field of `human`, `ai_assisted`, or `ai_generated`.

## Files

- `corpus/pilot/human/`: six public-domain passages (Thoreau, Twain, Darwin,
  Franklin, Douglass, Paine), 200 to 400 words, book id in the sibling json.
- `corpus/pilot/ai/`: empty except a README; the agent session fills it.
- `smoke.jsonl`: five documents for smoke tests. The two `ai_synthetic`
  rows are hand-written stand-ins in a generic corporate register about a
  fictional product, not real model outputs; do not treat their scores as
  evidence about any model. The `human_edited` row carries `source_text` so
  `clause_diff.py` can run on it.
- `bucket_map.json`: placeholder (`null`). `score_editlens.py` refuses to run
  a classification head until it holds bucket centers in label order.
- `outputs/`: where the agent session drops its `*.jsonl` files.

## Known failure points

- Gated repos: any download of the Pangram or Llama repos fails until login
  and terms are accepted. The scripts say so and exit with status 2.
- `bucket_map.json` left as `null` when the EditLens head is a classifier.
- The Llama adapter has no `config.json`; `num_labels` comes from the
  score head shape in `adapter_model.safetensors`. Check it against
  `inspect_labels.py` output.
- Binoculars asserts identical tokenizers; a different observer/performer
  pair with mismatched vocabularies is refused.
- Documents under 50 words are skipped everywhere (Pangram scope limit).
- Famous public-domain text is partly memorized by the observer model, so
  Binoculars scores it lower than fresh human prose (Douglass scored 0.93 on
  the pilot, below the corporate stand-ins). Calibrate on unseen human text.
- `clause_diff.py` uses a heuristic verb list to decide where a comma
  starts a new clause; check `--demo` output by hand before trusting rates.
- WSL2 memory: model loads that fail with a killed process usually mean
  `.wslconfig` memory is too low.
