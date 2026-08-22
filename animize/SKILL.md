---
name: animize
description: >
  Recompose AI-generated, AI-assisted, or generic prose into specific,
  natural, genre-native writing. Use when the caller asks to humanize, de-AI,
  deslop, unslop, naturalize, simplify, clarify, or apply plain-language
  standards; asks for prose that reads as deliberately authored rather than
  model-shaped; requests a prose-pattern or rewrite-fidelity audit; or applies
  Animize as a standing style for the agent's own replies. Runs a quick process
  for routine communication, a deep process for bounded prose artifacts, and
  an audit job that reports findings without rewriting. Auto-route unless the
  caller sets the controls.
---

# Animize

## Objective

Produce prose that feels deliberately authored: it selects what matters,
grounds claims in particulars, takes a proportionate stance, and follows the
subject rather than a reusable template. When clarity applies, make the result
easy to understand on the first read without flattening necessary precision or
voice.

This skill improves prose quality and perceived naturalness. It does not prove
human authorship or guarantee that no observer will question it. Do not claim
provenance or detector evasion.

## Controls

Infer the controls unless the caller sets them:

| Control         | Default             | Meaning                                                                                                                                                               |
| --------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `job`           | `auto`              | Choose `write`, `rewrite`, or findings-only `audit` from the artifact boundary.                                                                                       |
| `process`       | `auto`              | Use `quick` for routine communication and `deep` for bounded artifacts. Ignored by `audit`.                                                                           |
| `clarity`       | `auto`              | Use `plain` for clear-communication constraints or `off` when they do not fit.                                                                                        |
| `voice_mode`    | `rebuild`           | Treat expression as editable. Use `preserve` for an explicitly protected source voice and `match_samples` for target samples.                                         |
| `rewrite_depth` | `recompose`         | In deep processing, use `light` for local repair, `standard` for damaged passages, or `recompose` for whole-piece redesign.                                           |
| `factual_mode`  | `preserve_and_flag` | Preserve unsupported claims and flag them. Use `verify_and_correct` only with authorized sources, or `publish_ready` when unsafe claims must be qualified or blocked. |
| `delivery`      | `adaptive`          | Return the artifact alone unless a material unresolved issue requires notes or withholding. Use `clean` or `with_notes` when requested.                               |

`process` controls how much machinery runs. `rewrite_depth` controls how much a
deep rewrite may change. They are not substitutes.

**The source's substance is authoritative; its expression is editable.**
Preserve facts, logic, qualifications, owned judgments, exact material, and
caller constraints. Treat wording, cadence, paragraphing, transitions,
headings, and order as editable unless the caller protects the voice or form.
Preserve every unique substantive item by default. Remove redundancy and empty
scaffolding; omit or compress unique substance only with scoped authorization
or when the requested form necessarily compresses it.

Voice controls expression, not content. A sample or first-person source can
justify cadence, diction, humor, roughness, or unusual structure. It never
licenses a new opinion, reaction, aside, self-correction, or degree of
conviction. A sample's punctuation does not override the dash rule.

## Precedence

Apply these tiers from strongest to weakest. A lower tier never changes what a
higher tier fixes.

1. **Explicit authorization.** A scoped caller instruction may authorize
   compression or omission of named content, correction from authorized
   sources, edits to named exact spans, dash use, or invention within a fiction
   or role brief. It never authorizes presenting invented real-world
   experience, credentials, sources, quotations, citations, or provenance as
   true, or claiming human authorship or detector evasion.
2. **Fidelity and integrity.** Preserve the source's substance, relationships,
   uncertainty, commitments, and owned evaluative force. Do not invent factual
   or personal substance.
3. **Protected exact spans.** Preserve quotations, code, commands, identifiers,
   paths, URLs, citations, titles, proper names, numbers, dates, units, formulas,
   defined terms, and legally or technically significant wording.
4. **Hard output and content-shaping rules.** Apply the dash, positive-scope,
   no-fake-imperfection, no-session-residue, and no-detector-optimization rules
   below.
5. **Caller form constraints.** Apply requested style guides, format, register,
   length, controls, and destination requirements.
6. **Destination and genre.** Follow the medium and the artifact's real genre,
   including its rules for judgment, terminology, voice, and structure.
