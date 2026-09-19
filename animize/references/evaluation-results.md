# Evaluation results

Pilot run of 2026-09-19 against the two-pass design. Every number here is
pilot scale: 6 documents per cell, far below the protocol's 100. The numbers
answer "does the design behave as specified" on a small labeled corpus. They
do not establish the population rates the acceptance criteria ask for.

## Contents

- [Setup and provenance](#setup-and-provenance)
- [What was not run](#what-was-not-run)
- [Routing](#routing)
- [Preserve regime](#preserve-regime)
- [Recompose regime and the misrouting cost](#recompose-regime-and-the-misrouting-cost)
- [Detector column](#detector-column)
- [Quick core versus full skill](#quick-core-versus-full-skill)
- [Acceptance criteria, pass or fail](#acceptance-criteria-pass-or-fail)
- [Manual production spot check](#manual-production-spot-check)

## Setup and provenance

- Harness: the repository's `.eval/animize/` folder, run from a Python 3.11
  environment with CUDA torch on one RTX 4090 under WSL2.
- Corpus: `corpus/pilot/`. Six public-domain human passages (Thoreau, Twain,
  Darwin, Franklin, Douglass, Paine; 204 to 267 words), six synthetic mirrors
  written by an agent session on the same topic and register at the same
  length (`ai`), and six defect-injected copies of the human passages with
  exactly five injected defects each: a generic opening, a generic moral
  closing, a filler phrase, a trailing `-ing` significance tail, and an empty
  significance adverb (`human_defect`). A script verified that removing the
  five injected strings restores each original byte for byte.
- Runs: every deep run was executed by an independent agent session given
  the skill files and the job list, one session per cell. Cells: Preserve on
  `human_defect` at budgets 0.05, 0.15, and 0.30; Preserve on strong `human`
  drafts at 0.15; Recompose on `ai`; Recompose on `human_defect` with the
  caller stating the draft was generated (the misrouting cell). A separate
  session made routing decisions for all 18 documents from the text and
  request alone. 36 outputs in total.
- Detector: Binoculars, computed in `score_binoculars.py` with
  `Qwen/Qwen2.5-1.5B` (observer, revision `8faed761d4`) and
  `Qwen/Qwen2.5-1.5B-Instruct` (performer, revision `989aa7980e`), bf16, 512
  token windows with stride 256. Lower scores mean more model-like. No
  calibration file exists; the only reference line is the lowest score among
  the six strong human sources, which is not a verdict threshold.
- Clause diff: `clause_diff.py` with the document-level token count. Two
  splitter defects found during the run (a case-sensitive sentence boundary
  and "indeed" scored as a verb) were fixed before the final accounting.
- Raw rows: `outputs/*.jsonl`, `scores_binoculars_*.jsonl`, `diffs.jsonl`,
  and `pilot_summary.md` in the harness folder.

## What was not run

- The Open Pangram (EditLens) columns, threshold calibration on the
  `editlens_iclr` split, and the humanizer-head metric. The model and dataset
  repositories are gated behind a contact-information agreement and the base
  Llama model behind Meta's license; this machine had no Hugging Face login.
  The scripts exist and fail with a message naming the missing step.
- The blind human-preference and skeptical-observer suites. They need raters.
- The production spot check. See the last section.
- The protocol's synthetic-mirror comparison at scale, the academic and
  second-language `clarity: plain` cell, and the 100-per-cell corpus.

## Routing

18 documents, 18 decisions, 0 wrong guesses (a wrong guess is Preserve
assigned without a caller statement, or anything but Preserve assigned with
one).

| Hidden class | Caller statement   | Preserve | Recompose | Ask |
| ------------ | ------------------ | -------- | --------- | --- |
| human        | "Here is my draft" | 6        | 0         | 0   |
| human_defect | none               | 0        | 3         | 3   |
| ai           | none               | 0        | 3         | 3   |

The question fired on the same three memoir subjects (Douglass, Franklin,
Twain) in both the human and the mirror cells and never on the expository or
argumentative subjects. The heuristic reacts to genre, not to provenance,
which is what the routing section specifies: it decides whether to ask, and
the caller's answer decides the regime. The routing session's own note on the
rule: "particulars the model could not have supplied" is the phrase that
carries the decision, and a narrower reading (proper names and dates only)
would have silently recomposed two human memoirs. The broader reading costs
one question on generic first-person prose and is the safer default.

## Preserve regime

Injected-defect repair on `human_defect`, 6 drafts per cell:

| Budget | Generic opening | Generic closing | Filler | `-ing` tail | Empty adverb | All five |
| ------ | --------------- | --------------- | ------ | ----------- | ------------ | -------- |
| 0.05   | 6/6             | 6/6             | 6/6    | 6/6         | 6/6          | 6/6      |
| 0.15   | 6/6             | 6/6             | 6/6    | 6/6         | 6/6          | 6/6      |
| 0.30   | 6/6             | 6/6             | 6/6    | 6/6         | 6/6          | 6/6      |

Clause-diff accounting, totals over 6 drafts per cell:

| Cell                 | Kept | Edited | Deleted | Added | Reordered | Mean share | Max share | Within budget |
| -------------------- | ---- | ------ | ------- | ----- | --------- | ---------- | --------- | ------------- |
| human_defect, 0.05   | 99   | 11     | 35      | 0     | 0         | 0.002      | 0.014     | 6/6           |
| human_defect, 0.15   | 106  | 7      | 32      | 0     | 0         | 0.002      | 0.009     | 6/6           |
| human_defect, 0.30   | 102  | 8      | 35      | 0     | 0         | 0.000      | 0.000     | 6/6           |
| human (strong), 0.15 | 99   | 11     | 2       | 0     | 0         | 0.015      | 0.032     | 6/6           |

Findings:

- Every injected defect in this family was repaired by deletion or by a
  split at an existing clause boundary, so the budget never bound. The
  0.05, 0.15, and 0.30 cells are indistinguishable on this defect family. A
  budget experiment needs defects whose repair requires new words (a missing
  antecedent, a dangling comparison, an unstated actor), not scaffolding that
  can be cut.
- The only genuinely model-supplied tokens across the 18 defect-cell outputs
  were "my father's" in Franklin, substituted for a pronoun whose antecedent
  lived in the deleted generic opener, and "to it" for "thereto" in Paine.
  Both sessions flagged the father inference in the notes for the caller to
  confirm.
- Sessions delivered suggested openings or endings in the notes rather than
  the artifact in three cases (a Twain ending twice, a Paine ending once), as
  the edit policy requires.
- Over-editing on strong drafts is the real signal in that cell: 11 edited
  clauses across 6 drafts under a request that said "keep my wording where
  you can," including "prudential" to "practical" and "sung withal" to
  "sang as well" in Franklin, while Twain was returned verbatim. The session
  listed each change with a revert option, reverted one referent swap on its
  own proportion check, and every number, name, and quotation survived. The
  blind preference test that decides whether this is acceptable was not run.

## Recompose regime and the misrouting cost

Recompose on the six `ai` mirrors kept 4 to 17 source clauses per document,
regenerated the rest, and held length within 7% of the source. Model-token
share ranged from 0.047 to 0.231 (mean 0.126).

Recompose on the six `human_defect` drafts, with the caller stating the draft
was generated, removed all five injected defects in every document and cut
20 to 25% of the length. Model-token share ranged from 0.035 to 0.280 (mean
0.141), 5 to 15 clauses were kept per document, and the sessions split a
95-word Twain sentence and modernized "publick". That is the cost of routing
a human draft to Recompose: the defects are gone, and so is a fifth of the
author's wording. Under Preserve the same defects were removed at 0.000 to
0.014 model-token share.

Automated fidelity checks on all 36 outputs: 0 source numbers missing from
any output, 0 generated dash characters.

## Detector column

Binoculars with the 1.5B Qwen pair does not separate the cells:

| Source class | n   | Mean  | Median | Min   | Max   |
| ------------ | --- | ----- | ------ | ----- | ----- |
| ai           | 6   | 0.996 | 1.003  | 0.954 | 1.026 |
| human        | 6   | 0.979 | 0.980  | 0.928 | 1.022 |
| human_defect | 6   | 1.003 | 1.009  | 0.956 | 1.047 |

The agent-written mirrors score as high as the human passages, and the
famous human passages score lower than fresh prose because the observer has
partly memorized them. Two hand-written corporate stand-ins in the smoke test
did score lowest (0.961 and 0.977), so the score reacts to register, not to
provenance, at this model size. Paired output deltas were all small:

| Cell                        | Source mean | Output mean | Mean delta |
| --------------------------- | ----------- | ----------- | ---------- |
| ai, Recompose               | 0.996       | 1.002       | +0.006     |
| human, Preserve 0.15        | 0.979       | 0.968       | -0.011     |
| human_defect, Preserve 0.05 | 1.003       | 0.985       | -0.018     |
| human_defect, Preserve 0.15 | 1.003       | 0.990       | -0.013     |
| human_defect, Preserve 0.30 | 1.003       | 0.977       | -0.026     |
| human_defect, Recompose     | 1.003       | 0.997       | -0.006     |

Read this as: the skill did not move this detector in either direction by
more than the spread within a cell. It is consistent with the "does not
move a verdict" claim and is not evidence for it; a column with a trained
classifier and a calibrated threshold is required, and that column is
blocked on the gated weights.

## Quick core versus full skill

Six routine-communication drafts with 25 injected local defects (chatbot
wrappers, generated dashes, filler, `simply` and `please` in instructions,
`not just X, but Y`, an `-ing` significance tail, a label-restating list, an
unsupported `As a [role], I` opener, a described symbol with a visible name)
were given to two sessions: one with only the 47-line quick core as its
system rules and no files, one with the full entry point and the instruction
to run the quick pass.

| Condition  | Defects repaired | Exact tokens preserved | Fidelity notes                                                 |
| ---------- | ---------------- | ---------------------- | -------------------------------------------------------------- |
| Quick core | 25/25            | all                    | one stance strengthened ("does not block" to "ready to merge") |
| Full skill | 25/25            | all                    | none                                                           |

The full-skill session's file trace shows reads of `SKILL.md` only, so the
quick isolation invariant held.

## Acceptance criteria, pass or fail

| Criterion                                                            | Result at pilot scale                                                      |
| -------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Preserve: zero added clauses, share under budget                     | Pass: 0 added clauses in 24 outputs, max share 0.032                       |
| Preserve: at least 95% labeled human or AI-assisted                  | Not measurable; trained classifier blocked                                 |
| Preserve: zero humanizer-head positives                              | Not measurable; the open models have no such head                          |
| Preserve fidelity at or above Recompose                              | Pass: 0 number losses, 0 added clauses, 2 flagged inferences, all in notes |
| Recompose: verdict distribution unchanged on trained classifiers     | Not measurable; Binoculars deltas within cell spread                       |
| Human preference, 60% and 45% thresholds                             | Not run                                                                    |
| Routing accuracy at or above 90%, remainder resolved by the question | Pass: 0 wrong guesses in 18, 6 questions                                   |
| Quick pass loads no references                                       | Pass                                                                       |
| Quick core matches full skill on routine communication               | Pass on defect repair (25/25 each); one stance drift in the core           |

## Manual production spot check

Not performed. The protocol allows up to twenty final documents to be checked
by hand on the vendor's free web checker. That step needs a person at a
browser and is left for the maintainer, with the same rule as the rest of
the protocol: record the verdicts here under this heading, never frame one
as a bypass rate, and paste no user or customer text.
