---
name: animize
description: >
  Animize prose: strip AI tells, restore a human pulse. Use when the user wants
  text humanized, deslopped, de-AI'd, or made to sound less like ChatGPT (edit);
  wants writing audited or checked for AI patterns without rewriting (detect); or
  asks for a new draft that must read as human-written, such as a blog post,
  essay, LinkedIn post, newsletter, abstract, or report where authentic voice
  matters (write). Trigger on: humanize, deslop, slop, AI tells, "sounds like
  AI", "make it sound natural".
---

# Animize

An LLM predicts the statistically likely next token, so its prose regresses to the mean: the subject becomes less specific and more exaggerated at the same time. "Inventor of the first train-coupling device" fades into "a revolutionary titan of industry". The result is taxidermy: polished, lifelike, dead. The patterns that give it away are its tells. Animizing removes the tells and puts a pulse back in.

## The essence

Dead prose does three things. Living prose does the opposite. Every tell in the catalog is one of these three, so when you meet a pattern the catalog missed, ask which verb it fails and apply the cure.

| Dead prose... | Living prose... | Cure |
|---|---|---|
| **Performs.** Announces, inflates, decorates, symmetrizes: "marks a pivotal moment in the evolution of regional statistics." | **States.** "The institute was established in 1989." | State the fact plainly. Let the reader judge importance. |
| **Evades.** Hedges, blurs, hides actors and sources: "Experts argue the initiative faced challenges." | **Commits.** "The pilot lost $40k in Q2 and Ramos cancelled it." | Name the actor, the source, the number, the position. |
| **Flattens.** Same sentence length, same paragraph shape, same synonym rotation, a bow on every ending. | **Varies.** Long then short. A fragment. A paragraph that just stops. | Break the uniformity so a person shows through. |

State. Commit. Vary. That is the whole skill; everything below is execution.

## Two laws

1. **Never invent.** The output must not contain any fact, name, number, date, quote, or citation absent from the source text or the user. Swapping vague for specific is allowed only when the specific comes from them; if a sentence needs real-world detail to live, ask for it or write the plain version. A fabrication is a defect even when it sounds more human than the vague original. (Fiction is the exception: there, invented detail is the job.)
2. **Fix the disease, not the symptom.** A tell usually points at a deeper problem: an unsupported claim, an inflated fact, a vague authority, a missing source. Deleting the tell while keeping the problem just launders the text and makes the problem harder to spot. Cure the claim itself, or flag it to the user.

## Jobs

**Edit** (default whenever text is present). Rewrite it. Deliver the full edited text plus a short "What changed" note (3-6 lines, pattern-level, no line-by-line inventory). If you were invoked as one step of a larger task, deliver only the text. If the target is a file, edit the file in place: prose only, leave code blocks, frontmatter, data, and link targets untouched, and report a summary instead of pasting the rewrite back.

**Detect** (user asks to audit, scan, check, or flag, and wants no rewrite). For each hit: quote the line, name the pattern, give the fix in a few words. Then state whether the tells cluster (see Cluster judgment below). Never assert AI authorship as fact and never output a percentage score: humans write with these patterns too, and detectors, including you, have real error rates. Named patterns are evidence the user can verify; verdicts are guesses. Offer to edit afterward.

**Write** (user asks you to draft something new). Draft with the catalog in mind, then run the full Edit loop on your own draft before delivering. Deliver the piece and nothing else unless asked.

## Workflow

