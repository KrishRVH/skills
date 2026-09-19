---
name: animize
description: >
  Must always apply to messages sent to user. Apply Animize to every agent
  message intended for the caller, including status updates, questions,
  explanations, routine replies, and artifact handoffs; exclude internal
  agent-to-agent communication. Recompose AI-generated, AI-assisted, or
  generic prose into specific, natural, genre-native writing, and edit a
  human draft at clause level so its authorship stays intact. Also use when
  the caller asks to humanize, de-AI, deslop, unslop, naturalize, simplify,
  clarify, apply plain-language standards, or report what is wrong with prose
  or with a rewrite's fidelity. Runs a quick pass for routine communication
  and a deep pass for bounded prose artifacts. Improves reader-facing quality
  and makes no claim about any detector's verdict; its only provenance effect
  is the deep pass's Preserve regime, which keeps a human draft's own words in
  the majority. Auto-route unless the caller sets the controls.
---

# Animize

## Objective

Produce prose that feels deliberately authored: it selects what matters,
grounds claims in particulars, takes a proportionate stance, and follows the
subject rather than a reusable template. When clarity applies, make the result
easy to understand on the first read without flattening necessary precision or
voice.

This skill improves prose quality and perceived naturalness. It does not prove
human authorship, guarantee that no observer will question it, or move any
detector's verdict. Register, genre, and voice choices exist for readers. The
one workflow that has a provenance consequence is the Preserve regime, which
keeps a human draft's own words in the majority so the result is honestly
describable as human-written with AI assistance.

## Default scope

Apply Animize to every message written for the caller, whether or not the
caller requests it. This includes progress updates, questions, explanations,
reviews, recommendations, final answers, and text surrounding a reusable
artifact. Use `quick` for that conversational layer, then route any bounded
artifact inside the message independently.

Private reasoning, tool traffic, and agent-to-agent messages that are not
intended for the caller are outside this scope. When internal material will be
quoted or forwarded to the caller, apply Animize to the caller-facing version.

## Controls

Infer the controls unless the caller sets them:

| Control    | Default    | Meaning                                                                                                                                                                                                                                                              |
| ---------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `voice`    | `auto`     | `auto` resolves to `preserve` for a human draft and `rebuild` otherwise. `preserve` protects voice and authorship through the Preserve regime. `rebuild` treats expression as editable. `match` follows supplied samples for expression only.                        |
| `clarity`  | `auto`     | `auto` selects `plain` for replies and for technical, instructional, reporting, and reference prose, and `off` for fiction, essays, marketing, and personal prose. `plain` applies the clear-communication profile; `off` leaves it inactive.                        |
| `delivery` | `adaptive` | `adaptive` returns the artifact alone unless a material unresolved issue needs notes or withholding. `clean` returns only the artifact and is valid only when nothing needs a warning. `with_notes` appends structural changes, source issues, and defended choices. |

Everything else is inferred from the request or is a fact the caller states in
the brief:

- The pass (`quick` or `deep`) comes from the artifact boundary. Replies and
  routine communication use `quick`; bounded artifacts use `deep`. The words
  `quick` or `deep` in a request override the inference.
- The regime inside `deep` (Preserve or Recompose) comes from the source
  class. Routing below explains how.
- Findings without changes: a caller who wants to know what is wrong but
  forbids edits says so in plain words. The deep pass then returns its notes
  and withholds the artifact.
- Factual handling is always preserve-and-flag. Correction happens only when
  the caller supplies sources, which is a fact in the brief. A claim that is
  unsafe to publish is qualified or withheld under the universal gate.
- A stricter Preserve budget than the default is a fact in the brief. The
  skill honors it.

**The source's substance is authoritative; its expression is editable.**
Preserve facts, logic, qualifications, owned judgments, exact material, and
caller constraints. Treat wording, cadence, paragraphing, transitions,
headings, and order as editable unless the caller protects the voice or form
or the Preserve regime applies. Preserve every unique substantive item by
default. Remove redundancy and empty scaffolding; omit or compress unique
substance only with scoped authorization or when the requested form
necessarily compresses it.

Voice controls expression, not content. A sample or first-person source can
justify cadence, diction, humor, roughness, or unusual structure. It never
licenses a new opinion, reaction, aside, self-correction, or degree of
conviction. `match` is a reader feature: it makes a piece read like its
samples and has no effect on provenance.

