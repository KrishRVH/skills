# Deep recomposition

Use this workflow when `process` is `deep` and `job` is `write` or `rewrite`.
Complete the shared Frame step in [the entry point](../SKILL.md#frame) first.

## Contents

- [2. Lock the content](#2-lock-the-content)
- [3. Test sufficiency](#3-test-sufficiency)
- [4. Design before drafting](#4-design-before-drafting)
- [5. Recompose](#5-recompose)
- [6. Test authoredness](#6-test-authoredness)
- [7. Red-team the skeptical reader](#7-red-team-the-skeptical-reader)
- [8. Verify independently](#8-verify-independently)
- [9. Read continuously and deliver](#9-read-continuously-and-deliver)
- [Acceptance gate](#acceptance-gate)

## 2. Lock the content

For a rewrite, extract a compact content map from the source. For a write job,
extract it from the brief and authorized supporting material.

- propositions and actors
- causal, temporal, contrastive, comparative, and conditional relationships
- owned judgments and their strength
- uncertainty, scope, exceptions, and negation
- names, dates, numbers, units, places, terminology, quotations, citations,
  URLs, and required examples or actions
- promises, obligations, permissions, prohibitions, guarantees, and ownership
- current, prior, proposed, hypothetical, and unknown states
- unsupported or ambiguous source claims

Apply the entry point's positive-scope test before locking a negative scope
statement. Lock a decision-relevant constraint, prohibition, exclusion, or
commitment. Put every true but decision-irrelevant non-goal, topic omission, or
out-of-scope statement on a separate scaffolding discard list rather than in
the content map. Its truth does not make it substantive. Do not replace it with
a smoother sentence that announces the same omission.

The content map governs the artifact. The original sentences do not. Complete
the lock when every unique substantive item and protected exact element has
been recorded once.

## 3. Test sufficiency

Classify the material:

- **Sufficient:** enough claims and particulars exist for a specific piece.
- **Thin:** the point is usable, but evidence, examples, mechanisms, or stakes
  are sparse. Write the strongest narrower piece the source supports.
- **Unsafe:** a central claim is unsupported, contradictory, or misleading.
  Preserve and flag, verify with authorized sources, or qualify or block it
  according to `factual_mode`.

Never compensate for thin material with invented detail or personality. Treat
vague benefits, quality labels, and future action as proof gaps, not raw
material for a stronger claim. Narrow them to what the source establishes or
flag the missing actor, mechanism, changed step, metric, evidence, or owner.

Complete the test when the material is classified and the permitted response
to that classification is fixed.

## 4. Design before drafting

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
introduction-background-challenges-conclusion, or a takeaway after every
paragraph.

Complete the design when the reader path is clear and every planned omission
is authorized by the content lock.

## 5. Recompose

Draft from the content map and plan. Consult the source only to verify
substance, not as a sentence skeleton.

- state the main point early enough for the genre
- name the actual agent and mechanism when relevant; use conventional metonymy
  only when it does not hide responsibility
- use active voice when it clarifies responsibility; retain passive voice when
  the actor is unknown, irrelevant, deliberately withheld, or conventional for
  the genre
- prefer the plain word; say what a thing does or measures, not how it should
  feel
- use first person where the genre permits it and the material supports the
  position
- keep exact details that carry explanatory weight
- repeat the clearest term instead of cycling synonyms
- let paragraph length reflect importance and complexity
- attach qualifications to the claims they limit
- let syntax express cause, contrast, condition, sequence, and qualification;
  do not hide those relationships behind stacked declarations
- label supplied hypotheticals and placeholders; never harden them into fact
- omit every item on the scope-scaffolding discard list; do not recast it as a
  source caveat or artifact sentence
- end paragraphs when their local work is complete
- use sentence-case headings, straight quotes, spare bold, and no decorative
  emoji when no destination style controls those choices
- apply [the clear-communication profile](clear-communication.md) when
  `clarity` resolves to `plain`
- obey the entry point's dash rule in every voice and destination
- stop when the piece's final job is done

Under `recompose`, retain an original sentence only when it is already exact,
natural, and structurally appropriate, not merely to minimize edits.
Recomposition permits structural rebuilding; it does not require changing an
already deliberate, genre-native passage. Under `light`, make the minimum
effective edit and preserve working order and paragraph shape. Under
`standard`, rebuild defective local units and reorganize only where the reader
path fails.

Complete recomposition when every locked item is represented, every omission
is authorized, and the selected depth preserves no defect from inertia and
changes no working passage merely for consistency.

## 6. Test authoredness

Check whether the draft shows a coherent set of choices rather than polished
sentences assembled into a template:

- clear selection and hierarchy
- supported specificity
- visible but proportionate stance
- real information movement
- truthful constraints and trade-offs
- rhythm driven by thought
- non-mechanical paragraph shapes
- a genre-native opening and ending
- intervention proportionate to `rewrite_depth`, with strong passages left
  intact under `light` and intentional voice protected under `preserve`

Consult [authoredness.md](authoredness.md) for long, complex, genre-sensitive,
personal, sample-led, or still-generic prose.

Complete the test when the applicable properties pass without manufactured
quirks or changes to substance.

## 7. Red-team the skeptical reader

Mask protected exact spans before either pass. A scan may observe their
boundaries but must not diagnose or change their contents.

### Cluster pass

Review for mutually reinforcing structural choices:

- generic runway or closure
- exposed scaffolding or exhaustive symmetry
- pseudo-insight, importance inflation, or vague authority
- polished abstraction without particulars
- over-controlled transitions, recaps, or repeated sentence machinery
- synthetic balance, borrowed intimacy, promotional voice, or session residue
- staged rebuttals, fake alternatives, sloganized claims, or coined labels that
  substitute for an argument
- interchangeable blocks, list-shaped prose, or repeated metaphors and examples
  doing the same work
- formulaic challenges and outlook sections that manufacture conflict before a
  vague optimistic close

When two or more cues cluster or local patches keep creating new mannerisms,
consult [skeptic-patterns.md](skeptic-patterns.md) and rebuild the affected
section.

For prose longer than about one page, compare the claims made by distant
sections. Merge or remove a later restatement that adds no condition,
consequence, example, or requested summary. Preserve procedural repetition,
defined terms, refrains, and intentionally modular sections.

### Line sweep

Consult [tells.md](tells.md) and check each unmasked sentence for AI-default
vocabulary, fancy copulas, `not just X, but Y`, forced triads, false ranges,
superficial `-ing` tails, filler, significance adverbs, false agency, clipped
negations, unsupported verdicts, unmotivated passives, stacked declarations,
feeling-instead-of-mechanism claims, and typographic or drafting residue.

Classify each candidate as `fix`, `retain`, or `flag`. Fix it only when the form
is a defect rather than a specific genre, logical, precision, or voice choice.
Record defensible false positives internally; report them only for an audit or
when `delivery` is `with_notes` and the information helps the caller.

Complete the pass when every material cluster is repaired, no known tell
survives without a defensible function, and clean or constrained prose remains
untouched.

## 8. Verify independently

Compare the completed artifact with the content map, not only with memory.

- map every output claim to source support
- inspect additions, deletions, and strengthened or weakened claims
- compare actors, modality, negation, scope, chronology, causation,
  attribution, and evaluation
- compare promises, obligations, permissions, guarantees, ownership, and the
  status of proposed or hypothetical material
- verify exact names, numbers, dates, units, quotations, citations, URLs, code,
  and defined terms
- confirm that no personal experience, source, stance, or imperfection was
  invented
- confirm that instructions and examples about the artifact did not leak into
  it

Consult [verification.md](verification.md) for all fact-bearing nonfiction and
always for technical, academic, scientific, legal, policy, medical, financial,
or citation-bearing prose.

Complete verification when every locked item and output claim is accounted
for, every exact element matches, and no unauthorized addition or deletion
remains.

## 9. Read continuously and deliver

Read at normal speed. Ask:

- What would still make this read as obviously machine-shaped?
- Where is the reader held outside the room by abstraction, distance, or
  unnecessary explanation?
- Which remaining oddities have a defensible function, and which are residue?

Repair the answers, along with predictable template movement, repeated
announce-explain-recap paragraphs, slogan endings, and any repair that has
become a new mannerism. Stop when the remaining candidates serve the piece.

Before delivery, scan generated text for forbidden dash characters and hidden
Unicode residue. Preserve and flag suspicious source characters rather than
silently normalizing protected spans.

- `adaptive`: return only the artifact when nothing requires reporting;
  otherwise append concise source notes or withhold an unsafe artifact.
- `clean`: return only the artifact; use only when no unresolved issue requires
  a flag.
- `with_notes`: append material structural changes and unresolved source issues.

For file targets, edit only bounded prose and preserve frontmatter, code,
structured data, and link targets outside scope. Complete delivery when the
artifact and any required notes match the controls and the acceptance gate.
Keep source gaps, fidelity warnings, and explanations of removed source prose
outside the artifact. If `delivery: clean` conflicts with a required warning,
report that conflict or withhold the artifact rather than embedding the warning
as content.

## Acceptance gate

The artifact is ready only when all applicable checks pass:

- **Fidelity:** zero unauthorized substantive changes
- **Integrity:** zero invented experience, identity, source, quotation,
  evidence, preference, reaction, owned judgment, or error
- **Boundary:** no brief, example, placeholder, or drafting instruction appears
  as artifact content; no hypothetical becomes fact
- **Selection:** space and omission reflect consequence
- **Grounding:** important claims connect to supported particulars or limits
- **Stance:** judgment and uncertainty match the evidence
- **Structure:** organization follows the reader's problem, not a stock template
- **Movement:** each paragraph advances, qualifies, applies, or resolves
- **Cadence:** syntax follows thought without mechanical repetition or random
  variation
- **Proportion:** the amount and kind of change match `rewrite_depth` and
  `voice_mode`; no strong passage is regularized merely for consistency
- **Scope:** no negative scaffolding remains; every retained prohibition,
  exclusion, safety constraint, compatibility limit, or commitment changes a
  reader decision and has no lossless positive form
- **Clarity:** when the profile applies, each sentence has one likely reading
  and one main relationship bundle
- **Genre:** formality, terminology, headings, citations, and explanation fit
- **Skeptic pass:** no unresolved cluster of generic scaffolding, pseudo-insight,
  vague authority, over-symmetry, slogan endings, or session residue
- **Tells:** no known line-level tell survives without a genre, precision,
  source-voice, or sentence-function justification
- **Dashes:** zero generated `U+2013` or `U+2014` characters outside protected
  exact spans unless the caller explicitly overrides the rule
- **Delivery:** output contains only the requested artifact and necessary
  unresolved warnings
