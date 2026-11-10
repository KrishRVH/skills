---
name: animize
description: >
  Write, revise, or assess lasting prose artifacts such as PR descriptions,
  comments, documents, and messages intended to be sent or published.
disable-model-invocation: true
---

# Animize

## Objective

Produce prose that feels deliberately authored: it selects what matters,
grounds claims in particulars, takes a proportionate stance, and follows the
subject rather than a reusable template. When clarity applies, make the result
easy to understand on the first read without flattening necessary precision or
voice.

This skill improves prose quality and perceived naturalness. It does not prove
human authorship or guarantee that no observer will question it. Register,
genre, and voice choices exist for readers. The one workflow that has a
provenance consequence is the Preserve regime, which keeps a human draft's own
words in the majority so the result is honestly describable as human-written
with AI assistance.

## Scope

Use Animize when the caller invokes it for a lasting piece of writing: a PR
description, review or issue comment, document, article, email, post, or other
text intended to be saved, sent, or published. Apply the procedure to that
artifact. Keep surrounding conversation in the agent's ordinary voice. If the
caller explicitly asks to apply Animize to a conversational reply, treat the
requested reply as the artifact.

## One unattended procedure

Animize runs unattended. The caller sets nothing and is asked nothing. One
invocation runs four steps on one artifact, in order:

