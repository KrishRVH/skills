# Evaluation protocol

The skill's main input is model-written text: messages, emails, pull request
descriptions, write-ups, and articles. Its target is output that reads as
human-authored, that Pangram's live detector reads as human-written, that
carries no LLM-isms, and that preserves the source's substance. The live
verdict is the benchmark the skill is developed against. Reader ratings, the
defect suite, and the fidelity suite measure the rest.

Measured results live in [evaluation-results.md](evaluation-results.md).

## Contents

- [Systems to compare](#1-systems-to-compare)
- [Test corpus](#2-test-corpus)
- [Controlled defect suite](#3-controlled-defect-suite)
- [Fidelity suite](#4-fidelity-suite)
- [Blind human evaluation](#5-blind-human-evaluation)
- [Skeptical-observer test](#6-skeptical-observer-test)
- [Automated checks](#7-automated-checks)
- [Detector columns](#8-detector-columns)
- [Primary metrics](#9-primary-metrics)
- [Acceptance criteria](#10-acceptance-criteria)
- [What not to do](#11-what-not-to-do)
- [Local detector setup](#12-local-detector-setup)
- [Failure analysis](#13-failure-analysis)

## 1. Systems to compare

Evaluate at least:

1. Original draft
2. Generic prompt: `Make this sound more human`
3. Line-edit-only version of the skill
4. The prompt block alone ([examples/prompt-block.md](../examples/prompt-block.md))
5. Recompose core without references
6. Full skill with authoredness and skeptical-reader passes
7. Full skill plus an independent verifier
8. Professional human edit

Use identical source boundaries and caller briefs.
Include ordinary agent replies without an explicit Animize invocation. They
should remain outside the skill. For invoked cases, evaluate only the writing
the caller selected.

### Unattended-run matrix

Run each case as a bare request: the artifact, an instruction to run the
skill on it, and nothing else unless the case names it.

- origin: the caller says the draft is their own writing; the caller asks to
  keep its wording; the session shows a model producing the draft; a brief
  with no draft; origin unstated, including first-person drafts holding
  particulars a model could not have supplied
- a possessive with no statement of authorship, such as `my PR description`
- genre: one artifact the clear-communication profile applies to and one it
  leaves alone
- writing samples supplied
- a request for the text alone, and a request for a change summary
- a findings-only request
- material that leaves a framing question open
- length: a three-sentence message and a multi-page document

For every run record the regime, the files loaded, the steps run, every
question put to the caller, and the notes. Each of these is a failure:

- a question put to the caller
- Preserve assigned without a caller statement
- an unstated-origin run with no origin note
- a named default (an unstated origin or an open framing question) taken
  and left out of the notes
- loaded files that differ from the branch's fixed set in the entry point
- a step skipped because the artifact is short

Measure output quality and fidelity on the short cases separately, so a run
cannot pass merely because it skipped work.

## 2. Test corpus

Include multiple domains and lengths:

- professional email and memo
- technical explanation and incident report
- product or marketing copy
- analytical essay or newsletter
- academic or scientific passage
- policy or legal-adjacent prose
- personal prose with supplied authentic details

Include four source classes:

- raw model-generated prose
- AI-assisted prose with substantial human revision
- genuine human prose with injected generic defects
- genuine human prose that is already strong and should change little

The last class measures over-editing.

Add these cells for the regime work:

- human drafts with known reader-facing defects, run under the Preserve
  regime at budgets 0.05, 0.15, and 0.30 (vary the constant for the
  experiment only)
- the same drafts run under the Recompose regime, to measure what the
  unstated-origin default costs a human draft whose author does not say they
  wrote it
- matched pairs produced by synthetic mirroring of a human document (ask a
  model for the topic, then for an article on that topic at the same length
  and register), so the skill's treatment of a mirror can be compared with its
  treatment of the original
- academic and second-language human samples with no edits, to measure
  whether the clear-communication profile moves human text toward registers
  that detectors have flagged in human writing

Use at least 100 documents per cell and at least 200 words each. Detectors
need 50 words; longer documents give more precise estimates.

## 3. Controlled defect suite

Inject known defects into selected human passages:

- generic opening and conclusion
- importance inflation
- vague attribution
- unsupported causal interpretation
- transition clustering
- announce-explain-recap repetition
- identical paragraph shapes
- rhetorical contrast loops
- synonym cycling
- false agency and unsupported verdict fragments
- orphaned objections and discarded alternatives
- coined analytical labels and portable aphorisms
- interchangeable body paragraphs
- distant semantic duplication across nonadjacent sections
- editorial instructions mixed into artifact source material
- unsupported `As [role], I` identity framing
- zero-width, soft-hyphen, non-breaking-space, and mixed-script residue
- session residue

Because the clean human original is available, evaluators can measure recovery
without requiring exact textual overlap.

Pair defect cases with defended false-positive controls containing a useful
passive, exact technical term, deliberate triad, quoted watched phrase, code
identifier, literal system agency, named rebuttal, plausible design alternative,
modular FAQ block, historical rationale that affects present use, a real
negative prohibition, a source-supported how-to recommendation, and a sentence
longer than 30 words that carries one coherent relationship bundle. Require the
system to name the function that defends each retained candidate.

Test the tier 8 dash default with four separate controls:

1. Preserve `U+2013` and `U+2014` inside protected exact spans.
2. Rebuild unprotected source sentences that contain either character without a
   mechanical punctuation swap.
3. Honor a caller request, a controlling style guide, or a consistent sample
   habit as a stronger tier.
4. Apply the default when no stronger tier decides.

Raters and automated checks must not use the presence or absence of either
character as authorship evidence.

Test legitimate repetition against distant duplication: a point-of-action
safety warning, procedural reminder, defined term, deliberate refrain, requested
summary, modular reference section, and repeated fact supporting a new inference
should remain. A distant paraphrase that adds nothing should not.

## 4. Fidelity suite

Construct passages containing:

- similar names and dates
- percentages, ranges, currencies, and units
- qualified statistics
- negation and exceptions
- correlation without causation
- current versus proposed states
- actual versus hypothetical examples
- owned opinions with calibrated force
- promises, owners, deadlines, guarantees, permissions, and obligations
- missing information paired with an unsupported inference about motive or
  biography
- quotations, citations, and URLs
- legal or technical modality
- source-supplied versus revision-introduced Unicode candidates

Independently label every proposition and protected exact element.
For findings-only fidelity cases, require each material result to pair the
source and revision spans, classify the changed relationship, state the
consequence, and give the smallest repair.

Create destination pairs that hold content constant while changing the medium:
plain-text email, rendered Markdown, reference documentation, a tutorial,
policy text, and an article. Verify formatting, stance, recommendations,
technical terminology, negative prohibitions, and explanation depth against the
destination rather than one house style.

## 5. Blind human evaluation

Use raters who do not know which system produced each output. Separate the
questions rather than asking for one vague quality score.

Rate on a seven-point scale:

- clarity
- specificity to the subject
- fit for the stated reader and genre
- fit for the stated destination
- coherence of information order
- naturalness of sentence and paragraph movement
- strength and calibration of stance
- publication readiness

Ask pairwise questions as well:

- Which version would you publish?
- Which version feels more deliberately written?
- Which version preserves the source meaning more accurately?

Require raters to highlight any span that feels generic, assembled, inflated,
or unnatural and to name the reason. This produces actionable diagnostics.

For Preserve cells and sample-led cells, give raters the source samples
separately.
Require the system to identify three to five observable voice signals before
rewriting, then ask raters whether the revision remains recognizable as the same
writer without relying on topic vocabulary, copied catchphrases, or invented
biography. Score signal accuracy and recognition separately.

For Preserve cells, also ask raters to choose between the unedited human draft
and the Preserve output. This is the over-edit guard: on strong drafts the
output should not win by much, and on defect-injected drafts it should.

## 6. Skeptical-observer test

Mix outputs with matched, genuinely human-written controls. Tell raters that
some samples may be AI-assisted and ask for:

- perceived degree of human authorship on a seven-point scale
- confidence
- specific textual evidence for the judgment

Interpret this only as a perception measure. The target is parity with matched
human controls, not zero suspicion; skeptical observers can falsely question
actual human prose.

Report false suspicion on human controls alongside suspicion on rewritten
outputs. A system should not be rewarded for exploiting a rater's unreliable
heuristic.

## 7. Automated checks

Use automation for hard invariants, not for final naturalness judgments:

- exact names, numbers, dates, units, URLs, citations, and quotations
- negation and modal changes
- added causal markers
- proposition entailment review by an independent model or rule-assisted
  verifier
- unsupported first-person or biographical additions
- unresolved placeholders and session residue
- brief-to-artifact leakage and hypothetical-to-actual drift
- added promises, ownership, deadlines, permissions, or guarantees
- a dash character outside the tier 8 default without a stronger tier
  deciding it
- exact restoration of protected spans that contain either dash character
- introduced zero-width characters, `U+00AD`, `U+00A0`, and mixed-script
  confusables, with source provenance recorded for retained candidates
- paired source/revision fidelity-finding fields
- file-read traces showing each run loaded exactly its branch's fixed set
- any question put to the caller during a run
- the Preserve clause diff: added clauses, model-token share, and the
  budget check, computed by the steps in
  [the procedure](procedure.md#p3-clause-diff)
- any sentence in an output that describes the output's standing with a
  detector

## 8. Detector columns

Pangram's live verdict is the benchmark. Report it per cell as counts of
Human Written, AI Assisted, and AI Generated outputs, with each output's
highest humanizer score and its source's verdict beside it. First show that
the detector separates the corpus's own source classes; an unchanged verdict
on an output means nothing when the source was never detected.

The verdict and a reader's rating are separate measurements, and a high
rating does not predict a human verdict: on the pilot, the live model read as
AI-generated six Recompose outputs that a blind expert rated level with human
originals. Report both.

- Score every cell before and after a rule change, on the same documents.
- A change that moves a verdict toward human-written counts in its favor. A
  change that moves one toward machine-written is a regression; find the
  passages responsible.
- The live model bills by the word. Send the same few documents before and
  after a change, three at a time, and widen the sample only when a verdict
  moves.
- Score with the open models first, to rule a candidate out. They are more
  lenient than the live model, so a human reading from them is a reason to
  spend on a live check, never a result.
- A verdict gain never excuses a fidelity failure or fabricated material.
  [Section 10](#10-acceptance-criteria) requires all of them at once.

Record these columns:

- **The live model.** The harness's `score_pangram.py` sends documents to
  Pangram's text API and stores the verdict, the class fractions, and each
  passage's label and humanizer score, without the text. Record the model
  version the API reports.
- **The open classifiers of the same family.** The Open Pangram release (two
  EditLens models: a LoRA adapter on `meta-llama/Llama-3.2-3B` and a
  `roberta-large` classifier, CC BY-NC-SA 4.0, noncommercial only) runs on one
  24 GB consumer GPU. Both are Pangram 3 lineage, trained on human, AI-edited,
  and AI-generated versions of news, educational web text, reviews, and fiction
  written to prompts, with no humanizer head, no tokenwise decoding, and
  narrower domain coverage than the live model. Both read a quarter to a
  third of the AI-edited documents in their own test split as human. Use them
  as the free pre-check and for AI-fraction estimates on Preserve output.
  Report their verdicts as EditLens verdicts, never as live verdicts.
- **A perplexity-family detector** (Binoculars, open source) to compare how
  a perplexity score and a trained classifier respond to the same edit.
- **An optional second trained classifier** from another lineage. Never a
  verdict source.

Record detector names, revisions, calibration files, and dates. Results are
comparable only within a version.

## 9. Primary metrics

| Dimension              | Metric                                                            |
| ---------------------- | ----------------------------------------------------------------- |
| Critical fidelity      | Count of unauthorized proposition changes; target: 0              |
| Exact integrity        | Protected-element error rate; target: 0                           |
| Fabricated humanity    | Invented experience, identity, source, or error count; target: 0  |
| Naturalness            | Blind human rating and pairwise preference                        |
| Reader fit             | Blind rating for stated audience and genre                        |
| Deliberateness         | Blind rating plus highlighted generic spans                       |
| Publication readiness  | Pairwise preference against baseline and human edit               |
| Over-editing           | Unnecessary-change rate on strong human controls                  |
| Unattended conformance | Questions put to the caller (target: 0); defaults stated in notes |
| Routing accuracy       | Preserve only on a caller statement; origin note when unstated    |
| Unstated-origin cost   | Model-token share and reader preference on recomposed human text  |
| Voice recognition      | Signal accuracy and blinded same-writer recognition               |
| False-positive defense | Correct retains with an evidence-backed functional reason         |
| Destination fit        | Correct medium, formatting, stance, and explanation behavior      |
| Fixed loading          | Runs whose loaded files differ from the branch's set; target: 0   |
| Verdict distribution   | Human / AI-assisted / AI-generated / humanized per cell           |
| Humanizer positives    | Rate above baseline on any cell; target: 0                        |
| Live verdict           | Outputs the live model reads Human Written, per cell; target: all |
| Verdict shift          | Score and verdict change per cell after a rule change             |
| Preserve accounting    | Added clauses (target: 0) and model-token share under budget      |
| Reliability            | Variance across genres, lengths, models, and repeated runs        |
| Efficiency             | Tokens and latency per run                                        |

Report the over-edit rate on strong human prose beside the verdict shift on
the same cell. The two failure modes trade off, and a run that wins one by
losing the other has not improved.

## 10. Acceptance criteria

A production candidate should meet all of these:

- zero critical fidelity failures in the adjudicated test set
- zero fabricated personal or source material
- no regression against the baseline on reader fit or clarity
- statistically non-inferior naturalness and publication readiness relative to
  the professional human-edit condition within a predeclared margin
- materially fewer highlighted generic spans than both the original draft and
  generic-prompt baseline
- low unnecessary-change rate on already strong human prose
- zero failures on the unattended-run matrix: no question to the caller, no
  wrong regime, no missing note
- the tier 8 dash default applied unless a stronger tier decided
- exact preservation of protected dash and Unicode spans
- every run loads exactly its branch's fixed set and runs every step, at
  every artifact length
- defended false positives remain intact, including real prohibitions,
  supported recommendations, and coherent long sentences
- material distant duplication is removed without damaging legitimate
  repetition
- destination and writer-recognition cases meet their predeclared thresholds
- stable performance across repeated runs and major genres
- model-written input: the live model reads the output as Human Written
- no rule change moves a cell's live verdict toward machine-written
- Preserve regime at the default budget: at least 95% of outputs labeled
  human or AI-assisted, zero humanizer-head positives where a head exists,
  and a fidelity pass rate at or above Recompose's
- human preference for Preserve output over the unedited draft at or above
  60% on defect-injected drafts and no higher than 45% on strong drafts
- routing on the labeled corpus: Preserve assigned only on a caller
  statement, and the origin note present on every unstated-origin run
- the prompt block alone matches the full skill's local-defect repair rate on
  the controlled defect suite for short written artifacts

Do not declare the skill perfected from a single model, genre, evaluator group,
or detector.

## 11. What not to do

- Do not submit user or customer text to any detector service.
- Do not train, fine-tune, or run reinforcement learning against a detector
  inside this repository. Model-stack notes belong in
  [backends.md](backends.md) only.

## 12. Local detector setup

The scoring harness lives in the repository's `.eval/animize/` folder, outside
the skill package. Its README gives the setup: a Python environment with CUDA
torch, a Hugging Face login with the Open Pangram and Llama terms accepted,
label inspection before any scoring, a check that local scores reproduce the
vendor's published scores, a five-document smoke test, threshold calibration
on one labeled split at 1% and 0.5% false positive rates with a check on a
second split, and the run order for corpus build, scoring, clause diff, and
report. Every result
table cites the calibration file it used.

Keep model caches and the working tree on the Linux filesystem when running
under a Windows subsystem; cross-filesystem reads dominate scoring time.

## 13. Failure analysis

For every failed item, classify the root cause:

- content-lock failure
- source-sufficiency failure
- structural carryover
- generic house-style convergence
- unsupported specificity
- stance distortion
- cadence overcorrection
- protected-span or Unicode-provenance failure
- distant-duplication miss or legitimate-repetition damage
- unsupported persona or voice-recognition failure
- destination mismatch
- regime-routing, fixed-loading, or unattended-run failure (a question, a
  skipped step, or a missing note)
- Preserve edit-policy violation (added clause or budget overrun)
- undefended false positive
- genre mismatch
- verifier miss

Update the smallest relevant instruction or example. Do not expand a word
blacklist in response to isolated failures.
