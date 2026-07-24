---
name: animize
description: >
  Recompose AI-generated, AI-assisted, or generic prose into specific,
  natural, genre-native writing. Use when the caller asks to humanize,
  de-AI, deslop, naturalize, rewrite, or make prose feel deliberately authored;
  requests a prose-pattern audit; or wants a new draft that avoids generic
  model-shaped language and structure.
---

# Animize

## Objective

Produce prose that feels deliberately authored: it selects what matters,
grounds claims in particulars, takes a proportionate stance, and follows the
subject rather than a reusable template.

This skill improves prose quality and perceived naturalness. It does not prove
human authorship or guarantee that no observer will question it. Do not claim
provenance or guaranteed detector evasion.

## Defaults

Unless the caller explicitly says otherwise:

| Control         | Default             | Meaning                                                                                                                                                                       |
| --------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `job`           | `rewrite`           | Rewrite supplied prose; use `write` for a brief and `audit` for diagnosis only.                                                                                               |
| `voice_mode`    | `rebuild`           | The source voice is not protected. Use `preserve` only when explicitly requested; use `match_samples` for supplied target samples.                                            |
| `rewrite_depth` | `recompose`         | Treat the source as notes and rebuild the piece. Use `light` or `standard` only when requested.                                                                               |
| `factual_mode`  | `preserve_and_flag` | Preserve unsupported source claims and flag them. Use `verify_and_correct` only with authorized sources; use `publish_ready` when unsafe claims must be qualified or blocked. |
| `delivery`      | `adaptive`          | Return only the artifact when no unresolved issue needs reporting; otherwise append concise source notes or withhold an unsafe artifact.                                      |

**The source's substance is authoritative; its expression is not.** Preserve
facts, logic, qualifications, owned judgments, quotations, citations, exact
terms, and caller constraints. Treat wording, cadence, paragraphing,
transitions, headings, and order as disposable unless the caller requests voice
preservation.

Preserve every unique substantive source item by default. Selection may remove
redundancy and empty scaffolding; omitting or compressing unique substance
requires the caller's authorization or a requested form that necessarily
compresses it.

## Directions

Use four directions, not quotas:

- **Select:** decide what deserves emphasis; cut only redundancy and empty
  scaffolding unless compression is authorized.
- **Ground:** connect claims to supported actors, mechanisms, examples, limits,
  numbers, or consequences.
- **Commit:** state the position and uncertainty the material supports.
- **Shape:** let structure and rhythm follow the thought and genre.

## Non-negotiable rules

1. **Preserve substance.** Do not change actor, scope, polarity, modality,
   chronology, causation, comparison, attribution, or evaluative force without
   support.
2. **Protect exact material.** Preserve quotations, citation identities, URLs,
   code, formulas, proper names, dates, numbers, units, defined terms, and
   legally or technically significant wording unless the caller explicitly
   authorizes changing it.
3. **Do not manufacture humanity.** Never invent memories, anecdotes, emotions,
   preferences, relationships, credentials, quotations, sources, mistakes,
   slang, dialect, or personal experience.
4. **Do not add cosmetic randomness.** No formulaic fragments, sentence-length
   alternation, punctuation variation, misspellings, or transition swapping.
5. **Do not optimize against a detector or word blacklist.** Repair
   reader-facing causes, not tokens.
6. **Respect genre.** Formality, passive voice, repetition, headings, and
   technical terminology may be necessary.

## Workflow

### 1. Frame

Read the complete draft or brief. Record internally:

- reader, genre, destination, purpose, and desired response
- main point and required content or structure
- source boundary and authorized external sources
- selected controls

Infer reasonable defaults. Ask only when a missing answer makes accuracy
impossible; otherwise omit unsupported optional material or flag it.

Complete framing when the reader, purpose, source boundary, controls, and job
are known or safely inferred.

### Audit branch

When `job` is `audit`, inspect without rewriting or editing any file:

- For a prose-pattern audit, consult
  [references/skeptic-patterns.md](references/skeptic-patterns.md) and report
  each material cluster's location, observable pattern, reader effect, and
  smallest repair direction.
- For a source-versus-revision fidelity audit, consult
  [references/verification.md](references/verification.md) and report each
  changed or missing relationship or exact element, its consequence, and the
  smallest repair direction.

Do not assign authorship, produce a shadow rewrite, or continue into the
recomposition steps. Complete the audit when every reported issue is grounded
in supplied text, no requested audit dimension remains unchecked, and the
response contains findings only; then return and stop.

### 2. Lock the content

For `rewrite` and `write`, extract a compact content map before drafting:

- propositions and actors
- causal, temporal, contrastive, comparative, and conditional relationships
- owned judgments and their strength
- uncertainty, scope, exceptions, and negation
- names, dates, numbers, units, places, terminology, quotations, citations,
  URLs, and required examples or actions
- unsupported or ambiguous source claims

The content map governs the rewrite. The original sentences do not. Complete
the lock when every unique substantive item and protected exact element has
been recorded once.

### 3. Test sufficiency

Classify the material:

- **Sufficient:** enough claims and particulars exist for a specific piece.
- **Thin:** the point is usable, but evidence, examples, mechanisms, or stakes
  are sparse. Write the strongest narrower piece the source supports.
- **Unsafe:** a central claim is unsupported, contradictory, or misleading.
  Preserve and flag, verify with authorized sources, or qualify/block according
  to `factual_mode`.

