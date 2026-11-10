# Animize evaluation harness

Local harness for measuring what the `animize` skill does to prose: detector
scores before and after, clause-level fidelity under the preserve regime,
routing accuracy, and whether a run stayed unattended. It lives under
`.eval/` because it is repo infrastructure, not a skill. Nothing here is
committed by the scripts.

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
   `meta-llama/Llama-3.2-3B` (the adapter's base, approved separately by
   Meta). The dataset `pangram/editlens_iclr` has its own contact-info gate;
   accept that too.
3. Clone <https://github.com/pangramlabs/EditLens> anywhere outside this
   repository. Its `data/` folder holds the scores Pangram published for
   each dataset split; `compare_reference.py` checks local scores against
   them.
4. On WSL2, give the VM enough RAM for the Llama base in 4-bit plus two
   Qwen models: put `memory=32GB` (or more) and `swap=16GB` under
   `[wsl2]` in `%UserProfile%\.wslconfig`, then `wsl --shutdown`.

Until steps 1 and 2 are done, `inspect_labels.py`, `score_editlens.py`, and
`sample_iclr.py` exit with a message naming the missing step instead of a
traceback.

The Pangram models and dataset are CC BY-NC-SA 4.0, noncommercial only.
Dataset text is never committed: `iclr/` is ignored by git and only ids and
scores are tracked.

## Scripts

| Script                  | Purpose                                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `build_corpus.py`       | Assemble `corpus.jsonl` from `corpus/<cell>/<source_class>/*.txt`; `--fetch-pilot` downloads six Gutenberg passages |
| `sample_iclr.py`        | Draw a seeded sample of the gated dataset into `iclr/` as a second corpus cell, with its job list                   |
| `run_animize.py`        | `jobs` emits `jobs.jsonl` for the agent session; `merge` validates `outputs/*.jsonl` and counts unattended failures |
| `inspect_labels.py`     | Print the EditLens bucket counts and the `editlens_iclr` dataset shape                                              |
| `score_editlens.py`     | Score a JSONL file or a dataset split with `--model roberta` or `--model llama` (gated)                             |
| `compare_reference.py`  | Check local EditLens scores against the scores Pangram published for the same rows                                  |
| `score_binoculars.py`   | Score with the Binoculars ratio using Qwen2.5-1.5B base and Instruct (ungated)                                      |
| `calibrate.py`          | Pick thresholds (1% and 0.5% FPR, macro-F1) from a labeled split into `calibration.json`; `--check` adds held-out   |
| `clause_diff.py`        | Preserve-regime accounting: kept, edited, added, deleted clauses and model token share; `--demo` prints an example  |
| `report.py`             | Markdown report per cell and regime; runs on partial inputs and lists what is missing                               |
| `summarize_pilot.py`    | Pilot summary: paired Binoculars deltas, Preserve accounting, injected-defect repair, routing accuracy              |
| `summarize_editlens.py` | EditLens scores and calibrated verdicts for sources and outputs, per cell                                           |
| `score_rater.py`        | Unblind one rater's reading-room export: pairwise preference, single-passage ratings, and the rater's own edit      |
| `_common.py`            | Shared JSONL, windowing, job-row, and gate-check helpers                                                            |

Every script accepts `--help`.

## Run order

```sh
python build_corpus.py --fetch-pilot                  # corpus/pilot/human + corpus.jsonl
python run_animize.py jobs --origins own,generated,unstated --budgets 0.05,0.15,0.30
# ... one agent session per job runs the skill and writes outputs/*.jsonl ...
python run_animize.py merge --outputs 'outputs/*.jsonl' --out outputs.jsonl
python clause_diff.py --input outputs.jsonl --out diffs.jsonl
python score_binoculars.py --input outputs.jsonl --text-field output_text --out scores_binoculars_outputs.jsonl

python inspect_labels.py
python score_editlens.py --model roberta --iclr-split val --out scores_roberta_iclr_val.jsonl
python score_editlens.py --model roberta --iclr-split test --out scores_roberta_iclr_test.jsonl
python compare_reference.py --scores scores_roberta_iclr_val.jsonl --reference ~/EditLens/data/val.csv
python calibrate.py --scores scores_roberta_iclr_val.jsonl --split val \
    --check scores_roberta_iclr_test.jsonl --out calibration.json
python score_editlens.py --model roberta --input corpus.jsonl --out scores_roberta_source.jsonl
python score_editlens.py --model roberta --input outputs.jsonl --text-field output_text --out scores_roberta_outputs.jsonl
python summarize_editlens.py --outputs outputs.jsonl --source-scores scores_roberta_source.jsonl \
    --output-scores scores_roberta_outputs.jsonl --calibration calibration.json

python sample_iclr.py --split test --per-class 10     # iclr/corpus.jsonl + iclr/jobs.jsonl
# ... agent sessions write iclr/outputs/*.jsonl ...
python run_animize.py merge --jobs iclr/jobs.jsonl --outputs 'iclr/outputs/*.jsonl' --out iclr/outputs.jsonl
python clause_diff.py --input iclr/outputs.jsonl --out iclr/diffs.jsonl
python score_editlens.py --model roberta --input iclr/corpus.jsonl --out iclr/scores_roberta_source.jsonl
python score_editlens.py --model roberta --input iclr/outputs.jsonl --text-field output_text --out iclr/scores_roberta_outputs.jsonl
python summarize_editlens.py --outputs iclr/outputs.jsonl --source-scores iclr/scores_roberta_source.jsonl \
    --output-scores iclr/scores_roberta_outputs.jsonl --calibration calibration.json \
    --diffs iclr/diffs.jsonl --export iclr_scored_roberta.jsonl

python score_rater.py --answers rater_answers.json
```

