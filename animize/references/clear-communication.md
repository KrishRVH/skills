# Clear communication

Use this profile to make prose understandable on the first read without
simplifying away precision. It governs document shape, reader address,
sentence load, and ambiguity.
[The entry point](../SKILL.md#clear-communication-profile) decides whether it
applies.

## Contents

- [Precedence and Orwell escape rule](#precedence-and-orwell-escape-rule)
- [Choose the documentation genre](#choose-the-documentation-genre)
- [Reader address](#reader-address)
- [Sentence load](#sentence-load)
- [One reading](#one-reading)
- [Code-bearing prose](#code-bearing-prose)
- [Dead prose](#dead-prose)
- [Strict STE claims](#strict-ste-claims)

## Precedence and Orwell escape rule

The profile's rules are house preferences. Every higher tier of the entry
point's [Precedence](../SKILL.md#precedence) outranks them: fidelity,
protected exact spans, caller constraints and style guides, sample-backed
voice traits, and destination and genre conventions.

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
8. Prefer a period to a semicolon.
9. Make parenthetical text a complete grammatical unit or its own sentence.
   Form plurals directly instead of using `(s)`.
10. Write alternatives out instead of using slashes. Use `a, b, or both`, not
    `a/b` or `and/or`.
11. Replace idioms, colloquialisms, Latin abbreviations, and metaphors when a
    non-native reader, translator, or agent could parse them more than one way.

Complete this review when every modifier, pronoun, clause, series,
parenthetical, and alternative has one clear attachment and meaning.

## Code-bearing prose

Treat the codebase as the word list:

- Use the real symbol, file, flag, command, setting, or process name in code
  font. Do not substitute a synonym for an exact identifier.
- Use the plain verbs a developer would say aloud, such as `move` and `delete`,
  instead of an invented metaphor.
- Describe shipped behavior as the current state. Keep change framing where
  [diff-anchored reference prose](tells.md#typography-and-formatting) retains
  it.
- Name the human or system actor when responsibility matters. Literal system
  actions and conventional agency remain valid; repair wording only when it
  hides task-relevant agency. See
  [false agency](tells.md#sentence-machinery).

Complete code-bearing review when every symbol, path, flag, command, number,
and described behavior is real, source-supported, consistently named, and
formatted for its destination.

## Dead prose

Make every sentence change what the reader knows or can do. Remove
throat-clearing, placeholders such as `please note` and `at this time`,
announcements of what a section will cover, restatements of what it just
covered, and sentences kept only to fill out a structure.

Apply the entry point's
[positive-scope rule](../SKILL.md#universal-rules) to limits and non-goals.
Preserve a qualification, warning, exception, or limit when it changes what
the reader must understand or plan for. The phrase catalogs are
[the line-level tells](tells.md#sentence-machinery) and
[session and format residue](skeptic-patterns.md#16-session-and-format-residue).

Complete the dead-prose review when every remaining sentence adds a fact,
instruction, relationship, qualification, consequence, or necessary
transition.

## Strict STE claims

This profile uses Simplified Technical English as a practical baseline, not a
certification claim. Use an approved word with its approved meaning when the
relevant STE dictionary is available. Claim strict STE conformance only after
checking the requested issue of the standard and its dictionary. When strict
STE is requested, identify every necessary domain exception.
