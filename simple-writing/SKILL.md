---
name: simple-writing
description: Clear, direct user-facing prose using plain-language and developer-documentation standards.
disable-model-invocation: true
---

# Simple writing

Govern how the agent writes to the user: answers, explanations, walkthroughs,
status updates, summaries, and review reports delivered in conversation, plus
plain-language work the caller requests on supplied text. The goal is prose a
tired reader understands on the first read. Four questions get there, one per
layer below: what kind of response is this, how do sentences address the
reader, how much does each sentence carry, and can any sentence be read two
ways. Treat source-supported facts, quotations, and citations, necessary
precision, deliberate voice, and the caller's explicit constraints as
controlling contracts.

Standalone prose artifacts, such as PR descriptions, documentation, articles,
and creative writing, belong to the animize skill, which recomposes them
structurally and can apply these rules within it as sentence-level
constraints.

## Steps

1. **Establish the brief.** Identify the audience, purpose, format, tone, and
   style guide from the request or source text. Ask only when a missing choice
   would materially change the result.

   **Complete when:** Each factor is known, constrained by the source, or
   explicitly left to judgment.

2. **Follow the requested branch.**

   - Draft new prose with concrete subjects, active verbs, and enough detail to
     fulfill the brief.
   - Revise every relevant passage for clarity and concision while preserving
     its supported claims and intentional voice.
   - For a review, keep the source unchanged and report each material problem
     against the rules below with its location, reason, and a proposed
     replacement.

   **Complete when:** Every requested section or review concern has been
   handled.

3. **Apply the hard rules, Orwell's rules, and the four layers below.** Answer
   the layer questions in order: mode, reader address, sentence load,
   ambiguity.

   **Complete when:** Every sentence has passed each applicable rule and every
   exception serves a specific purpose.

4. **Run the checklist and deliver in the requested format.** Add notes only
   for material ambiguities, necessary exceptions, or requested explanations.

   **Complete when:** The result satisfies every controlling contract and is
   ready to use or act on.

## Hard rules

These three rules apply to every branch and mode.

1. **State scope positively.** Say what a system, document, or change does and
   who it serves. Remove "non-goals" sections, out-of-scope lists, and
   sentences about what something won't do, doesn't cover, or is not. Express
   a real limit as behavior the reader must plan for: "the client sends each
   request once" carries the boundary that "the client does not retry" states
   as an absence.
2. **No dead prose.** Every sentence changes what the reader knows or can do.
   Delete throat-clearing, placeholder phrases such as "please note" and "at
   this time", announcements of what a section will cover, restatements of
   what it just covered, and sentences kept only to fill out structure.
3. **The codebase is the word list.** Write the real symbol, file, flag, or
   command name in code font, never a synonym or a description of it. Use the
   words a developer would say out loud: "move", "delete", "a limit that only
   tightens", in place of invented metaphors such as "evacuate", "ratchet",
   or "endgame".

## Plain-English rules

Orwell's rules sit above the layers. Rules 2, 3, and 6 override every rule
below them: a sentence that follows every rule and still sounds
machine-written has failed.

1. Replace stale figures of speech with plain language or a fresh, specific
   image.
2. Choose a short, familiar word when it carries the same meaning. A long word
   has to buy its length with precision.
3. Cut every word that does no work. If the sentence survives without a word,
   the word goes.
4. Prefer active voice when the actor matters and is known.
5. Replace foreign phrases, jargon, and needless technical terms with everyday
   English when accuracy permits.
6. Break a rule when following it would make the prose crude, unclear, false,
   or tonally wrong. Fix the sentence another way or leave it alone.

## Pick the response mode

Two questions pick the mode: does the response inform action or understanding,
and is the user learning or working? Reach for these questions whenever a
response feels shapeless. Gut feel is often wrong here.

- **How-to** (action, working): steps to the user's goal. Assume competence,
  skip teaching, and link background instead of including it. Allow forks and
  judgment: "If you want x, do y."