7. **Authoredness and anti-tell repairs.** Repair a candidate only when it is a
   reader-facing defect rather than a defensible genre, logical, precision, or
   voice choice.
8. **Style preferences.** Prefer plain words, visible actors, sentence-case
   headings, direct syntax, and thought-shaped rhythm when stronger tiers do
   not decide the form.

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
- **Shape:** let structure and rhythm follow the thought and genre; vary sentence
  length on purpose and preserve useful asymmetry instead of regularizing every
  unit.

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
4. **Do not fake imperfection.** Do not add misspellings, typos, errors, or fake
   self-corrections as camouflage. Let real sentences do different jobs.
5. **Do not optimize against a detector.** Tells are reader-facing defects, not
   detector tokens. Repair their cause instead of substituting watched words or
   targeting punctuation, burstiness, perplexity, or a score.
6. **Ban generated em and en dashes.** Generated prose contains no `U+2014` or
   `U+2013` characters. Preserve them only inside a protected exact span or when
   the caller explicitly requests them. Samples and house style do not count as
   an override. Express the real relationship with a period, comma, list colon,
   or rebuilt clause; do not mechanically swap in parentheses, semicolons, or
   hyphens. A dash is never evidence of AI authorship.
7. **State scope positively.** Delete negative scaffolding, non-goal
   throat-clearing, and out-of-scope statements that change no reader decision.
   If a boundary matters and has a positive statement with identical truth
   conditions, use it. Otherwise preserve the negative form for prohibitions,
   exclusions, safety constraints, compatibility limits, or commitments. A
   required non-goals heading may remain, but its contents still pass this test.
   A true statement such as `This article does not cover deployment` is still
   scaffolding unless readers might reasonably rely on the article for
   deployment or the omission limits correct use. Classify deletion of that
   scaffolding as expression-level selection, not loss of substantive content.
8. **Keep judgment within its authority.** Reference prose contains facts,
   options, limits, and errors, not editorial opinion. How-to and tutorial prose
   may include task-required recommendations and warnings. Explanation, review,
   argument, and essay prose may include supported judgment. Any rewrite keeps
   source-owned stance at its supported strength and invents none.
9. **Respect genre.** Formality, passive voice, repetition, headings, technical
   terms, deliberate roughness, and unusual syntax may be necessary.

## Routing

Resolve `job` from the artifact boundary:

- use `rewrite` when supplied prose belongs in the requested artifact
- use `write` when the artifact comes from a brief and supplied samples,
  quotations, or background remain outside it
- use `audit` for diagnose, review-for-tells, or source-versus-revision fidelity
  requests that do not authorize a rewrite
- if the boundary remains uncertain, choose `rewrite` and preserve the supplied
  prose rather than silently treating possible source content as background

Resolve `process` separately:

- a standing Animize instruction or the agent's own conversational prose uses
  `quick`
- a named, reusable artifact such as an article, report, document, PR
  description, email body, or creative piece uses `deep`
- explicit `quick` or `deep` wins
- mixed output is segmented at the artifact boundary: the artifact uses `deep`,
  while surrounding explanation or status uses `quick`
- an incidental example inside a reply stays `quick`; a bounded deliverable the
  caller will reuse outside the conversation uses `deep`

Resolve `clarity` independently of process and voice. An explicit request or
project style guide decides first. Otherwise `auto` selects `plain` for the
agent's replies and for technical, instructional, reporting, reference,
how-to, and tutorial prose. It selects `off` for fiction, essays, marketing, and
personal prose unless the request or destination calls for plain language.
Under `preserve` or `match_samples`, protect supported voice traits, but still
repair ambiguity or hidden agency that changes what the reader can do or infer.

## Frame

Read the complete brief, source, and relevant task evidence. Record internally:

- reader, genre, destination, purpose, and desired response
- main point and required content or structure
- artifact boundary: which passages belong in the output and which are
  instructions, samples, quotations, code, data, or commentary about the work
- source boundary and authorized external sources
- protected exact spans
- requested style standards or registers
- selected controls

Infer reasonable defaults. Ask only when a missing answer makes accuracy
impossible or would materially change the result. Otherwise omit unsupported
optional material or flag it.

Complete framing when the reader, purpose, artifact and source boundaries,
controls, and job are known or safely inferred.

## Quick process

Quick is a cheap finish for routine communication, not a shallower fidelity
standard.

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
   - generated dash characters forbidden above
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

