# Line-level tells

Constructions that readers now recognize as machine defaults. Unlike the
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
- [Protected spans](#protected-spans)
- [Typography and formatting](#typography-and-formatting)
- [Session residue](#session-residue)
- [Overcorrection guard](#overcorrection-guard)
- [Provenance and license](#provenance-and-license)

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

**"Not just X, but Y."** State the point directly.

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

**Filler.** "In order to" → to. "Due to the fact that" → because. "It is
important to note that" → delete. "There is/are … that" → recast around the
real subject.

**Empty significance adverbs.** `Significantly`, `meaningfully`, `dramatically`,
`fundamentally`, and similar adverbs are defects when they supply importance
without a supported measure, mechanism, comparison, or consequence. Remove the
empty verdict or state the supported fact.

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
syntax that carries their real relationship. A deliberate sequence of beats is
fine when the order or emphasis does useful work.

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

## Protected spans

Before a deep line sweep, replace protected exact spans with stable placeholders.
Mask quotations, code, structured data, URLs, citation locators, published
titles, proper names, defined terms, caller-designated spans, and other material
whose exact form is outside the stylistic assignment. Diagnose the surrounding
prose, then restore every placeholder exactly. Inspect a protected span only
when the caller targets it.

Masking does not exempt a span from fidelity verification. Compare protected
source and output spans separately for exact preservation. If the surrounding
sentence misuses a quotation or citation, diagnose that relationship without
rewriting the protected contents.

## Typography and formatting

**Generated dash characters.** Generated output contains no `U+2013` or
`U+2014` characters. The only exceptions are a protected exact span restored
unchanged and an explicit caller instruction authorizing generation of the
named character. Supplied samples, house style, genre conventions, and
destination typography do not grant that authorization.

When unprotected source prose uses either character structurally, rebuild the
sentence so its syntax carries the relationship. Do not mechanically exchange
the character for a comma, colon, parenthesis, or hyphen. The presence or
absence of either character is never evidence of human or machine authorship;
the rule governs generated output only.

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
in changelogs, release notes, migrations, postmortems, and other version-scoped
genres, and retain historical rationale when it changes correct use or
interpretation.

**Destination mismatch.** Markdown markers in email or SMS, decorative social
tags in documentation, or repeated exclamation marks and ellipses in a quiet
register expose the wrong delivery convention. Match the actual medium and
supplied samples; do not enforce punctuation quotas.

**Quotation marks and apostrophes.** Under `rebuild`, default to straight marks.
Under `preserve` or `match_samples`, follow the supplied pattern; a single new
curly apostrophe in otherwise straight-punctuated prose is an integration seam.
Do not normalize protected quoted material. Before delivery, scan for U+2018,
U+2019, U+201C, and U+201D when straight marks are selected.

**Invisible and confusable Unicode residue.** Scan for zero-width characters,
`U+00AD` soft hyphens, `U+00A0` non-breaking spaces, and mixed-script
homoglyphs. Determine whether each candidate came from the source or the
revision. Remove introduced residue that has no linguistic or formatting job.
Flag suspicious source material with its location and code point; never
silently normalize a protected exact span.

Defend legitimate uses instead of treating the scan as a deletion list. These
include language-required joiners, intentional non-breaking spaces in
typesetting, and exact characters inside names, identifiers, quotations, or
code. A defense must name the character's function and its source support.

## Session residue

Chatbot phrases (`certainly`, `great question`, `I hope this helps`, offers to
do more), sycophancy, cutoff disclaimers ("while specific details are
limited…"), reasoning scaffolds, acknowledgment loops, restated briefs,
unresolved placeholders, and leaked reference tokens are covered as skeptic
pattern 16 in [skeptic-patterns.md](skeptic-patterns.md). Remove accidental
wrappers after recovering any real limitation. Flag a questionable URL or
citation for verification instead of silently changing protected exact
material.

## Overcorrection guard

Applying this catalog as unconditional substitution produces skeptic pattern 17,
mechanical lexical cleanup: a second artificial house style that damages
precision. Retain:

- field terminology that happens to look fancy but is exact
- conventional passive voice in genres that require it
- deliberate repetition, defined terms, and legal or technical modality
- a colon or triad doing real work
- clean grammar and complex formatting that fit the destination, subject to
  hard generated-output character rules
- genuine asides, fragments, self-corrections, contrasts, objections, and
  unusual details supported by the source or target samples

The test for every fix is the same as everywhere in this skill: does the change
repair something a reader would notice, without changing what the text claims?
If a formulaic sentence carries a unique judgment, repair its expression while
preserving that judgment's force; do not delete it or replace it with a plausible
new reaction.

For every `retain` decision in a deep diagnostic, record the exact candidate,
the apparent rule match, the function that makes it legitimate, and the source
or genre evidence for that function. "It sounds human" is not a defense. Report
defended false positives only in an audit or when notes would help the caller;
do not turn them into rewrite commentary by default.

## Provenance and license

The catalog integrates the conceptual sources listed in
[third-party notices and lineage](third-party-notices.md). Entries were
selected, reorganized, independently reworded, and given fidelity and
overcorrection guards. The sources are pattern leads, not evidence of authorship
or detector reliability.