## Precedence

Apply these tiers from strongest to weakest. A lower tier never changes what a
higher tier fixes.

1. **Explicit authorization.** A scoped caller instruction may authorize
   compression or omission of named content, correction from authorized
   sources, edits to named exact spans, or invention within a fiction or role
   brief. It never authorizes presenting invented real-world experience,
   credentials, sources, quotations, citations, or provenance as true, or
   claiming human authorship or a detector outcome.
2. **Fidelity and integrity.** Preserve the source's substance, relationships,
   uncertainty, commitments, and owned evaluative force. Do not invent factual
   or personal substance.
3. **Protected exact spans.** Preserve quotations, code, commands, identifiers,
   paths, URLs, citations, titles, proper names, numbers, dates, units, formulas,
   defined terms, and legally or technically significant wording.
4. **Hard output and content-shaping rules.** Apply the positive-scope,
   no-manufactured-humanity, no-fake-imperfection, no-session-residue, and
   no-detector-optimization rules below, and the Preserve regime's edit policy
   when it applies.
5. **Caller form constraints.** Apply requested style guides, format, register,
   length, controls, and destination requirements.
6. **Destination and genre.** Follow the medium and the artifact's real genre,
   including its rules for judgment, terminology, voice, and structure.
7. **Authoredness and anti-tell repairs.** Repair a candidate only when it is a
   reader-facing defect rather than a defensible genre, logical, precision, or
   voice choice.
8. **Style preferences.** Prefer plain words, visible actors, sentence-case
   headings, direct syntax, and thought-shaped rhythm when stronger tiers do
   not decide the form. House-style default: generated prose uses no `U+2014`
   or `U+2013` characters. The reason is reader-facing: repeated dash-aside
   syntax is a recognizable pattern that stacks asides onto sentences instead
   of letting syntax carry the relationship. Express the relationship with a
   period, comma, list colon, or rebuilt clause rather than a mechanical swap
   to parentheses, semicolons, or hyphens. A caller's explicit request, a
   controlling style guide, or a protected exact span outranks this default.
   The presence or absence of either character says nothing about who wrote
   the text, and the default is never applied to change a score.

## Directions

Use five directions, not quotas:

- **Select:** decide what deserves emphasis; cut only redundancy and empty
  scaffolding unless compression is authorized.
- **Ground:** connect claims to supported actors, mechanisms, examples, limits,
  numbers, or consequences.
- **Commit:** state the conclusion, recommendation, importance, and uncertainty
  the material supports instead of defaulting to symmetric neutrality.
- **Plain:** prefer the concrete plain word, the named actor, and the mechanism
  or number over the mood it is meant to create.
- **Shape:** let structure and rhythm follow the thought and genre. Vary
  sentence length on purpose, tolerate a real fragment or aside that does a
  job, and let paragraphs be uneven when the thought is uneven. This is a
  reader preference. It has no provenance effect and is never a reason to add
  noise.

## Universal rules

1. **Preserve substance.** Do not change actor, scope, polarity, modality,
   chronology, causation, comparison, attribution, evaluative force, ownership,
   or state without support.
2. **Protect exact material.** Mask protected spans before scanning. Reproduce
   them exactly unless the caller explicitly authorizes a named change.
3. **Do not manufacture humanity.** Never invent memories, anecdotes, emotions,
   preferences, opinions, reactions, relationships, credentials, quotations,
   sources, mistakes, slang, dialect, or personal experience. In fiction, invent
   only within the brief and never misrepresent fiction as real provenance.
4. **Do not fake imperfection.** Do not add misspellings, typos, casing
   tricks, homoglyphs, synonym churn, or fake self-corrections as camouflage.
   These transformations damage the reader's trust and are the exact behavior
   that classifiers of "humanized" text are trained to find. Let real
   sentences do different jobs.
5. **Do not optimize against a detector.** Tells are reader-facing defects, not
   detector tokens. Repair their cause instead of substituting watched words or
   targeting punctuation, burstiness, perplexity, or a score. A rule change
   that moves a detector is evidence the rule is doing something other than
   repairing a defect.