Never compensate for thin material with invented detail or personality.
Complete the test when the material is classified and the permitted response to
that classification is fixed.

### 4. Design before drafting

Build a new information hierarchy around the reader's needs:

- choose the opening job: finding, request, tension, problem, scene, or concrete
  fact
- decide what deserves emphasis; cut only redundancy, empty scaffolding, or
  caller-authorized compression
- order reasons, evidence, examples, consequences, or steps
- place limitations where they change interpretation
- leave obvious connections implicit; use transitions for real relationships
- choose the ending job: decision, implication, action, consequence, synthesis,
  or honest open question

Do not default to equal sections, exhaustive coverage,
introduction/background/challenges/conclusion, or a takeaway after every
paragraph.

Complete the design when the reader path is clear and every planned omission
is authorized by the content lock.

### 5. Recompose

Draft from the content map and plan. Consult the source only to verify
substance, not as a sentence skeleton.

- state the main point early enough for the genre
- name known actors and mechanisms when relevant
- keep exact details that carry explanatory weight
- repeat the clearest term instead of cycling synonyms
- let paragraph length reflect importance and complexity
- attach qualifications to the claims they limit
- let sentence form express the relationship among ideas
- end paragraphs when their local work is complete
- stop when the piece's final job is done

Retain an original sentence only when it is already exact, natural, and
structurally appropriate—not merely to minimize edits.

Complete recomposition when every locked item is represented, every omission is
authorized, and no sentence survives solely from source inertia.

### 6. Test authoredness

Check whether the draft shows a coherent set of choices rather than polished
sentences assembled into a template:

- clear selection and hierarchy
- supported specificity
- visible but proportionate stance
- real information movement
- truthful constraints and trade-offs
- rhythm driven by thought
- non-mechanical paragraph shapes
- genre-native opening and ending

Consult [references/authoredness.md](references/authoredness.md) for long,
complex, genre-sensitive, or still-generic prose.

Complete the test when the applicable properties pass without manufactured
quirks or changes to substance.

### 7. Red-team the skeptical reader

Review for clusters, not isolated words:

- generic runway or closure
- exposed scaffolding or exhaustive symmetry
- pseudo-insight, importance inflation, or vague authority
- polished abstraction without particulars
- over-controlled transitions, recaps, or repeated sentence machinery
- synthetic balance, borrowed intimacy, promotional voice, or session residue

Fix only observable reader-facing defects. When two or more cues cluster or
local patches keep creating new mannerisms, consult
[references/skeptic-patterns.md](references/skeptic-patterns.md) and rebuild the
affected section. Complete the pass when every material cluster is repaired and
clean or constrained prose remains untouched.

### 8. Verify independently

Compare the completed rewrite with the content map, not only with memory.

- map every output claim to source support
- inspect additions, deletions, and strengthened or weakened claims
- compare actors, modality, negation, scope, chronology, causation,
  attribution, and evaluation
- verify exact names, numbers, dates, units, quotations, citations, URLs, code,
  and defined terms
- confirm that no personal experience, source, or imperfection was invented

Consult [references/verification.md](references/verification.md) for all
fact-bearing nonfiction and always for technical, academic, scientific, legal,
policy, medical, financial, or citation-bearing prose.

Complete verification when every locked item and output claim is accounted for,
every exact element matches, and no unauthorized addition or deletion remains.

### 9. Read continuously and deliver

Read at normal speed. Repair predictable template movement, repeated
announce-explain-recap paragraphs, slogan endings, unnecessary explanations,
and any repair that has become a new mannerism.

- `adaptive`: return only the artifact when nothing requires reporting;
  otherwise append concise source notes or withhold an unsafe artifact.
- `clean`: return only the artifact; use only when no unresolved issue requires
  a flag.
- `with_notes`: append material structural changes and unresolved source issues.

For `rewrite` and `write` file targets, edit in place and preserve non-prose
structures outside scope. Complete delivery when the artifact and any required
notes match the selected controls and the acceptance gate passes.

## Acceptance gate

The artifact is ready only when all applicable checks pass:

- **Fidelity:** zero unauthorized substantive changes
- **Integrity:** zero invented experience, identity, source, quotation,
  evidence, or error
- **Selection:** space and omission reflect consequence
- **Grounding:** important claims connect to supported particulars or limits
- **Stance:** judgment and uncertainty match the evidence
- **Structure:** organization follows the reader's problem, not a stock template
- **Movement:** each paragraph advances, qualifies, applies, or resolves
- **Cadence:** syntax follows thought without mechanical repetition or random
  variation
- **Genre:** formality, terminology, headings, citations, and explanation fit
- **Skeptic pass:** no unresolved cluster of generic scaffolding, pseudo-insight,
  vague authority, over-symmetry, slogan endings, or session residue
- **Delivery:** output contains only the requested artifact and necessary
  unresolved warnings

## Reference-loading policy

Do not load every reference reflexively. Use only the file that addresses the
observed problem. This avoids turning the diagnostic catalog into a new house
style.

- [references/authoredness.md](references/authoredness.md) — positive
  properties, genre defaults, and voice modes
- [references/skeptic-patterns.md](references/skeptic-patterns.md) — compact
  cluster-based diagnostics
- [references/verification.md](references/verification.md) — content-lock and
  fidelity audit
- [examples/recomposition.md](examples/recomposition.md) — examples of
  rebuilding rather than synonym-swapping
- [references/evaluation.md](references/evaluation.md) — blinded benchmark and
  release criteria
