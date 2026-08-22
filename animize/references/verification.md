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
artifact_boundary:
  include: []
  exclude: []
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
commitments: []
state_labels: []
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
- **hypothetical:** an authorized illustration that remains visibly hypothetical
- **added:** not supported
- **changed:** actor, scope, modality, polarity, chronology, causation,
  comparison, attribution, or evaluative force differs

Remove or repair every unauthorized `added` or `changed` claim.

### Paired source/revision finding

For a fidelity audit, report each material issue as a source and revision pair:

```text
Source: <exact span, claim ID, or [absent]>
Revision: <exact span or [missing]>
Finding: added | changed | missing | exact-element mismatch
Relationship: <actor, scope, modality, polarity, time, causation, attribution,
  evaluation, commitment, state, or exact element>
Consequence: <what the difference changes>
Repair: <smallest change that restores fidelity>
```

Use `[absent]` for an unsupported addition and `[missing]` for a deletion. Quote
only the shortest span needed to establish the difference. Do not report a
stylistic preference in this shape unless it changes a locked relationship or
protected exact element.

## 3. Addition and deletion ledger

Inspect both directions.

### Additions

Look for newly introduced:

- facts, examples, mechanisms, motives, or consequences
- causal language such as `because`, `therefore`, `led to`, or `resulted in`
- universals or broadened quantifiers
- stronger certainty or recommendation
- positive or negative evaluation
- a new first-person opinion, reaction, aside, or owned judgment, even when it
  resembles the supplied voice
- promises, guarantees, permissions, obligations, owners, deadlines, follow-up,
  or remediation
- a hypothetical, placeholder, proposal, or prior state presented as current fact
- a motive, preference, or biography inferred only from missing information
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
- commitments, prohibitions, permissions, or responsibility
- labels that distinguish current, proposed, prior, hypothetical, and unknown
  states
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
- protected spans containing unusual spacing, joiners, or look-alike characters

Do not normalize exact elements without authorization.

For deep stylistic diagnostics, mask each protected exact span with a stable
identifier and restore it exactly afterward. Masking keeps the diagnostic from
rewriting the span; it does not replace the source-versus-output exactness
check.

Scan Unicode candidates by provenance. Record whether zero-width characters,
`U+00AD` soft hyphens, `U+00A0` non-breaking spaces, or mixed-script homoglyphs
were source-supplied or introduced by the revision. Remove unsupported
introduced residue. Flag suspicious source residue with its location and code
point, and never silently normalize a protected span. Defend language-required
joiners, intentional typesetting spaces, and exact characters in names, code,
identifiers, or quotations.

Generated prose must contain no `U+2013` or `U+2014` outside a protected exact
span unless the caller explicitly authorizes the named character. A supplied
sample or house style is not authorization. Verify this as an output invariant,
not as evidence about authorship.

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
An authorized illustrative scenario must remain labeled as an example,
supposition, or placeholder; never recast it as an observed event.

### Commitments and obligations

Do not add or remove a promise, owner, deadline, guarantee, permission,
prohibition, follow-up, remediation step, or service level. In support,
incident, policy, recruiting, and operational prose, a polished future action
can create a real obligation even when it sounds routine.

### Absence and motive

Missing public or supplied information establishes only that the information is
missing. It does not establish privacy preferences, a low profile, motive,
upbringing, intent, or likely history.

### Artifact boundary

Check every source passage classified as an instruction, example, quotation,
code block, data block, or editorial comment. Its constraints may govern the
rewrite, but its text must not appear as artifact content unless explicitly
included.

## 6. Human-integrity check

The rewrite must contain zero invented:

- memories or anecdotes
- sensory observations or first-hand scenes
- emotions, preferences, or beliefs attributed to the caller
- relationships, credentials, employment history, or biography
- a first-person role claim, including `As [role], I`, when the role is not
  established by the source or authorized context
- quotations, testimonials, reviews, or sources
- mistakes, slang, dialect, or typographical errors added as camouflage
- preferences, motives, or personal history inferred from an absence of evidence

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
- brief instructions, sample text, and reasoning residue remain outside the
  artifact

Structural independence is not a license to reorder chronology, logic, or
procedural steps incorrectly.

## 8. Skeptical-reader red team

Mask protected exact spans before this pass. Read the remaining output while
assuming it may be AI-assisted. Mark every span that feels assembled rather
than decided. For each mark, name the observable reason:

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

For every candidate retained as a false positive, record the exact span, the
apparent pattern, its legitimate function, and the evidence for that function.
Do not count defended false positives as defects. In a fidelity audit, report a
defense only when exhaustive accounting is requested or the defense explains a
material decision.

## 9. Acceptance decision

Reject or revise the artifact when any of these remain:

- unsupported added claim
- changed actor, scope, modality, polarity, causation, chronology, attribution,
  or evaluation
- fabricated personal or source material
- invented commitment, obligation, permission, owner, deadline, or guarantee
- leaked brief material or a hypothetical presented as fact
- corrupted quotation, citation, URL, code, or exact value
- generated `U+2013` or `U+2014` outside a protected span without explicit
  caller authorization
- unsupported Unicode residue introduced by the revision
- central generic scaffolding that survives a requested recompose
- unresolved material claim that makes publication unsafe

Minor stylistic preferences are not blockers when the prose is clear,
genre-native, and deliberate.
