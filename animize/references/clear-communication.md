# Clear communication

Use this profile to make prose understandable on the first read without
simplifying away precision. It governs document shape, reader address,
sentence load, and ambiguity inside Animize. It does not select `job`,
`process`, or `voice_mode`.

## Contents

- [When the profile applies](#when-the-profile-applies)
- [Precedence and Orwell escape rule](#precedence-and-orwell-escape-rule)
- [Establish the brief](#establish-the-brief)
- [Choose the documentation genre](#choose-the-documentation-genre)
- [Reader address](#reader-address)
- [Sentence load](#sentence-load)
- [One reading](#one-reading)
- [Code-bearing prose](#code-bearing-prose)
- [Dead prose](#dead-prose)
- [Strict STE claims](#strict-ste-claims)
- [Completion check](#completion-check)
- [Sources](#sources)

## When the profile applies

Treat `clarity` as independent of `process` and `voice_mode`:

- `plain` applies this profile.
- `off` leaves its preferences inactive. Animize's fidelity and integrity
  rules still apply.
- `auto` resolves from the caller's request first, then a caller or project
  style guide, then the destination and genre.

Under `auto`, apply the profile to agent replies and to technical,
instructional, reporting, reference, how-to, and tutorial prose. Leave it off
for essays, fiction, marketing, and personal prose unless the caller or a
controlling style guide requests plain language.

Use the same profile under `quick` and `deep`; the process changes the amount
of work, not the clarity standard. For a clarity audit, inspect and report
without rewriting.

Complete routing when `clarity` is resolved and the applicable destination and
genre are known or can be inferred safely.

## Precedence and Orwell escape rule

Apply clarity rules in this order:

1. Preserve substance and every protected exact span. Use
   [verification](verification.md) for fact-bearing rewrites.
2. Follow the caller's explicit constraints and the caller or project style
   guide.
3. Under `preserve` or `match_samples`, retain evidence-backed voice traits.
4. Apply destination and genre conventions.
5. Apply this profile's house preferences.

Voice does not protect a sentence with two plausible readings or wording that
hides task-relevant agency. Treat either as a material clarity defect and
repair it without regularizing unrelated voice.

Use these plain-English priorities throughout the profile. Rules 2, 3, and 6
outrank the preferences that follow:

1. Replace a stale figure of speech with plain language or a fresh, specific
   image supported by the source and genre.
2. Choose the short, familiar word when it carries the same meaning. A longer
   word must add precision.
3. Cut every word that does no work.
4. Prefer active voice when the actor matters and is known.
5. Replace foreign phrases, jargon, and needless technical terms with everyday
   English when accuracy permits.
6. Break a lower rule when following it would make the prose crude, unclear,
   false, or tonally wrong. Repair the sentence another way or leave it alone.

Complete precedence review when every exception follows a controlling
contract or prevents a concrete loss of clarity, fidelity, precision, or fit.

## Establish the brief

Identify the audience, purpose, format, tone, destination, and controlling
style guide from the request or source. Ask only when a missing choice would
materially change the result.

- For new prose, use concrete subjects, active verbs, and enough supported
  detail to fulfill the brief.
- For a rewrite, improve clarity and concision while preserving supported
  claims, exact material, and intentional voice.
- For a clarity review or audit, keep the source unchanged. Report each
  material problem with its location, reason, and a proposed replacement or
  smallest repair direction.

Complete the brief when every factor is known, constrained by the source, or
explicitly left to judgment, and every requested section or review concern is
accounted for.

## Choose the documentation genre

Use two questions when documentation feels shapeless: does the reader need
action or understanding, and are they learning or working?

| Genre           | Reader need                  | Shape                                                                                                                                                                                      | Opinion policy                                                                         |
| --------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| **How-to**      | Action while working         | Give steps to the goal. Assume competence, link background instead of teaching it, and allow useful forks such as `If you want X, do Y`.                                                   | Include only task-required recommendations and warnings.                               |
| **Reference**   | Understanding while working  | State facts, options, limits, and errors for lookup. Describe rather than instruct or persuade. Keep it dry, complete, and certain only to the degree the evidence permits.                | Add no authorial opinion or persuasion. Report attributed views without adopting them. |
| **Explanation** | Understanding while learning | Explain how and why through decisions, constraints, history, relationships, and alternatives.                                                                                              | State supported judgment, weigh trade-offs, and calibrate uncertainty.                 |
| **Tutorial**    | Action while learning        | Teach by doing. Open with what the reader will build, make each step produce a visible result, and state what they should observe, such as an expected output, prompt change, or log line. | Include only task-required recommendations and warnings.                               |

Give one response one dominant documentation genre. When two are genuinely
needed, separate them with structure and keep each section faithful to its own
job.

Reviews and arguments may state supported judgment. Any rewrite preserves the
source's owned stance and its force, regardless of genre, but invents no
opinion, reaction, or degree of conviction.

Complete genre selection when the response's dominant job, structure, and
opinion policy agree.

## Reader address

Follow a caller or project style guide first. Otherwise use these developer
documentation defaults:

1. Address the reader as "you". Reserve "we" for the authoring organization.
2. Describe current behavior in the present tense. Keep prose timeless by
   dropping words such as `currently`, `soon`, and `new`; use `will` only for
   events that genuinely happen later.
3. Sound like a knowledgeable friend: conversational and direct, with plain
   words instead of slang, wordplay, exclamation marks, or pop-culture
   references.
4. Write instructions as plain imperatives, such as "Click **View**." Remove
   politeness and ease claims such as `please`, `simply`, `easily`, `just`, and
   `quickly`.
5. Put the condition or goal before the instruction so an unaffected reader
   can skip it: `To delete the file, click **Delete**.`
6. Put the common case first and exceptions after it.
7. Use sentence-case headings that carry the point. Use a bare verb phrase for
   a task heading and a noun phrase for a concept heading.
8. Use numbered lists for sequences and bulleted lists for other collections.
   Introduce every list with a complete sentence, keep its items parallel, and
   label a partial list before it starts instead of ending it with `etc.`
9. Make link text describe the linked destination.
10. Put code, commands, filenames, and identifiers in code font. Use bold for
    user-interface elements, serial commas in lists, and unambiguous dates such
    as 18 August 2026.
11. Write for a global audience with familiar words, culture-neutral examples,
    accessible structure, and alt text for every informative image.
12. Avoid consecutive sentences with the same opening unless repetition does
    useful rhetorical work. Read an awkward sentence aloud and rewrite it if
    it remains awkward.

For cadence beyond consecutive openings, use
[rhythm that follows thought](authoredness.md#6-rhythm-that-follows-thought).

Complete reader-address review when instructions, headings, lists, links,
dates, formatting, and accessibility all fit the reader and destination.

## Sentence load

Use Simplified Technical English principles as a baseline for technical,
instructional, and reporting prose:

1. Give each sentence one main action, statement, or relationship bundle. A
   longer sentence may keep a cause, condition, sequence, or qualification
   together when splitting it would hide the relationship. Split independent
   jobs.
2. Use a clear subject and an active verb. Name the actor when the actor
   matters or responsibility would otherwise be hidden.
3. Use one term for one thing, one word for one action, and one meaning for one
   word. Repeat the exact term instead of cycling synonyms.
4. Use familiar words with precise meanings. Replace idioms, slang, figurative
   language, and vague verbs when accuracy permits.
5. Keep necessary technical terms. Define them or link to their definitions.
6. Keep noun groups short. Use prepositions to show relationships among terms.
7. Keep articles such as `the` and `a` when they determine which item the
   sentence means.
8. Prefer plain verb forms over `-ing` forms when the latter obscures the
   action or grammatical role.
9. Write procedures as direct instructions. Put a warning or condition before
   the step it governs, and state the condition, action, and expected result.
10. State what the reader must do. Prefer positive instructions when they are
    clear.
11. For new prose, use consistent American English unless a controlling style
    guide selects another variety. In supplied prose, preserve the established
    spelling variety unless the caller authorizes normalization.
12. Preserve code, commands, identifiers, names, legal text, quotations, and
    other protected exact material unless the caller authorizes a change.

Complete the load review when each sentence carries one recoverable logical
job, and reducing its load further would separate relationships the reader
needs together or lose precision.

## One reading

Leave each sentence open to one supported interpretation:

1. Keep modifiers such as `only` and `not` next to what they modify. `Only
fails on growth` and `fails only on growth` make different claims.
2. Break up long noun strings. Replace `the proto import budget check script`
   with `the script that checks the proto-import budget` when that is the
   intended relationship.
3. Give every `it`, `they`, `this`, and `which` one obvious antecedent. Repeat
   the noun when a pronoun could point to two things or to a whole clause.
4. Give every clause its verb. Write `Phase 1 moves the converters, and Phase 2
moves the runtime`, not a construction that leaves the second action
   implicit.
5. Keep small structural words when they prevent a misread. Retain `that` in
   `Ensure that the switch is off` when it makes the sentence parse once.
6. Repeat an article in a series when it distinguishes two things, as in `the
client and the host`.
7. Make the grouping of `and` and `or` explicit. Use constructions such as
   `both ... and`, `either ... or`, and `if ... then` when they remove doubt.
8. Prefer a period to a semicolon. Apply Animize's universal dash rule even
   when a sample or house style uses dashes; only a protected exact span or an
   explicit caller override permits one. Rebuild the relationship instead of
   swapping punctuation mechanically. See
   [typography and formatting](tells.md#typography-and-formatting).
9. Make parenthetical text a complete grammatical unit or its own sentence.
   Form plurals directly instead of using `(s)`.
10. Write alternatives out instead of using slashes. Use `a, b, or both`, not
    `a/b` or `and/or`.
11. Call each thing by one name throughout the passage.
12. Replace idioms, colloquialisms, Latin abbreviations, and metaphors when a
    non-native reader, translator, or agent could parse them more than one way.

Complete this review when every modifier, pronoun, clause, series,
parenthetical, and alternative has one clear attachment and meaning.

## Code-bearing prose

Treat the codebase as the word list:

- Use the real symbol, file, flag, command, setting, or process name in code
  font. Do not substitute a synonym for an exact identifier.
- Use the plain verbs a developer would say aloud, such as `move` and `delete`,
  instead of an invented metaphor.
- Describe shipped behavior as the current state. Keep change framing for
  changelogs, release notes, migrations, postmortems, and other version-scoped
  destinations. See
  [diff-anchored reference prose](tells.md#typography-and-formatting).
- Name the human or system actor when responsibility matters. Literal system
  actions and conventional agency remain valid; repair wording only when it
  hides task-relevant agency. See
  [false agency](tells.md#sentence-machinery).
- Preserve code blocks, structured data, frontmatter, formulas, link targets,
  and exact technical text outside the authorized prose scope.

Complete code-bearing review when every symbol, path, flag, command, number,
and described behavior is real, source-supported, consistently named, and
formatted for its destination.

## Dead prose

Make every sentence change what the reader knows or can do. Remove
throat-clearing, placeholders such as `please note` and `at this time`,
announcements of what a section will cover, restatements of what it just
covered, and sentences kept only to fill out a structure.

Apply [Animize's universal positive-scope rule](../SKILL.md) to limits and
non-goals. Preserve a qualification, warning, exception, or limit when it
changes what the reader must understand or plan for. Use the canonical
[line-level tells](tells.md#sentence-machinery) and
[session-residue rules](tells.md#session-residue) instead of building another
phrase blacklist here.

Complete the dead-prose review when every remaining sentence adds a fact,
instruction, relationship, qualification, consequence, or necessary
transition.

## Strict STE claims

This profile uses Simplified Technical English as a practical baseline, not a
certification claim. Use an approved word with its approved meaning when the
relevant STE dictionary is available. Claim strict STE conformance only after
checking the requested issue of the standard and its dictionary. When strict
STE is requested, identify every necessary domain exception.

## Completion check

Deliver only when all applicable checks pass:

- A reader can understand the prose on the first read.
- Every sentence has one supported reading.
- Every sentence carries one main action, statement, or relationship bundle.
- The structure, address, opinion, spelling, and formatting fit the genre and
  destination.
- Instructions state the condition, action, and expected result where each is
  relevant.
- Code-bearing prose uses real, protected names and values.
- No clarity edit loses precision, qualification, stance, or protected exact
  material.
- Every retained exception follows the precedence and escape rule.

## Sources

- [Diataxis](https://diataxis.fr/) for documentation genres
- [Developer documentation style guide](https://developers.google.com/style)
  for reader address
- [ASD-STE100](https://asd-ste100.org/) for the sentence-load baseline
- John R. Kohl, _The Global English Style Guide_, for single-reading syntax
- The MIT-licensed
  [`technical-writing` skill](https://github.com/cursor/plugins/blob/46125561306434d8a1d7745d540d8932ab0cd2a2/pstack/skills/technical-writing/SKILL.md),
  adapted here with Animize's fidelity, voice, and genre precedence
