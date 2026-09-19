# Deep pass

Use this workflow when the pass is `deep`. Complete the shared Frame step in
[the entry point](../SKILL.md#frame) first, including the regime decision. The
Preserve branch applies to a human draft. The Recompose branch applies to an
AI draft, an AI-assisted draft, or a brief with no draft.

## Contents

- [Preserve branch](#preserve-branch)
  - [P1. Edit policy](#p1-edit-policy)
  - [P2. Budget](#p2-budget)
  - [P3. Clause diff](#p3-clause-diff)
  - [P4. Disclosure and delivery](#p4-disclosure-and-delivery)
- [Recompose branch](#recompose-branch)
  - [2. Lock the content](#2-lock-the-content)
  - [3. Test sufficiency](#3-test-sufficiency)
  - [4. Design before drafting](#4-design-before-drafting)
  - [5. Recompose](#5-recompose)
  - [6. Test authoredness](#6-test-authoredness)
  - [7. Red-team the skeptical reader](#7-red-team-the-skeptical-reader)
  - [8. Verify independently](#8-verify-independently)
  - [9. Read continuously and deliver](#9-read-continuously-and-deliver)
- [Acceptance gate](#acceptance-gate)

## Preserve branch

Preserve keeps a human draft's authorship intact while repairing reader-facing
defects. The draft's own words stay in the majority; the model contributes
deletions, reorderings, and small lexical edits, and nothing it composed from
meaning alone. The result is honestly describable as human-written with AI
assistance. The skill does not verify that the draft is human. It takes the
caller's word and says so in its notes.

Preserve does not load `tells.md` or `skeptic-patterns.md` as repair lists.
Read the draft for defects a reader would notice, then repair each one within
the edit policy. When a defect cannot be repaired within the policy, list it in
the notes.

### P1. Edit policy

Permitted, in order of preference:

1. **Delete.** Remove redundancy, scaffolding, and negative scope statements
   that change no reader decision.
2. **Reorder.** Move sentences, paragraphs, and sections.
3. **Lexically edit within a clause.** Replace a word, fix agreement, tighten
   a phrase, or cut a modifier. The clause stays recognizable as the source
   clause: most of its tokens survive in order.
4. **Merge or split at clause boundaries.** Join two source clauses with a
   conjunction or a period, or separate them, without introducing a clause
   that has no source.

Prohibited:

- regenerating a sentence or paragraph from its meaning
- adding a clause with no lexical anchor in the source
- adding a transition, framing sentence, opening, or ending the source lacks

When the draft needs an opening, a transition, or an ending it does not have,
draft it as a clearly marked suggestion in the notes and leave the artifact
without it. The caller decides whether to write it in.

Every other rule of the skill still applies: substance is preserved, exact
spans are protected, nothing personal or factual is invented, and no
imperfection is faked. Preserve narrows what the model may write. It does not
loosen what it must keep.

Complete the policy check when every planned change is one of the four
permitted operations.

### P2. Budget

`PRESERVE_BUDGET = 0.15`. Model-added tokens must be strictly fewer than the
source's tokens and under 15% of the output's tokens. The constant lives here
and is not a caller control. A caller who needs a stricter budget states it in
the brief, and the pass honors the stricter number. A caller cannot loosen it;
a draft that needs more change than the budget allows belongs in Recompose,
and the notes say so.

The 15% figure is the share below which a window of text keeps one dominant
provenance label in the labeling scheme Pangram publishes for mixed
authorship. The skill uses it as an honest boundary for the phrase "with AI
assistance," not as a target to approach.

If the budget cannot be met without leaving a defect the brief requires
fixing, deliver within budget and list the residual defects as notes. Never
exceed the budget silently.

### P3. Clause diff

Before delivery, compute a clause-level diff of source against output and
report it. The procedure is designed to be run by hand on a short draft and by
script on a long one.

1. **Split both texts into clauses.** Break at sentence ends, then at a comma,
   semicolon, colon, or dash that separates two groups each holding a subject
   and a verb and at least four words. Number the source clauses S1, S2, ...
   and the output clauses O1, O2, ...
2. **Normalize.** Lowercase, drop punctuation, collapse whitespace.
3. **Match each output clause to its best source clause.** Count the tokens
   the two clauses share in order (the longest common subsequence of tokens)
   and divide by the longer clause's token count. Each source clause may be
   consumed once.
4. **Classify each output clause:**
   - `kept`: shared share at or above 0.9
   - `lexically_edited`: shared share from 0.5 up to 0.9
   - `added`: shared share below 0.5, or no unconsumed source clause left
5. **Classify each unmatched source clause as `deleted`.**
6. **Mark `reordered`** for kept and edited clauses whose source numbers are
   not in ascending order in the output.
7. **Count model-added tokens:** every token in an `added` clause, plus every
   token in a `kept` or `lexically_edited` clause that appears nowhere in the
   source. Count against the whole source, not only the matched clause, so
   that rejoining two of the author's own fragments after cutting a
   parenthetical costs nothing.
8. **Compute the share:** model-added tokens divided by output tokens.

Report: clauses kept, deleted, reordered, lexically edited, and added;
model-added tokens; source tokens; output tokens; share. Under Preserve any
`added` clause is a violation, and a share at or above the budget is a
violation. Repair a violation by reverting the offending clause to a permitted
operation or by moving the fix to the notes.

### P4. Disclosure and delivery

Deliver the artifact, then the notes:

- the clause-diff summary from P3, unless the caller asked for `clean`
- one line stating that the draft was treated as the caller's own writing on
  the caller's word, or on the fallback when the routing question went
  unanswered
- residual defects left unrepaired because of the budget, each with the
  smallest repair the caller could make
- suggested openings, transitions, or endings, clearly marked as suggestions
  and not present in the artifact

Complete the Preserve branch when the artifact contains only permitted
operations, the diff shows zero added clauses and a share under budget, and
the notes account for every residual defect and suggestion. The Recompose
branch's acceptance gate applies with its Proportion check read as the
Preserve edit policy.

## Recompose branch

Use this branch for an AI draft, an AI-assisted draft, or a write job from a
brief. The steps below are numbered to follow Frame as step 1.

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
  are sparse. Write the strongest narrower piece the source supports. If the
  entry point's three framing questions are unanswered, ask them now rather
  than drafting around the gap.
- **Unsafe:** a central claim is unsupported, contradictory, or misleading.
  Preserve and flag it. Correct it only from sources the caller supplied.
  Qualify or withhold it when publishing it unqualified would mislead.

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
- follow the entry point's tier 8 dash default unless a stronger tier decides
- stop when the piece's final job is done

Retain an original sentence only when it is already exact, natural, and
structurally appropriate, not merely to minimize edits. Recomposition permits
structural rebuilding; it does not require changing an already deliberate,
genre-native passage. Under `voice: match`, apply the recorded voice signals
to expression only.

Complete recomposition when every locked item is represented, every omission
is authorized, no defect survives from inertia, and no working passage changed
merely for consistency.

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
- strong passages left intact, and recorded voice signals protected under
  `match`

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
Record defensible false positives internally; report them only in a
findings-only run or when `delivery` is `with_notes` and the information helps
the caller.

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
or citation-bearing prose. Verification is internal to the pass. Its findings
reach the caller only as notes, or as the whole response in a findings-only
run.

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

Before delivery, scan generated text for hidden Unicode residue and for dash
characters the tier 8 default does not allow. Preserve and flag suspicious
source characters rather than silently normalizing protected spans.

- `adaptive`: return only the artifact when nothing requires reporting;
  otherwise append concise source notes or withhold an unsafe artifact.
- `clean`: return only the artifact; use only when no unresolved issue requires
  a flag.
- `with_notes`: append material structural changes and unresolved source issues.
- findings-only: return the notes and withhold the artifact.

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
- **Proportion:** under Recompose, no strong passage is regularized merely for
  consistency; under Preserve, every change is a permitted operation, the
  clause diff shows zero added clauses, and the model-token share is under
  budget
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
- **Dashes:** generated prose follows the tier 8 default unless a stronger tier
  decided otherwise
- **Detector silence:** no sentence describes the output's standing with any
  detector
- **Delivery:** output contains only the requested artifact and necessary
  unresolved warnings, or only the notes in a findings-only run