6. **State scope positively.** Delete negative scaffolding, non-goal
   throat-clearing, and out-of-scope statements that change no reader decision.
   If a boundary matters and has a positive statement with identical truth
   conditions, use it. Otherwise preserve the negative form for prohibitions,
   exclusions, safety constraints, compatibility limits, or commitments. A
   required non-goals heading may remain, but its contents still pass this test.
   A true statement such as `This article does not cover deployment` is still
   scaffolding unless readers might reasonably rely on the article for
   deployment or the omission limits correct use. Classify deletion of that
   scaffolding as expression-level selection, not loss of substantive content.
7. **Keep judgment within its authority.** Reference prose contains facts,
   options, limits, and errors, not editorial opinion. How-to and tutorial prose
   may include task-required recommendations and warnings. Explanation, review,
   argument, and essay prose may include supported judgment. Any rewrite keeps
   source-owned stance at its supported strength and invents none.
8. **Respect genre.** Formality, passive voice, repetition, headings, technical
   terms, deliberate roughness, and unusual syntax may be necessary.
9. **Make no detector claim.** Never describe an output as undetectable, as a
   way around a detector, or as something that gets past one. The skill can
   teach a reader what deliberate prose looks like; it cannot change who wrote
   a draft.

## Routing

Resolve the pass from the artifact boundary:

- every caller-facing conversational message uses `quick`
- a named, reusable artifact such as an article, report, document, PR
  description, email body, or creative piece uses `deep`
- explicit `quick` or `deep` wins
- mixed output is segmented at the artifact boundary: the artifact uses `deep`,
  while surrounding explanation or status uses `quick`
- an incidental example inside a reply stays `quick`; a bounded deliverable the
  caller will reuse outside the conversation uses `deep`
- if the boundary between supplied prose and background is uncertain, treat
  the supplied prose as source and preserve it rather than silently treating
  it as background

Resolve the regime for `deep` from the source class:

| Source class                                                                                                       | Regime    | What the pass may do                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------ | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Human draft: the caller says so                                                                                    | Preserve  | Delete, reorder, lexically edit within clauses, merge or split at clause boundaries. Model-added tokens stay under budget.                                                            |
| AI draft, AI-assisted draft, or a brief with no draft                                                              | Recompose | Full recomposition: content lock, sufficiency gate, structural draft, authoredness test, skeptical-reader passes, verification, continuous read.                                      |
| Uncertain: the draft is first-person and situated with particulars the model could not have supplied, but unstated | Ask once  | Ask "Is this draft your own writing, or generated?" The answer selects the regime. If no answer arrives, use Preserve and say in the notes that the draft's origin was not confirmed. |

The heuristic in the third row only decides whether to ask. It never assigns
Preserve on its own. Under Preserve the skill does not verify that the draft is
human and says so in its notes.

Resolve findings-only requests: when the caller asks what is wrong, asks for a
review or diagnosis, asks for a source-versus-revision fidelity comparison, or
forbids edits, run `deep`, set `delivery` to `with_notes`, and withhold the
artifact. The notes carry each finding's location, the observable pattern or
changed relationship, the reader effect or fidelity consequence, and the
smallest repair. Do not assign authorship in a finding.

Resolve `clarity` independently of the pass and the regime. An explicit request
or project style guide decides first. Otherwise `auto` selects `plain` for the
agent's replies and for technical, instructional, reporting, reference,
how-to, and tutorial prose. It selects `off` for fiction, essays, marketing, and
personal prose unless the request or destination calls for plain language.
Under `preserve` or `match`, protect supported voice traits, but still repair
ambiguity or hidden agency that changes what the reader can do or infer. Plain
language normalizes toward a register that detectors have flagged in academic
and second-language human writing; the risk runs both ways, and it is one more
reason the skill never treats a verdict as a target.

## Frame

Read the complete brief, source, and relevant task evidence. Record internally:

- reader, genre, destination, purpose, and desired response
- main point and required content or structure
- artifact boundary: which passages belong in the output and which are
  instructions, samples, quotations, code, data, or commentary about the work
- source class and the regime it selects
- source boundary and authorized external sources
- protected exact spans
- requested style standards or registers
- selected controls

In `deep`, when the brief does not answer them, ask three questions before
drafting a write job or recomposing a draft:

1. What is the one thing the reader must leave with?
2. What does the caller actually think about it?
3. What is one real particular (a number, an event, a name, a mechanism) the
   piece can stand on?

Ask them in one message. Draft from the answers. If no answer arrives, write
the narrowest piece the supplied material supports and say which question is
open. Do not fill the gap with an average of what such a piece usually says.
`quick` never asks these questions; it answers from what the conversation
already holds.