1. [Route](#routing) the run to a regime.
2. [Frame](#frame) the artifact.
3. [Run the procedure](#procedure): load the routed branch's files, run every
   step of the branch, and pass the acceptance gate.
4. [Deliver](#destination-and-delivery) the artifact and any notes.

Three properties hold on every run:

- **Same steps at every length.** A three-sentence message runs every step a
  long report runs. Length changes how long a step takes, never which steps
  run.
- **Defaults, then notes.** Settle every open fact from the request, the
  text, and the session. When none of them settles it, take the default this
  entry point names, finish the work, and state the default in the notes.
  Two defaults are named: an unstated origin, under Routing, and an open
  framing question, under Frame. An ordinary inference about reader, format,
  register, or house style needs no note.
- **Plain instructions still govern.** A style guide, a length, a register,
  writing samples, or a request for a change summary is an ordinary
  instruction and takes its tier in [Precedence](#precedence). A run is
  complete without any of them.

## Routing

Route from the request, the text, and the session. Every case below has an
outcome, so routing completes without the caller.

### Regime

| What the run knows                                                                            | Regime    | What the regime does                                                                           |
| --------------------------------------------------------------------------------------------- | --------- | ---------------------------------------------------------------------------------------------- |
| The caller says the draft is their own writing, or asks to keep its wording                   | Preserve  | Repairs reader-facing defects inside the draft's own wording, under an edit policy and budget. |
| Anything else: a draft a model produced, a brief with no draft, or a draft of unstated origin | Recompose | Rebuilds the piece from its locked content.                                                    |

Only the caller's statement selects Preserve: `I wrote this`, `my own draft`,
`keep the wording`. A possessive such as `my PR description` names whose
artifact it is, not who wrote it. A draft's first-person content, roughness,
or particulars never select Preserve on their own. Under Preserve the run
takes the caller's word about authorship, does not verify it, and says so in
the notes.

When a draft's origin is unstated and the session does not show a model
producing it, Recompose still runs and the notes carry the origin note:

> Origin note: this draft's origin was not stated, so it was fully
> recomposed. If you wrote it, say so and the next run keeps your wording.

### Findings only

When the caller asks what is wrong, asks for a review or diagnosis, asks for a
source-versus-revision fidelity comparison, or forbids edits, run the
procedure as a diagnosis: apply every check to the text as it stands and
change nothing. Return the findings as notes, ranked by cost to the reader,
and withhold the artifact. Each finding carries its location, the observable
pattern or changed relationship, the reader effect or fidelity consequence,
and the smallest repair. For a cluster, that is one repair to the whole
passage. Name the pattern and its effect, never who or what wrote the text.
A framing question the material leaves open is a finding. The run changes
nothing, so it carries no origin note.

### Clear-communication profile

The profile in [clear-communication.md](references/clear-communication.md)
applies to technical, instructional, reporting, reference, how-to, and
tutorial prose, including workplace messages such as PR text, issue comments,
and status email. It stays inactive for fiction, essays, marketing, and
personal prose. A caller request or a project style guide decides first.
Marketing copy inside a technical destination, such as a README or product
documentation, gets the profile.
When following writing samples, protect supported voice traits, but still
repair ambiguity or hidden agency that changes what the reader can do or
infer. Preserve repairs clarity defects through its own edit policy and runs
without the profile.

Complete routing when the regime, the findings-only decision, and the profile
are each settled by a row or sentence above.

## Frame

Read the complete brief, the source, and the task evidence the artifact
reports on. Record internally:

- reader, genre, destination, purpose, and desired response
- main point and required content or structure
- artifact boundary: which passages belong in the output and which are
  instructions, samples, quotations, code, data, or commentary about the work
- source boundary: the source draft, the brief, the task evidence, and any
  external source the caller authorized
- protected exact spans
- requested style standards or registers
- writing samples, when the caller supplied any

Under Recompose, answer three questions before drafting:

1. What is the one thing the reader must leave with?
2. What does the caller actually think about it? When the caller states no
   view, what does the evidence support concluding?
3. What is one real particular (a number, an event, a name, a mechanism) the
   piece can stand on?

Answer them from the material inside the source boundary. When it leaves a
question open, take the default: write the narrowest piece the material
supports and name the open question in the notes. Never fill the gap with an
average of what such a piece usually says.

Complete framing when the reader, purpose, artifact and source boundaries,
and protected spans are each settled from the material or from a default.

## Procedure

Load the routed branch's files before its first step. The set is fixed for
every run of the branch:

| Branch                                 | Files                                                                                                             |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Preserve                               | `procedure.md`, `verification.md`                                                                                 |
| Recompose, and every findings-only run | `procedure.md`, `verification.md`, `tells.md`, `skeptic-patterns.md`, `authoredness.md`, `clear-communication.md` |

- [procedure.md](references/procedure.md): the steps of both branches and
  the acceptance gate
- [verification.md](references/verification.md): the content-lock schema and
  the fidelity checks
- [tells.md](references/tells.md): line-level reader-facing defects
- [skeptic-patterns.md](references/skeptic-patterns.md): cluster diagnostics
- [authoredness.md](references/authoredness.md): positive properties, genre
  defaults, and voice
- [clear-communication.md](references/clear-communication.md): the
  clear-communication profile

Preserve leaves the repair catalogs unloaded on purpose: its edit policy
repairs what a reader would notice in the draft, not what a catalog can find.
Loading a file does not activate it: the profile's rules apply only when
Routing selects the profile.

Then follow [procedure.md](references/procedure.md): every step of the routed
branch in order, then the acceptance gate. Verification is an internal step
of every run. It never becomes a separate output; its findings surface only
as notes.

Complete the procedure only when the acceptance gate passes.

## Destination and delivery

| Destination                  | Rule                                                                                                            |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Invoked conversational reply | Return the answer without a change log or self-review.                                                          |
| Artifact embedded in chat    | Return clean artifact text apart from any explanation. Fence it when it carries markup its destination renders. |
| File target                  | Edit only bounded prose; preserve frontmatter, code, data, and link targets outside scope.                      |
| Email, DM, or SMS            | Return sendable plain text without literal Markdown markers.                                                    |
| Social post                  | Follow the requested platform form without importing documentation structure or decorative tags.                |
| Code-bearing prose           | Use real identifiers in code font and never reflow or restyle code.                                             |
| Repository review            | Report and rank candidates without editing files unless the caller selects them for repair.                     |

A file of unstated origin is overwritten only when version control can
restore the original. Otherwise leave the file as it is, return the
recomposed text in the reply, and say so in the notes.

Return the artifact alone when nothing requires reporting. Notes follow the
artifact, never enter it, and are written in the agent's ordinary voice. Keep
each note that accompanies an artifact to the one or two sentences the caller
needs in order to act on it. A run returns notes when any of these applies:

- the origin note from Routing
- under Preserve: the notes
  [its last step](references/procedure.md#p4-verify-disclose-and-deliver)
  lists
- a framing question the material left open, or a thin source that narrowed
  the piece
- a source claim that is unsupported, contradictory, qualified, or withheld
- the caller asked what changed: material structural changes and defended
  choices

A caller who asks for the text alone gets it without the origin note or the
clause-diff summary. A warning about an unresolved source issue still follows
the artifact, and an unsafe artifact is withheld with the notes returned in
its place.

## Substance and expression

**The source's substance is authoritative; its expression is editable.**
Preserve facts, logic, qualifications, owned judgments, exact material, and
caller constraints. Treat wording, cadence, paragraphing, transitions,
headings, and order as editable unless the caller protects the voice or form
or the Preserve regime applies. Preserve every unique substantive item by
default. Remove redundancy and empty scaffolding; omit or compress unique
substance only with scoped authorization or when the requested form
necessarily compresses it.

Factual handling is preserve-and-flag. Correct a claim only from material
inside the source boundary. Qualify or withhold a claim that is unsafe to
publish.

Voice shapes expression, never content. Writing samples or a first-person
source can justify cadence, diction, humor, roughness, or unusual structure.
They never license a new opinion, reaction, aside, self-correction, or degree
of conviction.

## Precedence

Apply these tiers from strongest to weakest. A lower tier never changes what a
higher tier fixes.

1. **Explicit authorization.** A scoped caller instruction may authorize
   compression or omission of named content, correction from authorized
   sources, edits to named exact spans, or invention within a fiction or role
   brief. It never authorizes presenting invented real-world experience,
   credentials, sources, quotations, citations, or provenance as true, or
   claiming human authorship.
2. **Fidelity and integrity.** Preserve the source's substance, relationships,
   uncertainty, commitments, and owned evaluative force. Do not invent factual
   or personal substance.
3. **Protected exact spans.** Preserve quotations, code, commands,
   structured data, identifiers, paths, URLs, citations, titles, proper names,
   numbers, dates, units, formulas, defined terms, and legally or technically
   significant wording.
4. **Hard output and content-shaping rules.** Apply the
   no-manufactured-humanity, no-fake-imperfection, and positive-scope rules
   below. Keep brief and session residue out of the artifact. Apply the
   Preserve regime's edit policy when it applies.
5. **Caller form constraints.** Apply requested style guides, format, register,
   length, writing samples, and destination requirements.
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
   the text.

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
5. **State scope positively.** Delete negative scaffolding, non-goal
   throat-clearing, and out-of-scope statements that change no reader decision.
   If a boundary matters and has a positive statement with identical truth
   conditions, use it. Otherwise preserve the negative form for prohibitions,
   exclusions, safety constraints, compatibility limits, or commitments. A
   required non-goals heading may remain, but its contents still pass this test.
   A true statement such as `This article does not cover deployment` is still
   scaffolding unless readers might reasonably rely on the article for
   deployment or the omission limits correct use. Classify deletion of that
   scaffolding as expression-level selection, not loss of substantive content.
6. **Keep judgment within its authority.** Reference prose contains facts,
   options, limits, and errors, not editorial opinion. How-to and tutorial prose
   may include task-required recommendations and warnings. Explanation, review,
   argument, and essay prose may include supported judgment. Any rewrite keeps
   source-owned stance at its supported strength and invents none.
7. **Respect genre.** Formality, passive voice, repetition, headings, technical
   terms, deliberate roughness, and unusual syntax may be necessary.

## Files outside a run

A run loads none of these files. They serve maintainers and callers outside a
run:

- [examples/recomposition.md](examples/recomposition.md): Preserve and
  Recompose examples
- [examples/pairs.md](examples/pairs.md): paired before-and-after examples by
  genre
- [examples/prompt-block.md](examples/prompt-block.md): a compact rule block
  to paste into a writing prompt where the skill is not installed
- [backends.md](references/backends.md): optional model-stack note for callers
  who control their pipeline; outside the prose rules
- [evaluation.md](references/evaluation.md): forward tests, benchmarks, and
  release criteria
- [evaluation-results.md](references/evaluation-results.md): measured results
  with detector versions and dates
