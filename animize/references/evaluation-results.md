# Evaluation results

Pilot run of 2026-09-19, with the trained-classifier column, a second
corpus cell, and one blind expert rating added on 2026-11-09. Every number
here is pilot scale: 6 to 10 documents per cell, far below the 100 the
protocol calls for. The numbers answer "does the design behave as specified"
on a small labeled corpus. They do not establish the population rates the
acceptance criteria ask for.

Those runs measured the Preserve and Recompose branches with the regime
stated in every job. On those dates the skill also had a lighter pass for
short artifacts and asked the caller one question about a first-person draft
of unstated origin. Both were removed on 2026-11-09, when the skill became
one unattended procedure. [Unattended runs](#unattended-runs) holds the
forward tests of that change and of the consolidation that followed, and
[Guardrail check after consolidation](#guardrail-check-after-consolidation)
holds the detector scores for both.

## Contents

- [Setup and provenance](#setup-and-provenance)
- [What was not run](#what-was-not-run)
- [Routing](#routing)
- [Preserve regime](#preserve-regime)
- [Recompose regime and its cost on a human draft](#recompose-regime-and-its-cost-on-a-human-draft)
- [Detector column](#detector-column)
- [Trained-classifier column](#trained-classifier-column)
- [Prompt block versus the skill](#prompt-block-versus-the-skill)
- [Blind expert rating](#blind-expert-rating)
- [Unattended runs](#unattended-runs)
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
- Runs: every run was executed by an independent agent session given the
  skill files and the job list, one session per cell. Cells: Preserve on
  `human_defect` at budgets 0.05, 0.15, and 0.30; Preserve on strong `human`
  drafts at 0.15; Recompose on `ai`; Recompose on `human_defect` with the
  caller stating the draft was generated (the recomposed-human cell). A separate
  session made routing decisions for all 18 documents from the text and
  request alone. 36 outputs in total.
- Detector: Binoculars, computed in `score_binoculars.py` with
  `Qwen/Qwen2.5-1.5B` (observer, revision `8faed761d4`) and
  `Qwen/Qwen2.5-1.5B-Instruct` (performer, revision `989aa7980e`), bf16, 512
  token windows with stride 256. Lower scores mean more model-like. No
  calibration file exists; the only reference line is the lowest score among
  the six strong human sources, which is not a verdict threshold.
- Trained classifiers: the two open EditLens models (CC BY-NC-SA 4.0), the
  RoBERTa classifier `pangram/editlens_roberta-large` (revision
  `f93e1ace74`) and the LoRA adapter `pangram/editlens_Llama-3.2-3B`
  (revision `b5f8044f63`) on `meta-llama/Llama-3.2-3B` loaded in 4-bit.
  `score_editlens.py` scores the way the reference inference script does
  (EditLens repository commit `05a588f1`): text lowercased and
  whitespace-normalized, one pass truncated at 512 tokens (RoBERTa) or 1,024
  (Llama), and a score equal to the expected bucket, scaled to 0 through 1.
  Thresholds live in `calibration.json`, chosen on the dataset's `val` split
  and checked on its `test` split.
- Clause diff: `clause_diff.py` with the document-level token count. Two
  splitter defects found during the run (a case-sensitive sentence boundary
  and "indeed" scored as a verb) were fixed before the final accounting.
- Raw rows: `outputs/*.jsonl`, `scores_binoculars_*.jsonl`, `diffs.jsonl`,
  and `pilot_summary.md` in the harness folder.

## What was not run

- The production checker on outputs of the current text. A blind packet of
  twenty outputs from the guardrail check is prepared and has not been
  pasted. The production results below are from the pilot run.
- A blind rating of the current text's outputs, or of the two model tiers.
- A guardrail check that separates the two changes of 2026-11-09. One run
  covers both.
- The full procedure on the short-artifact defect suite. That suite was run
  against the lighter pass the skill then had.
- The humanizer-head metric. Neither open model has such a head.
- The blind human-preference and skeptical-observer suites at protocol
  scale. One expert rater completed a reduced packet; see
  [Blind expert rating](#blind-expert-rating).
- The protocol's synthetic-mirror comparison at scale, the academic and
  second-language clear-communication cell, and the 100-per-cell corpus.

## Routing

Measured on 2026-09-19 under the rule of that date: the caller's statement
decided the regime, and a first-person draft of unstated origin drew one
question. 18 documents, 18 decisions, 0 wrong guesses (a wrong guess is
Preserve assigned without a caller statement, or anything but Preserve
assigned with one).

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

The skill no longer asks. Under the current rule all twelve unstated drafts
route to Recompose with the origin note, including the three human memoirs
that drew a question here. The next section measures what that costs a human
draft.

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
- The strong-draft cell shows over-editing: 11 edited
  clauses across 6 drafts under a request that said "keep my wording where
  you can," including "prudential" to "practical" and "sung withal" to
  "sang as well" in Franklin, while Twain was returned verbatim. The session
  listed each change with a revert option, reverted one referent swap on its
  own proportion check, and every number, name, and quotation survived. The
  blind rating later put a reader's judgment on these edits; see
  [Blind expert rating](#blind-expert-rating).

## Recompose regime and its cost on a human draft

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
0.014 model-token share. An author who does not say they wrote a draft now
gets the first result, and the origin note tells them how to get the second.

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
move a verdict" claim and is not evidence for it; that takes a trained
classifier with a calibrated threshold, which the next section supplies.

## Trained-classifier column

Added 2026-11-09 with both open EditLens models: the RoBERTa classifier and
the LoRA adapter on `meta-llama/Llama-3.2-3B` (adapter revision
`b5f8044f63`, base loaded in 4-bit as in the reference script). Every
verdict below is an EditLens verdict from an open research model. None is a
production verdict.

### Reproduction and calibration

Local scores reproduce the scores Pangram published for the same dataset
rows, which is the check that the models are loaded and fed correctly:

| Model   | Rows compared | Mean absolute gap | Largest gap | Pearson r |
| ------- | ------------- | ----------------- | ----------- | --------- |
| RoBERTa | 8,515         | 0.0004            | 0.057       | 1.0000    |
| Llama   | 8,515         | 0.0007            | 0.022       | 1.0000    |

Thresholds were chosen on the dataset's `val` split (2,400 documents) and
then applied unchanged to its `test` split (6,115 documents: 2,038 human,
2,031 AI-edited, 2,046 AI-generated). A score at or below the human line
reads as human, a score above the generated line reads as AI-generated, and
anything between reads as AI-assisted.

| Model   | Human line | Generated line | Human read as not human | Generated read as not human | AI-edited read as human | Generated read as only assisted | Three-class accuracy |
| ------- | ---------- | -------------- | ----------------------- | --------------------------- | ----------------------- | ------------------------------- | -------------------- |
| RoBERTa | 0.290      | 0.998          | 0.7%                    | 99.9%                       | 33.4%                   | 9.6%                            | 0.837                |
| Llama   | 0.199      | 0.974          | 0.5%                    | 100.0%                      | 26.2%                   | 6.8%                            | 0.879                |

Two base rates in that table govern everything after it. Both models
separate human from fully generated text almost perfectly on their own
data. Both also read a quarter to a third of AI-edited documents as human,
so a human verdict from either cannot rule out light machine editing.

### Pilot corpus

Counts read human / AI-assisted / AI-generated.

| Source class         | n   | RoBERTa mean | RoBERTa verdicts | Llama mean | Llama verdicts |
| -------------------- | --- | ------------ | ---------------- | ---------- | -------------- |
| ai (agent mirrors)   | 6   | 0.098        | 6 / 0 / 0        | 0.467      | 0 / 6 / 0      |
| human                | 6   | 0.050        | 6 / 0 / 0        | 0.134      | 5 / 1 / 0      |
| human_defect         | 6   | 0.095        | 6 / 0 / 0        | 0.254      | 2 / 4 / 0      |
| smoke: corporate, AI | 2   | 1.000        | 0 / 0 / 2        | 1.000      | 0 / 0 / 2      |

| Cell                        | n   | RoBERTa source to output | RoBERTa verdicts after | Llama source to output | Llama verdicts before | Llama verdicts after |
| --------------------------- | --- | ------------------------ | ---------------------- | ---------------------- | --------------------- | -------------------- |
| ai, Recompose               | 6   | 0.098 to 0.064           | 6 / 0 / 0              | 0.467 to 0.484         | 0 / 6 / 0             | 0 / 6 / 0            |
| human, Preserve 0.15        | 6   | 0.050 to 0.055           | 6 / 0 / 0              | 0.134 to 0.155         | 5 / 1 / 0             | 5 / 1 / 0            |
| human_defect, Preserve 0.05 | 6   | 0.095 to 0.058           | 6 / 0 / 0              | 0.254 to 0.175         | 2 / 4 / 0             | 5 / 1 / 0            |
| human_defect, Preserve 0.15 | 6   | 0.095 to 0.055           | 6 / 0 / 0              | 0.254 to 0.159         | 2 / 4 / 0             | 5 / 1 / 0            |
| human_defect, Preserve 0.30 | 6   | 0.095 to 0.056           | 6 / 0 / 0              | 0.254 to 0.167         | 2 / 4 / 0             | 5 / 1 / 0            |
| human_defect, Recompose     | 6   | 0.095 to 0.060           | 6 / 0 / 0              | 0.254 to 0.171         | 2 / 4 / 0             | 3 / 3 / 0            |

Findings:

- **The RoBERTa model cannot see this corpus.** It reads the six
  agent-written mirrors as human at scores of 0.06 to 0.15, although it
  scores two generic corporate stand-ins at 1.000. An unchanged verdict on
  an output means nothing when the source was never detected, so this model
  says nothing about Recompose here.
- **The Llama model reads the mirrors as AI-assisted, never AI-generated.**
  The production checker read the same six as AI-generated. The open models
  are weaker than production on this register, as the protocol expects.
- **The Llama model labels the defect drafts correctly.** Four of six read
  as AI-assisted, and they are: human paragraphs with model-written
  sentences injected. Preserve deleted those sentences and all four
  returned to human at every budget, at scores close to the clean
  originals. That is the Preserve claim in miniature: the output carries
  the label of the text that is left.
- **Preserve moved one draft the wrong way.** Paine read as human with the
  defects in (0.167) and as AI-assisted after Preserve at every budget
  (0.375 to 0.435). The clean Paine paragraph already sits above the human
  line at 0.247, a false positive on prose from 1776, and Preserve on that
  strong draft raised it to 0.291. The edits were the ones the blind rater
  preferred: a long semicolon chain split into sentences, "thereto"
  replaced by "to it," "nay" by "or." The reader and the classifier
  disagree about that edit. Under the protocol the reader decides, and a
  detector moving is not grounds to change a rule.
- **Recompose shows no direction on the mirrors.** Four of six Llama scores
  rose and two fell. The Twain passage, returned unchanged, scored 0.165 as
  a source and 0.169 as an output, so differences of that size on this
  model are run-to-run noise.

### Second cell: documents from the detector's own data

The pilot corpus has two weaknesses for this column: its human text is
famous, and its generated text is not detected. A second cell fixes both.
Twenty documents of 200 to 400 words were drawn at random, with a fixed
seed and with no selection on any score, from the dataset's `test` split:
ten human (news, educational web pages, fiction written to prompts) and ten
generated (by three vendors' models, across news, reviews, reference text,
and fiction). Three independent sessions ran the procedure: Recompose on
the generated ten, Preserve on the human ten with the caller calling the
draft their own, and Recompose on the human ten with the caller calling it
generated. The dataset is gated, so its text is not in this repository;
`iclr_sample.json` lists the ids, and `iclr_scored_roberta.jsonl` and
`iclr_scored_llama.jsonl` hold the per-job scores.

| Cell                 | n   | RoBERTa source to output | RoBERTa verdicts before | RoBERTa verdicts after | Llama source to output | Llama verdicts before | Llama verdicts after |
| -------------------- | --- | ------------------------ | ----------------------- | ---------------------- | ---------------------- | --------------------- | -------------------- |
| generated, Recompose | 10  | 0.999 to 0.996           | 0 / 1 / 9               | 0 / 1 / 9              | 0.991 to 0.946         | 0 / 1 / 9             | 0 / 4 / 6            |
| human, Preserve 0.15 | 10  | 0.018 to 0.035           | 10 / 0 / 0              | 10 / 0 / 0             | 0.007 to 0.013         | 10 / 0 / 0            | 10 / 0 / 0           |
| human, Recompose     | 10  | 0.018 to 0.040           | 10 / 0 / 0              | 10 / 0 / 0             | 0.007 to 0.020         | 10 / 0 / 0            | 10 / 0 / 0           |

Clause-diff accounting from `clause_diff.py`, totals over ten documents:

| Cell                 | Kept | Edited | Deleted | Added | Reordered | Mean share | Share range    | Output length |
| -------------------- | ---- | ------ | ------- | ----- | --------- | ---------- | -------------- | ------------- |
| human, Preserve 0.15 | 240  | 16     | 0       | 2     | 3         | 0.008      | 0.000 to 0.039 | 100% of draft |
| human, Recompose     | 130  | 92     | 34      | 31    | 17        | 0.157      | 0.061 to 0.291 | 98% of draft  |
| generated, Recompose | 70   | 136    | 45      | 39    | 21        | 0.190      | 0.074 to 0.361 | 94% of draft  |

Findings:

- **No Recompose output on generated text read as human.** On RoBERTa no
  verdict changed and the mean fell by 0.003. On Llama the lowest output
  score was 0.672 against a human line of 0.199.
- **Recompose did lower the Llama score.** Nine of ten outputs scored below
  their source, and three crossed from AI-generated to AI-assisted: one
  clearly (1.000 to 0.672), two at the line (1.000 to 0.960, and 0.986 to
  0.974). The Llama model already reads 6.8% of its own generated test
  documents as assisted, and ten documents cannot separate four of ten from
  one of ten (Fisher exact p = 0.30), but nine of ten moving one way is not
  noise (sign test p = 0.02). The accurate statement is narrower than the
  one the protocol set out to prove: Recompose leaves generated text
  reading as machine-written, and it can shift the estimate of how heavily
  machine-written. The skill makes no claim about any detector's verdict,
  and this result is why.
- **Preserve on ordinary human writing reads as human, ten of ten, on both
  models.** These are unpublished drafts of the kind the regime is for, so
  the famous-text caveat on the pilot does not apply. The edits were a
  missing space, agreement and tense repairs, typos, one wrongly decoded
  character, one cut filler phrase, and one deleted navigation line; one
  draft was returned unchanged. Missing openings and paragraph breaks went
  to the notes as suggestions.
- **The two "added" clauses are instrument artifacts.** `clause_diff.py`
  flagged one clause in each of two Preserve outputs. Read by hand, neither
  adds anything: in one the session restored the spaces in
  `"Good evening."I said."What brings you here?"`, which created a sentence
  boundary the source lacked; in the other it corrected "her commitment as
  not simply a military one" to "was," which gave a verbless fragment a
  verb and so a clause boundary. Without those two rows the largest
  model-token share in the cell is 0.008. The splitter's blind spots are
  glued punctuation and verbless clauses; a flagged clause still needs a
  human look.
- **A human verdict does not certify Preserve.** The same ten documents
  after Recompose, with 6% to 29% of their tokens supplied by the model,
  also read as human ten of ten on both models. At this length neither open
  model distinguishes a typo repair from a rebuilt article. The detector
  column shows that Preserve does not trip these classifiers. The evidence
  that its output is still the author's text is the clause diff.

### Guardrail baseline

The protocol now uses these scores as a guardrail on rule changes. The
tables above are the baseline: a later change to the skill is scored on the
same two corpora with `calibration.json` as it stands, and a cell whose
mean rises or whose verdicts move toward machine-written is flagged for a
reader's judgment. The baseline also shows the guardrail's limit. Every
Recompose output on generated text still reads as machine-written, on the
production checker and on both open models, including outputs a blind
expert rated level with human originals. A score from these detectors can
flag a regression. It has not tracked how a skilled reader judged the same
prose.

### Guardrail check after consolidation

Run of 2026-11-09 on the skill text as committed after two changes: one
unattended procedure, and one home per rule. The baseline predates both, so
this check covers them together and cannot separate them. The corpora,
`calibration.json`, and the three detectors are unchanged, and re-scoring
the 18 pilot sources reproduced the recorded EditLens scores exactly.

The sessions differ from the baseline's in one way that matters. Each job
was a caller message and nothing else: "I wrote this draft myself", "A
model generated this draft", or no statement, then "Run Animize on this:"
and the text. No session was told a regime, a budget, or a genre. One
session ran each cell: seven cells and 54 documents on the top tier, and
the same seven on the mid tier. The human drafts reached Recompose by
having no stated origin, which is how they reach it now. Raw rows are in
the harness folder under `consolidated/`.

Unattended checks, from `run_animize.py merge` and each session's recorded
tool calls: 108 jobs, 0 questions, 0 wrong regimes, 0 missing origin notes,
and every session loaded exactly its branch's fixed set.

Top tier. Counts read human / AI-assisted / AI-generated. Each score
column reads source, then baseline output, then this run's output.

| Pilot cell              | n   | RoBERTa mean          | RoBERTa verdicts now | Llama mean            | Llama verdicts: source | baseline  | now       |
| ----------------------- | --- | --------------------- | -------------------- | --------------------- | ---------------------- | --------- | --------- |
| human_defect, Preserve  | 6   | 0.095 / 0.055 / 0.051 | 6 / 0 / 0            | 0.254 / 0.159 / 0.130 | 2 / 4 / 0              | 5 / 1 / 0 | 5 / 1 / 0 |
| human, Preserve         | 6   | 0.050 / 0.055 / 0.054 | 6 / 0 / 0            | 0.134 / 0.155 / 0.145 | 5 / 1 / 0              | 5 / 1 / 0 | 5 / 1 / 0 |
| ai, Recompose           | 6   | 0.098 / 0.064 / 0.100 | 6 / 0 / 0            | 0.467 / 0.484 / 0.515 | 0 / 6 / 0              | 0 / 6 / 0 | 0 / 6 / 0 |
| human_defect, Recompose | 6   | 0.095 / 0.060 / 0.056 | 6 / 0 / 0            | 0.254 / 0.171 / 0.152 | 2 / 4 / 0              | 3 / 3 / 0 | 5 / 1 / 0 |

| Second cell          | n   | RoBERTa mean          | RoBERTa verdicts: source | baseline   | now        | Llama mean            | Llama verdicts: source | baseline   | now        |
| -------------------- | --- | --------------------- | ------------------------ | ---------- | ---------- | --------------------- | ---------------------- | ---------- | ---------- |
| human, Preserve      | 10  | 0.018 / 0.035 / 0.036 | 10 / 0 / 0               | 10 / 0 / 0 | 10 / 0 / 0 | 0.007 / 0.013 / 0.014 | 10 / 0 / 0             | 10 / 0 / 0 | 10 / 0 / 0 |
| generated, Recompose | 10  | 0.999 / 0.996 / 0.991 | 0 / 1 / 9                | 0 / 1 / 9  | 0 / 1 / 9  | 0.991 / 0.946 / 0.921 | 0 / 1 / 9              | 0 / 4 / 6  | 0 / 4 / 6  |
| human, Recompose     | 10  | 0.018 / 0.040 / 0.051 | 10 / 0 / 0               | 10 / 0 / 0 | 10 / 0 / 0 | 0.007 / 0.020 / 0.032 | 10 / 0 / 0             | 10 / 0 / 0 | 10 / 0 / 0 |

Clause-diff accounting from `clause_diff.py` as it stands, run on the
baseline outputs and on this run's. Share is model-added tokens over output
tokens.

| Cell                           | Run      | Kept | Edited | Deleted | Added | Mean share | Max share | Output length |
| ------------------------------ | -------- | ---- | ------ | ------- | ----- | ---------- | --------- | ------------- |
| Pilot, human_defect, Preserve  | baseline | 105  | 7      | 32      | 0     | 0.002      | 0.009     | 82%           |
| Pilot, human_defect, Preserve  | now      | 106  | 7      | 31      | 0     | 0.000      | 0.000     | 83%           |
| Pilot, human, Preserve         | baseline | 99   | 11     | 2       | 0     | 0.015      | 0.032     | 100%          |
| Pilot, human, Preserve         | now      | 112  | 0      | 0       | 0     | 0.000      | 0.000     | 100%          |
| Pilot, ai, Recompose           | baseline | 65   | 53     | 12      | 15    | 0.127      | 0.231     | 96%           |
| Pilot, ai, Recompose           | now      | 108  | 12     | 10      | 7     | 0.058      | 0.185     | 97%           |
| Pilot, human_defect, Recompose | baseline | 52   | 48     | 44      | 10    | 0.141      | 0.280     | 79%           |
| Pilot, human_defect, Recompose | now      | 95   | 12     | 37      | 1     | 0.018      | 0.097     | 82%           |
| Second, human, Preserve        | baseline | 240  | 16     | 0       | 2     | 0.008      | 0.039     | 100%          |
| Second, human, Preserve        | now      | 244  | 12     | 0       | 2     | 0.008      | 0.034     | 100%          |
| Second, generated, Recompose   | baseline | 70   | 136    | 45      | 39    | 0.190      | 0.361     | 94%           |
| Second, generated, Recompose   | now      | 50   | 135    | 66      | 55    | 0.253      | 0.490     | 94%           |
| Second, human, Recompose       | baseline | 130  | 92     | 34      | 31    | 0.157      | 0.291     | 98%           |
| Second, human, Recompose       | now      | 123  | 98     | 35      | 37    | 0.147      | 0.307     | 98%           |

Findings:

- **No verdict moved toward machine-written in any cell, on either
  model.** One cell moved the other way: Recompose on the pilot's defect
  drafts read 3 / 3 / 0 on Llama at baseline and reads 5 / 1 / 0 now.
- **Two cells are flagged, because their mean rose against the baseline.**
  Recompose on the pilot mirrors went from 0.484 to 0.515 on Llama. One
  document carries it: the Twain mirror scored 0.422 as a source, 0.570 at
  baseline, and 0.655 now, with 6% of its tokens from the model. Three of
  the six scored below their baseline. The Paine mirror came back with two
  cuts, a paragraph break, and no model-added token, and moved from 0.593
  to 0.613, so a move of 0.02 on this model takes no new wording. Recompose
  on the second cell's human drafts went from 0.020 to 0.032 on Llama and
  0.040 to 0.051 on RoBERTa. All ten read as human on both; the highest
  output scored 0.074 against a human line of 0.199, and 0.109 against
  0.290. Neither flag led to a rule change. Both are for a reader's
  judgment, as the protocol says.
- **Recompose on generated text still reads as machine-written, ten of
  ten.** The Llama mean fell from 0.991 to 0.921, every output scored at or
  below its source, and the verdicts match the baseline's. The lowest
  output scored 0.564. No model-written document reads as human after the
  skill on either model, here or at baseline. A regex screen for common
  machine constructions (dashes, `not just X but Y`, signposts, stock
  vocabulary, `-ing` tails) counts 13.0 per thousand words in those ten
  sources and 2.7 in the outputs, with no dash and no `not just`. What
  remains is stock wording inside praise the source owned, such as "deeply
  moving". The classifiers are not reading those surface features.
- **Preserve stopped over-editing strong drafts.** The baseline changed 11
  clauses across six polished passages. This run changed none: five came
  back byte for byte, and Paine got two semicolons for comma splices. That
  Paine draft still reads AI-assisted on Llama, 0.247 as a source and 0.311
  after the two semicolons.
- **Preserve removed 29 of 30 injected defects, against 30.** "In order to"
  stayed in the Darwin draft on both tiers. Without the repair catalogs the
  sessions did not read it as a defect, and in that passage it is ordinary
  period English. Recompose removed all 30.
- **Recompose keeps more of a good draft than it did.** On the pilot's
  defect drafts the model-token share fell from 0.141 to 0.018, and on the
  mirrors from 0.127 to 0.058. The sessions said why: with the injected
  scaffolding cut, nearly every remaining sentence passed R4's test for
  retaining a sentence that is already exact. On the second cell's ordinary
  drafts, which have real defects, the share is where it was (0.147 against
  0.157), and on real model output Recompose rebuilt more than before
  (0.253 against 0.190).
- **The two `added` clauses under Preserve are the baseline's two
  instrument artifacts**, in the same two documents: repaired dialogue
  punctuation, and "as" corrected to "was". Without them the largest share
  in the cell is 0.008.
- **Binoculars moved by less than its spread**, as before. Pilot output
  means run from 0.979 to 0.993 against sources of 0.979 to 1.003.
- **Fidelity checks:** 0 source numbers missing from any pilot output and 0
  generated dash characters, on both tiers.

Outputs that read as human, top tier, as a count per cell:

| Draft and branch                                 | Corpus      | RoBERTa  | Llama    |
| ------------------------------------------------ | ----------- | -------- | -------- |
| Human draft, caller's own, Preserve              | pilot       | 12 of 12 | 10 of 12 |
| Human draft, caller's own, Preserve              | second cell | 10 of 10 | 10 of 10 |
| Human draft, origin unstated, Recompose          | pilot       | 6 of 6   | 5 of 6   |
| Human draft, origin unstated, Recompose          | second cell | 10 of 10 | 10 of 10 |
| Model-written draft, stated generated, Recompose | pilot       | 6 of 6   | 0 of 6   |
| Model-written draft, stated generated, Recompose | second cell | 0 of 10  | 0 of 10  |

The RoBERTa count on the pilot mirrors is that model failing to detect
them as sources, not an effect of the skill. The three pilot outputs that
do not read as human on Llama are the Paine passage, whose clean original
already reads AI-assisted. So a person's draft reads as a person's after
either branch, and a model's draft reads as a model's after Recompose with
its surface constructions gone. The production checker has not been run on
this run's outputs; a blind packet of twenty is prepared.

The two tiers on the same jobs. Share is the mean model-token share, and
length is output tokens over source tokens.

| Cell                           | Llama mean, top / mid | Llama verdicts, top | mid        | Share, top / mid | Length, top / mid |
| ------------------------------ | --------------------- | ------------------- | ---------- | ---------------- | ----------------- |
| Pilot, human_defect, Preserve  | 0.130 / 0.133         | 5 / 1 / 0           | 5 / 1 / 0  | 0.000 / 0.000    | 83% / 82%         |
| Pilot, human, Preserve         | 0.145 / 0.145         | 5 / 1 / 0           | 5 / 1 / 0  | 0.000 / 0.001    | 100% / 100%       |
| Pilot, ai, Recompose           | 0.515 / 0.477         | 0 / 6 / 0           | 0 / 6 / 0  | 0.058 / 0.023    | 97% / 97%         |
| Pilot, human_defect, Recompose | 0.152 / 0.133         | 5 / 1 / 0           | 5 / 1 / 0  | 0.018 / 0.002    | 82% / 82%         |
| Second, human, Preserve        | 0.014 / 0.015         | 10 / 0 / 0          | 10 / 0 / 0 | 0.008 / 0.007    | 100% / 98%        |
| Second, generated, Recompose   | 0.921 / 0.964         | 0 / 4 / 6           | 0 / 3 / 7  | 0.253 / 0.116    | 94% / 89%         |
| Second, human, Recompose       | 0.032 / 0.024         | 10 / 0 / 0          | 10 / 0 / 0 | 0.147 / 0.072    | 98% / 98%         |

- **On drafts a person wrote, the tiers read the same.** Every such cell
  has the same verdict counts on both models, and the means sit within
  0.02 of each other.
- **On model-written text the mid tier rebuilt half as much and scored
  higher.** Its share was 0.116 against 0.253. Three of its ten outputs
  scored above their source on Llama, against none on the top tier. The
  regex screen counts 3.9 per thousand words against 2.7, including a
  `not just X but Y` and an `-ing` tail the top tier had removed. It also
  cut more: one draft went from 284 words to 182 by withholding claims the
  top tier had narrowed and kept.
- **Under Preserve the mid tier deleted what the top tier flagged.** It
  cut two photo captions from a news draft, a forum poster's opening
  remark, and the label "state-of-the-art". The top tier deleted no clause
  in the ten drafts and reported the captions in its notes. The mid-tier
  session also withheld two punctuation repairs because its own clause
  diff would have counted them as added clauses.
- **The mid tier does a fraction of the work.** Per document it wrote 1,400
  to 4,000 tokens, reasoning and output together, and took 11 to 31
  seconds. The top tier wrote 8,800 to 21,500 and took 82 to 210 seconds.
  Both report running every step.
- **Routing, loading, and the unattended rules held on both.** A tier
  difference shows in the edits, not in the process checks.

Limits: one session per cell, and one session ran six or ten documents in
a row, as in the baseline. The baseline sessions were told the regime and
this run's were not, so a difference from baseline may come from the
session prompt as well as from the skill text. Six to ten documents per
cell cannot separate a mean shift of 0.03 from noise. The regex screen is
a crude count of surface constructions, not the skill's catalog and not a
reader.

## Prompt block versus the skill

Six routine-communication drafts with 25 injected local defects (chatbot
wrappers, generated dashes, filler, `simply` and `please` in instructions,
`not just X, but Y`, an `-ing` significance tail, a label-restating list, an
unsupported `As a [role], I` opener, a described symbol with a visible name)
were given to two sessions on 2026-09-19: one with only the pasteable prompt
block as its system rules and no files, one with the skill's entry point
running the lighter pass it then had for short artifacts.

| Condition               | Defects repaired | Exact tokens preserved | Fidelity notes                                                 |
| ----------------------- | ---------------- | ---------------------- | -------------------------------------------------------------- |
| Prompt block            | 25/25            | all                    | one stance strengthened ("does not block" to "ready to merge") |
| Entry point, light pass | 25/25            | all                    | none                                                           |

The lighter pass is gone, so the second row is a baseline for the block and
not a measurement of today's skill. The full procedure has not been run on
this suite.

## Blind expert rating

One rater, an experienced writer and editor outside the project, completed
the reading-room packet in two sittings (2026-10-12 and 2026-10-19). Sides
were randomized and unlabeled; the page highlighted the words that differed
between the two sides of a pair and never said which side was the skill's
output. The rater ticked "I recognize the source" on no passage. One rater
is a reading, not a rate: every figure below is a count from one person.
Raw answers: `rater_answers.json` in the harness folder, scored by
`score_rater.py`.

### Pairwise preference

Seventeen pairs, each a pilot source beside the skill's output on it. The
sixth strong-draft pair was dropped because Preserve returned Twain
unchanged and the two sides were identical.

| Cell                         | n   | Would publish output | Output more deliberate | Same meaning | Strength of output picks | Strength of source picks |
| ---------------------------- | --- | -------------------- | ---------------------- | ------------ | ------------------------ | ------------------------ |
| Defect draft vs Preserve     | 6   | 6/6                  | 6/6                    | 6/6          | 6 strong                 | none                     |
| Strong draft vs Preserve     | 5   | 2/5                  | 2/5                    | 5/5          | 1 coin toss, 1 clear     | 2 slight, 1 clear        |
| Generated draft vs Recompose | 6   | 4/6                  | 4/6                    | 6/6          | 3 slight, 1 strong       | 1 slight, 1 clear        |

Findings:

- **Defect drafts.** The rater chose the Preserve output six times of six,
  each time strongly, and in every pair took the output for the original
  and the defect draft for the edited version. The injected opening and
  closing sentences read to them as an editor's additions: "amateurish and
  juvenile, reading more like a high school paper than the sophisticated
  prose that is the rest of the text." The defect family is one a skilled
  reader sees at once, and Preserve removes it without leaving a mark.
- **Strong drafts.** The rater preferred the unedited draft in three of
  five pairs and picked out the original in four of five. Two of the three
  source picks came with a note naming the model's own word: an inserted
  "organic" in Darwin ("entirely redundant"), and "eventually" substituted
  for "at length" in Thoreau ("simply does not fit the preceding diction
  and tone"). The two output picks were Paine, where the output split a
  long semicolon chain the rater read as a run-on, and Franklin, a coin
  toss. Over-editing on strong drafts is real and specific: a reader of
  this skill notices a period word replaced by a modern near synonym and
  counts it against the edit, and accepts a split at an existing clause
  boundary.
- **Generated drafts.** Recompose won four of six, three of them slightly.
  The two losses carried the most useful notes. On the Twain mirror the
  rater flagged two things Recompose had introduced: "one" repeated for
  two different referents in a paragraph, and a sandbar "on" a river where
  the draft had "along." On the Paine mirror, which Recompose won, they
  named what the win consisted of: "imagine doing without one" for
  "imagine a situation without one."
- **Meaning.** The rater marked all seventeen pairs as saying the same
  thing, and wrote in closing that "the principle, core meaning of the
  overall text was perfectly maintained throughout all edits."

### Single passages

Nine passages read alone: three unedited human sources, three Recompose
outputs on agent-written mirrors, and three Preserve outputs on strong
drafts (one of them the unchanged Twain). Authorship runs from 1, a person
wrote every word, to 7, a machine wrote or rewrote it.

| Class                       | n   | Publish as is | With light edits | No  | Mean deliberateness (1 to 7) | Mean authorship | Authorship scores |
| --------------------------- | --- | ------------- | ---------------- | --- | ---------------------------- | --------------- | ----------------- |
| Human source                | 3   | 0             | 2                | 1   | 4.67                         | 3.33            | 4, 3, 3           |
| Recompose on a mirror       | 3   | 1             | 2                | 0   | 4.33                         | 3.33            | 2, 3, 5           |
| Preserve on a strong source | 3   | 1             | 2                | 0   | 6.00                         | 2.33            | 2, 3, 2           |

The outputs sit at parity with the human controls, which is the protocol's
target, and the table also shows why the protocol reports false suspicion
beside it. The rater gave Darwin's own paragraph a 4 and would not publish
Paine's, finding in it "a slight excess of verbosity ... not too dissimilar
to the output of a model who has been prompted to provide lush text." The
one passage scored toward the machine end was the Recompose output on the
Thoreau mirror, where "the overall diction of the text feels uncohesive,"
moving between an elevated, antiquated style and a modern, casual one. The
rater also caught the Preserve edit on Franklin without seeing
the source, writing that "some of the wording has been altered to be
partially modernized." It had been: "sung withal" to "sang as well" and
"prudential" to "practical."

### The rater's own edit

The rater edited the defect-injected Douglass draft under the same request
the skill received. `clause_diff.py` scored both edits against the draft.

| Version              | Injected defects removed | Kept | Edited | Deleted | Added | Added-token share |
| -------------------- | ------------------------ | ---- | ------ | ------- | ----- | ----------------- |
| Rater edit           | 4 of 5                   | 17   | 0      | 4       | 0     | 0.000             |
| Skill, Preserve 0.15 | 5 of 5                   | 15   | 1      | 5       | 0     | 0.000             |

A skilled human editing for a general reader did what the Preserve policy
prescribes: cut the scaffolding, added no clause, and wrote no new words.
The rater left the empty adverb ("thus fundamentally ignorant") in place
and left a stray comma where the filler phrase had been. They also did
one thing the skill's output did not, joining two pairs of short sentences
with semicolons, and their closing advice names it: "sentences of varying
lengths tend to be more pleasing to the average reader." Their other
closing notes: the edits lose subtlety, because "two words can have very
similar meanings in a dictionary, but convey entirely different states of
mind," and an editor should "keep in mind the era of the text ... and
alter both your syntax and diction appropriately."

## Unattended runs

Forward test of 2026-11-09 on the single-procedure skill. Five independent
agent sessions each received the skill's location, a short session history,
and one caller message, and returned the reply they would send plus a trace
of the files they opened and the steps they ran. No session was told the
intended behavior. The reference counts below come from each session's
recorded tool calls, not from its own account.

| Case                                                | Caller's words about origin | Regime    | References loaded | Questions | Notes returned                                             |
| --------------------------------------------------- | --------------------------- | --------- | ----------------- | --------- | ---------------------------------------------------------- |
| PR description the agent drafted earlier in session | none                        | Recompose | 6 of 6            | 0         | three withheld claims, one open ambiguity                  |
| Release note from a one-line commit message         | none, and no draft          | Recompose | 6 of 6            | 0         | thin source, its open question, format choices             |
| Cover note to a hiring committee                    | "I wrote this ... myself"   | Preserve  | 2 of 2            | 0         | clause diff, authorship line, one residual, one suggestion |
| First-person status email, run 1                    | "my update email"           | Recompose | 6 of 6            | 0         | origin note, two source flags                              |
| The same email, run 2                               | "my update email"           | Recompose | 6 of 6            | 0         | origin note, two source flags, the dash default            |

Findings:

- **No session asked a question, and every session loaded exactly its
  branch's fixed set.** Zero failures in five on regime, loading, and the
  unattended check.
- **The possessive did not select Preserve.** Both email sessions cited the
  same sentence of the entry point as deciding the regime and returned the
  origin note word for word. The email is first-person with particulars a
  model could not have supplied, the case that drew a question under the
  earlier rule.
- **The session's own draft carried no origin note.** The PR description
  was recomposed without one, because the session showed the agent
  producing it.
- **A one-sentence artifact ran every step.** The release note went through
  the content lock (four items), the sufficiency test (thin), both
  skeptical-reader passes, and verification, and came back as one sentence
  with the gaps in the commit message named in the notes.
- **Preserve stayed light.** It made four changes to a 154-token note: two
  deleted scaffolding phrases and two grammar corrections. `clause_diff.py`
  counts 12 clauses, 9 kept, 3 edited, 0 added, and a model-token share of
  0.014. "Such as it is" and "rather proud of" stayed as the author's
  wording.
- **Recompose withheld what the evidence did not support.** The PR
  description lost three claims with no basis in the diff ("significantly
  improving reliability across the platform", "dramatically reduces failed
  invoice fetches", "improves performance for end users"), each reported in
  the notes, along with its `the real issue` framing and its chat sign-off.
- **The repeated case agreed on process and differed in wording.** The two
  email outputs have different subject lines, and one moves the
  recommendation to the first line. Both keep every name, number, and
  deadline. The skill aims at a repeatable process, not identical text.
- **Notes were the inconsistent part.** One session reported its format
  choices, one the dash default, and three reported neither. The entry
  point now names the two defaults that need a note and says an ordinary
  inference about format or house style needs none.
- **Cost.** A run took 96,000 to 145,000 tokens and 3 to 9 minutes. The
  one-sentence release note took 107,000 tokens and just over 3 minutes.
  That is the price of the same steps at every length.

Limits: five sessions on one model, with cases written for this test. The
matrix's file-target, findings-only, supplied-samples, text-alone, and
long-document cases were not run. The tested text predates four small edits
made in response: the two named defaults, a length cap on notes, the
Preserve wording about which residual defects go in the notes, and the rule
against overwriting a file that version control cannot restore.

### Re-test after consolidation, on two model tiers

Forward test of 2026-11-09 on the consolidated text: one gate, one home per
rule, and Recompose steps numbered R1 to R8. The session shape is the one
above. Each case ran on the model the earlier test used (top tier) and on a
smaller, faster model from the same family (mid tier), one session per
cell. The reference counts come from each session's recorded tool calls.

| Case                                         | Tier | Regime        | References loaded | Questions | Tokens  | Time       |
| -------------------------------------------- | ---- | ------------- | ----------------- | --------- | ------- | ---------- |
| PR description the agent drafted             | top  | Recompose     | 6 of 6            | 0         | 105,000 | 5 min 42 s |
| The same PR description                      | mid  | Recompose     | 6 of 6            | 0         | 71,000  | 36 s       |
| Cover note, "I wrote this ... myself"        | top  | Preserve      | 2 of 2            | 0         | 73,000  | 3 min 27 s |
| The same cover note                          | mid  | Preserve      | 2 of 2            | 0         | 55,000  | 52 s       |
| First-person status email, "my update email" | mid  | Recompose     | 6 of 6            | 0         | 75,000  | 62 s       |
| README section, edits forbidden              | top  | Findings only | 6 of 6            | 0         | 114,000 | 7 min 25 s |
| The same section, after the fixes below      | mid  | Findings only | 6 of 6            | 0         | 76,000  | 65 s       |

Findings:

- **Zero failures in seven on regime, loading, and the unattended check, on
  both tiers.** The email session returned the origin note word for word.
- **Both tiers made the same Preserve edits.** Two scaffolding phrases cut
  and two grammar corrections, reported as 11 clauses, 9 kept, 2 edited, 0
  added, at a model-token share of 0.014. The top-tier session also moved
  the closing sentence into its own paragraph.
- **Both tiers withheld the same unsupported claims from the PR
  description**, and both flagged the same ambiguity in the evidence: it
  says "retries up to 3 times" and also "gives up after 3 attempts".
- **The mid tier ran no scripts.** Every top-tier session computed its
  clause diff, word counts, and Unicode scan with a script. Every mid-tier
  session did them by reading. Its Preserve note reported 149 source tokens
  and 142 output tokens where the scripted count is 154 and 147; the share
  came out the same.
- **The mid tier's judgment slipped in two places.** Its findings-only
  review advised deleting a paragraph that holds an owned judgment about
  existing caches, hedged with "if the point is yours"; the top-tier review
  kept the judgment at full strength and repaired its framing. Its email
  changed "I think we book it" to "I think we should book it" and returned
  a three-sentence note.
- **The findings-only path had never run, and it was broken in four
  places.** The fixed origin note says the draft "was fully recomposed",
  which is false when nothing changed. The two-sentence cap on notes
  contradicted the four parts a finding carries. Nothing ranked the
  findings. Verification had no revision to compare. The top-tier session
  worked around each and reported it. The skill now gives a findings-only
  run no origin note, ranks findings by cost to the reader, applies the cap
  only to notes that accompany an artifact, and runs only the Unicode scan
  when there is a single text. The mid-tier session ran on the fixed text
  and followed all four.
- **The traces produced nine more edits.** The content lock fills from the
  whole source boundary, including task evidence the caller did not paste.
  Narrowing an unsupported claim is authorized, so verification does not
  count it as a weakened one. An open framing question is named as a
  default. PR descriptions and commit messages keep change framing. An
  artifact that carries markup is fenced. Marketing copy inside a technical
  destination gets the clear-communication profile. Moving a paragraph
  break is a Preserve operation. The Preserve notes name each edit in plain
  words, because the clause labels count clauses and reported "0 deleted"
  beside two visible cuts. Notes are written in the agent's ordinary voice.

Limits: one session per cell, short artifacts, cases written for the test,
and the tier differences graded by the maintainer's agent with no blind
rating. The top-tier sessions and the first three mid-tier sessions ran
before the edits listed above. The file-target, supplied-samples,
text-alone, and long-document cases remain unrun, as does any tier
comparison on a long or fidelity-critical document.

### Final text, every path

The edits above landed after most of the sessions that prompted them, so
the four cases ran once more, top tier, on a frozen copy of the text as
committed. The cases and the session shape are unchanged.

| Case                                         | Regime        | References loaded | Questions | Tokens  | Time       |
| -------------------------------------------- | ------------- | ----------------- | --------- | ------- | ---------- |
| PR description the agent drafted             | Recompose     | 6 of 6            | 0         | 104,000 | 5 min 21 s |
| Cover note, "I wrote this ... myself"        | Preserve      | 2 of 2            | 0         | 72,000  | 3 min 10 s |
| First-person status email, "my update email" | Recompose     | 6 of 6            | 0         | 132,000 | 9 min 53 s |
| README section, edits forbidden              | Findings only | 6 of 6            | 0         | 105,000 | 5 min 55 s |

Findings:

- **Zero failures in four on regime, loading, and the unattended check.**
- **The outputs match the earlier runs where the rules did not change.**
  Preserve made the same four edits to the cover note. The PR description
  lost the same unsupported claims and kept the same flag on the retry
  count. The email carried the origin note word for word and kept "I think
  we book", which the mid-tier session had changed.
- **The edits did what they were written for.** The PR description came
  back fenced, with three notes of at most two sentences. The Preserve
  notes named each edit in words. The findings-only review ranked five
  findings, carried no origin note, withheld the artifact, and listed the
  seven spans it had checked and kept.

The sessions also reported instructions they had to interpret. None was
changed, so that the text tested is the text shipped:

- The gate requires each named default to be stated in the notes, and a
  findings-only run on a draft of unstated origin carries no origin note.
- The origin note says the draft "was fully recomposed". Two sessions kept
  most sentences as already exact and found the note overstated the change.
- The two-sentence cap on a note strains against what a path must report:
  Preserve's diff line, edit line, residuals, and suggestions, or a PR
  description with eight unsupported claims.
- A plain-text artifact is returned unfenced, and nothing says how to mark
  where it ends and the notes begin.
- P3 does not define a clause when a parenthetical splits a subject from
  its verb, or whether a hyphenated compound is one token. Its similarity
  measure (shared in-order tokens over the longer clause) also differs
  from the one `clause_diff.py` computes (the mean of a sequence ratio and
  token-set overlap). Counts differed by one clause between readings; the
  added-token count and the zero-violation result did not.
- An email's subject line is either a protected title or an editable
  heading; the text supports both readings.
- R4 says to retain a sentence only when it is already exact, and also
  that no working passage changes merely for consistency. On prose that is
  already good the two give no line for how much to rebuild.
- Under Preserve, deleting a generic opener can strand a pronoun whose
  antecedent it held. The text does not say whether to keep the opener,
  supply the antecedent, or flag it.

## Acceptance criteria, pass or fail

| Criterion                                                               | Result at pilot scale                                                                                                                                                                                                                                                                                                                                                                  |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Preserve: zero added clauses, share under budget                        | Pass: 0 added clauses in 34 outputs after hand review of 2 flagged clauses, max share 0.039; after consolidation, 0 in 22 top-tier outputs after hand review of the same 2 flagged clauses, max share 0.034                                                                                                                                                                            |
| Preserve: at least 95% labeled human or AI-assisted                     | Pass at this scale: 10 of 10 Human on production (famous text), 10 of 10 human on both open models (ordinary text), 5 human and 1 assisted on Llama (famous text)                                                                                                                                                                                                                      |
| Preserve: zero humanizer-head positives                                 | Not measurable; the open models have no such head                                                                                                                                                                                                                                                                                                                                      |
| Preserve fidelity at or above Recompose                                 | Pass: 0 number losses, 0 added clauses, 2 flagged inferences, all in notes                                                                                                                                                                                                                                                                                                             |
| Recompose: output no more machine-written than its source               | Pass at this scale: unchanged on production (6 of 6) and RoBERTa (10 of 10); on Llama 9 of 10 scored lower and 3 of 10 moved from AI-generated to AI-assisted; none read as human; after consolidation the verdicts are the same, every Llama score on the second cell's generated text is at or below its source, and the pilot mirrors' Llama mean rose 0.048 with no verdict change |
| Human preference at least 60% on defect drafts                          | 6 of 6, one rater                                                                                                                                                                                                                                                                                                                                                                      |
| Human preference at most 45% on strong drafts                           | 2 of 5, one rater; both named objections were lexical substitutions                                                                                                                                                                                                                                                                                                                    |
| Skeptical-observer parity with human controls                           | Mean authorship 3.33 for human sources, 3.33 for Recompose outputs, 2.33 for Preserve outputs; one rater, three passages per class                                                                                                                                                                                                                                                     |
| Routing: Preserve only on a caller statement, origin note when unstated | 5 of 5 sessions under the current rule, 2 of them unstated; 0 wrong guesses in 18 under the earlier rule, which also asked 6 questions; 108 of 108 batch jobs after consolidation                                                                                                                                                                                                      |
| Unattended matrix: no question, right regime, notes present             | 5 of 5 sessions, then 11 of 11 after consolidation with findings-only added; four of the matrix's cases not run                                                                                                                                                                                                                                                                        |
| Fixed loading and every step at every length                            | 5 of 5 by tool-call trace, including a one-sentence artifact; 11 of 11 sessions and 14 of 14 batch sessions after consolidation                                                                                                                                                                                                                                                        |
| Prompt block matches the skill's local-defect repair                    | 25/25 for the block against 25/25 for the since-removed lighter pass; one stance drift in the block; not run against the full procedure                                                                                                                                                                                                                                                |

One instruction changed in response to the rating. The Preserve edit policy
now says a lexical replacement must repair a defect, and that the author's
diction, period idiom, and register are not defects. The outputs in the
table predate that sentence. The guardrail check after consolidation
re-measured it: 0 edited clauses on the six strong drafts, against 11.

## Manual production spot check

Performed 2026-09-19 by the maintainer on the vendor's free web checker,
twenty pilot outputs pasted by hand, blind to regime (the numbering key was
held by the session, not the checker). Verdicts and percentages are the
checker's own wording. Raw rows: `spot_check_results.jsonl` and
`spot_check_key.json` in the harness folder.

| Regime    | Source cell  | n   | Human | AI-assisted | AI-generated |
| --------- | ------------ | --- | ----- | ----------- | ------------ |
| Preserve  | human_defect | 6   | 6     | 0           | 0            |
| Preserve  | human        | 4   | 4     | 0           | 0            |
| Recompose | ai           | 6   | 0     | 0           | 6            |
| Recompose | human_defect | 4   | 3     | 1           | 0            |

Every Human verdict showed 100%. Five of the six AI-generated verdicts
showed 100%; the sixth (the Franklin mirror) showed 81% with the checker
noting a human-written portion at the opening. The one AI-assisted verdict
(Recompose on the Darwin draft) showed 18% and named a single rewritten
sentence as the assisted span.

Reading:

- **Recompose does not move the production verdict.** The six mirrors were
  written fresh by an agent session, went through the full recomposition
  with every reference loaded, and still read as AI-generated. This is the
  result the skill's scope statement predicts and is the one row of the
  table free of the caveat below.
- **Preserve output carries the label its workflow earns.** Ten of ten read
  as Human. The caveat: the sources are famous pre-1927 books, which are
  inside the window the detector trains its human class on, so a Human
  verdict on a lightly edited Thoreau passage may reflect recognition of
  the text as much as the regime's token budget. The open models have since
  scored Preserve output on ordinary unpublished writing (see
  [Trained-classifier column](#trained-classifier-column)); a production
  check on such drafts has not been done.
- **Recompose on a human draft mostly still reads Human.** Three of four did,
  and the fourth was labeled assisted with the exact regenerated sentence
  identified. Under the vendor's own scope rule (the model's added tokens stayed
  below the human's), that is the expected label, not an evasion; the drafts
  were human. It also shows what a statement of authorship protects: the checker
  found the one rewritten sentence, and the author's wording it did not find had
  been discarded.
