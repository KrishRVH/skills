# Line-level tells

Constructions that readers recognize as machine defaults. Unlike the
skeptical-reader clusters, these can usually be judged and repaired locally.
For each candidate, choose `fix`, `retain`, or `flag`: one conspicuous formula
may justify a fix, while an ordinary word or punctuation mark usually matters
only in context. Never fix a tell by introducing another, and never let the
sweep flatten the piece into a second house style. See
[Overcorrection guard](#overcorrection-guard).

## Contents

- [Vocabulary](#vocabulary)
- [Sentence machinery](#sentence-machinery)
- [Plain speech](#plain-speech)
- [Typography and formatting](#typography-and-formatting)
- [Overcorrection guard](#overcorrection-guard)

## Vocabulary

**AI-default vocabulary.** Delve, fostering, garner, interplay, intricate,
landscape (abstract), pivotal, showcase, tapestry (abstract), testament,
underscore, vibrant. Replace a conspicuous default with the plain word or
specific claim the sentence needs. Treat ordinary connective and evaluative
words such as `additionally`, `crucial`, `enhance`, `important`, `key`,
`notably`, and `valuable` as density signals, not isolated defects.

**Fancy ways to say "is" or "has".** `serves as`, `stands as`, `boasts`,
`features`, `represents` (when it means "is"). Say "is" or "has".

**Inflated synonyms.** `utilize` → use, `leverage` → use, `facilitate` → help,
`numerous` → many, `in the event that` → if, `prior to` → before. The fancier
synonym is rarely clearer.

**Abstract metaphors.** Substrate, wedge, vector, locus, nexus, primitive
(as noun), harness (as metaphor), bedrock, scaffolding (as metaphor), modality,
paradigm, ratchet (as metaphor), endgame, north star, flywheel, load-bearing
(outside engineering). These read as technical but usually hide a plainer
concrete word: "substrate" → base, "wedge in" → add, "vector" → way, "ratchet"
→ the mechanism's real name or "a limit that only tightens", "the load-bearing
assumption" → the assumption everything else depends on. Retain only when the
term is the field's exact word.

**Coined analytical labels.** A domain noun joined to `paradox`, `trap`,
`divide`, `creep`, `vacuum`, `inversion`, or another abstract problem noun can
name a pattern without explaining it. Define the mechanism and use the label
only if it remains useful after the explanation. Preserve established field
terms and caller-defined concepts.

**Promotional adjectives.** Nestled, vibrant, breathtaking, groundbreaking,
renowned, stunning, seamless, robust, must-visit. Use neutral description or
the supported comparison.

## Sentence machinery

**Staged contrast.** `Not just X, but Y`; `X rather than Y`; `Rather than X,
Y`; `It is not X. It is Y.` across two sentences; `should not be confused
with`. Each raises a position nobody held so that the point can arrive as a
correction. State the point alone: "the outage was a process failure rather
than a technical one" → "the outage was a process failure". Retain the
contrast when the rejected side is real: the source or the reader holds it,
it is the earlier state of the work, it is an alternative someone weighed,
or it is the mistake an instruction exists to prevent ("the key is per
user, not per session").

**"The real X."** `The real problem`, `the real question`, `the real work`,
`the real win`, `the real story`. The phrase promises a truth hidden behind a
decoy the text never showed, which stages an ordinary point as a revelation.
State the claim with the thing as its subject: "the real bottleneck is review
time" → "review time is the bottleneck". Swapping in `true`, `actual`, or
`underlying` keeps the defect. Retain `real` when the text has shown the
apparent version it corrects ("the listed price is $40; the real price with
fees is $57"), when it separates the thing from a stand-in ("real traffic,
not the load test"), and in fixed terms such as `real number` and `real
time`.

**Clipped negations.** Tails such as `no guessing`, `no friction`, and `no
wasted motion` often gesture at a benefit without stating the actor, mechanism,
or condition. Write the supported clause or delete the tail. Retain concise
negation when its meaning is exact.

**Rule of three.** Ideas forced into groups of three. Use the natural number.

**False ranges.** "From X to Y" where X and Y are not on a meaningful scale.
List the items directly.

**Superficial -ing tails.** Trailing participles that append unearned
significance: "…, highlighting the need for…", "…, ensuring reliability",
"…, showcasing its flexibility". Delete the tail or expand it into a supported
claim with its own sentence.

**Synonym cycling.** Protagonist, main character, central figure, hero within
one passage. Pick the clearest term and repeat it.

**Filler.** "It is important to note that" → delete. "Due to the fact that"
→ because. Leave a single `in order to`, `the fact that`, `as a result of`,
or `there is … that` as it stands: each is ordinary English that people
write more often than models do. Tighten only a passage that stacks them.

**Empty significance adverbs.** `Significantly`, `meaningfully`, `dramatically`,
`fundamentally`, `unusually`, and similar adverbs are defects when they supply
importance without a supported measure, mechanism, comparison, or consequence.
Remove the empty verdict or state the supported fact.

**Factual adverbs.** Preserve adverbs that carry manner, degree, frequency, or
scope and therefore change the proposition: `writes atomically`, `is nearly
full`, `usually retries once`, and `only validates signed tokens`. Do not delete
an adverb merely because of its part of speech. Replace a vague degree only when
the source supports a more exact measure.

**Unmotivated passive.** "Is/are/was/were + past participle" with a knowable
actor: "queries are validated" → "the compiler validates queries". Passive is
fine when the actor is unknown, irrelevant, or the genre's convention.

**False agency.** An abstraction performs a deliberate human act: `the data
tells us`, `the decision emerges`, `the market rewards`, `the complaint becomes
a fix`. Name who interpreted, decided, paid, or fixed when the wording hides
responsibility. Keep conventional metonymy when responsibility remains clear,
along with literal system and mechanical actions: a report can argue, a compiler
can reject code, and a valve can stop flow.

**Unsupported verdict fragments.** A sentence or paragraph adds only `This
matters`, `That instinct backfires`, `The result? Devastating`, or another
demonstrative judgment. Name the consequence or remove the verdict. Retain a
short beat when the surrounding evidence earns it and the voice uses it
deliberately.

**Stacked declaratives.** A run of short statements hides cause, contrast,
condition, or qualification behind dramatic cadence. Join the thoughts with
the plain conjunction that carries their real relationship: `because`, `so`,
`but`, `if`, or `although`. A deliberate sequence of beats is fine when the
order or emphasis does useful work.

## Plain speech

**Say what it does, not how it feels.** "SQL you can read", "the database
stays close at hand", "types that follow your schema" name a feeling. Name the
mechanism or the number instead: "`.toSQL()` returns the exact string sent to
the database", "a column rename fails the build". If a sentence cannot be
restated as a concrete instruction, fact, or number, cut it. This is the
sentence-level form of the anywhere test: a line that could appear unchanged in
another project's docs says nothing about this one.

**First-pass syntax.** A sentence may carry several ideas when their
relationship is clear. If the reader must backtrack to recover that
relationship, split the sentence or remove nonessential clauses.

**Spelled-out contractions.** A message, email, comment, PR description, or
post that writes out every `do not`, `it is`, and `we will` reads stiffer
than a person writing in that register. Contract where a speaker would.
Keep the full form where it carries stress or states a rule ("do not run
this in production", `must not`), in legal, academic, and formal reference
prose, and wherever supplied samples or the destination's existing text
write it out. A mix is normal: convert only what reads stiff.

**Compressed speech.** A message, email, or comment trimmed past how its
writer would say it aloud: a cause carried by a colon, a participle, or
`due to` where a speaker says `because`; "three risks remain" where a
speaker says "there are still three risks"; a dropped article, `that`, or
verb. Write the sentence at speaking length, small words included. Keep the
tight form in reference prose, headings, lists, commit subjects, and any
register that is terse on purpose, and add no word that carries nothing a
speaker would say.

## Typography and formatting

**Dash characters.** `U+2013` or `U+2014` in generated prose. Apply the
entry point's tier 8 default, including what outranks it. When unprotected
source prose uses either character structurally, rebuild the sentence so its
syntax carries the relationship.

**Colon as mid-sentence connector.** Colons belong before a list, example, or
quotation, not as glue between clauses that could stand as their own sentences.

**Boldface overuse.** Do not bold every proper noun, acronym, or key term.

**Inline-header lists.** The tell is a bold label plus colon that restates its
own line: "**Performance:** performance improved…". Convert to prose. A bold
lead-in that ends in a period, names the item, and is followed by genuinely new
detail is fine.

**Title case headings.** Use sentence case unless the destination's style guide
says otherwise.

**Decorative emojis.** Remove from headings and bullets.

**Diff-anchored reference prose.** `Was added`, `now uses`, `has been updated`,
and `replaces the old` narrate an edit instead of explaining current behavior.
Describe the steady state in reference docs and comments. Retain change framing
in commit messages, PR descriptions, changelogs, release notes, migrations,
postmortems, and other version-scoped genres, and retain historical rationale
when it changes correct use or interpretation.

**Destination mismatch.** Markdown markers in email or SMS, decorative social
tags in documentation, or repeated exclamation marks and ellipses in a quiet
register expose the wrong delivery convention. Match the actual medium and
supplied samples; do not enforce punctuation quotas.

**Quotation marks and apostrophes.** Default to straight marks. When the
caller supplied samples, follow their pattern. A single new curly apostrophe
in otherwise straight-punctuated prose is an integration seam. Leave protected
quoted material as it is. Before delivery, scan for U+2018, U+2019, U+201C,
and U+201D when straight marks are selected.

**Invisible and confusable Unicode residue.** Zero-width characters, soft
hyphens, non-breaking spaces, and mixed-script homoglyphs. Apply the Unicode
scan in [verification.md](verification.md#4-exact-element-checks).

## Overcorrection guard

Applying this catalog as unconditional substitution produces skeptic pattern 17,
mechanical lexical cleanup: a second artificial house style that damages
precision. Retain:

- field terminology that happens to look fancy but is exact
- conventional passive voice in genres that require it
- deliberate repetition, defined terms, and legal or technical modality
- a colon or triad doing real work
- ordinary idiom that people use freely: a single `in order to` or
  `there is`, a plain `because`, and a request's `please`
- clean grammar and complex formatting that fit the destination
- genuine asides, fragments, self-corrections, contrasts, objections, and
  unusual details supported by the source or target samples

The test for every fix is the same as everywhere in this skill: does the change
repair something a reader would notice, without changing what the text claims?
If a formulaic sentence carries a unique judgment, repair its expression while
preserving that judgment's force; do not delete it or replace it with a plausible
new reaction.
