# Pangram AI-text detector: how it works and what moves its verdict

Date: 2026-11-09. Source: Pangram Labs' technical reports, papers, engineering
blog, model card, and API documentation, plus independent papers and reports
that tested Pangram, each read at the URL cited next to the claim. A bullet is
stated by the source it cites unless it is marked **Inferred:** (my reading,
with the sources it rests on) or **Not found:** (no source read answers it).
Every rate carries the Pangram version and date it was measured on: the
production model was replaced several times in the period covered, and a
figure from one version does not transfer to another. The live model on this
date is Pangram 4.1
([model card, 2026-10-19](https://www.pangram.com/research/model-card)).
Nothing here comes from calling Pangram's API.

## Summary for benchmarking against the live verdict

1. **The verdict is decoded from per-token provenance labels.** Pangram 4
   labels each token human, AI-assisted, or AI-generated over 512-token
   windows at stride 256, smooths the labels with a CRF, snaps them to
   sentences, and reports fractions of the document by character count, with
   `prediction_short` of "AI", "Human", or "Mixed"
   ([Pangram 4 report](https://arxiv.org/abs/2607.27183),
   [API reference](https://docs.pangram.com/api-reference/ai-detection)).
   Pangram's own evaluation rule is Human when the human fraction is at least
   0.90, AI when the AI fraction is at least 0.80, and Mixed otherwise. The
   production rule that turns fractions into a `headline` string is not
   published.
2. **The benchmark measures learned stylistic provenance.** Training pairs
   each human document with a model-written mirror on the same topic so that
   topic and length carry no signal; Pangram says it does not rely on
   perplexity or burstiness and that removing its highlighted phrases does not
   lower the score ([Pangram 4 report](https://arxiv.org/abs/2607.27183),
   [knowledge hub](https://www.pangram.com/knowledge-hub/does-pangram-use-perplexity-and-burstiness),
   [editing post](https://www.pangram.com/blog/can-you-avoid-ai-detection-through-editing)).
   Pangram also calls the predictions "to some degree a black box".
3. **Published error rates hold only inside the stated scope.** Pangram 4.1
   reports an FPR of 0.0090% (70 of 781,981 English documents) and an FNR of
   0.3652% (1,899 of 520,000 outputs from 26 models), with any Mixed verdict
   counted as an error
   ([model card](https://www.pangram.com/research/model-card)). The scope is
   prose of at least 50 words in complete sentences. Markdown, code, templated
   writing, instructions, and reference sections are out of scope. A benchmark
   that submits Markdown or short text measures outside those conditions.
4. **Length and context move the verdict.** On 4.1 the FNR is 1.29% at 50 to
   99 words and 0.21% at 250 to 499 words
   ([accuracy post](https://www.pangram.com/blog/is-pangram-accurate)). The
   same passage can score differently alone and inside a longer document
   ([Pangram 4 report](https://arxiv.org/abs/2607.27183)). Pangram 4.1 reports
   that unintended verdict flips across 29,103 paired small edits fell from
   1.08% on Pangram 4 to 0.15%
   ([model card](https://www.pangram.com/research/model-card)).
5. **Most tested methods leave model-written text detected on Pangram 4, by
   Pangram's own measurements.** Thirteen commercial humanizers left 97.67% of
   text labeled AI-generated; a prompt-instruction skill for removing AI
   writing signs left a false-negative rate of 0.430%; synonym and character
   perturbations left 99.96% or more detected
   ([Pangram 4 report](https://arxiv.org/abs/2607.27183)). The second section
   gives every entry with its conditions.
6. **Independent tests exist only for earlier versions, and some found large
   effects.** One commercial humanizer moved Pangram 3.0's "AI" verdicts from
   100% to 44.6%, with another 48.2% "Mixed"
   ([Saha et al., 2026](https://arxiv.org/abs/2603.20450)). Few-shot imitation
   of a human author gave a 10.1% false-negative rate on 3.3.2, and 25% on
   scientific text
   ([Epoch AI, 2026](https://epoch.ai/data-insights/ai-detectors-false-negatives)).
   Text from author-specific fine-tuned models was flagged 3% of the time
   against 97% for prompted text
   ([Chakrabarty et al., 2025](https://arxiv.org/abs/2510.13939)).
   Continuations from a base model scored 98.8% human against 17.1% for the
   instruction-tuned model
   ([Xu et al., 2026](https://arxiv.org/abs/2605.19516)). **Not found:** an
   independent paper or report that measured Pangram 4 or 4.1 against any of
   these methods.
7. **AI editing of human text is where the label is least settled.** Pangram 4
   calls 99.45% of lightly polished student essays Human, but splits text
   edited under open rewriting prompts into 41.37% Human, 55.01% Mixed, and
   3.62% AI, and Pangram says it "leans human when encountering mixed text"
   ([Pangram 4 report](https://arxiv.org/abs/2607.27183),
   [accuracy post](https://www.pangram.com/blog/is-pangram-accurate)).
   **Inferred:** a benchmark of edited human drafts will see Human and Mixed
   outcomes that track how much text was rewritten.
8. **Record the version with every score.** The `pangram-4` selector can
   change minor version without the selector changing, and the response's
   `version` field says which one answered
   ([models reference](https://docs.pangram.com/api-reference/models)). Rates
   moved materially from 3.3.2 to 4 and again from 4 to 4.1.

## Methods that change the verdict on model-written text

Status: stated for every entry below except where marked. Entries keep the
level of detail the source reports. "Pangram's run" marks a public benchmark
that Pangram scored itself in its own report; the benchmark's authors did not
publish Pangram results unless the entry says so. **Not found:** any
independent measurement on Pangram 4 or 4.1 for any method class; Pangram
itself notes that the largest third-party evaluation was run "over a year ago"
and asks for new ones
([call for evaluations, 2026-11-06](https://www.pangram.com/blog/a-call-for-new-pangram-evaluations)).

### Paraphrasing tools

- **Masrour, Emi, and Spero, "DAMAGE" (Pangram, 2025-01-06; baseline and
  humanizer-augmented models of that date)**
  ([arXiv 2501.03437](https://arxiv.org/abs/2501.03437)). The paper audits 19
  tools, three of them paraphrasers (DIPPER, Grammarly, Quillbot). On the RAID
  benchmark's paraphrase and synonym splits, TPR at 5% FPR was 91.6% and 96.2%
  for the baseline and 93.0% and 97.0% for the augmented model. The same paper
  reports DIPPER cutting the SynthID watermark's TPR at 1% FPR from 66.5% to
  1.5%; that result is about a watermark, not Pangram.
- **Pangram post (2025-08-27; production model of that date)**
  ([humanizer table](https://www.pangram.com/blog/humanizers-aug-25)).
  Accuracy on tool output: DIPPER 97.6%, Quillbot 100%, Grammarly 100%. No
  quality measure.
- **Russell, Karpinska, and Iyyer (independent; ACL 2025; early-2025 Pangram
  models)** ([arXiv 2501.15654](https://arxiv.org/abs/2501.15654)). On 30
  GPT-4o articles given an additional round of paraphrasing, both the base
  Pangram model and the "Pangram Humanizers" model had 100% TPR with 0% FPR on
  the 30 paired human articles. The paper states that "neither paraphrasing
  nor humanization effectively removes all of these signatures".
- **Xu et al., "Base Models Look Human To AI Detectors" (independent; preprint
  2026-05-19; Pangram version not stated, before Pangram 4)**
  ([arXiv 2605.19516](https://arxiv.org/abs/2605.19516)). Of the existing
  paraphrase baselines tested on Pangram, "only DIPPER still achieves a
  non-trivial semantic-evasion trade-off", and "Both Simple Paraphrase and
  StealthRL fail to achieve a meaningful trade-off on either detector". The
  homoglyph method SilverSpeak "raises Pangram human probability slightly".
  The paper's own method, a paraphraser built from a minimally fine-tuned base
  model and applied for up to 10 rounds, raises Pangram's human probability
  while a 0-to-10 semantic-preservation score assigned by a judge model
  declines gradually; the numbers are in figures only. The same method run
  through a hosted fine-tuning API on an instruction-tuned model failed: the
  human probability "quickly falls and remains low". The authors caution that
  "detector-evasion results are unlikely to remain static".
- **MELD-eval, Pangram's run on Pangram 4 (2026-07-29)** (Table 26,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)). TPR at 1% FPR on
  31,448 AI texts per attack, attacks applied to the AI text only: none
  100.00%, synonym substitution 99.96% (10 false negatives; 85 on Pangram
  3.3.2, 99.72%), homoglyph 99.97%, upper-lower flip 99.99%, whitespace
  99.99%, number perturbation 100.00%, zero-width space 100.00%; 21 false
  negatives in 220,136 overall.
- **DetectRL, Pangram's run** (Table 24,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)). Average F1 95.30 for
  Pangram 4 against 96.70 for Pangram 3.3.2, with 96.00 on the multi-attack
  split. This is one benchmark where Pangram reports the newer model slightly
  below the older one.

### Humanizer tools

- **Masrour, Emi, and Spero, "DAMAGE" (Pangram, 2025-01-06)**
  ([arXiv 2501.03437](https://arxiv.org/abs/2501.03437)). Describes humanizers
  as "a new class of online software tools meant to paraphrase and rewrite
  AI-generated text in a way that allows them to evade AI detection software"
  and sorts 19 tools into three fluency tiers. At default thresholds the
  baseline detected 100% of unmodified AI academic text and 73.07% after
  humanization, with a 0.27% FPR; the augmented model detected 97.47% of
  humanized text with a 3.40% FPR. At a fixed 5% FPR the figures are 95.74%
  and 98.26%; GPTZero scored 60.04% and Binoculars 28.23% on the same
  humanized set. Quality cost: a GPT-4o judge preferred the humanized version
  over the original 26.0% of the time for the best tier, 14.67% for the middle
  tier, and 2.67% for the worst, and the authors conclude that "all humanizers
  tend to degrade the quality of the original text". A humanizer the authors
  fine-tuned on the detector's own false negatives was still detected 93.2% of
  the time at the default threshold, with a fluency win rate of 14.13%.
- **Pangram post (2025-08-27; production model of that date)**
  ([humanizer table](https://www.pangram.com/blog/humanizers-aug-25)).
  Per-tool accuracy on humanized AI text ran from 90.3% (Undetectable AI) to
  100%, with TwainGPT 92.7%, Just Done 93.5%, humanizeai.io 93.8%, and
  StealthGPT 95.6%. Pangram states: "The more readable/fluent the humanizer
  text is, the more likely it is to be detected". It also says internal models
  that detect humanizers near-perfectly had a higher false positive rate and
  were not shipped.
- **Jabarian and Imas (independent; working paper dated 2025-08-26; Pangram
  "API v2025-05")**
  ([BFI WP 2025-116](https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf)).
  Every AI passage was sent through the StealthGPT default rewrite endpoint.
  Pangram's FNR on the rewritten text ranged from 0.0000 to 0.0500 by genre
  and generating model (0.0500 for Gemini 2.0 Flash Amazon reviews, 0.0400 for
  Claude Opus 4 Amazon reviews, 0.0000 for novels and resumes), against
  roughly 0.25 to 0.77 for GPTZero. No quality measure.
- **Saha et al. (independent; ICML 2026; "Pangram version 3.0 dated
  03.01.26")** ([arXiv 2603.20450](https://arxiv.org/abs/2603.20450)). Fully
  AI-written peer reviews were passed once through the Undetectable AI API.
  Pangram's "AI" verdicts fell from 100% to 44.6%; another 48.2% were "Mixed",
  so 92.8% were still not "Human". GPTZero's TPR fell from 96.7% to 86.7%. The
  authors note the experiments "only simulate a single pass through an
  off-the-shelf humanizer". No quality measure for the humanized reviews.
- **Pangram release notes (3.2 on 2026-02-27; 3.3 on 2026-05-13)**
  ([3.2](https://www.pangram.com/blog/introducing-pangram-3-2),
  [3.3](https://www.pangram.com/blog/meet-pangram-3-3)). Relative claims on
  internal sets only: 3.2 improved the humanizer detection rate "by 4x
  compared to Pangram 3.1", and 3.3 reports "catching twice as many
  commercially humanized texts as its predecessor". No absolute rates.
- **Pangram 4 report (Pangram's own test; Pangram 4; 2026-07-29)** (sec. 5.9.1
  and Table 14, [Pangram 4 report](https://arxiv.org/abs/2607.27183)).
  Thirteen commercial humanizers chosen by web traffic in early 2026: "We
  detect humanized text as AI-generated 97.67% of the time and as either Mixed
  or AI-generated 98.83% of the time." Per-tool AI recall ran from 92.78% to
  99.70%. No quality measure. The qualitative defects Pangram describes in
  humanizer output (changed punctuation and casing, removed spaces,
  hallucinated content, "tortured phrases") are in a separate post without
  rates
  ([2026-02-27](https://www.pangram.com/blog/ai-humanizers-the-slop-2-problem)).
- **Public benchmarks, Pangram's run on Pangram 4** (Table 12 and Appendix C,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)). On the Jabarian and
  Imas humanizer split, TPR at 1% FPR was 98.93% at full length (N = 15,932;
  Pangram 3 98.08%, GPTZero 44.32%, Originality 28.49%) and 73.32% under 50
  words (Pangram 3 61.74%). On GEDE's humanized subset (N = 189) it was
  100.0%. On the Perkins et al. manipulated-text set (N = 89) mean accuracy
  was 94.1% against 100.0% on the 15 unmanipulated texts (Copyleaks 58.7%,
  GPTZero 16.7%, Turnitin 7.9% on manipulated text).
- **Van Vlasselaer, Van Droogenbroeck, and Spruyt (independent; published
  June 2026)**
  ([Int. J. Educational Integrity 22:16](https://doi.org/10.1007/s40979-026-00226-w)).
  The abstract says the humanised condition was produced with "a prompt
  designed to resemble possible student behaviour", so it is listed under
  prompt-level instructions below.

### Prompt-level style and persona instructions

- **Russell, Karpinska, and Iyyer (independent; ACL 2025; early-2025 Pangram
  models)** ([arXiv 2501.15654](https://arxiv.org/abs/2501.15654)). The
  authors' humanization is a prompt for o1-Pro built from their expert
  annotators' explanations of what gives AI text away. On 30 such articles the
  base Pangram model's TPR was 90.0% (FPR 6.7% on the paired human articles)
  and the Pangram Humanizers model's was 96.7% (FPR 10%), against 100% for
  both on unhumanized o1-Pro articles. GPTZero fell to 46.7%, Fast-DetectGPT
  to 23.3%, and Binoculars to 6.67%.
- **Epoch AI, Lee (independent report; 2026-07-15; Pangram 3.3.2)**
  ([data insight](https://epoch.ai/data-insights/ai-detectors-false-negatives)).
  The model was asked to imitate a specific human author given five reference
  passages of about 500 words. Directly prompted text had 0 false negatives in
  297; imitation text had 30 in 297 (10.10%, 90% CI 7.58 to 13.35), with 0
  false positives on 495 human passages. By genre: blog 4%, fiction 1%,
  scientific 25%. By model: Claude Opus 4.8 5%, GPT-5.5 5%, Gemini 3.1 Pro
  20%, and 48% (16 of 33) for Gemini on scientific text. Only a clean "AI"
  verdict counts as detection; counting Mixed as detection lowers the rate
  "from 10.1% to 6.1% for Pangram". The report says: "We test a single evasion
  method" and did not test "paraphrasing tools, manual editing, or other
  approaches". No quality measure.
- **The same benchmark, Pangram's run on Pangram 4 (2026-07-29)** (Table 23,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)). Document-level FNR
  across both AI conditions together: 2.86% (17 of 594) for Pangram 4 against
  5.05% (30 of 594) for 3.3.2, with 0 of 495 false positives. The report does
  not split the 17 by condition.
- **Pangram 4 report (Pangram's own test; Pangram 4)** (Table 15,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)). A public repository
  of instructions for LLMs on how to "remove signs of AI-generated writing
  from text" was used to prompt three frontier models to rewrite generated
  text. False negatives: 17 of 3,404 for GPT-5.5 (0.499%), 14 of 3,412 for
  Opus 4.8 (0.410%), 13 of 3,407 for Sonnet 4.6 (0.382%); 44 of 10,223 overall
  (0.430%). No quality measure.
- **Pangram 4 report, automated red-teaming (Pangram 4, pre-release)** (sec.
  5.9.2, [Pangram 4 report](https://arxiv.org/abs/2607.27183)). An agent with
  API access for 24 hours tested hypotheses including "imitating specific
  human voices and styles, using different operational and professional
  registers, imitating a notetaker, using much terser vocabulary". Pangram
  reports: "The only bypass explicitly found by the agent was acting as a
  surgeon/pathologist dictating notes aloud", which it ruled out of scope
  because the outputs resembled "extremely terse factual bullets rather than
  open-ended prose". No rates are given.
- **Chakrabarty, Ginsburg, and Dhillon (independent; preprint v4 2026-03-17;
  Pangram version not stated)**
  ([arXiv 2510.13939](https://arxiv.org/abs/2510.13939)). Excerpts of up to
  450 words written by GPT-4o, Claude 3.5 Sonnet, and Gemini 1.5 Pro under
  in-context prompting to emulate one of 50 authors were classified as
  machine-generated 97% of the time at a 0.9 threshold.
- **Van Vlasselaer et al. (independent; 2026)**
  ([abstract](https://doi.org/10.1007/s40979-026-00226-w)). 160 synthetic
  documents in four conditions; the abstract says Pangram "consistently
  performed better" than the other three tools. Pangram's summary of the paper
  gives detection rates of 97.5% on fully AI text, 95% on humanised text, and
  0% false positives
  ([third-party evaluations post](https://www.pangram.com/blog/third-party-pangram-evals)).
  I could not reach the full text to confirm those figures or the Pangram
  version.
- **Pangram release notes**
  ([3.2](https://www.pangram.com/blog/introducing-pangram-3-2),
  [3.3](https://www.pangram.com/blog/meet-pangram-3-3)). Each release claims
  roughly a threefold improvement over its predecessor on an internal set of
  adversarial prompts, which the 3.2 post describes as "texts generated by a
  language model that has been instructed to intentionally add mistakes and
  write in a style that evades AI detection". No absolute rates.

### Choice of generating model

- **Pangram 4 report (Pangram 4 and 3.3.2; 2026-07-29)** (Table 3,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)). FNR on 20,000 chat
  prompts per model across 26 models. Pangram 4 ranges from 0.130% (Claude
  Haiku 4.5) to 0.605% (Grok 4.3); by family, Claude 0.195%, GPT 0.316%,
  DeepSeek 0.388%, Gemini 0.498%. Pangram 3.3.2 on the same texts ranged from
  0.300% to 6.380% (Gemini 3.1 Pro Preview), with Llama 3.3 70B at 4.405%.
  Pangram finds "no significant correlation between release date and FNR".
- **Pangram 4.1 model card (2026-10-19)**
  ([model card](https://www.pangram.com/research/model-card)). Same benchmark:
  Claude family 0.181%, GPT family 0.323%, Gemini 3.1 Pro 0.600%, Llama 3.3
  70B 0.720%, Grok 4.3 0.720%. Spot checks on four models released in
  September 2026 are 0.29% to 0.41%
  ([accuracy post](https://www.pangram.com/blog/is-pangram-accurate)).
- **Epoch AI (independent; Pangram 3.3.2)**
  ([data insight](https://epoch.ai/data-insights/ai-detectors-false-negatives)).
  Under author imitation the false-negative rate was 20% for Gemini 3.1 Pro
  against 5% each for Claude Opus 4.8 and GPT-5.5.
- **Jabarian and Imas (independent; Pangram "API v2025-05")**
  ([BFI WP 2025-116](https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf)).
  FNR at a 0.5 threshold: GPT-4.1 0.0131, Claude Sonnet 4 0.0151, Claude Opus
  4 0.0216, Gemini 2.0 Flash 0.0272.
- **Xu et al. (independent; preprint 2026-05-19; version not stated)**
  ([arXiv 2605.19516](https://arxiv.org/abs/2605.19516)). For Llama-3-8B
  continuing single-sentence human prefixes, "GPTZero and Pangram assign human
  probabilities of 96.7% and 98.8% to the base model's continuations,
  respectively, and 30.3% and 17.1% to the instruct model's continuations".
  The authors conclude that "current detectors are tracking artifacts of
  instruction tuning and local context more than any invariant notion of
  machine-generated text". Pangram's DAMAGE paper says of its training data:
  "We do not train on base models"
  ([arXiv 2501.03437](https://arxiv.org/abs/2501.03437)).
- **Chakrabarty, Ginsburg, and Dhillon (independent; version not stated)**
  ([arXiv 2510.13939](https://arxiv.org/abs/2510.13939)). Thirty GPT-4o
  models, each fine-tuned on one author's works: "only 3% of fine-tuned texts
  were classified as AI-generated", against 97% for in-context prompting.
  Human text was never misclassified. Quality: MFA-trained readers preferred
  the fine-tuned output over human-written excerpts, with odds ratios of 8.16
  for stylistic fidelity and 1.87 for writing quality. Median generation cost
  was $81 per author.
- **Emi and Spero, 2024 report (2024 model)**
  ([arXiv 2402.14873](https://arxiv.org/abs/2402.14873)). Recall above 99.6%
  on open-source models not seen in training.

### Human post-editing of model text

- **Not found:** a measurement of production Pangram, any version, on model
  text that people then edited by hand at scale. Epoch AI says it did not test
  manual editing
  ([data insight](https://epoch.ai/data-insights/ai-detectors-false-negatives)),
  and Saha et al. test only a tool pass
  ([arXiv 2603.20450](https://arxiv.org/abs/2603.20450)).
- **Thai et al., "EditLens" (Pangram; ICLR 2026; the research model, not the
  production detector)**
  ([arXiv 2510.03154](https://arxiv.org/abs/2510.03154)). On the BEEMO set of
  AI text edited by humans, the EditLens score fell by a mean of 0.33
  (standard deviation 0.30) and fell in 88.9% of documents.
- **Pangram post (2025-08-29; one essay, anecdotal)**
  ([editing post](https://www.pangram.com/blog/can-you-avoid-ai-detection-through-editing)).
  On a single generated essay, removing the highlighted AI phrases, swapping
  common words, and rewriting a sentence each left the result unchanged. The
  post says flagged text became undetected only when "a majority of the words
  have been completely replaced".
- **Pangram 4 technical post (2026-07-29)**
  ([technical post](https://www.pangram.com/blog/pangram-4-technical)). Cites
  outside research that "writers who edit LLM output toward their personal
  style still produce text that reads closer to LLM writing than to their
  own". This is a citation, not a Pangram measurement.
- **Label policy** ([Pangram 4 report](https://arxiv.org/abs/2607.27183),
  [Pangram 3.0 post](https://www.pangram.com/blog/introducing-ai-assistance-detection)).
  AI-Generated covers text "significantly more AI-authored than
  human-authored", and the 3.0 post says the top category "also includes text
  that is primarily AI-generated, or text that was initially generated by AI".

### Mixing in human-written text

- **Pangram 4 report (Pangram 4)** (Table 7,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)). Documents alternating
  N human sentences with N model sentences. Token-level recall of the AI spans
  rises with run length: 62.86% at N = 1, 85.43% at N = 4, 92.31% at N = 8,
  96.31% at N = 20, with precision between 92.82% and 99.66%. Document-level
  error in the AI fraction falls from 18.27% at N = 1 to 1.52% at N = 20.
  Overall token accuracy is 92.02% against 64.18% for 3.3.2.
- **Decode thresholds** (sec. 5.1,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)). In Pangram's
  evaluation rule a document is AI only when the AI fraction is at least 0.80
  and Human only when the human fraction is at least 0.90; everything between
  is Mixed. Pangram says it "leans human when encountering mixed text"
  ([accuracy post](https://www.pangram.com/blog/is-pangram-accurate)).
- **Saha et al. (independent; Pangram 3.0)**
  ([arXiv 2603.20450](https://arxiv.org/abs/2603.20450)). Reviews written by a
  model from a human's key points were labeled "AI" 100% of the time on the
  easier model set and 92.6% on the harder one, with 5.8% "Mixed". The authors
  read these reviews as mixed authorship that Pangram calls "AI" rather than
  "Mixed".
- **Xu et al. (independent; version not stated)**
  ([arXiv 2605.19516](https://arxiv.org/abs/2605.19516)). Continuations of
  human-written prefixes look "slightly more human than AI prefixes".
- **Van Vlasselaer et al. (independent; 2026)**
  ([third-party evaluations post](https://www.pangram.com/blog/third-party-pangram-evals)).
  Per Pangram's summary, 95% detection on the hybrid condition of human
  documents with model-inserted passages. Full text not reached.
- **Pangram 4 report, automated red-teaming** (sec. 5.9.2,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)). "conditioning its
  output on detailed source writing" and "aggregating multiple AI documents
  together" were among the hypotheses tested without a reported bypass. No
  rates.

## Training

Status: stated, with gaps marked.

- **Human side.** The 2024 model drew on a pool of about 28 million human
  documents from 2021 and earlier, open and licensed for commercial use, with
  4 million held out ([2024 report](https://arxiv.org/abs/2402.14873)).
  Pangram 4's human data is "either openly licensed for commercial use or
  their rights are owned by the company" and the model is "not trained on
  user-submitted data, customer data from API users, or data obtained by
  unauthorized Internet crawls"
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **AI side: synthetic mirrors.** For each human document a model writes a
  counterpart matched on topic and length. The 2024 prompts were hand-tuned
  per domain and some asked the model to continue from an excerpt of the human
  text ([2024 report](https://arxiv.org/abs/2402.14873)). Pangram 4 uses two
  steps: ask a model for the document's topic, then ask for an article on that
  topic, grounded in titles or keywords where available, and discard mirrors
  that repeat much of the source verbatim. The stated aim: "We want the model
  to learn “How was this text written?” as opposed to “What is this text
  about?”" ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Which models.** Pangram 4 used 75 models "including all presently
  available OpenAI and Anthropic models"
  ([technical post](https://www.pangram.com/blog/pangram-4-technical)). The
  2025 model used GPT-3.5 through GPT-4o, Claude 2 and 3, Llama 2 to 3.1,
  Mistral, and Gemini, all instruction-tuned
  ([DAMAGE](https://arxiv.org/abs/2501.03437)).
- **AI-assisted examples.** Generated by applying editing prompts to human
  text. EditLens used 303 editing prompts with GPT-4.1, Claude Sonnet 4, and
  Gemini 2.5 Flash over 60k training, 6k validation, and 2.4k test examples
  ([EditLens](https://arxiv.org/abs/2510.03154)). Pangram 4 follows that
  method and labels each clause of the edited text against the source
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)); the label rule is
  under "Label set".
- **Hard-negative mining.** In 2024: train on 40,000 examples per domain, run
  the model over the human pool, take up to 10,000 false positives per domain,
  mirror them, add both, retrain, and repeat. Domain-weighted FPR on the
  holdout fell from 2.29% to 0.02%
  ([2024 report](https://arxiv.org/abs/2402.14873)). Pangram 4 runs one
  offline round that finds "human text that the current checkpoint labels as
  AI", mirrors it, and then "Pangram 4 is then retrained from scratch"
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Bias toward low FPR.** A wrong call on a human document is weighted "by a
  much heavier factor" in the loss than a wrong call on an AI document, and
  thresholds are calibrated
  ([false positives post, 2025-09-15](https://www.pangram.com/blog/all-about-false-positives-in-ai-detectors)).
  "We deliberately tune Pangram to be more inclined to produce false negatives
  rather than false positives"
  ([accuracy post](https://www.pangram.com/blog/is-pangram-accurate)).
- **Humanizer data, 2025 model.** Output of the best-fluency tier of
  humanizers was added for both human and AI documents at 0.68% of the
  dataset, oversampled 18 times; humanized human documents kept the human
  label. Adding all tiers raised the default-threshold FPR to 6.00%
  ([DAMAGE](https://arxiv.org/abs/2501.03437)).
- **Cadence.** February 2024 first report; May 2024 update for GPT-4o four
  days after its release
  ([2024 update post](https://www.pangram.com/blog/updating-pangram-text-gpt4o));
  January 2025 humanizer model
  ([announcement](https://www.pangram.com/blog/humanizers-announcement)); 3.0
  on 2025-12-11
  ([3.0 post](https://www.pangram.com/blog/introducing-ai-assistance-detection));
  3.2 on 2026-02-27 with data regenerated from Claude Opus 4.6
  ([3.2 post](https://www.pangram.com/blog/introducing-pangram-3-2)); 3.3 on
  2026-05-13, then 3.3.1 and 3.3.2 within five days
  ([3.3 post](https://www.pangram.com/blog/meet-pangram-3-3)); 4 on
  2026-07-29, with Pangram 3 deprecated on 2026-09-30
  ([Pangram 4 post](https://www.pangram.com/blog/introducing-pangram-4)); 4.1
  on 2026-10-19 with "No change from Pangram 4" in training and inference
  ([model card](https://www.pangram.com/research/model-card)).
- **Not found:** the size of the Pangram 4 training set, the names of its
  human corpora, and the backbone's identity.

## Model and inference

Status: stated for the architecture and decode; the headline mapping is not
found.

- **Backbone.** Pangram 4 is "based on a popular open-weight MoE model",
  unnamed, fine-tuned with LoRA, with linear heads
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)). It is "our largest
  model yet, with 6x as many parameters as Pangram 3.3"
  ([technical post](https://www.pangram.com/blog/pangram-4-technical)).
  Earlier disclosures: a 12-billion-parameter Mistral NeMo with LoRA and a
  512-token context for the 2025 model
  ([DAMAGE](https://arxiv.org/abs/2501.03437)); the best EditLens research
  model was a Mistral Small 24B
  ([EditLens](https://arxiv.org/abs/2510.03154)).
- **Heads.** A segment head that sorts the window's weighted AI fraction into
  15 ordered buckets; a per-token head over human, AI-assisted, and
  AI-generated; a binary mixed-authorship head, positive "when more than 15%
  of the supervised tokens in a window belong to provenance classes other than
  the dominant class"; and the humanizer head
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Windows.** Inference uses "overlapping windows of at most S=512 tokens
  with a stride of 256 tokens". The input is repeated twice in the context and
  the token labels are read from the second copy
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)). Pangram 3 windows
  did not overlap
  ([v3 migration guide](https://www.pangram.com/blog/v3-api-migration-guide)).
- **Decode.** Per-token logits are averaged across the windows that cover each
  token and calibrated; a linear-chain CRF with a penalty on label changes,
  relaxed where the mixed head fires, is decoded with Viterbi; labels are then
  set by majority vote within each sentence ("Product output is constrained to
  sentence-level resolution"), and runs shorter than a configured minimum are
  merged into a neighbor. Document fractions are shares of characters per
  class ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Document verdict.** For evaluation: Human if the human fraction is at
  least 0.90, AI if the AI fraction is at least 0.80, Mixed otherwise (sec.
  5.1, [Pangram 4 report](https://arxiv.org/abs/2607.27183)). The API returns
  `prediction_short` of "AI", "Human", or "Mixed" with `fraction_ai`,
  `fraction_ai_assisted`, and `fraction_human`; the documented example with
  0.6 AI-assisted and 0.4 human returns headline "AI Assisted" and
  `prediction_short` "Mixed"
  ([API reference](https://docs.pangram.com/api-reference/ai-detection)). The
  dashboard percentage is the share of the document flagged AI-generated or
  AI-assisted
  ([score post](https://www.pangram.com/blog/what-does-your-ai-detection-score-mean)).
- **Inferred:** `prediction_short` follows the 0.90 and 0.80 rule, because the
  4.1 model card scores its evaluations on `prediction_short` and counts any
  Mixed as an error
  ([model card](https://www.pangram.com/research/model-card)). The report uses
  the symbol for the AI fraction both for the AI-generated share and for a
  weighted fraction that adds half the AI-assisted share, and does not say
  which one the 0.80 test uses.
- **Not found:** the rule that maps fractions to `headline`. The headline
  strings I saw documented are "Human Written", "AI Assisted", and "AI
  Detected" for Pangram 4 and "Fully Human Written" for Pangram 3
  ([API reference](https://docs.pangram.com/api-reference/ai-detection),
  [quickstart](https://docs.pangram.com/quickstart-rest),
  [v3 migration guide](https://www.pangram.com/blog/v3-api-migration-guide)).
  "Mostly Human Written" appears in no source read. Also not found: the
  minimum run length, the CRF parameters, and the cut-offs for the High,
  Medium, and Low `confidence` labels.
- **Window fields.** `label` is "AI-Generated", "AI-Assisted", or "Human
  Written"; `ai_assistance_score` runs 0 to 1; 4.1 adds `class_probabilities`
  ([API reference](https://docs.pangram.com/api-reference/ai-detection)). The
  report says confidence "is not a recalibrated probability that the final
  constrained label is correct"
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Length limits.** Minimum 50 words, lowered from 75 in 3.2
  ([3.2 post](https://www.pangram.com/blog/introducing-pangram-3-2)); the
  dashboard caps a scan at 18,725 words
  ([input sizes](https://www.pangram.com/knowledge-hub/minimum-and-maximum-input-sizes)).
  On 4.1 the dashboard "has changed to reflect less certainty for text under
  150 words" ([model card](https://www.pangram.com/research/model-card)).
- **Preprocessing.** "Pangram 4 may normalize the submitted text before
  inference" and returns the normalized text
  ([API reference](https://docs.pangram.com/api-reference/ai-detection)). What
  the normalization does is not documented.

## Label set

Status: stated.

- **Human.** Text that is solely human "or that the amount of AI contribution
  is so low as to be negligible (e.g., light copyediting, literal translation,
  spelling and grammar fixes)"
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **AI-Assisted.** Text that is "co-authored and homogeneously mixed", meaning
  human text that a model has edited, as opposed to heterogeneous text where
  human and model spans sit side by side
  ([EditLens](https://arxiv.org/abs/2510.03154)). It replaces Pangram 3's
  "Lightly AI-Assisted" and "Moderately AI-Assisted"
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183),
  [Pangram 4 migration guide](https://www.pangram.com/blog/pangram-4-migration-guide)).
- **AI-Generated.** Solely model-written, or text that "is significantly more
  AI-authored than human-authored"
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)). The scope also
  requires that the model produce more tokens than it was given: "we must
  consider the output to be human if the AI does not add any original tokens
  of its own".
- **Light against heavy editing.** Pangram 3 defined light assistance as
  "surface-level changes that do not affect the underlying ideas, structure,
  or content" and moderate assistance as cases where the model "may have
  rewritten significant portions of the text or added content of its own"
  ([Pangram 3.0 post](https://www.pangram.com/blog/introducing-ai-assistance-detection)).
  On Pangram 4.1 the target is: proofreading and copy editing stay human,
  substantial rewrites are AI-assisted, large rewrites can be AI-generated,
  and a model expanding a human claim gives mixed human and AI-generated text
  ([accuracy post](https://www.pangram.com/blog/is-pangram-accurate)). Pangram
  says "defining the exact line between these categories is more of an art
  than a science"
  ([knowledge hub](https://www.pangram.com/knowledge-hub/what-is-ai-assisted)).
- **What EditLens measures.** The size of the change a model made to a human
  text. Its objective "is not to attribute authorship, but to predict the
  magnitude of change between x and y", trained against the embedding cosine
  distance between source and edit or a soft n-gram overlap score; in the
  paper a cosine distance under 0.03 counts as unedited and over 0.15 as fully
  AI ([EditLens](https://arxiv.org/abs/2510.03154)). Example scores from the
  3.0 post: 0.52 for a clean-up prompt, 0.79 for "Make the language more
  vibrant", 0.89 for a rewrite in a named author's style
  ([3.0 technical post](https://www.pangram.com/blog/pangram-3-0-technical)).
- **Pangram 4's label rule.** The edited text is split into clauses. A clause
  with a near-exact lexical match in the source is human, one with only a
  semantic match is AI-assisted, and one with neither is AI-generated. The
  weighted AI fraction is the AI-generated share of characters plus half the
  AI-assisted share. Deleting or reordering human sentences does not change
  the label ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Ideas against wording.** "While Pangram cannot infer where an idea came
  from, it will pick up on stylistic signals that AI uses in its word choice."
  ([Pangram 3.0 post](https://www.pangram.com/blog/introducing-ai-assistance-detection)).

## Humanizer head

Status: stated for task and design; training data not found.

- **Task.** Pangram defines humanization as "the deliberate transformation or
  obfuscation of AI-generated text to evade AI-text detection". The head is a
  four-way classifier over "human, ai-generated, humanized-ai,
  mixed-authorship" and "is applied when Pangram 4 detects evidence of
  AI-generated content"
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **What it targets.** "deliberate typo injection, casing changes, synonym
  substitution, homoglyph attacks, and transformations produced by services
  that advertise humanization or AI-detector evasion". PDF-extraction errors,
  copy-and-paste corruption, OCR errors, and encoding problems "are not
  classified as humanization"
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Design.** It is trained as a probe with a stop-gradient and a loss weight
  of 0.25, so it cannot shape the backbone. The reason given: letting its
  gradients flow "kept top-level FPR equivalent, but concentrated the failures
  in specific registers: academic writing and ESL essays"
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Accuracy.** On paired unmodified and humanized AI text: accuracy 96.82%,
  F1 0.9678, precision 98.02%, recall 95.57%; 1.93% of unmodified AI text was
  called humanized and 4.43% of humanized text was called plain AI. Per-tool
  recall ran from 91.52% to 99.39% (Table 13,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **API surface.** `is_humanized` is "Whether Pangram 4's humanizer head
  classified the window as humanized. Present on every Pangram 4 window.";
  `humanizer_score` runs 0.0 to 1.0
  ([API reference](https://docs.pangram.com/api-reference/ai-detection)).
- **Inferred:** the head is a second opinion on text already judged AI and
  does not feed the Human, Mixed, or AI verdict. The report calls it
  "supplemental" and "auxiliary", trains it behind a stop-gradient, and
  describes no path from it into the decode
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Not found:** which tools or how many examples trained the head, the score
  cut-off behind `is_humanized`, and how often it fires on human text (the
  report tests it only on AI text).

## Paraphrasers, humanizers, and edited text

Status: stated. Model-written text passed through tools or prompts is covered
in the second section; this section covers editing in both directions.

- **Light AI polishing of human text (Pangram 4).** 11,363 student texts
  lightly edited by Grammarly, Apple Intelligence, Gemini in Google Docs, and
  three frontier models: 99.45% Human, 0.54% Mixed, 0.01% AI. Pangram 3.3.2:
  99.70%, 0.12%, 0.18% (Table 4,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Open editing prompts on human text (Pangram 4).** 14,990 texts edited
  under prompts such as "Rewrite" and "Paraphrase it": 41.37% Human, 55.01%
  Mixed, 3.62% AI. Pangram 3.3.2: 79.23%, 5.54%, 15.22% (Table 5,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Real-world edit requests (Pangram 4).** 4,826 edits with a ground-truth AI
  fraction between 0.25 and 0.75: 27.85% Human, 65.17% Mixed, 6.98% AI.
  Pangram 3.3.2: 65.27%, 12.62%, 22.11% (Table 6,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Chained edits, Pangram's run of OpAI-Bench (Pangram 4).** Across eight
  successive model edits of a human text, the mean predicted AI-plus-assisted
  fraction trails the true AI share of characters: 0.0001 against 0.2075 after
  one polish, 0.3257 against 0.6858 after five edits, 0.6950 against 0.9935
  after eight (Table 29,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **AI-polished peer reviews (independent; Pangram 3.0)**
  ([Saha et al., 2026](https://arxiv.org/abs/2603.20450)). 3.0% and 3.1% of
  human-written, model-polished reviews were labeled "AI" on the two model
  sets, from 0.5% for GPT-5 to 5.5% for Qwen-3-30B as the polisher. Polished
  reviews in which the model introduced new content were labeled "AI" around
  20% of the time. Polishing with personal style instructions gave 2.42%;
  back-translation through another language gave 1.1% to 4.5%; accepting every
  Grammarly suggestion on 100 reviews gave 89 Human, 11 Mixed, 0 AI. Pangram's
  rerun of the benchmark reports 1.4% and 2.5% on Pangram 4 and 14.9% and 4.5%
  on 3.3.2 (Table 28, [Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **AI-polished text, early 2025 (independent; pre-EditLens Pangram at a 0.01
  threshold)** ([Saha and Feizi, 2025](https://arxiv.org/abs/2502.15666)).
  After "extremely minor edits with LLaMA-2-7B", 42.56% of samples were
  detected as AI. That model had no AI-assisted class.
- **Notions of permitted AI use (independent; 2026)**
  ([Dycke et al., 2026](https://arxiv.org/abs/2606.04906)). With every
  non-human label mapped to AI: "Even methods explicitly trained to minimize
  FPR, such as Pangram, exhibit high FPR, particularly for non-genesis-based
  notions". The numbers are in a figure and the Pangram version was not found.
- **Translation.** 3.3 brought a "slight uptick in the false positive rate for
  human-written text that has been passed through Google Translate"
  ([3.3 post](https://www.pangram.com/blog/meet-pangram-3-3)); the 4.1 card
  lists machine translation as out of scope
  ([model card](https://www.pangram.com/research/model-card)).
- **Model edits of model text (EditLens research model).** The score moved by
  a mean of -0.05, against +0.38 when the same edits were applied to human
  text ([EditLens](https://arxiv.org/abs/2510.03154)).
- **Human edits of model text.** See "Human post-editing of model text" above:
  one research-model result and no production measurement.

## Length, genre, domain, non-native English, and model family

Status: stated.

- **Length (Pangram 4.1)**
  ([accuracy post](https://www.pangram.com/blog/is-pangram-accurate)). 50 to
  99 words: FPR 0.02%, FNR 1.29%. 100 to 249 words: FPR 0.009%, FNR 0.41%. 250
  to 499 words: FPR 0.004%, FNR 0.21%. The Pangram 4 report says "AI detection
  is often harder on shorter texts" and gives its length curve only as a
  figure ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Length (independent; Pangram "API v2025-05")**
  ([Jabarian and Imas](https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf)).
  On passages under 50 words the FPR reached 0.025 (restaurant reviews) and
  the FNR reached 0.2222 for Claude Opus 4 news text, while most cells stayed
  near zero.
- **Length in the field (Pangram 4)**
  ([agent-swarm post, 2026-09-10](https://www.pangram.com/blog/pangram-on-colluding-agent-swarm)).
  On 11,712 agent-written pages, the share labeled AI was 16.0% under 50
  words, 42.5% at 50 to 99, 65.1% at 100 to 199, 93.1% at 200 to 499, and
  99.0% at 500 or more. Pages that were more than 65% URL characters were
  detected less often.
- **Domain FPR (Pangram 4.1)**
  ([accuracy post](https://www.pangram.com/blog/is-pangram-accurate)).
  Academic 0.019%, news 0.003%, how-to 0.016%, creative 0.000%, speeches
  0.000%, recipes 0.049%, poetry 0.078%.
- **Domain FNR (Pangram 4.1)**
  ([accuracy post](https://www.pangram.com/blog/is-pangram-accurate)).
  Academic 0.000% (48,443 texts), creative 0.269% (41,940), random real-world
  sample 0.315% (2,536).
- **Genre (independent; Pangram 3.3.2, author imitation)**
  ([Epoch AI](https://epoch.ai/data-insights/ai-detectors-false-negatives)).
  False negatives: scientific 25%, blog 4%, fiction 1%.
- **Genre (independent; 2025 Pangram)**
  ([Jabarian and Imas](https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf)).
  FPR by genre between 0.0000 (blogs, novels, resumes) and 0.0075 (restaurant
  reviews); FNR at most 0.02.
- **Out of scope (Pangram 4.1)**
  ([model card](https://www.pangram.com/research/model-card)). Code, markup or
  Markdown text, tables of contents and reference sections, templated or
  automated writing, machine translation, instructions, recipes, technical
  manuals, math notation, and figure text. The intended input is "long-form
  natural-language writing samples of at least 50 words, written primarily in
  complete sentences".
- **Non-native English (Pangram 4)** (Table 9,
  [Pangram 4 report](https://arxiv.org/abs/2607.27183)). One false positive in
  24,586 learner texts (0.0041%), across ELLIPSE, ICNALE, PELIC, and the 89
  Liang et al. TOEFL essays. Pangram 4.1 reports 0 in 15,420 university essays
  by writers with 51 first languages
  ([college essays post](https://www.pangram.com/blog/pangram-performance-college-essays)).
- **Other languages (Pangram 4)**
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)). FPR 0.0014% on
  996,273 texts in 104 languages; FNR 1.24% over 18 languages, with Urdu at
  5.31% and Persian at 3.17%. Pangram 4.1 reports 0.0033% and 1.99%
  ([model card](https://www.pangram.com/research/model-card)).
- **Model family.** See "Choice of generating model" above.

## Published error rates

Status: stated. Pangram's figures count Mixed as an error on both sides unless
noted.

- **Pangram 4.1 (2026-10; Pangram)**
  ([model card](https://www.pangram.com/research/model-card)). FPR 0.0090% (70
  of 781,981 pre-2022 English documents, after cleaning the set); FNR 0.3652%
  (1,899 of 520,000 outputs from 26 models answering chat prompts).
- **Pangram 4 (2026-07; Pangram)**
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)). FPR 0.0041% on over
  a million English texts (95% CI 0.0032% to 0.0050%); FNR 0.3396% (1,766 of
  519,993); AUROC 0.9916.
- **Pangram 3.3.2 (2026-07; Pangram)**
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)). On the same two
  sets: FPR 0.0539%, FNR 1.9942%.
- **Pangram 3.3.2 (2026-07; independent)**
  ([Epoch AI](https://epoch.ai/data-insights/ai-detectors-false-negatives)). 0
  of 495 false positives; 0 of 297 false negatives on directly prompted text;
  30 of 297 under author imitation.
- **Pangram 3.2 (2026-03; Pangram)**
  ([Open Pangram post](https://www.pangram.com/blog/introducing-open-pangram)).
  On a 10,000-text RAID sample: FPR 0.002, FNR 0.007.
- **Pangram 3.0 (2026; independent)**
  ([Saha et al.](https://arxiv.org/abs/2603.20450)). Peer reviews: human FPR
  0.0%; fully AI reviews labeled "AI" 97.0% to 100%; human-written,
  model-polished reviews labeled "AI" 3.0% and 3.1%.
- **Pangram 3.0 (2025-12; Pangram)**
  ([Pangram 3.0 post](https://www.pangram.com/blog/introducing-ai-assistance-detection)).
  Human essays: 99.84% fully human, 0.14% lightly assisted, 0.013% moderately
  assisted, 0.0064% fully AI.
- **Pangram "API v2025-05" (independent)**
  ([Jabarian and Imas](https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf)).
  1,992 human passages and 1,992 AI passages per model, four models, six
  genres: FPR 0 at raw thresholds of 0.5 and above; FNR at 0.5 from 0.0131 to
  0.0272; AUROC never below 0.9979.
- **Early-2025 models (independent)**
  ([Russell et al.](https://arxiv.org/abs/2501.15654)). 300 articles: base
  model TPR 98.0% with FPR 2%; Humanizers model TPR 99.3% with FPR 2.7%.
- **2024 model (Pangram)** ([2024 report](https://arxiv.org/abs/2402.14873)).
  1,976 documents across 10 domains and 8 models: accuracy 99%; on held-out
  email, FPR 0.8% and FNR about 2%.
- **Inferred:** the 4.1 FPR is higher than the 4.0 figure because the
  evaluation set and target changed, not only the model. The card says the set
  was cleaned and that "we return to our standard of calibrating our headline
  false positive rate to roughly 1 in 10,000"
  ([model card](https://www.pangram.com/research/model-card)).
- Jabarian and Imas caution that "we do not expect the results presented here
  to remain constant over time"
  ([BFI WP 2025-116](https://bfi.uchicago.edu/wp-content/uploads/2025/09/BFI_WP_2025-116.pdf)).

## What the classifier keys on

Status: stated by Pangram in general terms; no source gives a feature-level
account.

- **Not perplexity or burstiness.** "No, Pangram does not rely on perplexity
  and burstiness for our model predictions."
  ([knowledge hub](https://www.pangram.com/knowledge-hub/does-pangram-use-perplexity-and-burstiness)).
  The 2024 report's reason: perplexity methods "fail on human-written
  documents that happen to be in the training set of LLMs"
  ([2024 report](https://arxiv.org/abs/2402.14873)).
- **Framed as authorship.** "AI detection is a problem of author
  identification", and "Visible LLM-isms are only one signal among hundreds of
  thousands that Pangram considers."
  ([how Pangram works](https://www.pangram.com/blog/how-does-pangram-work)).
- **Not the highlighted phrases.** The dashboard's AI phrases "are not
  directly used by Pangram's prediction model, and changing or reducing the
  number of them will not reduce your AI prediction". The model is "sensitive
  to thousands of tiny signals" ranging "from the frequency of certain words
  and phrases, to the structure and composition of sentences, to the overall
  organization and tone of the document"
  ([editing post](https://www.pangram.com/blog/can-you-avoid-ai-detection-through-editing)).
- **Topic and format are controlled away.** Mirrors match topic and length;
  mirror prompts are tuned to strip openers and titles; the 2024 benchmark was
  normalized to remove formatting cues
  ([2024 report](https://arxiv.org/abs/2402.14873)). Pangram reports once
  catching a model that had overfit to a Wikipedia formatting quirk
  ([false positives post](https://www.pangram.com/blog/all-about-false-positives-in-ai-detectors)).
- **Local evidence.** Each decision sees at most 512 tokens
  ([Pangram 4 report](https://arxiv.org/abs/2607.27183)); the 2025 paper says
  the window was chosen "to constrain the model to using only short-range
  features" ([DAMAGE](https://arxiv.org/abs/2501.03437)).
- **Edit signals.** The EditLens paper says the model learns "lexical
  volatility, style drift, fluency/consistency cues"
  ([EditLens](https://arxiv.org/abs/2510.03154)).
- **Opaque by Pangram's account.** "Its predictions are also to some degree a
  black box", and "Pangram 4 does not account for people who intentionally
  write like LLMs or who have absorbed elements of LLM style into their
  writing." ([Pangram 4 report](https://arxiv.org/abs/2607.27183)).
- **Independent readings.** Xu et al. conclude detectors track "artifacts of
  instruction tuning and local context"
  ([arXiv 2605.19516](https://arxiv.org/abs/2605.19516)); Pangram's own post
  agrees that post-training narrows model style and says detection holds "as
  long as these model developers continue to have specific preferences"
  ([2026-08-20 post](https://www.pangram.com/blog/no-llms-dont-just-mimic-human-text)).
  Chakrabarty et al. find that cliche density mediates 16.4% of the detector
  score's effect on reader preference for prompted text and 1.3% for
  fine-tuned text ([arXiv 2510.13939](https://arxiv.org/abs/2510.13939)).
- **Not found:** any published feature attribution, probe, or ablation that
  says which properties of a text carry the Pangram 4 decision.

## Sources not reached

- **Van Vlasselaer et al. (2026), full text.** The publisher page served an
  automated-client check, which I did not work around, and the preprint host
  required a login. I used the abstract and Pangram's summary; the
  per-condition figures above are Pangram's account of the paper
  ([article](https://doi.org/10.1007/s40979-026-00226-w)).
- **Hugging Face model cards.** `pangram/editlens_roberta-large` and
  `pangram/editlens_Llama-3.2-3B` are gated behind a terms agreement; the
  public card pages give only base model, license, and language. The
  `pangram/editlens_iclr` dataset card is empty
  ([model page](https://huggingface.co/pangram/editlens_roberta-large),
  [dataset page](https://huggingface.co/datasets/pangram/editlens_iclr)).
  Configuration values came from the repository instead
  ([EditLens repository](https://github.com/pangramlabs/EditLens)).
- **GEDE (Gehring and Paassen, 2025) and Perkins et al. (2024) originals.**
  Not located; the figures above are from Pangram's report tables, and I did
  not confirm whether those papers tested Pangram themselves.
- **Numbers held only in figures.** The Pangram 4 length curve, the Xu et al.
  paraphrase trade-off curves, and the Dycke et al. per-notion rates.
- **Versions.** Xu et al., Chakrabarty et al., Dycke et al., and Van
  Vlasselaer et al. do not state, in what I could read, which Pangram version
  they tested.
