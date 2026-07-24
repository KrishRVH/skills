---
name: animize
description: >
  Animize prose: strip generic AI patterns and restore a specific human pulse
  without inventing facts or replacing the writer's voice. Use when the caller
  asks to humanize, deslop, or de-AI text, says it sounds like AI or ChatGPT,
  or wants it less generic (edit); asks to scan, audit, check, or flag
  AI-pattern issues without a rewrite or an authorship verdict (audit); or
  wants a natural-sounding draft of a blog post, essay, professional post,
  newsletter, abstract, or report (write).
---

# Animize

An LLM predicts the statistically likely next token, so unedited model prose regresses to the mean: subjects become less specific and more exaggerated at once, and the same ceremonies repeat. Animize is the editing method that reverses this. It removes generic performance, evasion, and flattening, and restores what the material actually supports. It is not an authorship detector.

## The essence

Three verbs diagnose any weak passage, including patterns the catalog does not name.

| Weak prose | Strong prose | Cure |
|---|---|---|
| **Performs.** Announces importance, decorates facts, manufactures drama. | **States.** Gives the fact room to carry its own weight. | Remove the ceremony; keep the substance. |
| **Evades.** Hides the actor, source, uncertainty, or actual claim. | **Commits.** Names what the available material supports. | Clarify, source, qualify, or flag the claim. |
| **Flattens.** Repeats one cadence, structure, transition, or finish. | **Varies.** Follows the thought and the writer's habits. | Break the repetition that dulls the passage. |

State. Commit. Vary. These are editing directions, not quotas.

## Two laws

1. **Never invent, never silently change substance.** Every added or sharpened fact, name, number, date, quote, and citation must come from the source boundary: the supplied material, the caller's statements, and sources the caller authorized. Distinguish style from substance. Ceremony, decoration, and empty scaffolding are style; cut them freely. Propositions, evaluations, and contrasts are substance; preserve them, restate them plainly, or flag them, because a style cue never licenses deleting what the text claims. One register exception: in encyclopedic and reference prose, unsourced editorializing is itself the defect, and the genre licenses cutting it. Fiction may invent within the brief. A fabrication is a defect even when it sounds more human than the vague original.
2. **Fix the disease, not the symptom.** A watched phrase usually points at puffery, weak evidence, hidden agency, or monotony. Repair that underlying problem; cosmetic removal just launders the text. If no problem remains in context, keep the phrase.

**Precedence** when instructions compete: first factual fidelity and intended meaning, then the caller's request, constraints, and house style, then the writer's established voice and the genre's conventions, then this skill's heuristics. Two implications worth noticing: a caller who asks to de-AI their own draft has licensed removing its ceremony (the request outranks voice preservation for exactly the patterns they named), and nothing in this skill outranks what the text truthfully claims.

## Voice ownership

Record early whether the text has a voice worth preserving; this one judgment sets the editing posture everywhere below.

- **Owned:** an identified writer's prose, a supplied sample, a human draft the caller wants kept theirs. Posture: triage. Fix what harms the piece, retain what belongs to the writer, and match their habits, including their punctuation rate.
- **Unowned:** model-drafted text, ghost-written or boilerplate copy, a Write-job draft of your own, or text the caller disclaims. Posture: fix by default. Catalog patterns are defects here unless an entry's keep-when condition applies, and there is no author rate to protect.

When ownership is ambiguous and the difference would materially change the edit, ask; otherwise infer from context. "Make this sound less like ChatGPT" usually signals unowned text or, at minimum, a license to remove ceremony from owned text.

## Jobs

### Edit

The default when the caller supplies prose and permits a rewrite. Return the complete edited text followed by a three- to six-line `What changed` note covering material patterns, retained exceptions, and unresolved flags. When another workflow invokes this skill as an editing step, return only the edited text and propagate material unresolved concerns to that workflow.

For a file target, edit prose in place. Preserve code, frontmatter, structured data, quoted material, and link targets unless the caller includes them in scope, and report a concise summary instead of pasting the file back.

### Audit

For requests to scan, audit, check, or flag without rewriting. Report each material issue with the four-field shape in tells.md §8: excerpt, pattern, effect, repair. End with a cluster summary. Never assign an authorship label, model family, probability, or detector-evasion advice. If the caller asks who or what wrote the text, explain that prose cues alone cannot establish provenance, and point to process evidence: drafts, version history, source notes, timestamps, and a conversation with the writer. Offer to edit afterward.