- **Reference** (understanding, working): facts for lookup. Describe, only
  describe. State facts, options, limits, and errors dry, complete, and sure,
  with no instruction, persuasion, or opinion.
- **Explanation** (understanding, learning): why and how it works. Give design
  decisions, constraints, history, and alternatives. Opinion is allowed here
  and nowhere else, so weigh the trade-offs and say what you make of them.
- **Tutorial** (action, learning): teaching by doing, for a user new to a
  tool. Open with what they will build, make every step produce a visible
  result, and tell them what they should see: the expected output, the prompt
  change, the log line.

One response, one dominant mode. When a reply genuinely needs two, separate
them with structure and keep each part in its own mode.

## Reader address (Google developer style)

Use the [Google developer documentation style
guide](https://developers.google.com/style) as the default house style. A
caller or project style guide outranks it.

1. Address the reader as "you". Reserve "we" for the authoring organization.
2. Write in present tense about what the code does now. Keep the text
   timeless: describe shipped behavior, and drop time-relative words such as
   "currently", "soon", and "new". Use "will" only for things that genuinely
   happen later.
3. Sound like a knowledgeable friend: conversational and direct, with plain
   words in place of slang, wordplay, exclamation marks, and pop-culture
   references.
4. Write instructions as plain imperatives ("Click **View**"). Drop "please",
   "simply", "easily", "just", and "quickly". If it were simple, the reader
   would not be here.
5. Put the condition or goal before the instruction, so the reader can skip
   what does not apply: "To delete the file, click **Delete**."
6. Put the common case first and the exceptions after it.
7. Use sentence-case headings that carry the point, not just the topic: a
   task heading is a bare verb phrase ("Create an instance"), a concept
   heading is a noun phrase.
8. Use numbered lists for sequences and bulleted lists for other lists.
   Introduce a list with a complete sentence, keep items parallel, and say up
   front that a list is partial instead of ending it with "etc.".
9. Make link text describe its target.
10. Use code font for code, commands, filenames, and identifiers, bold for UI
    element names, serial commas, and unambiguous date formats such as
    "18 August 2026".
11. Write for a global audience: familiar words, culture-neutral examples,
    accessible structure, and alt text for images.
12. Avoid starting consecutive sentences with the same phrase. Read the
    awkward sentence aloud, and if it stays awkward, rewrite it.

## Sentence load (STE baseline)

Use STE by default for technical, instructional, and reporting prose:

1. Use short sentences. Put one main action or statement in each sentence.
   One thought per sentence does not mean one length per sentence: split the
   sentence that carries two thoughts, and keep the long sentence that
   carries one.
2. Split an instruction longer than about 20 words and any other sentence
   longer than about 25.
3. Use a clear subject and an active verb. Name the actor when the actor
   matters.
4. Use one term for one thing, one word per action, and one meaning per word.
   Repeat the term even when a synonym would sound less repetitive. Write
   "start" everywhere, never "start" here and "initiate" there. If "check"
   means inspect, it never also means restrain.
5. Use familiar words with precise meanings. Avoid idioms, slang, figurative
   language, and vague verbs.
6. Keep necessary technical terms. Define them or link to their definitions.
7. Keep noun groups short. Use prepositions to show relationships between
   terms.
8. Keep "the" and "a": "Remove backup file" reads two ways, "Remove the
   backup file" reads one.
9. Prefer plain verb forms over "-ing" words, which take too many grammatical
   jobs and breed misreadings.
10. Write procedures as direct instructions, and put the warning or condition
    before the step it guards. State the condition, action, and expected
    result.
11. State what the reader must do. Prefer positive instructions when they are
    clear.
12. Use consistent American English unless the caller's style guide requires
    another variety.
13. Preserve code, commands, identifiers, names, legal text, and required
    quotations exactly unless the caller authorizes changes.

Use an approved word with its approved meaning when the relevant STE
dictionary is available. Claim strict STE conformance only after checking the
requested issue of the standard and its dictionary. Mark each necessary domain
exception when strict STE is requested.

## One reading only (Global English)

Leave no sentence open to two readings:

1. Keep words like "only" and "not" next to the word they change: "only fails
   on growth" and "fails only on growth" say different things.
2. Break up long noun strings: "the proto import budget check script" becomes
   "the script that checks the proto-import budget".
3. Make every "it", "they", and "this" point at one obvious thing. Repeat the
   noun when in doubt, and keep "this" and "which" from pointing at a whole
   clause.
4. Give every clause its verb: "Phase 1 moves the converters and Phase 2 the
   runtime" leaves Phase 2 without one.
5. Keep the small words that show structure. "Ensure that the switch is off"
   keeps "that" because it makes the sentence parse one way. Clarity outranks
   word count.
6. Repeat the article in a series when it prevents a misread: "the client and
   the host" when they are two things.
7. Say which parts "and" or "or" joins when a sentence can group two ways.
   "Both...and", "either...or", and "if...then" are free disambiguators.
8. Use periods in place of semicolons, and a new sentence in place of an em
   dash.
9. Make text in parentheses a full grammatical unit or its own sentence, and
   form plurals without "(s)".
10. Write out alternatives in place of slashes: "a, b, or both", never "a/b"
    or "and/or".
11. Call each thing by one name, everywhere. A reply that says "the gate",
    "the ratchet", and "the budget check" for one thing teaches three things.
12. Skip idioms, colloquialisms, Latin abbreviations, and metaphors. A
    non-native reader, a translator, and an agent all parse plain
    constructions best.

## Vary the rhythm

The layers decide what a response says and how much each sentence carries. A
reply can obey all of them and still read machine-written: every sentence
clipped short, no view anywhere, nothing specific.

- Mix sentence lengths on purpose. Short sentences land a point. Longer ones
  that take their time carry a fact with its condition or consequence.
- Have a view where the mode allows it. Explanation weighs trade-offs, so say
  what you make of them. Reference stays dry.
- Be specific over sterile: "a column rename fails the build", never "schema
  changes can cause issues".

## Worked example

Before:

> The failing test issue has been investigated and it was determined that the
> flakiness was caused by timing-related factors. Updates have been made to
> the relevant files to address this, ensuring that the tests now pass
> reliably going forward.

After:

> `checkout.test.ts` was flaky because its mock clock never advanced past the
> 300 ms debounce window. I set the debounce to zero in `setup.ts:12`. All 34
> tests pass.

The fixes, by layer: "updates have been made" becomes "I set", so someone does
something (reader address). The real file and line replace "the relevant
files" (the codebase is the word list). "It was determined that" and "going
forward" go (no dead prose). The cause arrives before the fix, in its own
sentence (sentence load). "Timing-related factors" becomes the debounce window
and its number (specific over sterile).

## Checklist

Before delivering, check:

1. Is the response one mode, with any second mode separated by structure?
2. Is every instruction a command with its condition in front?
3. Does any sentence carry two thoughts? Split it.
4. Can any word be cut without losing meaning? Cut it.
5. Is "only" next to the word it changes? Does every "it" and "this" point at
   one thing? Does every clause keep its verb?
6. Does each thing have exactly one name throughout?
7. Would a developer say these words out loud, and are all symbols, paths,
   and numbers real in this repository?

## Sources

- [Diátaxis](https://diataxis.fr) for response modes
- [Google developer documentation style
  guide](https://developers.google.com/style) for reader address
- [ASD-STE100](https://asd-ste100.org) for sentence load
- Kohl, _The Global English Style Guide_ (SAS Press) for single-reading syntax
- Layer structure and several rules adapted from the `technical-writing` skill
  in [cursor/plugins](https://github.com/cursor/plugins) (MIT license), with
  changes: modes retargeted at conversational responses, and rules merged with
  Orwell's rules and this skill's hard rules
