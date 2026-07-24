# Verification

Use this reference after the rewrite is complete. Generation and verification
are separate tasks. Do not accept a revision merely because it reads well.

## Contents

- [Content-lock schema](#1-content-lock-schema)
- [Claim mapping](#2-claim-mapping)
- [Addition and deletion ledger](#3-addition-and-deletion-ledger)
- [Exact-element checks](#4-exact-element-checks)
- [High-risk semantic checks](#5-high-risk-semantic-checks)
- [Human-integrity check](#6-human-integrity-check)
- [Structural verification](#7-structural-verification)
- [Skeptical-reader red team](#8-skeptical-reader-red-team)
- [Acceptance decision](#9-acceptance-decision)

## 1. Content-lock schema

The internal content lock should contain, where applicable:

```yaml
purpose: ""
reader: ""
genre: ""
main_point: ""
claims:
  - id: C1
    proposition: ""
    actor: ""
    support: supplied | authorized_source | inference | unsupported
    modality: may | likely | will | must | none
    scope: ""
    polarity: positive | negative
    attribution: ""
relationships:
  - type: cause | sequence | contrast | condition | comparison
    from: C1
    to: C2
protected:
  names: []
  numbers: []
  dates: []
  units: []
  terms: []
  quotations: []
  citations: []
  urls: []
owned_judgments: []
source_gaps: []
```

The representation may be informal, but it must capture the same distinctions.

## 2. Claim mapping

For every substantive output sentence, determine which content-lock item
supports it.

Classify the sentence as:

- **preserved:** same proposition in new wording
- **combined:** two or more supported propositions joined without a new
  relationship
- **inferred:** logically entailed and authorized
- **added:** not supported
- **changed:** actor, scope, modality, polarity, chronology, causation,
  comparison, attribution, or evaluative force differs

Remove or repair every unauthorized `added` or `changed` claim.

## 3. Addition and deletion ledger

Inspect both directions.

### Additions

Look for newly introduced:

- facts, examples, mechanisms, motives, or consequences
- causal language such as `because`, `therefore`, `led to`, or `resulted in`
- universals or broadened quantifiers
- stronger certainty or recommendation
- positive or negative evaluation
- first-person experience, emotion, or identity
- source attributions, quotations, or citations

### Deletions

Look for removed:

- exceptions, conditions, limitations, and uncertainty
- actors and responsibility
- negation
- chronology
- numbers, dates, units, and locations
- unfavorable facts or counterevidence
- owned evaluative force
- citation scope

A cleaner sentence is not acceptable if it loses a material distinction.

## 4. Exact-element checks

Compare source and output for:

- proper names and spelling
- dates and time zones
- numbers, percentages, ranges, currencies, and units
- versions, model names, identifiers, and defined terms
- quoted text and quote boundaries
- citation identifiers, locators, and link targets
- code, commands, formulas, file paths, and structured data

Do not normalize exact elements without authorization.

## 5. High-risk semantic checks

### Modality

Check changes among `can`, `may`, `might`, `should`, `will`, and `must`.

### Scope

Check `some`, `many`, `most`, `all`, `often`, `usually`, `always`, and `never`.

### Polarity

Check lost or added negation, exceptions, and double negatives.

### Causation

Do not turn sequence, association, or juxtaposition into cause.

### Attribution

Do not change who said, believed, measured, decided, or caused something.

### Evaluation

Do not strengthen or weaken praise, criticism, urgency, confidence, or
recommendation unless authorized.

### Time

Do not collapse past, current, proposed, expected, and hypothetical states.

## 6. Human-integrity check

The rewrite must contain zero invented:

- memories or anecdotes
- sensory observations or first-hand scenes
- emotions, preferences, or beliefs attributed to the caller
- relationships, credentials, employment history, or biography
- quotations, testimonials, reviews, or sources
- mistakes, slang, dialect, or typographical errors added as camouflage

If such material is necessary to the requested genre, flag the missing input or
omit it. Do not simulate it.

## 7. Structural verification

For `rewrite_depth: recompose`, check that the result is not merely a lexical
paraphrase:

- the information hierarchy reflects the reader's needs
- paragraph boundaries follow the new plan
- generic source scaffolding was not carried over by inertia
- sentence architecture was rebuilt where the source was mechanical
- preserved wording is retained because it is exact or protected, not because
  the agent failed to recompose

Structural independence is not a license to reorder chronology, logic, or
procedural steps incorrectly.

## 8. Skeptical-reader red team

Read the output while assuming it may be AI-assisted. Mark every span that feels
assembled rather than decided. For each mark, name the observable reason:

- generic or portable claim
- exposed template
- over-symmetry
- inflated importance
- vague authority
- repeated rhetorical device
- unnecessary recap or transition
- slogan ending
- borrowed intimacy
- polished abstraction without particulars

Repair only supported defects. A suspicion without an observable reader-facing
problem does not justify random change.

## 9. Acceptance decision

Reject or revise the artifact when any of these remain:

- unsupported added claim
- changed actor, scope, modality, polarity, causation, chronology, attribution,
  or evaluation
- fabricated personal or source material
- corrupted quotation, citation, URL, code, or exact value
- central generic scaffolding that survives a requested recompose
- unresolved material claim that makes publication unsafe

Minor stylistic preferences are not blockers when the prose is clear,
genre-native, and deliberate.
