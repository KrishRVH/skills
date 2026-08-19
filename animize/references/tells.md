# Line-level tells

Constructions that readers now recognize as machine defaults. Unlike the
skeptical-reader clusters, these are judged sentence by sentence: one instance
is usually worth fixing. Default to `fix`; `retain` only when genre, precision,
quoted material, or a caller constraint requires the form. Never fix a tell by
introducing another, and never let the sweep flatten the piece into a second
house style. See [Overcorrection guard](#overcorrection-guard).

## Contents

- [Vocabulary](#vocabulary)
- [Sentence machinery](#sentence-machinery)
- [Plain speech](#plain-speech)
- [Typography and formatting](#typography-and-formatting)
- [Session residue](#session-residue)
- [Overcorrection guard](#overcorrection-guard)
- [Provenance and license](#provenance-and-license)

## Vocabulary

**AI-default words.** Additionally, crucial, delve, enduring, enhance,
fostering, garner, interplay, intricate, landscape (abstract), pivotal,
showcase, tapestry (abstract), testament, underscore, vibrant. Replace with the
plain word the sentence actually needs.

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

**Promotional adjectives.** Nestled, vibrant, breathtaking, groundbreaking,
renowned, stunning, seamless, robust, must-visit. Use neutral description or
the supported comparison.

## Sentence machinery

**"Not just X, but Y."** State the point directly.

**Rule of three.** Ideas forced into groups of three. Use the natural number.

**False ranges.** "From X to Y" where X and Y are not on a meaningful scale.
List the items directly.

**Superficial -ing tails.** Trailing participles that append unearned
significance: "…, highlighting the need for…", "…, ensuring reliability",
"…, showcasing its flexibility". Delete the tail or expand it into a supported
claim with its own sentence.

**Synonym cycling.** Protagonist, main character, central figure, hero within
one passage. Pick the clearest term and repeat it.

**Filler.** "In order to" → to. "Due to the fact that" → because. "It is
important to note that" → delete. "There is/are … that" → recast around the
real subject.

**Adverb propping a weak verb.** "Runs quickly" → is fast, or the number.
"Significantly improves" → the measured delta. An adverb doing the verb's work
means the verb is wrong.

**Unmotivated passive.** "Is/are/was/were + past participle" with a knowable
actor: "queries are validated" → "the compiler validates queries". Passive is
fine when the actor is unknown, irrelevant, or the genre's convention.

## Plain speech

**Say what it does, not how it feels.** "SQL you can read", "the database
stays close at hand", "types that follow your schema" name a feeling. Name the
mechanism or the number instead: "`.toSQL()` returns the exact string sent to
the database", "a column rename fails the build". If a sentence cannot be
restated as a concrete instruction, fact, or number, cut it. This is the
sentence-level form of the anywhere test: a line that could appear unchanged in
another project's docs says nothing about this one.

**One idea per sentence.** If the reader must backtrack to parse a sentence,
split it or drop clauses.

## Typography and formatting

**Em dashes.** Avoid them entirely; prefer zero in the finished piece. Use
periods or commas only. No parentheses, en dashes, or hyphens as substitutes,
since swapping the glyph just trades one tell for another. If a thought needs
separation, end the sentence or use a comma. Retain an em dash only inside
quoted material or where a caller or house style explicitly requires it.

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

**Curly quotes.** Replace with straight quotes. Retain typographic quotes only
when the destination's style guide or typesetting pipeline requires them.

## Session residue

Chatbot phrases (`certainly`, `great question`, `I hope this helps`, offers to
do more), sycophancy, and cutoff disclaimers ("while specific details are
limited…") are covered as skeptic pattern 16 in
[skeptic-patterns.md](skeptic-patterns.md). Remove on sight; recover any real
limitation the disclaimer was hiding before deleting it.

## Overcorrection guard

Applying this catalog as unconditional substitution produces skeptic pattern 17,
mechanical lexical cleanup: a second artificial house style that damages
precision. Retain:

- field terminology that happens to look fancy but is exact
- conventional passive voice in genres that require it
- deliberate repetition, defined terms, and legal or technical modality
- a colon or triad doing real work

The test for every fix is the same as everywhere in this skill: does the change
repair something a reader would notice, without changing what the text claims?

## Provenance and license

This catalog adapts patterns from the `unslop` skill in
[cursor/plugins](https://github.com/cursor/plugins) (MIT license). Changes were
made: entries were reorganized, reworded, given retain conditions, and merged
with Animize's cluster-based diagnostics.