### Write

For a new draft. Draft from the brief and authorized sources, then run the full Edit workflow on the draft before delivery. Return only the piece unless the caller asks for commentary.

## Workflow

1. **Frame.** Read the complete text or brief. Record an internal note: job, reader, register, purpose, core point, constraints, source boundary, voice ownership, and, for owned text, three to five voice signals worth preserving. For a sparse nonfiction brief, batch the blocking questions before drafting; omit optional unsupported details and track those gaps internally rather than as placeholders. Done when every field is known, reasonably inferred, or marked unresolved.
2. **Sweep.** Open [references/tells.md](references/tells.md) and check every section against the whole text. Give every plausible hit a disposition: **fix**, **retain**, or **flag**. Default by ownership: in unowned text, fix unless a listed keep-when condition applies; in owned text, fix what harms the piece and retain what belongs to the writer. Every retain gets a stated reason; every flag names what lies outside the source boundary. Record per-section hit counts in the internal note, including zeros; a section with no recorded count has not been swept. Audit job: record material hits in the §8 shape and go to step 6. Done when every catalog section has a recorded count against the full text and every hit has a disposition.
3. **Restore the pulse** (edit and write). Open [references/pulse.md](references/pulse.md) and apply the moves that fit the writer, reader, and genre, preferring local repairs to wholesale normalization. Done when the prose has a coherent voice, readable cadence, supported specificity, and an opening and ending doing their genre's jobs.
4. **Account for fidelity** (edit and write). Compare the revision with its source or brief and account for every changed fact, implication, evaluation, name, number, date, quote, citation, and link target. Restore any change the boundary does not entail. Where citation verification was out of scope, preserve the citation and flag the concern rather than substituting. Done when every substantive change is entailed by the boundary.
5. **Read and gate.** Read the final prose continuously, once, holding one question: what here would still read as machine ceremony or evasive mush? Then run the gate below. Repair failures without minting a new repeated mannerism; keep an exception only per the precedence order, with its reason recorded. Done when every gate line passes or carries its reason.
6. **Deliver** per the job contract, with material unresolved concerns in the required note or summary and no unintended placeholders anywhere.

## Editing rules

- **Make the minimum effective edit.** Keep strong sentences. Preserve humor, profanity, uncertainty, digressions, technical vocabulary, dialect, and roughness that belong to the writer.
- **Protected text is untouchable.** Never rewrite quotations, titles, proper names, code, cited wording, or examples that mention a watched phrase rather than use it.
- **Keep the intelligence.** Prefer plain wording without deleting necessary nuance, domain language, qualification, or logical structure. Plain is smart; dumbed-down is a different failure.
- **Never fabricate humanity.** No invented anecdotes, personal details, typos, errors, or persona. The rhythm moves in pulse.md remain available; the line runs between shaping real material and faking evidence of a person.
- **Avoid secondary convergence.** The fix for one mannerism must not become the next mannerism: not every transition replaced with the same word, not every ending clipped, not a length pattern imposed. Let form follow thought.
- **Let register govern personality.** Personal writing carries opinions and asides. Technical, legal, scientific, and reference prose may be neutral, repetitive, passive, or formally structured for good reasons; there, neutral is the correct human voice.

## Verification gate

Each line passes or carries a recorded reason.

- **Fidelity.** Every changed proposition is entailed by the source boundary; no invented specifics; quotes, citations, and link targets keep their meaning.
- **Purpose.** The output answers the request and fits reader, register, genre, and house style.
- **Voice.** Owned signals survive; no replacement house voice; no manufactured quirks.
- **Catalog.** Every section swept; every hit dispositioned; every retain has a reason; every flag is reported.
- **Clarity.** No unsupported importance, vague authority, empty scaffolding, chat or markup residue, or placeholders remain unreported.
- **Cadence.** The catalog's countable tripwires clear (§3 symmetry, §4 transitions, §5 dashes); the continuous read finds no accidental monotony and no repeated repair pattern.
- **Delivery.** The output matches the job contract with no process narration.

## Files

- [references/tells.md](references/tells.md): the review catalog for step 2, with dispositions, keep-when conditions, countable tripwires, sourced before/after pairs, and the audit reporting guardrail.
- [references/pulse.md](references/pulse.md): voice, rhythm, specificity, stance, openings, endings, and register for steps 3 through 5.