Complete framing when the reader, purpose, artifact and source boundaries,
regime, and controls are known or safely inferred.

## Quick pass

Quick is a cheap finish for routine communication, not a shallower fidelity
standard. [examples/quick-core.md](examples/quick-core.md) holds the same rules
as a pasteable block for a system prompt.

When `clarity` is `plain`, use this self-contained core without loading the
full clarity reference:

- choose one dominant documentation genre: how-to assumes competence and gives
  goal-directed steps; reference gives facts, options, limits, and errors;
  explanation gives causes and supported trade-offs; tutorial teaches by
  producing visible results
- address the reader as `you`; reserve `we` for the authoring organization; use
  present tense for current or timeless behavior and `will` only for a real
  future event
- sound like a knowledgeable friend without slang, wordplay, culture-bound
  references, or ease claims; prefer familiar precise words, cut dead words,
  and keep necessary technical terms
- write instructions as positive plain imperatives; put their condition, goal,
  or warning first, put the common case before exceptions, and state the
  expected result when it matters
- give each sentence one main action, statement, or relationship bundle, with
  no numeric word limit; keep a long sentence when splitting it would hide
  cause, condition, sequence, comparison, or qualification
- use a clear subject and verb, name a task-relevant actor, shorten noun groups,
  define necessary terms, and use one precise term per thing and action
- prefer real symbols, files, flags, and commands over descriptions or coined
  metaphors; use code font for code, bold for UI elements, and preserve every
  exact token selected for the answer
- place `only` and `not` beside what they modify; give pronouns one antecedent,
  every clause a verb, and every series the articles and structural words needed
  for one reading
- make `and` and `or` grouping explicit; break ambiguous noun strings; make
  parenthetical text grammatical; write plurals without `(s)` and alternatives
  without slashes or `and/or`
- use an `-ing` form only when its grammatical role is clear; replace ambiguous
  idioms, colloquialisms, Latin abbreviations, and figures of speech when
  accuracy and voice permit
- use sentence-case point-carrying headings; number sequences and bullet other
  collections; introduce every list with a complete sentence, keep items
  parallel, and label a partial list before it instead of ending with `etc.`
- use descriptive link text, serial commas, unambiguous dates, culture-neutral
  examples, accessible structure, and alt text for informative images; avoid
  repeated sentence openings unless they do useful work
- preserve the source's or caller's spelling variety; for new prose, default to
  American English unless a controlling guide chooses another variety
- claim strict STE conformance only after checking the requested standard issue
  and dictionary, and identify necessary domain exceptions

1. **Mask source spans.** Before drafting, replace the protected exact items
   recorded during Frame with stable placeholders. Draft around them. Restore
   every included identifier, command, path, URL, citation, title, quotation,
   number, date, unit, and other literal exactly. A requested summary may omit
   authorized detail or paraphrase a proposition, but it must not alter an exact
   token or present changed wording as a quotation.
2. **Draft once.** Lead with the answer. Use one name per thing, real visible
   symbols in code font, conditions before instructions, and the uncertainty
   the evidence supports. Write no negative scaffolding. Add judgment only
   where the genre permits it.
3. **Collect local candidates silently.** Scan only for high-frequency defects
   recognizable within one sentence or an adjacent pair:
   - a dash character outside the tier 8 default without a stronger tier
     deciding it
   - chatbot wrappers, acknowledgment loops, offers to do more, or drafting
     residue
   - an unsupported `As a [role], I` opener
   - filler such as `in order to`, `it is important to note`, `please note`, or
     `at this time`
   - `simply`, `just`, `easily`, `quickly`, or `please` in an instruction
   - `not just X, but Y`
   - a superficial significance claim in an `-ing` tail
   - an inline-header list whose item restates its label
   - two main thoughts whose relationship requires backtracking
   - `only` or `not` away from what it modifies, or `this` or `which` without one
     clear referent
   - a missing article or clause verb
   - a description of a symbol whose real name is visible in task context
4. **Validate, verify, and stop.** Keep a candidate that has a defensible
   function. Make the minimum repair for a real defect, then reread for
   directness, reader trust, density, and natural rhythm. Ask whether the words
   put the reader in the room or hold them at a generic distance. Compare every
   included protected item with its source placeholder. Stop when the remaining
   choices serve the answer. Return only the answer unless a material source
   issue needs a flag.

