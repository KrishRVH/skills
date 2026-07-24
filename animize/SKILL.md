---
name: animize
description: >
  Edit or draft prose so it sounds specific, natural, and true to its writer.
  Use when the caller asks to humanize, deslop, de-AI, or make text sound less
  generic; asks for a prose-pattern audit without a rewrite or authorship
  verdict; or wants a natural-sounding blog post, essay, professional post,
  newsletter, abstract, or report.
---

# Animize

Animize removes generic performance, evasion, and flattening without replacing
the writer's voice with another house style. It is an editing method, not an
authorship detector.

## The essence

Use three verbs to diagnose a weak passage, including patterns the catalog does
not name.

| Weak prose                                                                  | Strong prose                                                     | Cure                                              |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------- |
| **Performs.** Announces importance, decorates facts, or manufactures drama. | **States.** Gives the fact enough room to carry its own weight.  | Remove the ceremony; keep the substance.          |
| **Evades.** Hides the actor, source, uncertainty, or actual claim.          | **Commits.** Names what the available material supports.         | Clarify, source, qualify, or flag the claim.      |
| **Flattens.** Repeats one cadence, structure, transition, or finish.        | **Varies.** Follows the thought and the writer's natural habits. | Break only the repetition that dulls the passage. |

State. Commit. Vary. These are editing directions, not quotas.

## Two laws

1. **Never invent or silently change substance.** Preserve factual and logical
   propositions. Ground every added or sharpened fact, name, number, date,
   quote, and citation in the supplied material, the caller's statements, or
   sources the caller asked or authorized the agent to consult. A style cue
   does not authorize deleting an asserted consequence, evaluation, or
   contrast. Delete or narrow one only when it is redundant, the authorized
   material shows it to be unsupported and the requested scope permits the
   correction, or the caller approves. Otherwise, flag it. Fiction may invent
   within the brief.
2. **Fix the disease, not the symptom.** A watched phrase may point to puffery,
   weak evidence, vague agency, or monotonous structure. Repair that underlying
   problem. If no problem remains in context, keep the phrase.

When instructions compete, use this order:

1. factual fidelity and intended meaning
2. the caller's request, constraints, and house style
3. the writer's established voice and the genre's conventions
4. the heuristics in this skill

## Choose the job

### Edit

Use this job by default when the caller supplies prose and permits a rewrite.
Return the complete edited text followed by a three- to six-line
`What changed` note covering material patterns, consequential retained
exceptions, and every unresolved flag. When another workflow invokes the skill as
an editing step, return only the edited text and propagate any material
unresolved concern to that workflow.

For a file target, edit prose in place. Preserve code, frontmatter, structured
data, quoted material, and link targets unless the caller includes them in
scope. Report a concise summary instead of pasting the file back. Put any
unresolved factual or citation concern that affects safe use in the
`What changed` note or file summary.

### Audit

Use this job when the caller asks to scan, detect, check, or flag patterns
without rewriting. For each material issue, report:

- a brief excerpt or location
- the observable pattern
- its effect on this reader and genre
- a concise repair direction

End with a cluster summary. Do not assign an authorship label, model family,
probability, or detector-evasion claim. If the caller asks who or what wrote the
text, explain that prose cues alone cannot establish provenance and suggest
process evidence such as drafts, version history, source notes, or direct
discussion with the writer.

### Write

Use this job when the caller requests a new draft. Draft from the supplied
brief and authorized sources, then run the Edit workflow before delivery.
Return only the piece unless the caller asks for commentary.

## Workflow

1. **Frame the work.** Read the complete text or brief. Record an internal note
   with the job, reader, register, purpose, core point, constraints, source
   boundary, and whether the material establishes a voice. When it does,
   record three to five voice signals worth preserving; otherwise, record the
   caller's voice constraints and the genre's defaults. For a sparse
   nonfiction brief, batch required questions before drafting when their
   answers are necessary for an accurate, useful result. Omit optional
   unsupported details and track those gaps only in the internal note; do not
   create placeholders for them. Complete this step when every field is known,
   reasonably inferred, or internally marked unresolved.
2. **Sweep and classify.** Open
   [references/tells.md](references/tells.md) and check each section against the
   whole text. Classify every plausible hit as **fix**, **retain**, or **flag**.
   Fix only when the pattern harms meaning, evidence, voice, rhythm, or fitness
   for the reader. Record why any material hit is retained. For every flag,
   name the fact, source, interpretation, or decision missing from the source
   boundary. For the Audit job, record material hits and continue to Step 6.
   Complete this step when every catalog section has been checked and every hit
   has a disposition.