1. **Frame.** Read the entire text (or brief) first. Write an internal note: the job, the reader, the register, the core point, and 3-5 voice signals to preserve (vocabulary, cadence, bluntness, humor, hedges, digressions). If you cannot identify the core point, ask the user; that is the one clarifying question this skill permits. Done when the note exists.
2. **Sweep the tells.** Open `references/tells.md` and check every section of it against the full text, start to finish. Each entry pairs a pattern with its fix. Edit and write: fix every hit. Detect: log every hit and stop after this step. Done when no section of the catalog remains unchecked against any part of the text.
3. **Restore the pulse** (edit and write only). Open `references/pulse.md` and apply it: voice, rhythm, specificity, commitment, openings and endings, register. Done when its checks pass.
4. **Audit** (edit and write only). Interrogate your own draft with two questions and answer them explicitly before moving on: "What still makes this read as AI-generated?" and "Does the rewrite state any fact, name, number, date, quote, or citation absent from the source or the user?" Fix everything the answers surface. A fabrication is a defect even when it sounds more human than the vague original. Done when both answers are "nothing".
5. **Verify.** Run the gate below against the final text. Any failed row: fix it and run the gate again. A row may be knowingly kept only with a one-line reason (usually: it is the author's own voice, or it sits inside quoted material). Done when every row passes or carries its reason.
6. **Deliver** per the job's contract.

## Core rules

- **Minimum effective edit.** Preserve the writer's point and voice. Keep humor, profanity, digressions, strong opinions, and genuine hedges ("I think", "maybe", "perhaps" when the writer means them). Leave strong human sentences alone; after editing, the same person should sound back.
- **Quoted material is untouchable.** Never rewrite watched phrases inside quotations, titles, proper names, or examples where the phrase is being discussed rather than used.
- **Vary your fixes.** The fix for a cliche is never another cliche. If you replace every "Furthermore" with "Also", or end every paragraph with the same clipped cadence, you have created a new tell (secondary convergence). Rotate approaches; often the best transition is none.
- **Cluster judgment.** One tell in isolation is weak evidence and may be a clean human sentence; a single em dash or one "however" means nothing. Edit an isolated pattern only when the fix genuinely improves the sentence. When tells stack (em dash plus tricolon plus "vibrant tapestry" plus a Conclusion section), edit hard.
- **Keep the intelligence.** Simple wording, full substance. Plain is smart; dumbed-down is a different failure.
- **Human beats sanitized.** Do not over-correct into fake-casual ("fellow humans, am I right?" is worse than slop) and do not scrub every hedge, intensifier, or superlative: "very", "perhaps", "was the first" are human speech. The reader should never think about how the text was written at all.
- **Register decides personality.** Blogs, essays, and posts want a visible person. Encyclopedic, technical, legal, and scientific text wants neutral and plain; there, neutral IS the human voice, so inject no first person or opinion.

## Verification gate

| # | Check |
|---|---|
| 1 | Banned vocabulary (tells §1): zero instances remain |
| 2 | Puffery and importance inflation (testament, pivotal, vital role, nestled, vibrant, rich heritage): zero |
| 3 | Negative parallelisms (not X but Y, not just X, no X just Z): zero |
| 4 | Rule-of-three triads: none left without a deliberate reason |
| 5 | Trailing "-ing" analyses (highlighting, ensuring, reflecting, showcasing): zero |
| 6 | Throat-clearing, filler phrases, chat artifacts, placeholders: zero |
| 7 | Rhetorical question answered in the next breath, colon reveals: zero |
| 8 | Stacked short fragments or a quotable kicker manufacturing drama: none |
| 9 | Every attributed claim has a named source or is cut; nothing invented |
| 10 | Passive voice or false agency where the actor is known: zero |
| 11 | Formal transitions (Furthermore, Moreover, Additionally): two or fewer, never clustered |
| 12 | Em and en dashes: zero in short copy, at most two in long form, or the author's own rate |
| 13 | Bold-first bullets, decorative emoji, Title Case Headings: none, unless house style demands them |
| 14 | Vague declaratives replaced by their specific ("The implications are significant" names the implication) |
| 15 | Sentence lengths vary; no three consecutive sentences share length and shape |
| 16 | At least a third of paragraphs end without a bow; the piece ends on something concrete, no recap |
| 17 | Voice signals from step 1 survive; meaning and facts unchanged |
| 18 | Fixes varied; read the text aloud once and it sounds like a person |

## Files

- `references/tells.md`: the exhaustive tell catalog for step 2, with a table of contents, before/after pairs per pattern, replacement tables, and an era-drift table for detect. Words, phrases, sentences, composition, formatting, evidence, tone, detection guidance.
- `references/pulse.md`: the positive craft for step 3. Voice, rhythm, specificity, commitment, openings and endings, register table.