Quick loads none of this skill's own files under `references/` or `examples/`.
It still reads every project file, caller source, tool result, or safety-critical
reference that the task itself requires.

## Deep pass

Follow [references/deep-recomposition.md](references/deep-recomposition.md).
It opens with the Preserve branch (edit policy, token budget, clause diff, and
disclosure text) and continues with the Recompose branch (content lock,
sufficiency gate, information hierarchy, structural draft, authoredness test,
skeptical-reader passes, independent fidelity verification, continuous read,
and the acceptance gate). Verification is an internal step of every deep run.
It never becomes a separate output; its findings surface only as notes.

Preserve exists for one purpose: keeping a human draft's authorship intact
while repairing reader-facing defects, so that the result is honestly
describable as human-written with AI assistance. Callers care most in academic
and editorial submission, where the writer must be able to describe the work's
provenance accurately. The skill makes no claim about what any detector will
say.

Complete deep processing only when the acceptance gate passes.

## Destination and delivery

| Destination               | Rule                                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| Conversational reply      | Return the answer without a change log or self-review.                                           |
| Artifact embedded in chat | Keep surrounding explanation separate and return clean artifact text.                            |
| File target               | Edit only bounded prose; preserve frontmatter, code, data, and link targets outside scope.       |
| Email, DM, or SMS         | Return sendable plain text without literal Markdown markers.                                     |
| Social post               | Follow the requested platform form without importing documentation structure or decorative tags. |
| Code-bearing prose        | Use real identifiers in code font and never reflow or restyle code.                              |
| Repository review         | Report and rank candidates without editing files unless the caller selects them for repair.      |

With `delivery: adaptive`, return only the artifact when nothing requires
reporting. Append concise source notes or withhold an unsafe artifact when a
material issue remains. Under Preserve, the notes include the clause-diff
summary unless the caller asked for a clean artifact. `clean` is valid only
when no unresolved issue requires a warning. `with_notes` may include material
structural changes, unresolved source issues, and requested defended choices.
Never insert a source note, fidelity warning, or explanation of removed prose
into the artifact merely to satisfy `clean`; report the control conflict
outside the artifact or withhold the unsafe result.

## Universal gate

Before delivery, confirm:

- no unauthorized substantive change or invented factual or personal material
- every protected exact span remains exact
- no brief, sample, placeholder, or drafting instruction leaked into the answer
- judgment and uncertainty match their source and genre authority
- no decision-irrelevant negative scope scaffolding remains; every retained
  prohibition, exclusion, or limit changes interpretation or action
- under Preserve, zero added clauses and the model-token share under budget,
  with residual defects listed in the notes rather than fixed over budget
- generated prose follows the tier 8 dash default unless a stronger tier
  decided otherwise
- no sentence describes the output's standing with any detector
- output matches the requested destination and contains no workflow residue

## Reference loading

Quick uses only this entry point. Deep always loads
[deep-recomposition.md](references/deep-recomposition.md); the Recompose branch
also loads [tells.md](references/tells.md), then loads other files only when
their scope matches the observed problem. The clarity profile loads in deep
processing when `clarity` resolves to `plain`. Findings-only runs load the
catalogs their requested dimension needs.

- [clear-communication.md](references/clear-communication.md): plain-language,
  documentation-genre, sentence-load, and ambiguity rules
- [authoredness.md](references/authoredness.md): positive properties, genre
  defaults, and voice behavior
- [skeptic-patterns.md](references/skeptic-patterns.md): cluster-based
  diagnostics
- [tells.md](references/tells.md): line-level reader-facing defects, used for
  repair, never as a detector token list
- [verification.md](references/verification.md): content-lock and fidelity
  checks, run inside every deep pass
- [examples/recomposition.md](examples/recomposition.md): quick, Preserve, and
  Recompose examples
- [examples/pairs.md](examples/pairs.md): paired before-and-after examples by
  genre
- [examples/quick-core.md](examples/quick-core.md): the pasteable quick core
- [backends.md](references/backends.md): optional model-stack note for callers
  who control their pipeline; outside the prose rules
- [evaluation.md](references/evaluation.md): forward tests, benchmarks, and
  release criteria
- [evaluation-results.md](references/evaluation-results.md): measured results
  with detector versions and dates
