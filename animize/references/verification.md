# Verification

Generation and verification are separate tasks. Do not accept a revision
merely because it reads well. The content-lock schema is filled before
drafting, at the procedure's lock step. Every later section runs on the
finished text: against the content lock under Recompose, and against the
caller's draft under Preserve.

## Contents

- [Content-lock schema](#1-content-lock-schema)
- [Claim mapping](#2-claim-mapping)
- [Addition and deletion ledger](#3-addition-and-deletion-ledger)
- [Exact-element checks](#4-exact-element-checks)
- [High-risk semantic checks](#5-high-risk-semantic-checks)
- [Human-integrity check](#6-human-integrity-check)
- [Structural verification](#7-structural-verification)

## 1. Content-lock schema

The content lock records, where applicable:

```yaml
purpose: ""
reader: ""
genre: ""
main_point: ""
required_content: [] # examples, actions, or sections the brief requires
artifact_boundary:
  include: []
  exclude: []
claims:
  - id: C1
    proposition: ""
    actor: ""
    support: supplied | authorized_source | inference | unsupported
    modality: may | likely | will | must | none
    scope: "" # quantifiers, exceptions, and conditions
    polarity: positive | negative
    attribution: ""
relationships:
  - type: cause | sequence | contrast | condition | comparison
    from: C1
    to: C2
protected:
  names: []
  places: []
  numbers: []
  dates: []
  units: []
  terms: []
  quotations: []
  citations: []
  urls: []
  code: []
owned_judgments: [] # each with its strength
commitments: [] # promises, obligations, permissions, prohibitions, guarantees, owners
state_labels: [] # current, prior, proposed, hypothetical, or unknown
source_gaps: [] # unsupported or ambiguous source claims
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

For a findings-only fidelity review, report each material issue as a source
and revision pair:

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

Scan Unicode candidates by provenance. Record whether zero-width characters,
`U+00AD` soft hyphens, `U+00A0` non-breaking spaces, or mixed-script homoglyphs
were source-supplied or introduced by the revision. Remove unsupported
introduced residue. Flag suspicious source residue with its location and code
point, and never silently normalize a protected span. Defend language-required
joiners, intentional typesetting spaces, and exact characters in names, code,
identifiers, or quotations. A defense names the character's function and its
source support.

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

This section applies under Recompose; Preserve verifies structure with its
clause diff. Check that the result is not merely a lexical paraphrase:

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
