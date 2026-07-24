# Evidence note for a prose-editing “humanization” skill

Date: 2026-07-23

## Bottom line

The skill should improve clarity, specificity, and fidelity to the writer’s
intent. It should not infer authorship, promise detector evasion, or treat a
list of stylistic “tells” as rules. Surface patterns can be useful editing cues
and can support probabilistic review in a validated, matched setting, but they
are not proof about an individual text.

## Detection, false positives, and non-native writers

- A 2023 study tested seven detectors on 91 TOEFL essays by non-native English
  writers and 88 US eighth-grade essays. The detectors’ average false-positive
  rate on the TOEFL essays was 61.3%; all seven flagged 19.8% of those essays,
  and at least one flagged 97.8%. Vocabulary enrichment reduced the average
  false-positive rate to 11.6%. This demonstrates a serious failure mode in
  those detectors and samples, not a universal rate for all detectors or
  non-native writers. ([Liang et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/))
- The evidence is not one-directional. Purpose-built detectors trained on
  well-sampled GRE writing achieved near-perfect performance and showed no
  evidence of disadvantaging non-native English writers. Detector bias is
  therefore dependent on the detector, training data, language, domain, and
  target population; the skill should not claim that every detector is biased
  in the same way. ([Jiang et al., 2024](https://doi.org/10.1016/j.compedu.2024.105070))
- In a 54-document test of 14 tools, every tool scored below 80% accuracy,
  false-positive rates ranged from 0% to 50%, and translation, manual editing,
  and paraphrasing degraded performance. The authors rejected these tools as
  standalone evidence of misconduct. The sample and tools were limited to
  2023, so the result establishes risk, not a permanent ceiling.
  ([Weber-Wulff et al., 2023](https://link.springer.com/article/10.1007/s40979-023-00146-z))
- The larger RAID benchmark—more than six million generations across 11
  models, eight domains, 11 attacks, and four decoding strategies—found that
  12 detectors were vulnerable to adversarial edits, decoding changes, and
  unseen generators. This is evidence against carrying a detector’s benchmark
  accuracy into an unmatched real-world setting.
  ([Dugan et al., 2024](https://aclanthology.org/2024.acl-long.674/))
- A peer-reviewed theoretical and empirical study showed that paraphrasing can
  sharply reduce several detector families’ performance and that, as human and
  machine text distributions converge, even the optimal text-only detector’s
  performance approaches chance. This does **not** mean every detector performs
  at chance in every bounded setting.
  ([Sadasivan et al., 2025](https://openreview.net/pdf?id=OOgsAZdFOt))
- Official UK education guidance likewise warns that false positives can
  unfairly penalize students and recommends a holistic investigation, including
  discussion with the student and evidence of the work’s process.
  ([UK Department for Education, 2025](https://assets.publishing.service.gov.uk/media/6842f27f57f3515d9611f067/Module_3_Developing_the_safe_use_of_AI_in_education_-_Transcript.pdf))

### What surface markers can support

Surface features do contain population-level signal. A large matched-corpus
study found systematic grammatical and rhetorical differences between human
text and outputs from several models, but the differences also varied by model
family and tuning; its classifier still mislabeled 9.8% of human texts.
([Reinhart et al., 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11874169/))
A separate study found that a five-person majority of frequent writing-tool
users mislabeled only one of 300 English nonfiction articles, using lexical
clues together with broader judgments about formality, originality, and
clarity. That result shows that combined cues can be informative in a bounded
sample, not that any word, punctuation mark, or construction proves authorship.
([Russell et al., 2025](https://aclanthology.org/2025.acl-long.267/))

**Supported inference:** use alleged “AI markers” only to locate prose worth
reviewing—for example, vague claims, repetitive transitions, unsupported
significance, or broken citations. Judge and edit the underlying defect. Do not
emit an AI-likelihood score or an authorship verdict.

## Editing principles

### Established or institutionally supported

- **Write for a defined audience and task.** CDC guidance recommends stating
  the main message early, using language familiar to the intended audience,
  grouping one idea at a time, and pretesting with that audience. The same
  guide says its checklist cannot replace audience research or testing.
  ([CDC Clear Communication Index guide](https://www.cdc.gov/ccindex/pdf/clear-communication-user-guide.pdf))
- **Plain language can improve comprehension, but not universally.** In a
  randomized trial of 488 adults, a plain-language health-recommendation format
  improved understanding and usability relative to the standard format.
  ([Sayfi et al., 2024](https://doi.org/10.1016/j.jclinepi.2023.11.009))
  A related randomized trial of 268 youths found no statistically significant
  comprehension improvement. ([Pottie et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10407760/))
  The safe rule is to improve for the actual audience and verify the result,
  not to equate shorter or simpler prose with universally better prose.
- **Prefer concrete actors, actions, and details when they resolve ambiguity.**
  Federal guidance recommends concrete wording and gives specific behavioral
  directions rather than vague abstractions.
  ([National Archives](https://www.archives.gov/federal-register/write/legal-docs/clear-writing.html),
  [CDC guide](https://www.cdc.gov/ccindex/pdf/clear-communication-user-guide.pdf))
  An editor should never invent examples, evidence, or precision that the
  source text does not support.
- **Use active voice when the actor or responsibility matters; do not ban the
  passive.** Federal guidance explicitly retains passive voice when the actor
  is unknown, unimportant, or obvious, and the NCBI style guide treats both
  voices as useful choices of emphasis.
  ([National Archives](https://www.archives.gov/federal-register/write/legal-docs/clear-writing.html),
  [NCBI Style Guide](https://www.ncbi.nlm.nih.gov/books/NBK993/))
- **Preserve meaning and authorial voice through minimal intervention.**
  Professional editorial standards say to change only what is required and to
  maintain voice, tone, and register without altering intended meaning. This is
  a professional norm, not an authorship-detection result.
  ([Editors Canada Professional Editorial Standards](https://editors.ca/publications/professional-editorial-standards/stylistic-editing/))

### Preliminary evidence and editorial heuristics

A 2026 preprint found that three models systematically normalized 300 personal
narratives across 13 style markers. An explicit voice-preservation instruction
reduced the mean magnitude of change by 32% but did not remove its direction.
This is preliminary, single-study evidence, but it supports localized edits and
source-to-revision comparison rather than whole-text rewriting.
([van Nuenen, 2026](https://arxiv.org/abs/2604.22142))

Varying sentence length, removing stock transitions, retaining contractions,
and keeping characteristic diction may be useful editorial heuristics when
they fit the writer and genre. They are not validated tests of humanity. Do not
add errors, slang, random punctuation, or fabricated personal detail to make
text appear “human.”

## Claims the skill should not make

- “This text was written by AI” or “this text is human” based on prose alone.
- “These words, em dashes, sentence lengths, or transitions are uniquely AI.”
- “All detectors are useless” or, conversely, “a detector score proves
  authorship.”
- “All non-native writers are penalized by all detectors.”
- “Removing these markers will bypass detection.”
- “Active voice, shorter sentences, or plain language always improve a text.”
- “A voice-preserving prompt guarantees preservation of the author’s voice.”
- “Wikipedia’s list is a policy or a scientifically validated diagnostic.”
  The page describes itself as an unreviewed advice page, calls its list
  descriptive rather than prescriptive, and says the indicators are not
  sufficient on their own.
  ([pinned revision](https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&oldid=1365519760))

## Adapting Wikipedia’s “Signs of AI writing”

The pinned revision is published under CC BY-SA 4.0.
([page footer](https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&oldid=1365519760))
If the skill copies or closely adapts the page’s expressive wording, examples,
or distinctive organization, Wikimedia’s reuse terms require:

1. Attribution, which may be a link to the reused page because its history
   identifies contributors.
2. A clear indication that changes were made.
3. A CC BY-SA license notice and link (or a copy of the license).
4. CC BY-SA 4.0 or later for the modified or added adapted content.

([Wikimedia Terms of Use, §§7–8](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use#7._Licensing_of_Content),
[CC BY-SA 4.0 deed](https://creativecommons.org/licenses/by-sa/4.0/deed.en))

A suitable notice is:

> Adapted from Wikipedia contributors, “[Wikipedia:Signs of AI
> writing](https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&oldid=1365519760),”
> revision 1365519760. Changes were made. The adapted material is licensed
> under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

Facts and ideas are not protected by copyright, and Creative Commons states
that its license conditions do not apply where copyright does not apply.
([Creative Commons FAQ](https://creativecommons.org/faq/))
The lowest-risk route is therefore to derive the skill’s rules independently
from primary evidence, avoid tracking Wikipedia’s wording or organization, and
link to the page only as acknowledged inspiration. This licensing summary is
general information, not legal advice.
