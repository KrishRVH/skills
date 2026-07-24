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
- session residue

Because the clean human original is available, evaluators can measure recovery
without requiring exact textual overlap.

## 4. Fidelity suite

Construct passages containing:

- similar names and dates
- percentages, ranges, currencies, and units
- qualified statistics
- negation and exceptions
- correlation without causation
- current versus proposed states
- owned opinions with calibrated force
- quotations, citations, and URLs
- legal or technical modality

Independently label every proposition and protected exact element.

## 5. Blind human evaluation

Use raters who do not know which system produced each output. Separate the
questions rather than asking for one vague quality score.

Rate on a seven-point scale:

- clarity
- specificity to the subject
- fit for the stated reader and genre
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

Detector scores may be recorded as a secondary robustness diagnostic, never as
the optimization target or release criterion.

## 8. Primary metrics

| Dimension             | Metric                                                           |
| --------------------- | ---------------------------------------------------------------- |
| Critical fidelity     | Count of unauthorized proposition changes; target: 0             |
| Exact integrity       | Protected-element error rate; target: 0                          |
| Fabricated humanity   | Invented experience, identity, source, or error count; target: 0 |
| Naturalness           | Blind human rating and pairwise preference                       |
| Reader fit            | Blind rating for stated audience and genre                       |
| Deliberateness        | Blind rating plus highlighted generic spans                      |
| Publication readiness | Pairwise preference against baseline and human edit              |
| Over-editing          | Unnecessary-change rate on strong human controls                 |
| Reliability           | Variance across genres, lengths, models, and repeated runs       |
| Efficiency            | Tokens, latency, and number of passes                            |

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
- genre mismatch
- verifier miss

Update the smallest relevant instruction or example. Do not expand a word
blacklist in response to isolated failures.