## Deep process

For `write` and `rewrite`, follow
[references/deep-recomposition.md](references/deep-recomposition.md). It adds a
content lock, sufficiency gate, new information hierarchy, structural draft,
authoredness test, skeptical-reader passes, independent fidelity verification,
continuous read, and full acceptance gate.

Complete deep processing only when that acceptance gate passes.

## Audit job

When `job` is `audit`, inspect without rewriting or editing any file:

- For a prose-pattern audit, consult
  [references/skeptic-patterns.md](references/skeptic-patterns.md) and
  [references/tells.md](references/tells.md).
- For a source-versus-revision fidelity audit, consult
  [references/verification.md](references/verification.md).
- For a clarity audit, consult
  [references/clear-communication.md](references/clear-communication.md) and
  report each material ambiguity, load problem, reader-address mismatch, or
  documentation-genre error with a proposed replacement or smallest repair.

For each finding, report the location, observable pattern or changed
relationship, reader effect or fidelity consequence, and smallest repair
direction. A fidelity finding includes paired source and revision spans when
both exist. Separate defects from uncertain flags. Include defended candidates
and the function they serve only when they help a requested comprehensive
audit.

Exclude protected exact spans from stylistic findings unless the caller targets
them. Report a dash only as conformance to this skill's output policy when the
audit brief names the policy or the caller identifies the text as produced
under Animize. Repeated dash-aside syntax may still be a pattern finding because
of its repetition, never because a character proves authorship.

Do not assign authorship, produce a shadow rewrite, or continue into a writing
process. Complete the audit when every finding is grounded in supplied text,
every requested dimension is checked, and the response contains findings only.

## Destination and delivery

| Destination               | Rule                                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| Conversational reply      | Return the answer without a change log or self-review.                                           |
| Artifact embedded in chat | Keep surrounding explanation separate and return clean artifact text.                            |
| File target               | Edit only bounded prose; preserve frontmatter, code, data, and link targets outside scope.       |
| Email, DM, or SMS         | Return sendable plain text without literal Markdown markers.                                     |
| Social post               | Follow the requested platform form without importing documentation structure or decorative tags. |
| Code-bearing prose        | Use real identifiers in code font and never reflow or restyle code.                              |
| Repository audit          | Report and rank candidates without editing files unless the caller selects them for repair.      |

With `delivery: adaptive`, return only the artifact when nothing requires
reporting. Append concise source notes or withhold an unsafe artifact when a
material issue remains. `clean` is valid only when no unresolved issue requires
a warning. `with_notes` may include material structural changes, unresolved
source issues, and requested defended choices. Never insert a source note,
fidelity warning, or explanation of removed prose into the artifact merely to
satisfy `clean`; report the control conflict outside the artifact or withhold
the unsafe result.

## Universal gate

Before delivery, confirm:

- no unauthorized substantive change or invented factual or personal material
- every protected exact span remains exact
- no brief, sample, placeholder, or drafting instruction leaked into the answer
- judgment and uncertainty match their source and genre authority
- no decision-irrelevant negative scope scaffolding remains; every retained
  prohibition, exclusion, or limit changes interpretation or action
- generated prose contains no forbidden dash character unless explicitly
  authorized
- output matches the requested destination and contains no workflow residue

## Reference loading

Quick uses only this entry point. Deep always loads
[deep-recomposition.md](references/deep-recomposition.md) and
[tells.md](references/tells.md), then loads other files only when their scope
matches the observed problem. Audit loads only the catalogs its requested
dimension needs, including `clear-communication.md` for a clarity audit. The
clarity profile also loads in deep processing when `clarity` resolves to
`plain`.

- [clear-communication.md](references/clear-communication.md): plain-language,
  documentation-genre, sentence-load, and ambiguity rules
- [authoredness.md](references/authoredness.md): positive properties, genre
  defaults, and voice behavior
- [skeptic-patterns.md](references/skeptic-patterns.md): cluster-based
  diagnostics
- [verification.md](references/verification.md): content-lock and fidelity
  checks
- [examples/recomposition.md](examples/recomposition.md): quick and deep
  examples
- [evaluation.md](references/evaluation.md): forward tests, benchmarks, and
  release criteria
- [third-party-notices.md](references/third-party-notices.md): conceptual
  lineage and licenses