3. **Restore the pulse.** For Edit and Write jobs, open
   [references/pulse.md](references/pulse.md). Apply only the moves that suit
   the writer, reader, and genre. Prefer local repairs to wholesale
   normalization. Complete this step when the prose has a coherent voice,
   readable cadence, source-backed specificity, and an opening and ending that
   do their genre-specific jobs.
4. **Audit fidelity.** Compare the revision with its source or brief. Account
   for every changed fact, implication, evaluation, contrast, name, number,
   date, quote, citation, and link target. Restore every unsupported change.
   Track gaps already present in the source separately; disclosing a gap does
   not make a new claim safe. When citation verification was not requested,
   preserve the citation and flag concerns instead of silently replacing it.
   Complete this step when every substantive change is entailed by authorized
   material.
5. **Read and verify.** Read the final prose continuously, not as isolated
   sentences, and run the gate below. Repair failures without creating a new
   repeated mannerism. Complete this step when every gate item passes or a
   deliberate exception follows the precedence order.
6. **Deliver.** Follow the selected job's output contract. For Edit, report
   material unresolved concerns in the required note or summary. For Write,
   append uncertainty or open questions only when the caller requested
   commentary; ask blocking questions before drafting and omit optional
   unsupported details. Complete this step when the requested artifact and any
   required note are present, with no unintended placeholder sections.

## Editing rules

- **Make the minimum effective edit.** Keep strong sentences. Preserve humor,
  profanity, uncertainty, digressions, technical vocabulary, dialect, and
  roughness when they belong to the writer.
- **Preserve protected text.** Do not rewrite quotations, titles, proper names,
  code, cited wording, or examples that mention a watched phrase merely because
  the phrase appears.
- **Judge in context.** A single transition, dash, passive construction,
  triad, hedge, or formal word can be exactly right. Repetition plus a real
  reader-facing defect warrants intervention.
- **Preserve evaluative force.** In owned opinion, words that set the strength,
  direction, or certainty of a judgment are substance. Keep that force unless
  the caller authorizes a substantive change; a plainer restatement must not
  weaken or strengthen it. In unowned or formal prose, test evaluative praise
  against the source boundary: correct and report it when the scope permits,
  otherwise preserve and flag it. Unsupported promotional praise is not voice
  evidence.
- **Keep the intelligence.** Prefer plain wording without deleting necessary
  nuance, domain language, qualifications, or logical structure.
- **Do not manufacture humanity.** Never add typos, slang, fragments,
  anecdotes, personal details, or random variation to imitate a person.
- **Avoid secondary convergence.** Do not replace every transition with the
  same word, clip every ending, or force a sentence-length pattern. Let form
  follow thought.
- **Let register govern personality.** Personal writing can carry opinions and
  asides. Technical, legal, scientific, and reference prose may be neutral,
  repetitive, passive, or formally structured for good reasons.

## Verification gate

- **Fidelity:** Every changed proposition is entailed by the source boundary;
  unsupported claims already present in the source are preserved and flagged
  unless authorized evidence and the requested scope permit a supported
  correction. A materially unsafe or misleading unsupported claim cannot pass
  through a detached note alone: obtain caller direction, add an authorized
  in-artifact qualification, or withhold the artifact as not ready.
  Quotations, citations, and link targets retain their intended meaning.
- **Purpose:** The result answers the caller's request and fits its reader,
  register, genre, constraints, and house style.
- **Voice:** The recorded voice signals survive; no generic replacement voice
  or manufactured quirk has been introduced.
- **Catalog:** Every section was reviewed, and each plausible hit was fixed,
  retained for a reason, or flagged with the missing input identified.
- **Clarity:** Unsupported importance, vague authority, empty scaffolding,
  chat residue, leaked internal markup, and unresolved placeholders are gone
  or explicitly reported.
- **Cadence:** A continuous read reveals no distracting monotony, repeated
  repair pattern, or forced variation.
- **Delivery:** The output matches the selected job and omits irrelevant
  process narration.

## Files

- [references/tells.md](references/tells.md) is the review catalog for the
  sweep and the reporting guardrail for Audit jobs.
- [references/pulse.md](references/pulse.md) covers voice, rhythm, specificity,
  stance, openings, endings, and register for Edit and Write jobs.
