# Evaluation results

Pilot run of 2026-09-19 against the two-pass design. Every number here is
pilot scale: 6 documents per cell, far below the protocol's 100. The numbers
answer "does the design behave as specified" on a small labeled corpus. They
do not establish the population rates the acceptance criteria ask for. The
trained-classifier column, a second corpus cell, and one blind expert rating
were added on 2026-11-09.

## Contents

- [Setup and provenance](#setup-and-provenance)
- [What was not run](#what-was-not-run)
- [Routing](#routing)
- [Preserve regime](#preserve-regime)
- [Recompose regime and the misrouting cost](#recompose-regime-and-the-misrouting-cost)
- [Detector column](#detector-column)
- [Trained-classifier column](#trained-classifier-column)
- [Quick core versus full skill](#quick-core-versus-full-skill)
- [Blind expert rating](#blind-expert-rating)
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
- Trained classifier: the open EditLens RoBERTa model
  (`pangram/editlens_roberta-large`, revision `f93e1ace74`, CC BY-NC-SA 4.0),
  scored by `score_editlens.py` the way the reference inference script does
  (EditLens repository commit `05a588f1`): text lowercased and
  whitespace-normalized, one pass truncated at 512 tokens, and a score equal
  to the expected bucket over four buckets, scaled to 0 through 1. Thresholds
  live in `calibration.json`, chosen on the dataset's `val` split and checked
  on its `test` split.
- Clause diff: `clause_diff.py` with the document-level token count. Two
  splitter defects found during the run (a case-sensitive sentence boundary
  and "indeed" scored as a verb) were fixed before the final accounting.
- Raw rows: `outputs/*.jsonl`, `scores_binoculars_*.jsonl`, `diffs.jsonl`,
  and `pilot_summary.md` in the harness folder.

## What was not run

- The EditLens Llama model. Its adapter and the scoring path are in place,
  but the base model needs a separate approval from Meta that had not been
  granted on this account. Every trained-classifier number here comes from
  the RoBERTa model, the weaker of the two in the vendor's own tables.
- The humanizer-head metric. Neither open model has such a head.
- The blind human-preference and skeptical-observer suites at protocol
  scale. One expert rater completed a reduced packet; see
  [Blind expert rating](#blind-expert-rating).
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
  blind rating later put a reader's judgment on these edits; see
  [Blind expert rating](#blind-expert-rating).

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
and fiction). Three independent sessions ran the deep pass: Recompose on
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

## Acceptance criteria, pass or fail

| Criterion                                                            | Result at pilot scale                                                                                                                                                |
| -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Preserve: zero added clauses, share under budget                     | Pass: 0 added clauses in 34 outputs after hand review of 2 flagged clauses, max share 0.039                                                                          |
| Preserve: at least 95% labeled human or AI-assisted                  | Pass at this scale: 10 of 10 Human on production (famous text), 10 of 10 human on both open models (ordinary text), 5 human and 1 assisted on Llama (famous text)    |
| Preserve: zero humanizer-head positives                              | Not measurable; the open models have no such head                                                                                                                    |
| Preserve fidelity at or above Recompose                              | Pass: 0 number losses, 0 added clauses, 2 flagged inferences, all in notes                                                                                           |
| Recompose: verdict distribution unchanged on trained classifiers     | Mixed: unchanged on production (6 of 6) and RoBERTa (10 of 10); on Llama 3 of 10 moved from AI-generated to AI-assisted and 9 of 10 scored lower; none read as human |
| Human preference at least 60% on defect drafts                       | 6 of 6, one rater                                                                                                                                                    |
| Human preference at most 45% on strong drafts                        | 2 of 5, one rater; both named objections were lexical substitutions                                                                                                  |
| Skeptical-observer parity with human controls                        | Mean authorship 3.33 for human sources, 3.33 for Recompose outputs, 2.33 for Preserve outputs; one rater, three passages per class                                   |
| Routing accuracy at or above 90%, remainder resolved by the question | Pass: 0 wrong guesses in 18, 6 questions                                                                                                                             |
| Quick pass loads no references                                       | Pass                                                                                                                                                                 |
| Quick core matches full skill on routine communication               | Pass on defect repair (25/25 each); one stance drift in the core                                                                                                     |

One instruction changed in response to the rating. The Preserve edit policy
now says a lexical replacement must repair a defect, and that the author's
diction, period idiom, and register are not defects. The outputs measured
here predate that sentence, and it has not been re-measured.

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
- **Recompose on a human draft mostly still reads Human.** Three of four
  did, and the fourth was labeled assisted with the exact regenerated
  sentence identified. Under the vendor's own scope rule (the model's added
  tokens stayed below the human's), that is the expected label, not an
  evasion; the drafts were human. It also shows what the routing question
  protects: the checker found the one rewritten sentence, and the author's
  wording it did not find had been discarded.