Each session gets the skill, the job's `source_text`, and the job's
`caller_statement` as the caller's own words. An `unstated` job passes the
text with a bare request and nothing else. The session records the regime it
ran (`regime_assigned`), whether it put a question to the caller
(`asked_question`), and its `notes`. `merge` counts a question, a regime
other than the job's, and an `unstated` run without the origin note as
failures.

Repeat every `--model roberta` step with `--model llama` and `llama` in the
file names. Calibrate on one split and check on another: thresholds picked
on `val` are applied to `test`, and the sampled cell is drawn from `test`,
so no document is scored by a threshold it helped choose.

## Files

- `corpus/pilot/human/`: six public-domain passages (Thoreau, Twain, Darwin,
  Franklin, Douglass, Paine), 200 to 400 words, book id in the sibling json.
- `corpus/pilot/ai/`: six agent-written mirrors of those passages, each on
  its passage's topic and in its register, with the topic and generator in
  the sibling json.
- `corpus/pilot/human_defect/`: the six human passages with five defects
  injected into each. The sibling json lists the inserted strings under
  `injected`; `summarize_pilot.py` and `score_rater.py` count a defect as
  repaired when its string is gone from the output.
- `smoke.jsonl`: five documents for smoke tests. The two `ai_synthetic`
  rows are hand-written stand-ins in a generic corporate register about a
  fictional product, not real model outputs; do not treat their scores as
  evidence about any model. The `human_edited` row carries `source_text` so
  `clause_diff.py` can run on it.
- `calibration.json`: thresholds per detector, with the split they came
  from and their held-out rates.
- `scores_*_iclr_*.jsonl`: ids, labels, and scores for the dataset splits.
  Untracked; regenerate them with `score_editlens.py --iclr-split`.
- `iclr_sample.json`: the split, seed, and ids of the sampled second cell.
  `iclr/` itself (dataset text, jobs, outputs) is untracked;
  `iclr_scored_roberta.jsonl` and `iclr_scored_llama.jsonl` keep its
  per-job scores and clause-diff counts without any text.
- `rater_answers.json`: one rater's reading-room export, with the rater
  identified only as `R1`. `rater_edit.jsonl` is that rater's own edit as a
  scoreable row.
- `outputs/`: where the agent session drops its `*.jsonl` files.
- `jobs.jsonl`, `outputs/`, `outputs.jsonl`, `diffs.jsonl`, the
  `scores_*_outputs.jsonl` files, and the two `iclr_scored_*.jsonl` files
  hold the runs of 2026-09-19 and 2026-11-09. Their job ids carry a
  `__deep__` segment and their job rows carry `pass` and `controls` fields,
  the job format on those dates. `merge` and every script after it read
  both formats.

## Known failure points

- Gated repos: any download of the Pangram or Llama repos fails until login
  and terms are accepted. The scripts say so and exit with status 2.
- The Llama adapter has no `config.json`; the bucket count comes from the
  score head shape in `adapter_model.safetensors`, and the head is a
  LayerNorm followed by a bias-free Linear, not the stock Linear. Loading
  prints `score.weight | MISSING` for the base model; the adapter supplies
  the head, and `compare_reference.py` confirms it.
- Llama scores for identical text vary by a few thousandths between runs
  with different batch composition.
- EditLens lowercases and whitespace-normalizes text before scoring, and
  truncates at 512 tokens (roberta) or 1024 (llama). A longer document is
  scored on its opening only; the `truncated` field says when.
- The open RoBERTa model reads the pilot's agent-written mirrors as human.
  Detector sensitivity on a corpus has to be shown on its sources before
  an unchanged verdict on its outputs means anything.
- Binoculars asserts identical tokenizers; a different observer/performer
  pair with mismatched vocabularies is refused.
- Documents under 50 words are skipped everywhere (Pangram scope limit).
- Famous public-domain text is partly memorized by the observer model, so
  Binoculars scores it lower than fresh human prose (Douglass scored 0.93 on
  the pilot, below the corporate stand-ins). Calibrate on unseen human text.
- `clause_diff.py` uses a heuristic verb list to decide where a comma
  starts a new clause; check `--demo` output by hand before trusting rates.
  It reports a false `added` clause when an edit repairs glued punctuation
  (`."I said."What`) or gives a verbless fragment its verb, because either
  moves a clause boundary. Read every flagged clause before counting it.
- WSL2 memory: model loads that fail with a killed process usually mean
  `.wslconfig` memory is too low.
