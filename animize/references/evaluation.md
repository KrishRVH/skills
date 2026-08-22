# Evaluation protocol

No evaluation can prove that a text was written by a person. The useful
question is whether the skill produces prose that is as natural, deliberate,
reader-specific, and publication-ready as a matched human edit while preserving
substance.

## Contents

- [Systems to compare](#1-systems-to-compare)
- [Test corpus](#2-test-corpus)
- [Controlled defect suite](#3-controlled-defect-suite)
- [Fidelity suite](#4-fidelity-suite)
- [Blind human evaluation](#5-blind-human-evaluation)
- [Skeptical-observer test](#6-skeptical-observer-test)
- [Automated checks](#7-automated-checks)
- [Primary metrics](#8-primary-metrics)
- [Acceptance criteria](#9-acceptance-criteria)
- [Failure analysis](#10-failure-analysis)

## 1. Systems to compare

Evaluate at least:

1. Original draft
2. Generic prompt: `Make this sound more human`
3. Line-edit-only version of the skill
4. Recomposition core without references
5. Full skill with authoredness and skeptical-reader passes
6. Full skill plus an independent verifier
7. Professional human edit

Use identical source boundaries and caller briefs.

### Control matrix

Exercise every applicable combination of:

- `job: auto | write | rewrite | audit`
- `process: auto | quick | deep`, with `audit` explicitly ignoring `process`
- `clarity: auto | plain | off`

Test `auto` values against requests whose correct resolution is unambiguous,
then test each explicit value against the same material. For deep write and
rewrite cases, also cross `light`/`preserve`, `standard`/`rebuild`,
`recompose`/`rebuild`, and `match_samples`. Record invalid or inapplicable
combinations instead of silently treating them as another setting.

Instrument file reads. A `process: quick` run must load no file under
`animize/references/`; all required quick behavior must come from the entry
point. Measure its output quality and fidelity separately so a cheap run cannot
pass merely because it skipped work.

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

Test the dash invariant with four separate controls:

1. Preserve `U+2013` and `U+2014` inside protected exact spans.
2. Rebuild unprotected source sentences that contain either character without a
   mechanical punctuation swap.
3. Reject samples, house style, and destination typography as implicit
   authorization.
4. Permit generation only when the caller explicitly authorizes the named code
   point.

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
For fidelity-audit cases, require each material result to pair the source and
revision spans, classify the changed relationship, state the consequence, and
give the smallest repair.

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

For `preserve` and `match_samples`, give raters the source samples separately.
Require the system to identify three to five observable voice signals before
rewriting, then ask raters whether the revision remains recognizable as the same
writer without relying on topic vocabulary, copied catchphrases, or invented
biography. Score signal accuracy and recognition separately.

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
- generated `U+2013` or `U+2014` outside protected spans without explicit
  caller authorization
- exact restoration of protected spans that contain either dash character
- introduced zero-width characters, `U+00AD`, `U+00A0`, and mixed-script
  confusables, with source provenance recorded for retained candidates
- paired source/revision fidelity-finding fields
- file-read traces proving `process: quick` loaded no Animize reference

Detector scores may be recorded as a secondary robustness diagnostic, never as
the optimization target or release criterion.

## 8. Primary metrics

| Dimension              | Metric                                                           |
| ---------------------- | ---------------------------------------------------------------- |
| Critical fidelity      | Count of unauthorized proposition changes; target: 0             |
| Exact integrity        | Protected-element error rate; target: 0                          |
| Fabricated humanity    | Invented experience, identity, source, or error count; target: 0 |
| Naturalness            | Blind human rating and pairwise preference                       |
| Reader fit             | Blind rating for stated audience and genre                       |
| Deliberateness         | Blind rating plus highlighted generic spans                      |
| Publication readiness  | Pairwise preference against baseline and human edit              |
| Over-editing           | Unnecessary-change rate on strong human controls                 |
| Control conformance    | Correct `job`, `process`, `clarity`, depth, and voice behavior   |
| Voice recognition      | Signal accuracy and blinded same-writer recognition              |
| False-positive defense | Correct retains with an evidence-backed functional reason        |
| Destination fit        | Correct medium, formatting, stance, and explanation behavior     |
| Quick isolation        | Reference loads during `process: quick`; target: 0               |
| Reliability            | Variance across genres, lengths, models, and repeated runs       |
| Efficiency             | Tokens, latency, and number of passes                            |

## 9. Acceptance criteria

A production candidate should meet all of these:

- zero critical fidelity failures in the adjudicated test set
- zero fabricated personal or source material
- no regression against the baseline on reader fit or clarity
- statistically non-inferior naturalness and publication readiness relative to
  the professional human-edit condition within a predeclared margin
- materially fewer highlighted generic spans than both the original draft and
  generic-prompt baseline
- low unnecessary-change rate on already strong human prose
- zero material control, depth, or voice conformance failures on the matrix
- zero unauthorized generated `U+2013` or `U+2014` characters
- exact preservation of protected dash and Unicode spans
- zero Animize reference loads during `process: quick`
- defended false positives remain intact, including real prohibitions,
  supported recommendations, and coherent long sentences
- material distant duplication is removed without damaging legitimate
  repetition
- destination and writer-recognition cases meet their predeclared thresholds
- stable performance across repeated runs and major genres

Do not declare the skill perfected from a single model, genre, evaluator group,
or detector.

## 10. Failure analysis

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
- control-routing or quick-reference-load failure
- undefended false positive
- genre mismatch
- verifier miss

Update the smallest relevant instruction or example. Do not expand a word
blacklist in response to isolated failures.
