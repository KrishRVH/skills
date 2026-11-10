# Humanizer and anti-slop skills: survey and gaps against Animize

Date: 2026-11-09. Source: the public skills, rule sets, and tools named below,
each read at the commit or revision given in its note; the Pangram 4 Technical
Report; and Wikipedia's "Signs of AI writing". Star and fork counts come from
the GitHub REST API and install counts from the skills.sh search API
(`https://skills.sh/api/search?q=<term>`), both read without authentication on
2026-11-09. No detector was queried and nothing was signed up for. A claim is
stated by the source cited next to it unless it is marked **Inferred:** (my
reading, with the sources it rests on). Quotations run a line or two at most,
and each note names the source's license. Animize was read from this
repository's working tree on the same date. The detector's own mechanics are
covered in [pangram-detector.md](pangram-detector.md).

## Summary

1. **No prose-rule skill shows evidence that it moves a trained classifier,
   and four sources report that it does not.** Pangram missed 44 of 10,223
   texts rewritten with the most-starred skill, a 0.430% false negative rate
   ([Pangram 4 report, Table 15](https://arxiv.org/html/2607.27183v1)). That
   skill's own README now says detectors
   "[still flag most of its output](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/README.md)".
   A second skill built on detection literature says GPTZero, Grammarly, and
   Pangram still score its output as 99–100% AI
   ([README](https://github.com/harshaneel/humanize/blob/9c3dec34dc8e0ed9d26de14a869900a714da8f9e/README.md)).
   A third party had Claude Sonnet follow the most-starred skill on 60 drafts
   and Originality.ai flagged 60 of 60
   ([eval notes](https://github.com/sgaofen/humanizer-local-model/blob/7dd4be90cb3acb2e5d18aeea5837f888d2bb2d52/eval/README.md)).
   The only surveyed tool with a dated third-party result in its favor is a
   fine-tuned rewriting model, not a rule set: 11 of 210 rewrites flagged by
   Originality.ai on 2026-10-02, with no Pangram figure
   ([README](https://github.com/sgaofen/humanizer-local-model/blob/7dd4be90cb3acb2e5d18aeea5837f888d2bb2d52/README.md)).
2. **Sources now list constructions that lean human, and Animize's Filler
   rule removes some of them.** Wikipedia's page gained a "Signs of human
   writing" section whose syntax list includes `there is a`, `it has a`,
   `very`, `perhaps`, `tends to`, `in order to`, and `the fact that`
   ([revision 1384793302](https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&oldid=1384793302)).
   Sepia keeps an "add back" list of features instruction-tuned models
   under-use: contractions, discourse particles, plain `because`, hedges, and
   first and second person
   ([style-pass.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c962fcc35f596c167c6e38045d6cb8/skills/sepia/references/style-pass.md)).
   Animize's Filler rule rewrites `in order to` and `there is/are … that`
   wherever they appear ([tells.md](../animize/references/tells.md)), and no
   Animize file mentions contractions. The evidence is corpus frequency. No
   source shows that restoring these features changes a detector verdict.
3. **Sentence-length spread is the one syntactic difference two sources
   measured, and a narrow band of short sentences joined only by commas and
   periods is the newest claimed sign.** On a 2024 parallel corpus the median
   coefficient of variation of sentence length was 0.40–0.44 for three models
   against 0.65 for matched human text
   ([patterns.md](https://github.com/conorbronsdon/avoid-ai-writing/blob/30971f1c50c6412a0c414e8c7b15032a32b21939/references/patterns.md)).
   Wikipedia moved em dash overuse to "Historical indicators (2022–September
   2026)" and says, with a citation-needed tag, that the drop in punctuation
   variety "has become its own sign of AI writing"
   ([revision 1384793302](https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&oldid=1384793302)).
   Animize bans both dash characters by default
   ([SKILL.md](../animize/SKILL.md)) and its clarity profile prefers a period
   to a semicolon and one main action per sentence
   ([clear-communication.md](../animize/references/clear-communication.md)).
   **Inferred:** the three defaults together push output toward the profile
   these sources describe.
4. **Contrast framing has variants Animize's catalog does not name.**
   Wikipedia and the most-starred skill both now list the reversed form
   (`X rather than Y`), the contrast split across two sentences, and a
   mid-2026 family of "corrective framings". Animize lists only
   `Not just X, but Y` and clipped negations
   ([tells.md](../animize/references/tells.md)), and `rather than` appears in
   its entry file and in four of the references the executor loads.
5. **Sepia is the closest match to Animize's use case and has three
   mechanisms Animize lacks.** It samples two or three recent human artifacts
   from the destination before writing, keeps a human baseline per workplace
   genre, and runs a deletion test and a reversion test on its own edits
   ([SKILL.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c962fcc35f596c167c6e38045d6cb8/skills/sepia/SKILL.md)).
   All three are reader-facing. Sepia states the research that motivates them
   and reports no detector result.
6. **Three skills now guard against instructions embedded in the text they
   edit. Animize states no such rule.** The most-starred skill added the
   guard in 4.0.0
   ([CHANGELOG.md](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/CHANGELOG.md)).
7. **Two evaluation methods found real failures in the skills that ran
   them.** One skill audited its own output and confirmed that it traded one
   recognizable register for another
   ([analysis](https://github.com/theclaymethod/unslop/blob/17ed39c9d0b522f44190ff0c6233867eadee192a/evals/ADVERSARIAL-WRITING-ANALYSIS.md)).
   Another tested each rule against a human corpus and rejected two rules
   whose target construction humans used twice as often as models
   ([evidence.md](https://github.com/epoko77-ai/im-not-ai/blob/b37e0206d31fffd9149bf57168d4d62eb2086bee/docs/en/evidence.md)).
8. **The Pangram citation in `backends.md` has the right number and three
   loose claims around it.** The report names one repository, not several. Its
   "hard negatives" are human texts the model mislabels, not humanizer
   output. It does not say which version of the skill it tested. Details are
   in [The Pangram 4 report lead](#the-pangram-4-report-lead).

## Comparison table

Ranked by GitHub stars. Installs are the skills.sh count for the same skill
where the registry lists one. "Aim" is whether the source says it targets an
AI-text detector. "Detector evidence" is a measured result on a detector the
source does not own.

| #   | Source                              | Stars  | Installs | Version read                        | License            | Method                                                                   | Aim                                    | Detector evidence                                               |
| --- | ----------------------------------- | ------ | -------- | ----------------------------------- | ------------------ | ------------------------------------------------------------------------ | -------------------------------------- | --------------------------------------------------------------- |
| 1   | blader/humanizer                    | 67,183 | 12,503   | 4.0.0, `b48c832`, 2026-11-09        | MIT                | 26 patterns ordered by strength, four-step draft and check, voice sample | No                                     | None of its own. Third parties: 0.430% missed; 60 of 60 flagged |
| 2   | op7418/Humanizer-zh                 | 22,403 | 57,417   | `f4518a8`, 2026-09-23               | MIT                | Chinese port of blader 3.0.0, 31 checks                                  | No                                     | None                                                            |
| 3   | hardikpandya/stop-slop              | 18,786 | 19,350   | `8da1f03`, 2026-03-18               | MIT                | Eight rules, quick checks, five-dimension score                          | No                                     | None                                                            |
| 4   | petergyang/no-ai-slop               | 13,307 | 30,362   | `000650b`, 2026-09-01               | MIT                | Edit and detect jobs, final self-check file                              | No                                     | None                                                            |
| 5   | miqdadbadjuber/anti-slop            | 8,782  | 9,825    | 3.2.27, `3b75daa`, 2026-11-09       | MIT                | Pattern, reason, before, after catalog for product copy                  | No                                     | None                                                            |
| 6   | epoko77-ai/im-not-ai                | 6,482  | 1,025    | `b37e020`, 2026-10-12               | MIT                | Korean. 85 sub-patterns with severity, routed passes, change-rate gate   | No                                     | None. Own corpus study of rule frequencies                      |
| 7   | conorbronsdon/avoid-ai-writing      | 5,535  | 5,076    | 3.38.0, `30971f1`, 2026-11-05       | MIT                | Editing contract, three modes, profiles, regex scorer, validators        | No                                     | None. Own scorer measured at chance on a corpus                 |
| 8   | AIScientists-Dev/academic-humanizer | 3,929  | 736      | 0.3.3, `94b88b2`, 2026-07-03        | MIT                | Six layers for papers and funding proposals                              | No                                     | None                                                            |
| 9   | Nanako0129/sepia                    | 3,743  | 1,664    | 0.13.0, `0eb11d6`, 2026-11-03       | MIT                | Four operations, domain files, passes, per-model tables                  | No                                     | None of its own. Keeps a ledger of third-party results          |
| 10  | lynote-ai/humanize-text             | 3,491  | none     | `3be99a5`, 2026-10-22               | MIT                | Translation-chain pipeline with a detector feedback loop                 | Yes                                    | Five samples, unnamed detector, undated                         |
| 11  | Raymondhou0917/speak-human-tw       | 1,157  | none     | `7cb730a`, 2026-11-09               | MIT                | Traditional Chinese. Six-step flow, 40-case eval with a model judge      | No                                     | None                                                            |
| 12  | theclaymethod/unslop                | 1,024  | 5,959    | 2.3.0, `17ed39c`, 2026-09-07        | MIT in frontmatter | Edit contract, deterministic scripts, measured voice card                | No                                     | None. Own behavioral eval                                       |
| 13  | sgaofen/humanizer-local-model       | 840    | none     | `7dd4be9`, 2026-10-18               | Apache-2.0         | Fine-tuned rewriting model, not rules                                    | Headline metric, not a training signal | Originality.ai: 11 of 210 flagged, 2026-10-02                   |
| 14  | harshaneel/humanize                 | 618    | none     | `9c3dec3`, 2026-09-22               | MIT                | Nine "levers" with numeric quotas, audit loop                            | Yes                                    | Binoculars only. Says trained classifiers are unmoved           |
| n/a | Wikipedia: Signs of AI writing      | n/a    | n/a      | revision 1384793302, 2026-11-10 UTC | CC BY-SA 4.0       | Field guide for editors, with caveats and human-writing signs            | No                                     | Warns against relying on detectors alone                        |

Three of these repositories were created after the August consolidation:
miqdadbadjuber/anti-slop (2026-08-07), Nanako0129/sepia (2026-08-28), and
sgaofen/humanizer-local-model (2026-09-11), by the GitHub API's `created_at`
field. The ten skills Animize was consolidated from are covered in
[Changes since the August consolidation](#changes-since-the-august-consolidation);
three of them (blader, stop-slop, no-ai-slop) are also in this table.

One repository that would rank fifth by stars is left out of the table. See
[Sources not reached, excluded, or unverified](#sources-not-reached-excluded-or-unverified).

## Per-source notes

### 1. blader/humanizer

- **Read:** version 4.0.0 at commit `b48c832`, released 2026-11-09. MIT.
  ([SKILL.md](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/SKILL.md),
  [CHANGELOG.md](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/CHANGELOG.md))
- **Method:** one account of why model text sounds as it does, then 26
  patterns numbered strongest first. Patterns 1 to 5 justify an edit on one
  sighting. A pattern marked _weak alone_ needs other tells in the same
  passage. The process has four steps: mark tells, draft, check, final. The
  check asks first whether any fact, name, number, date, or quote was dropped
  or changed, then reads the draft aloud, then searches again for the tells
  that most often survive
  ([SKILL.md](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/SKILL.md)).
- **Voice:** a supplied writing sample overrides the patterns, including the
  dash rule: if the sample uses dashes, the rewrite keeps them at about the
  same rate. Without a sample, voice comes from the kind of text
  ([SKILL.md](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/SKILL.md)).
- **Rule categories:** staged contrast and one-line closers first; rhythm
  applied by rule; inflation; formatting applied by rule; chatbot leftovers;
  and, since 3.1.0, replies that re-explain context the reader already has
  ([CHANGELOG.md](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/CHANGELOG.md)).
- **When not to act:** text written before 30 November 2022 is not AI-written,
  and ordinary hedges such as `perhaps` or `tends to` are "human habits and
  not tells"
  ([SKILL.md](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/SKILL.md)).
- **Detector aim:** none. The README says the skill "does not try to get past
  AI detectors, and detectors still flag most of its output"
  ([README.md](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/README.md)).
- **Evidence:** the README gives no number, detector name, or date for that
  sentence. The two measurements of this skill that exist were made by others:
  Pangram's Table 15 and the Originality.ai baseline in note 13.

### 2. op7418/Humanizer-zh

- **Read:** commit `f4518a8`, 2026-09-23. MIT.
  ([README.md](https://github.com/op7418/Humanizer-zh/blob/f4518a8eab97b8bfebc66a89d34320a89bef6930/README.md))
- **Method:** a Chinese port of blader 3.0.0 that keeps 31 checkpoints in the
  A to F grouping. Its September update concentrates on preserving meaning.
- **Detector aim and evidence:** none. The README says the skill cannot prove
  who wrote a text and does not guarantee passing any AI detector
  ([README.md](https://github.com/op7418/Humanizer-zh/blob/f4518a8eab97b8bfebc66a89d34320a89bef6930/README.md)).
- **For Animize:** nothing beyond blader. It has the highest install count in
  the registry (57,417), so the blader lineage is larger than its star count
  alone shows.

### 3. hardikpandya/stop-slop

- **Read:** commit `8da1f03`, 2026-03-18, unchanged since the August read. MIT.
  ([SKILL.md](https://github.com/hardikpandya/stop-slop/blob/8da1f030185bdfe8471220585162991eaeb970e9/SKILL.md))
- **Method:** eight core rules, a quick-check list, and a score on five
  dimensions from 1 to 10, with revision required below 35 of 50.
- **Rule categories:** adverbs, passive voice, sentence starters, dashes,
  extremes, distant narration, and joining phrases. One quick check is a
  quota: when three consecutive sentences match in length, break one.
- **Detector aim and evidence:** none claimed, none offered.

### 4. petergyang/no-ai-slop

- **Read:** commit `000650b`, 2026-09-01. MIT.
  ([SKILL.md](https://github.com/petergyang/no-ai-slop/blob/000650b156983f5159695b441477f4e63b25dc85/skills/no-ai-slop/SKILL.md),
  [eval.md](https://github.com/petergyang/no-ai-slop/blob/000650b156983f5159695b441477f4e63b25dc85/skills/no-ai-slop/eval.md))
- **Method:** two jobs, edit and detect, with a final read against a
  five-item check file.
- **Detector aim:** none. The skill's position is that "AI detectors guess"
  and that named patterns are evidence a person can check
  ([SKILL.md](https://github.com/petergyang/no-ai-slop/blob/000650b156983f5159695b441477f4e63b25dc85/skills/no-ai-slop/SKILL.md)).
- **Evidence:** none offered.

### 5. miqdadbadjuber/anti-slop

- **Read:** version 3.2.27 at commit `3b75daa`, 2026-11-09. MIT. Created
  2026-08-07.
  ([antislop-copywriting/SKILL.md](https://github.com/miqdadbadjuber/anti-slop/blob/3b75daa1fb6bb4c2b8a3807f82eed50914dee6b2/skills/antislop-copywriting/SKILL.md))
- **Method:** a rule system for coding agents that covers interface, code, and
  text. The copy skill gives each pattern the same four parts (the pattern,
  why it reads as AI, before, after) and ties it to a numbered core rule. A
  delivery gate in the core file is the final check.
- **Rule categories:** tone and voice, rhythm and structure, honesty and
  evidence, hygiene and Markdown. It also has "What not to flag" and "Signs
  of human writing (preserve these)" sections, and two cross-cutting rules:
  never invent facts, and "do not over-sterilize".
- **Detector aim and evidence:** none. The catalog overlaps blader 2.x and
  adds marketing patterns (social proof with no evidence, weasel
  attributions, all-caps emphasis).
- **For Animize:** little that is new. It is the fastest-growing source in the
  table: 8,782 stars in three months.

### 6. epoko77-ai/im-not-ai

- **Read:** commit `b37e020`, 2026-10-12. MIT. Korean.
  ([SKILL.md](https://github.com/epoko77-ai/im-not-ai/blob/b37e0206d31fffd9149bf57168d4d62eb2086bee/skills/humanize-korean/SKILL.md),
  [evidence.md](https://github.com/epoko77-ai/im-not-ai/blob/b37e0206d31fffd9149bf57168d4d62eb2086bee/docs/en/evidence.md))
- **Method:** ten categories and 85 sub-patterns, each with a severity. A
  deterministic pre-score routes the text to one, two, or three or more model
  calls. Roles are diagnostician, rewriter, and finalizer. A deterministic
  change-rate gate warns above 30% changed characters and stops above 50%.
  Only detected spans are touched.
- **Evidence for the rules:** a corpus study measured in July 2026. Sixty
  model pieces from three models under bare prompts were compared with sixty
  Korean pieces published before 2022, using G² tests. The negative
  antithesis ("not A but B") appeared 9.2 times as often in model text.
  Sentences of 100 or more characters appeared at a rate of 8.1 in model
  text against 91.3 in human text, in the table's per-thousand unit
  ([evidence.md](https://github.com/epoko77-ai/im-not-ai/blob/b37e0206d31fffd9149bf57168d4d62eb2086bee/docs/en/evidence.md)).
- **Rules the data rejected:** two rules were dropped because human writers
  used the target construction about twice as often as the models. The
  document's conclusions are "Do not treat frequency rules as bans" and
  never prescribe filling an absence, except by joining adjacent sentences,
  which adds no content
  ([evidence.md](https://github.com/epoko77-ai/im-not-ai/blob/b37e0206d31fffd9149bf57168d4d62eb2086bee/docs/en/evidence.md)).
- **Detector aim and evidence:** none. The English README calls it a writing
  quality tool, "not an 'AI detector bypass'"
  ([README.en.md](https://github.com/epoko77-ai/im-not-ai/blob/b37e0206d31fffd9149bf57168d4d62eb2086bee/README.en.md)).

### 7. conorbronsdon/avoid-ai-writing

- **Read:** version 3.38.0 at commit `30971f1`, 2026-11-05. MIT.
  ([SKILL.md](https://github.com/conorbronsdon/avoid-ai-writing/blob/30971f1c50c6412a0c414e8c7b15032a32b21939/SKILL.md),
  [patterns.md](https://github.com/conorbronsdon/avoid-ai-writing/blob/30971f1c50c6412a0c414e8c7b15032a32b21939/references/patterns.md))
- **Method:** an editing contract (a candidate becomes a finding, and a
  finding becomes an edit only when the request authorizes it), three modes
  (rewrite, detect, edit), severity tiers, word tiers, context profiles for
  LinkedIn, blog, technical blog, investor email, docs, and casual text, and
  a two-pass ceiling. A bundled regex scorer gives a 0 to 100 score, and a
  validator checks that protected content survived.
- **Rules worth noting:** a "never inject" list (fabricated speaker
  perspective, manufactured stakes, forced contrarianism, performed candor,
  staccato conversion, invented specifics); reply-specific tells
  (recap-and-flattery openers, wall-of-text replies); invented contrast
  pairs; moral adjectives on objects ("honest shape"); stranded auxiliary
  contrasts ("The tool died; the data didn't."); a colon that opens a triple;
  AI-tool URL parameters; and a check that hard-wrapped paragraphs are
  unwrapped for destinations that render newlines
  ([patterns.md](https://github.com/conorbronsdon/avoid-ai-writing/blob/30971f1c50c6412a0c414e8c7b15032a32b21939/references/patterns.md)).
- **Evidence about its own scorer:** on 875 human and 779 machine paragraphs
  from two public corpora, the composite score reached ROC-AUC 0.501 at
  paragraph level and 0.623 at document level. The repository's reading is
  that the score "cannot reliably separate machine text from human text"
  ([corpus/README.md](https://github.com/conorbronsdon/avoid-ai-writing/blob/30971f1c50c6412a0c414e8c7b15032a32b21939/corpus/README.md)).
- **Evidence about one feature:** the sentence-length figures in the third
  Summary item. They cover GPT-4o, GPT-4o-mini, and Llama 3 Instruct
  continuations from 2024 and held in all six registers of the corpus. The
  repository calls them
  exploratory and "a population tendency", not a per-passage test
  ([patterns.md](https://github.com/conorbronsdon/avoid-ai-writing/blob/30971f1c50c6412a0c414e8c7b15032a32b21939/references/patterns.md),
  [method](https://github.com/conorbronsdon/avoid-ai-writing/blob/30971f1c50c6412a0c414e8c7b15032a32b21939/docs/research/hape-2026-11/README.md)).
- **Dashes:** the skill still targets zero em dashes as writing-quality
  guidance and says the frequency is not evidence of machine authorship,
  because usage varies by model generation and vendor
  ([SKILL.md](https://github.com/conorbronsdon/avoid-ai-writing/blob/30971f1c50c6412a0c414e8c7b15032a32b21939/SKILL.md)).
- **Detector aim and evidence:** none. No external detector result appears
  for its output.

### 8. AIScientists-Dev/academic-humanizer

- **Read:** version 0.3.3 at commit `94b88b2`, 2026-07-03. MIT.
  ([SKILL.md](https://github.com/AIScientists-Dev/academic-humanizer/blob/94b88b23703bed7df507acae7d6d5876209a0cdf/SKILL.md))
- **Method:** six layers: general tells; academic tells (over-claiming verbs,
  significance hype, novelty padding, contribution-list cliches, citation
  dumping, vague hedging, clause-stacked sentences); a preserve list
  (evidence-tied hedging, passive voice, `we`); claim and evidence discipline
  (every empirical claim backed by a number, figure, or citation, and verb
  strength matched to the evidence); voice and venue matching; and a mode for
  funding proposals.
- **Detector aim:** none. The description says it is "not for evading AI-use
  disclosure".
- **Evidence:** none offered.

### 9. Nanako0129/sepia

- **Read:** version 0.13.0 at commit `0eb11d6`, 2026-11-03. MIT. Created
  2026-08-28.
  ([SKILL.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c962fcc35f596c167c6e38045d6cb8/skills/sepia/SKILL.md))
- **Method:** four operations (write, review, refactor, recreate). Text is
  routed by type to a domain file: release notes, developer replies,
  postmortems, tickets, technical articles, or journalism. Fiction gets
  separate narrative, discourse, and style passes.
- **Venue first:** before writing or editing, sample two or three recent
  human-written artifacts from the same venue and match their register,
  length, and formatting. "The venue corpus, not this skill, defines the
  target voice"
  ([professional-pass.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c962fcc35f596c167c6e38045d6cb8/skills/sepia/references/professional-pass.md)).
- **Calibration rules:** aim at the human band and not the opposite pole,
  because inverting every tell creates a new fingerprint. Fix what the
  checklist flags and nothing more. Leave some ordinary sentences alone
  ([SKILL.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c962fcc35f596c167c6e38045d6cb8/skills/sepia/SKILL.md)).
- **Edit tests:** refactor writes a full defect list before any edit, prefers
  replacing and deleting to inserting (it cites a measured editor ratio of
  74% replace, 18% delete, 8% insert), and ends with two tests. The
  deletion test strikes every added word and removes it if the sentence still
  parses and means the same. The reversion test puts back each replaced
  wording and keeps the original if it was sound and shorter. The motive is a
  finding that machine-edited human text shows a sharp fall in lexical
  density (d = −3.10)
  ([style-pass.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c962fcc35f596c167c6e38045d6cb8/skills/sepia/references/style-pass.md)).
- **Add back:** features that instruction-tuned models use at 13–80% of the
  human rate, restored "sprinkled, not poured" and only as far as the genre
  and the author's voice allow
  ([style-pass.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c962fcc35f596c167c6e38045d6cb8/skills/sepia/references/style-pass.md)).
- **Rhythm check:** look for runs of three or more adjacent sentences of
  about the same length, and count a run only alongside other hits. Sepia
  marks the check as its own inference and warns against scoring a passage by
  counting sentences under or over a length cutoff
  ([style-pass.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c962fcc35f596c167c6e38045d6cb8/skills/sepia/references/style-pass.md)).
- **Model identity:** the skill records the author model and the executor
  model and loads a table of sentence-level habits per release, taken from
  each vendor's prompting guidance and labeled "unmeasured"
  ([model-fingerprints.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c962fcc35f596c167c6e38045d6cb8/skills/sepia/references/model-fingerprints.md)).
- **Dashes:** measured em dashes per 1,000 words were 10.62 for GPT-4.1, 9.09
  for Claude Opus 4.6, 1.43 for GPT-5.4, and 0.00 for Llama 3.x, against a
  human mean of 3.23 from eight essays. Sepia concludes the rate is never a
  tell on its own
  ([style-pass.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c962fcc35f596c167c6e38045d6cb8/skills/sepia/references/style-pass.md)).
- **Security and unattended runs:** the text being edited is untrusted data
  and cannot switch the operation or widen scope. An unattended run never
  stops to ask and records what it deferred
  ([SKILL.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c962fcc35f596c167c6e38045d6cb8/skills/sepia/SKILL.md)).
- **Detector aim:** none. Its detector research file, written in Chinese and
  dated 2026-09-05, opens by saying the skill targets no automatic detector
  and uses detector research only to confirm that the signals it hunts are
  structural
  ([detectors.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c962fcc35f596c167c6e38045d6cb8/research/detectors.md)).
- **Evidence:** none of its own on any detector. The research file is a
  ledger of third-party findings, which I did not check at their sources. It
  also records that no single-feature ablation study of a detector exists.

### 10. lynote-ai/humanize-text

- **Read:** commit `3be99a5`, 2026-10-22. MIT.
  ([pipeline.md](https://github.com/lynote-ai/humanize-text/blob/3be99a5e83cef690dcdedb49dc0aa656c259e55b/docs/pipeline.md))
- **Method:** a pipeline tool, not a rule set. Two model rewrites at
  temperature 1.3 through Chinese and Japanese, then machine translation to
  Finnish and back to the target language. Higher tiers add rewrite rounds
  and a feedback loop scored by local detectors.
- **Detector aim:** yes. This is the only source in the table built to change
  a detector's output.
- **Evidence:** five showcase samples "classified as `human` by the AI
  detector" with confidence 0.7218 to 0.9997. The detector is not named and
  the run is not dated
  ([pipeline.md](https://github.com/lynote-ai/humanize-text/blob/3be99a5e83cef690dcdedb49dc0aa656c259e55b/docs/pipeline.md)).
  The README says no rewriting method makes text reliably undetectable
  ([README.md](https://github.com/lynote-ai/humanize-text/blob/3be99a5e83cef690dcdedb49dc0aa656c259e55b/README.md)),
  and the techniques file says its local detection models may not correlate
  with commercial detectors
  ([techniques.md](https://github.com/lynote-ai/humanize-text/blob/3be99a5e83cef690dcdedb49dc0aa656c259e55b/docs/techniques.md)).
  This is a claim of effect without usable evidence.

### 11. Raymondhou0917/speak-human-tw

- **Read:** commit `7cb730a`, 2026-11-09. MIT. Traditional Chinese.
  ([SKILL.md](https://github.com/Raymondhou0917/speak-human-tw/blob/7cb730a1d2e85b5300ee04f94920812932547174/SKILL.md))
- **Method:** six steps: read the context, lock a protected list, set the
  rewrite scope so long text does not shrink, rewrite by category, re-read
  for fidelity, and self-assess. It lists planned changes and waits for
  confirmation, with a non-interactive mode that applies everything and
  summarizes afterward. Where a stance is missing it writes an inline
  placeholder asking for the author's input. It marks suspicious citations
  for checking.
- **Evidence:** a 40-case eval dated 2026-07-10 with 26 should-fix and 14
  should-not-fix cases. The rewriter was one model family and the judge
  another. Should-fix cases passed at 96% (25 of 26) and no should-not-fix
  case was wrongly edited. The results file says none of its eight "human
  touch" goals is covered by the eval, on the ground that scoring them would
  turn them into another formula
  ([results-v1.4.0.md](https://github.com/Raymondhou0917/speak-human-tw/blob/7cb730a1d2e85b5300ee04f94920812932547174/evals/results-v1.4.0.md)).
- **Detector aim and evidence:** none.

### 12. theclaymethod/unslop

- **Read:** version 2.3.0 at commit `17ed39c`, 2026-09-07. The frontmatter
  says MIT; the repository has no license file.
  ([SKILL.md](https://github.com/theclaymethod/unslop/blob/17ed39c9d0b522f44190ff0c6233867eadee192a/SKILL.md))
- **Method:** a core contract (make the minimal edit, "prefer a no-op to an
  uncertain edit", copy every sentence without a finding byte for byte),
  four commands, four presets, and deterministic scripts for preservation,
  banned phrases, structure, readability, and diffs
  ([core-contract.md](https://github.com/theclaymethod/unslop/blob/17ed39c9d0b522f44190ff0c6233867eadee192a/references/core-contract.md)).
- **Voice card:** built by script from the writer's documents, never by the
  model scoring itself. The always-loaded card stays under 300 words and
  holds median sentence length, interquartile range, burstiness, contraction
  habits with real examples, punctuation the writer uses and avoids, top
  sentence openers, and a "Never" list. Thin samples set a `low_confidence`
  flag that must be shown to the user
  ([mimic.md](https://github.com/theclaymethod/unslop/blob/17ed39c9d0b522f44190ff0c6233867eadee192a/references/mimic.md)).
- **Self-audit:** an adversarial review supported the charge that the skill
  "trades one detectable register" for another. Its scanner scored its own
  house style (fragment contrasts, staccato triplets) at zero violations
  until new patterns were added
  ([analysis](https://github.com/theclaymethod/unslop/blob/17ed39c9d0b522f44190ff0c6233867eadee192a/evals/ADVERSARIAL-WRITING-ANALYSIS.md)).
- **Evidence:** the results file is headed "BETA; COMPARATIVE CLAIM NOT YET
  REVALIDATED". With the skill against the raw model, repaired issues were
  13 of 20 against 13 of 20 on one model and 15 of 20 against 14 of 20 on
  another. Clean documents left exactly unchanged were 7 of 7 against 4 of
  7, on the one model where that was scored
  ([CORE-RESULTS.md](https://github.com/theclaymethod/unslop/blob/17ed39c9d0b522f44190ff0c6233867eadee192a/evals/CORE-RESULTS.md)).
  The measured gain is restraint on clean text, not better repair.
- **Detector aim and evidence:** none.

### 13. sgaofen/humanizer-local-model

- **Read:** commit `7dd4be9`, 2026-10-18. Apache-2.0. Created 2026-09-11.
  ([README.md](https://github.com/sgaofen/humanizer-local-model/blob/7dd4be90cb3acb2e5d18aeea5837f888d2bb2d52/README.md))
- **Method:** a 12-billion-parameter model fine-tuned to rewrite a model
  draft toward the human original it was paired with, then trained further
  with preference pairs and a reinforcement step that rewards factual
  fidelity and penalizes copying. The README says "No AI detector was used
  anywhere in training".
- **Evidence:** Originality.ai, API v3, strictest setting, 2026-10-02, 210
  English drafts: 11 flagged as AI, against 26 for the previous release. A
  model judge found no factual problem in 376 of 420 rewrites. As a public
  baseline, Claude Sonnet followed blader/humanizer v3.1.0 on 60 of the
  drafts: 60 of 60 were flagged, with a median AI score of 100%, against 4 of
  60 for the model
  ([README.md](https://github.com/sgaofen/humanizer-local-model/blob/7dd4be90cb3acb2e5d18aeea5837f888d2bb2d52/README.md),
  [eval/README.md](https://github.com/sgaofen/humanizer-local-model/blob/7dd4be90cb3acb2e5d18aeea5837f888d2bb2d52/eval/README.md)).
- **Limits:** the figures are the author's own, on one detector, on one date.
  Nothing is reported for Pangram. The README says the model can still change
  a detail.

### 14. harshaneel/humanize

- **Read:** commit `9c3dec3`, 2026-09-22. MIT.
  ([SKILL.md](https://github.com/harshaneel/humanize/blob/9c3dec34dc8e0ed9d26de14a869900a714da8f9e/plugins/humanize/skills/humanize/SKILL.md),
  [README.md](https://github.com/harshaneel/humanize/blob/9c3dec34dc8e0ed9d26de14a869900a714da8f9e/README.md))
- **Method:** nine "levers" drawn from detection papers, with quotas: one or
  two surprising word choices per paragraph; at least one sentence of six
  words or fewer per 150 words; never three consecutive sentences within
  five words of each other in length; at most one em dash per 300 words. An
  audit and revise loop follows. Optional techniques include picking the best
  of several variants by detector score and distilling a writer profile from
  samples.
- **Detector aim:** yes in design. The README frames detection research as
  "the measuring instrument, not the target".
- **Evidence:** 25 inputs. Its own checker scored a mean of 5.24 of 27.
  Binoculars, run with a small substitute model pair, placed all 25 on the
  human side. The README then says trained commercial classifiers "still
  score the same humanized output as 99–100% AI"
  ([README.md](https://github.com/harshaneel/humanize/blob/9c3dec34dc8e0ed9d26de14a869900a714da8f9e/README.md)).
  No table or date backs that sentence, but it is an admission against the
  repository's interest.
- **For Animize:** this is the clearest public record that numeric rhythm
  and vocabulary quotas move a perplexity-family score and not a trained
  classifier.

### Wikipedia: Signs of AI writing

- **Read:** revision 1384793302, 2026-11-10 02:55 UTC, 181,038 bytes. CC
  BY-SA 4.0.
  ([permalink](https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&oldid=1384793302))
- **Method:** a field guide for editors, organized as caveats, content,
  language and grammar, style, communication intended for the user, markup,
  citations, comment-specific indicators, edit summaries, and miscellaneous
  signs. Three sections matter most here: Signs of human writing,
  Ineffective indicators, and Historical indicators.
- **Caveats:** do not rely on detection tools alone, and people judging by
  feel do poorly.
- **Contrast framing:** the negative parallelism section now has three
  forms, including `Y rather than X`, described as "particularly common in
  recent LLM output".
- **Mid-2026 disclaimers:** "corrective framings" that warn a claim should
  be treated as speculative `rather than` definitive, caution that the
  available information does not establish a conclusion, or say a topic
  "should not be confused" with another. The page says the pattern was
  almost unheard of before mid-2026.
- **Vocabulary by era:** the mid-2026 list adds `quietly`, `steady`,
  `clearer`, `dependable`, `matters`, and `practical`, with a note that this
  generation uses more periods and commas and shorter sentences in a band of
  about 8 to 20 words. The note cites one product review, which is a weak
  source.
- **Signs of human writing:** text from before 30 November 2022; the ability
  to explain one's own editorial choices; and a syntax list of constructions
  more common in human-written Wikipedia text than in model text: simple
  is/has phrases, plain verbs (`wrote`, `used`), superlative or definitive
  statements, qualifiers and intensifiers, and isolated wordy constructions.
- **Ineffective indicators:** perfect grammar, mixed registers, bland prose,
  formal prose, transition words in isolation, and unsourced content.
- **Historical indicators:** promotional language (2023–2025), knowledge
  cutoff statements, section summaries, prompt refusals, overuse of em dashes
  (2022–September 2026), abrupt cut-offs, and elegant variation. The em dash
  entry says models from September 2026 onward are increasingly built not to
  use the character and that punctuation variety fell as a side effect. That
  sentence carries a citation-needed tag dated October 2026.
- **Detector aim and evidence:** not applicable. The page describes what
  readers notice.

## What the surveyed skills have that Animize lacks

Each item names what it is, where it comes from, what Animize does today, the
kind of addition, and the evidence. "Reader-facing" means a writing technique
a reader benefits from. "Detector-only" means it exists to change a score.

### Rules

1. **Reversed and split contrast framing, and corrective framings.**
   `X rather than Y`, `Rather than X, …`, a contrast split across two
   sentences, and the mid-2026 disclaimers in the Wikipedia note above. The
   most-starred skill makes the staged contrast its first pattern and acts on
   a single sighting
   ([SKILL.md](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/SKILL.md)).
   - Animize today: `Not just X, but Y`, `The real X`, clipped negations, and
     the rebuttal-theater cluster
     ([tells.md](../animize/references/tells.md),
     [skeptic-patterns.md](../animize/references/skeptic-patterns.md)).
     `rather than` appears in Animize's entry file and in four references
     the executor loads (procedure, authoredness, skeptic patterns, and clear
     communication).
   - Kind: reader-facing.
   - Evidence: observational (Wikipedia's dated examples). None on a
     detector.
2. **Constructions to keep because humans use them more.** Isolated
   `in order to`, `the fact that`, `as a result of`, `there is a`; hedges
   such as `perhaps` and `tends to`; contractions; plain `because`; first and
   second person.
   - Animize today: the Filler rule rewrites the first group on sight, and
     the clarity profile removes `just`, `simply`, and `quickly` from
     instructions
     ([tells.md](../animize/references/tells.md),
     [clear-communication.md](../animize/references/clear-communication.md)).
     The overcorrection guard does not list these constructions.
   - Kind: reader-neutral. Concision and human frequency pull in opposite
     directions here, so the choice is a policy one: repair a stack of
     filler, and leave a single instance alone.
   - Evidence: corpus frequency, from Wikipedia's syntax list and the paper
     sepia cites for usage at 13–80% of the human rate. No source tests
     whether restoring them changes any verdict.
3. **Replies that re-explain what the reader already has, and
   reply-specific tells.** Blader's pattern 26 covers a reply that restates
   the conversation
   ([CHANGELOG.md](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/CHANGELOG.md)).
   Avoid-ai-writing adds recap-and-flattery openers and wall-of-text replies.
   Sepia's developer-reply file starts from "answer first"
   ([dev-replies.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c962fcc35f596c167c6e38045d6cb8/skills/sepia/references/domains/dev-replies.md)).
   - Animize today: a restated brief and acknowledgment loops count as
     session residue
     ([skeptic-patterns.md](../animize/references/skeptic-patterns.md)). No
     rule tests a reply against what the thread already established.
   - Kind: reader-facing.
   - Evidence: none.
4. **Release-specific habits: mannered prose and over-compression.** The
   cursor plugin's unslop added both in September: metaphor and flourish
   where a literal phrase exists, and dropped articles, verbless fragments,
   and arrows standing in for sentences
   ([commit e8d856f](https://github.com/cursor/plugins/commit/e8d856f0273b42ebafe0ec3546bd645709e7c1b0)).
   Sepia keys the same habits to the executor's release.
   - Animize today: abstract metaphors and slogan theater are covered, and
     the clarity profile keeps articles and verbs. Nothing is keyed to the
     model that runs the skill.
   - Kind: reader-facing.
   - Evidence: none. Sepia labels its table as vendor guidance, unmeasured.
5. **Small residue checks.** AI-tool URL parameters such as
   `utm_source=chatgpt.com` (Wikipedia, avoid-ai-writing), citation markup
   leaks listed per provider
   ([Aboudjem patterns.md](https://github.com/Aboudjem/humanizer-skill/blob/a58df065367550b6ce40ff3f648335018d8e0589/skills/humanizer/references/patterns.md)),
   hyphenated compound modifiers kept after the noun (blader), and hashtag
   stuffing.
   - Animize today: leaked reference tokens and unresolved placeholders are
     listed. URL parameters, hyphen habits, and hashtags are not.
   - Kind: reader-facing and mechanically checkable.
   - Evidence: observational.

### Procedure steps

1. **Sample the venue before writing.** Two or three recent human artifacts
   from the same destination set the register, length, and formatting
   (sepia, note 9).
   - Animize today: voice comes only from samples the caller supplies, and
     the Frame step records destination and genre without reading examples
     of either ([SKILL.md](../animize/SKILL.md)).
   - Kind: reader-facing. An unattended run can do this without a question
     when the destination is a repository or thread it can already read.
   - Evidence: none for the step. Its motive is a finding that
     instruction-tuned models struggle to match genre-specific variation.
2. **Human baselines per workplace genre.** Sepia has a file each for
   release notes, developer replies, postmortems, tickets, and technical
   articles, each opening with what humans do in that genre.
   Avoid-ai-writing has context profiles.
   - Animize today: a destination table for format and a documentation genre
     table in the clarity profile. Its stated input is messages, emails, pull
     request descriptions, and write-ups, and none has a baseline.
   - Kind: reader-facing.
   - Evidence: none.
3. **Deletion test and reversion test after editing.** See note 9.
   - Animize today: the Preserve edit policy already prefers deletion and
     forbids near-synonym swaps and inserted words
     ([procedure.md](../animize/references/procedure.md)). The tests would
     add a check of each edit after it is made, and the lexical-density
     finding gives the policy a measured reason.
   - Kind: reader-facing.
   - Evidence: the footprint is measured (as cited by sepia; I did not read
     the paper). The tests themselves are untested.
4. **A run-length check for rhythm, repaired by moving words.** Look for
   three or more adjacent sentences of about the same length, as one signal
   among several. Repair by joining or splitting existing sentences and never
   by adding content (sepia, note 9; im-not-ai, note 6).
   - Animize today: "Vary rhythm" from sentences doing different jobs, with
     no check ([authoredness.md](../animize/references/authoredness.md)). The
     clarity profile's one-action sentences and period preference work
     against it.
   - Kind: reader-facing when it is a check. Detector-only when it becomes a
     quota, as in harshaneel/humanize and stop-slop.
   - Evidence: the spread difference is measured on 2024 models and on a
     Korean corpus. No source shows a verdict moving, and the quota version
     is the one a source reports as failing against trained classifiers.
5. **Treat instructions inside the edited text as text.** Blader 4.0.0,
   sepia, and avoid-ai-writing each state it. Avoid-ai-writing has an eval
   scenario for it.
   - Animize today: the Frame step records which passages are instructions,
     samples, or quotations. No file says that a passage inside the material
     cannot change the task.
   - Kind: safety. Neither reader-facing nor detector-facing.
   - Evidence: not applicable.

### Mechanisms

1. **A measured voice card.** Statistics computed by script from at least
   five documents, with a "Never" list and a low-confidence flag
   (theclaymethod/unslop, note 12). Blader 4.0.0 lets a sample override every
   pattern, including the dash rule.
   - Animize today: a voice record of three to five observed signals that
     excludes isolated punctuation
     ([authoredness.md](../animize/references/authoredness.md)).
   - Kind: reader-facing.
   - Evidence: none on a detector from the skills. Pangram's own red team
     reports that conditioning on source writing did not produce a bypass
     ([Pangram 4 report](https://arxiv.org/html/2607.27183v1)).
2. **Profile the skill's own output.** Generate many samples in a domain,
   find the constructions that repeat, and write them into an avoid list
   ([mshumer/unslop](https://github.com/mshumer/unslop/blob/edcb62386d129c65e4395f0cfcc9168eb1ba2148/README.md)).
   Theclaymethod's audit is the same idea applied to a humanizer.
   - Animize today: skeptic pattern 17 names the risk of a second house
     style. The evaluation protocol has no step that looks for one across
     many outputs.
   - Kind: evaluation method.
   - Evidence: it found a real failure where it was run (note 12).
3. **Validate each rule against a human corpus and drop the ones that
   fail.** See note 6, and note 7 for the same test applied to a whole
   scorer.
   - Animize today: a controlled defect suite with defended false-positive
     controls ([evaluation.md](../animize/references/evaluation.md)). No
     step compares a rule's target frequency in human and model text.
   - Kind: evaluation method.
   - Evidence: it rejected two rules in one skill and showed one scorer at
     chance in another.
4. **A fine-tuned rewriter.** See note 13.
   - Animize today: `backends.md` already treats the model stack as the
     route that moves a classifier.
   - Kind: detector-only as a mechanism.
   - Evidence: self-reported, Originality.ai only.

### What the survey argues against adopting

- **Regex scores as a measure of human-likeness.** The one scorer that was
  tested sat at chance (note 7). Slopbeth's panel of public detectors
  disagreed on the same outputs and flagged the human control
  ([panel](https://github.com/ehmo/slopkit/blob/b33718bb9283c11b09567dc714f92d90ffb7bd16/skills/slopbeth/benchmarks/public-detector-panel-v1.md)).
- **Numeric quotas for burstiness and surprising words.** Note 14.
- **Adding specifics the model "knows to be true".** Blader 4.0.0 reversed
  its no-invention rule this way. It conflicts with Animize's content lock,
  and the changelog gives no evidence for the change.

## The Pangram 4 report lead

`backends.md` says "the measured ceiling for prose-rule humanizers against a
trained classifier is a false negative rate under half a percent (Pangram 4
Technical Report, arXiv 2607.27183, Table 15)" and that the vendor "benchmarks
popular repositories by name, retrains on hard negatives, and ships a
classification head for whatever tactic gets traffic".

**Confirmed.** The report exists under that number: "Pangram 4 Technical
Report", submitted 29 July 2026, one version
([abstract](https://arxiv.org/abs/2607.27183)). Table 15 exists and reports
false negatives on text "generated then rewritten using the BLADER series of
agent skills" ([HTML](https://arxiv.org/html/2607.27183v1)):

| Humanizing model | Missed | Texts  | False negative rate |
| ---------------- | ------ | ------ | ------------------- |
| GPT-5.5          | 17     | 3,404  | 0.499%              |
| Opus 4.8         | 14     | 3,412  | 0.410%              |
| Sonnet 4.6       | 13     | 3,407  | 0.382%              |
| Overall          | 44     | 10,223 | 0.430%              |

**Corrections.**

1. **One repository, not several.** The report names only blader/humanizer,
   in a footnote that gives its star count as "nearly 32,000" at publication.
   Section 5.9.1 describes it as "a popular GitHub repository containing
   instructions for AI agents to humanize their text". No other repository is
   named in the report or in the two vendor blog posts read
   ([August 2025](https://www.pangram.com/blog/humanizers-aug-25),
   [January 2025](https://www.pangram.com/blog/humanizers-announcement)).
2. **The skill version is not stated.** The report gives no commit, version,
   prompt, or source domain for the Table 15 texts. **Inferred:** it measured
   a 2.x version, because the commit pinned in August was still 2.11.2. The
   skill has been rebuilt twice since (3.0.0 and 4.0.0), and nobody has
   published a Pangram figure for either.
3. **"Ceiling" generalizes from one skill.** The table measures one rule set
   applied by three models. It is the only such measurement, and the
   independent result in note 13 points the same way on a different detector,
   but the report does not call it a ceiling.
4. **"Hard negatives" means something else in the report.** The active
   learning section mines human texts that a checkpoint labels as AI, which
   is false-positive mining, and then retrains from scratch. Humanizer output
   is handled by a separate head (next item). The January 2025 post says
   humanized text was added to the training corpus of the model of that
   time.
5. **The head is a probe with a fixed class list.** The auxiliary humanizer
   head predicts four classes (human, AI-generated, humanized AI, mixed
   authorship). It is trained with a stop-gradient because letting gradients
   flow concentrated false positives in academic and second-language writing.
   Its listed coverage is typo injection, casing changes, synonym
   substitution, homoglyphs, and services that advertise humanization. On
   paired data it scores accuracy 96.82%, F1 0.9678, false positive rate
   1.93%, false negative rate 4.43% (Table 13).

**Commercial tools in the report are anonymized.** Table 14 lists thirteen
humanizers as Commercial A to M, "chosen by top web traffic in early 2026".
AI recall ranges from 92.78% (H) to 99.70% (F), with 97.69% overall, and
98.83% counting a Mixed verdict as detection. The running text gives 97.67%
for the first figure, a small discrepancy inside the report.

**Named commercial tools appear only in a vendor blog post.** The August 2025
post lists twenty tools with detection accuracy, from 90.3% (Undetectable AI)
and 92.7% (TwainGPT) up to 100.0% for ten of them, including Grammarly and
Quillbot ([post](https://www.pangram.com/blog/humanizers-aug-25)). Those
figures are for an earlier model and are the vendor's own.

**Red team.** Two coding agents had API access for 24 hours. The
false-negative agent tried imitating human voices and registers, terse
vocabulary, conditioning on source writing, aggregating documents, and
multi-round translation. The one bypass it found was acting as a surgeon or
pathologist dictating notes aloud, which the authors set aside as out of
scope
([section 5.9.2](https://arxiv.org/html/2607.27183v1)).

**A suggested rewording for `backends.md`:** the one published measurement of
a prose-rule humanizer against this classifier is 44 misses in 10,223 texts
(0.430%), for blader/humanizer applied by three models, version unstated.

## Changes since the August consolidation

Each subsection compares the default branch on 2026-11-09 with the commit
read in August. Five skills are unchanged and five changed. None moved or
vanished, and none added a detector claim or a detector measurement.

### stop-slop

Unchanged. The default branch is still at the pinned commit `8da1f03`, dated
2026-03-18
([SKILL.md](https://github.com/hardikpandya/stop-slop/blob/8da1f030185bdfe8471220585162991eaeb970e9/SKILL.md)).

### no-ai-slop

One commit since the pin, on 2026-09-01
([000650b](https://github.com/petergyang/no-ai-slop/commit/000650b156983f5159695b441477f4e63b25dc85)).

- **Removed:** the workflow step that asked for three to five voice signals
  kept as an internal note, and the final-read item about separate editor
  and evaluator agents. The check file went from six items to five.
- **Added:** an agent metadata file in the skill folder.
- **Rules, detector claims, evaluation:** no change.
- **For Animize:** Animize's voice record of three to five signals came from
  the same idea. This source dropped it as a "planning ritual" without giving
  a measurement.

### humanizer (blader)

Sixty-eight commits since the pin, from version 2.11.2 with 35 patterns to
4.0.0 with 26
([compare](https://github.com/blader/humanizer/compare/e2e92e7b4b8229253ed5c8e81dc65463fdeddda5...b48c832f0f809c1b5658edbb838c2521b72f2413),
[CHANGELOG.md](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/CHANGELOG.md)).

- **3.0.0, rebuilt:** one account of why model text sounds as it does; 35
  patterns consolidated into 25 in five sections, numbered by strength and
  frequency so the staged contrast and the one-line closer come first.
- **3.0.0, removed:** false ranges and synonym cycling, because Wikipedia now
  lists them as human habits or historical. Animize still has both in
  [tells.md](../animize/references/tells.md). The `ai-detection` keyword was
  removed from the package files.
- **3.0.0, added:** vague connection or association, and longer watch lists.
- **3.1.0:** pattern 26 for replies that re-explain context; pattern 25
  widened to text that describes its own sourcing, assembly, or layout;
  headings written for effect; "That distinction matters."; and a README
  statement that getting past detectors is not a goal.
- **4.0.0, reversed:** the no-invention rule from 2.9.0. The skill now adds
  "a specific detail you know to be true" where text is generic, while still
  treating a lost or changed claim as an error.
- **4.0.0, added:** the embedded-instruction guard; file mode that reads the
  whole current file and reports how many sections it reviewed; reworked
  examples, several of which had been "vaguer or stiffer than the text they
  replaced".
- **New watch items since the pin:** reversed `X rather than Y`, a contrast
  split across sentences, clipped negative tails, rows of fragments,
  all-caps and word-by-word emphasis, hyphenated pairs after a noun,
  `quietly`, `gate` as a verb, a horizontal rule between every section, and
  narration of method
  ([SKILL.md](https://github.com/blader/humanizer/blob/b48c832f0f809c1b5658edbb838c2521b72f2413/SKILL.md)).
- **Detector claims:** the README sentence quoted in note 1 is new. It is a
  statement with no number behind it.
- **Evaluation method:** none added.

### unslop (cursor/plugins)

Five commits touch the file since the pin
([SKILL.md](https://github.com/cursor/plugins/blob/de8ee15dd1194627d21eb5fcd41cb1873208dabb/pstack/skills/unslop/SKILL.md)).
The plugin's license file is MIT. The registry lists 33,984 installs for this
copy and 10,034 for backnotprop/pstack, which lists a skill of the same
name.

- **2026-09-01:** model invocation disabled, so the skill runs only when
  called
  ([73f8be4](https://github.com/cursor/plugins/commit/73f8be4873ea4ba2b7378243a036d3360c69e04d)).
- **2026-09-07:** the "Adding soul" section removed (have opinions, vary
  rhythm, let some mess in). Rules for puffery, name-dropping, promotional
  language, formulaic challenges, and cutoff disclaimers removed. The
  sentence calling em dashes an AI tell removed. Rule 32 (mannered prose) and
  rule 33 (over-compression) added
  ([e8d856f](https://github.com/cursor/plugins/commit/e8d856f0273b42ebafe0ec3546bd645709e7c1b0)).
- **2026-09-22:** the self-audit step that asked what makes the draft
  obviously AI-generated removed
  ([70b2dc8](https://github.com/cursor/plugins/commit/70b2dc8b4b85c8d5648624ca40d692c421fff32f)).
- **2026-10-10 and 2026-10-11:** the process folded into one sentence and the
  description shortened
  ([00b14f1](https://github.com/cursor/plugins/commit/00b14f1df36b32a8dd1529324a3a459f6563b127),
  [bc697d0](https://github.com/cursor/plugins/commit/bc697d0a5a163cec979e362b601e36f5616083fd)).
- **Detector claims, evaluation:** none.
- **For Animize:** the direction is the opposite of most of the field. This
  skill removed its personality-adding section and its historical rules and
  added the two habits of current releases.

### slopbeth (ehmo/slopkit)

Unchanged. The default branch is still at the pinned commit `b33718b`, dated
2026-07-22
([SKILL.md](https://github.com/ehmo/slopkit/blob/b33718bb9283c11b09567dc714f92d90ffb7bd16/skills/slopbeth/SKILL.md)).
Its public detector panel, dated 2026-06-18 and already present at the pin,
concludes that public detectors are useful "as regression sensors, but not as
a release target"
([panel](https://github.com/ehmo/slopkit/blob/b33718bb9283c11b09567dc714f92d90ffb7bd16/skills/slopbeth/benchmarks/public-detector-panel-v1.md)).

### humanizer-skill (Aboudjem)

Twenty commits since the pin. Two touch the skill folder
([ff8a96a](https://github.com/Aboudjem/humanizer-skill/commit/ff8a96a9ae3b0441d567849b938db21bc97f315e),
[71a6abe](https://github.com/Aboudjem/humanizer-skill/commit/71a6abe4c776052b8b7e23cc5404392adb7775f6)).

- **Added rules:** two patterns, for 55 in total: argument residue and
  leftover hedge debris. The vague-association pattern gained two phrases,
  and citation markup leaks are now listed for five providers
  ([patterns.md](https://github.com/Aboudjem/humanizer-skill/blob/a58df065367550b6ce40ff3f648335018d8e0589/skills/humanizer/references/patterns.md)).
- **Changed:** the first word tier split into an evidence grade and a
  wordiness grade. A lower-confidence note was added for semicolon and colon
  clusters.
- **Added guards:** false-positive guards for low-variance prose by autistic
  and ADHD writers and for non-native English; an explicit no-fabrication
  rule for the pass that adds concrete detail; and a refusal to edit
  non-prose targets
  ([SKILL.md](https://github.com/Aboudjem/humanizer-skill/blob/a58df065367550b6ce40ff3f648335018d8e0589/skills/humanizer/SKILL.md)).
- **Added caveats:** an "Honest limits of this catalog" section that cites
  dissent on the Wikipedia talk page and a study in which expert humans
  identified AI text at 45–53% accuracy.
- **Repository level:** a fact-check flag in the command-line tool, a score
  breakdown, and a pre-commit hook.
- **Detector claims:** the science page still frames burstiness and
  perplexity as what "AI detectors and this skill" both look at
  ([science.md](https://github.com/Aboudjem/humanizer-skill/blob/a58df065367550b6ce40ff3f648335018d8e0589/docs/science.md)).
  That describes perplexity-family detectors. It cites papers and reports no
  measurement of the skill's own output. The README says writing better is
  the goal, "not beating a detector".

### deslop (stephenturner/skills)

Unchanged. The default branch is still at the pinned commit `48287d8`, dated
2026-03-26, and the pinned path resolves
([SKILL.md](https://github.com/stephenturner/skills/blob/48287d806e61534bc14939b55b72c3f3f11a7db5/deslop/SKILL.md)).
The same author also publishes the skill alone as stephenturner/skill-deslop
(438 stars, one commit, 2026-03-18).

### anti-slop (elithrar/dotfiles)

One commit touches the skill since the pin, on 2026-09-05
([a2a5f65](https://github.com/elithrar/dotfiles/commit/a2a5f651d8a67813f9c50d49dd557e3e20f98238)).

- **Changed:** the entry file shrank by about 95 lines to four paragraphs.
  The tell catalog, the examples, and the "what to keep" list moved to a
  reference file
  ([tells.md](https://github.com/elithrar/dotfiles/blob/eb4f994e0c1ebe1199f032f4e5fe1633d1b8067c/.agents/skills/anti-slop/references/tells.md)).
- **Removed:** the drafting workflow, the guardrails list, and the review
  checklist. The description now says ordinary drafting does not require the
  skill.
- **Added:** "Stylistic patterns cannot establish whether a person or model
  wrote a passage", and an instruction not to treat the vocabulary list as
  banned words. "Statistically flagged AI vocabulary" became "often overused
  vocabulary; assess it in context"
  ([SKILL.md](https://github.com/elithrar/dotfiles/blob/eb4f994e0c1ebe1199f032f4e5fe1633d1b8067c/.agents/skills/anti-slop/SKILL.md)).
- **Detector claims, evaluation:** none.

### soundshuman

Unchanged. The default branch is still at the pinned commit `a45cfbb`, dated
2026-08-08
([SKILL.md](https://github.com/aashaexo/soundshuman/blob/a45cfbba9fde843d670e553a0aa98f6a23d7fb28/SKILL.md)).
MIT, 306 stars.

### anti-ai-slop-writing (jalaalrd)

Unchanged. The default branch is still at the pinned commit `63255f9`, dated
2026-04-19
([SKILL.md](https://github.com/jalaalrd/anti-ai-slop-writing/blob/63255f9bbb75a265dc5786a04535cd033f487756/skills/anti-ai-slop-writing/SKILL.md)).
The repository has no license file. 598 stars.

### What the changes have in common

**Inferred:** from the five changed skills above.

- Four of the five cut rules or procedure: no-ai-slop dropped its voice
  note, the cursor plugin dropped its self-audit and its "soul" section,
  elithrar reduced its entry file to four paragraphs, and blader went from 35
  patterns to 26.
- Three added statements that style cannot establish authorship or that
  detectors are not the goal (blader, elithrar, Aboudjem).
- Two removed rules that Wikipedia reclassified (blader, the cursor plugin).
  Animize still carries false ranges, synonym cycling, promotional
  adjectives, and cutoff disclaimers.
- None added a measurement against any detector.

## Sources not reached, excluded, or unverified

- **AhmadHassan-BTed/Turnitout-Humanizer** (12,015 stars, 288 forks).
  Excluded. It is a program that strips zero-width characters and metadata
  and advertises bypassing Turnitin, GPTZero, Copyleaks, and ZeroGPT. It is
  not a writing rule set. I read only the top of its README and record no
  result from it. Its ratio of about 42 stars per fork is far outside the 9
  to 16 of the other repositories in the top eight.
- **proseify.xyz/anti-prose-slop** (53,204 registry installs). Not surveyed.
  Its skills.sh page returned 404. The skill archive I found is a fiction
  writing skill that depends on a keyed server, which I did not sign up for.
  Its one idea of note is retrieving three to five human passages from a
  public-domain corpus and matching their rhythm.
- **skills.sh rendered pages.** The leaderboard is drawn in the browser and
  returned nothing to a plain fetch. Install counts come from the site's
  search endpoint instead.
- **LifelongLazyLearner/qu-ai-wei** (743 stars, MIT, Chinese). Found and not
  read.
- **realrossmanngroup/no_ai_slop_writing_rules** (710 stars, no license).
  Searched, not read in full. Its detection reference has a burstiness
  threshold by sentence word count
  ([file](https://github.com/realrossmanngroup/no_ai_slop_writing_rules/blob/35e32ae45878148a6bd898572a9d15c96711affe/skills/no-ai-slop/references/ai-writing-detection.md)).
- **Third-party detector studies cited by sepia.** Read only as sepia
  summarizes them, not at their sources.
- **A watermarking claim.** One repository's runbook says a vendor announced
  text watermarking in August 2026 for its newer models
  ([runbook](https://github.com/epoko77-ai/im-not-ai/blob/b37e0206d31fffd9149bf57168d4d62eb2086bee/docs/watermark-baseline-runbook.md)).
  I did not verify it. If true it would matter more than any style rule, so
  it is worth a separate check.
- **Pangram blog figures.** Vendor's own, for models earlier than Pangram 4.
- **Excluded as off topic:** heydamir/unslop (interface design), a .NET
  string library that shares the "humanizer" name, and
  coreyhaines31/marketingskills/copy-editing, a general copy-editing skill
  with 159,042 installs that is not about AI tells.
