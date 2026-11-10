# Animize two-pass redesign: decision log

Date: 2026-09-19. Source: the research brief "Animize: research brief and
agent instructions for the two-pass redesign" (case reference detector
Pangram 4). This log answers the brief's open questions, records decisions the
repository's own rules forced, and lists corrections found while checking the
brief's citations.

## Open questions from the brief

1. **Human-draft detection.** The caller's statement decides. The heuristic
   (first person plus situated particulars the model could not have supplied)
   only decides whether to ask the single routing question. Preserve is never
   assigned on the heuristic alone. The one exception is the brief's own
   fallback: when the question goes unanswered, the deep pass uses Preserve and
   says in its notes that the draft's origin was not confirmed. Reason:
   over-rewriting a human draft destroys authorship, which the caller cannot
   get back; over-preserving a generated draft costs quality, which a second
   run repairs.
2. **Budget constant.** Ship 0.15 as the default and let the brief tighten it.
   Reason: 0.15 is Pangram's mixed-window threshold, so the default keeps the
   result honestly describable as AI-assisted or human. A 0.05 default would
   leave most defect repairs undone and push the pass to withhold fixes on
   ordinary drafts. A caller who needs a plain "human" label is exactly the
   caller who should state the stricter budget. The evaluation protocol runs
   0.05, 0.15, and 0.30 so the constant can be revisited with data.
3. **Findings-only requests.** A request that forbids edits, or that asks what
   is wrong, asks for a review, or asks for a fidelity comparison without
   authorizing a rewrite, resolves to the deep pass with `delivery: with_notes`
   and the artifact withheld. The routing section states this. The deep pass
   still runs its verification and skeptical-reader machinery; it returns the
   notes and no artifact.
4. **The word "humanize".** Kept in the description triggers, paired with the
   scope sentence. Reason: it is the search term, and the scope sentence is
   what tells a caller who wanted evasion that this skill does not sell it.
5. **Publishing detector results.** Publish the Recompose result (the skill
   does not move a trained classifier) and the Preserve result (the label
   matches the workflow). Never publish a figure framed as a bypass rate.
   Results from the Open Pangram models are labeled as EditLens and Pangram 3
   lineage, never as Pangram 4 verdicts.

## Revision of 2026-11-09: detector scores as a guardrail

The maintainer revised the brief's position that detector scores are never
an optimization signal. Reading as machine-written is one of the ways prose
gives an impression of low quality, and a detector is a cheap proxy for it,
so the evaluation now tracks detector scores as a bounded guardrail on rule
changes. The purpose is quality control, not circumvention.

What changed: the protocol scores every cell before and after a rule change,
flags a change that makes output read as more machine-written, lets a lower
score break a tie between changes readers rate equally, and replaces the
Recompose criterion "verdict unchanged" with "no more machine-written than
the source."

What did not change: every rule needs a reader-facing reason that stands
without the detector; the trick family (typos, casing, homoglyphs, synonym
churn, fake self-corrections) stays banned; the skill still makes no claim
about any detector's verdict; no figure is reported as a bypass rate; and
model-stack techniques stay outside the prose rules in `backends.md`.

Evidence on how far the proxy can be trusted, from the pilot: the
production checker read 6 of 6 Recompose outputs as AI-generated while a
blind expert rated the same kind of output level with human originals, and
a Preserve edit the expert preferred moved an open model's verdict from
human to AI-assisted. Open question 5 above predicted that Recompose would
not move a trained classifier; on the stronger open model it lowered 9 of
10 scores and moved 3 of 10 verdicts from AI-generated to AI-assisted.

## Revision of 2026-11-09: one unattended procedure

The maintainer reversed two decisions the brief had settled (two passes,
three controls) and open question 1 above (ask once, fall back to Preserve).
The intended use is `run the skill on X before sending it`: the heaviest
work on every run, with nothing for the caller to set or answer. In the
maintainer's words, "fire and forget."

The reason is consistency. Nobody had to set the old controls, because all
of them were inferred, and that inference was the problem: a bare invocation
passed through seven judgment calls (pass, regime, three controls, whether
to ask the framing questions, which references to load), and each one
changed how much work was done.

What changed:

- **One procedure.** The lighter pass for short artifacts is gone. Every
  invocation runs every step of its branch, at every length.
- **No controls.** The regime comes from the caller's statement, the
  clear-communication profile from the genre, voice from supplied samples,
  and notes from whether anything needs reporting. A plain instruction in the
  request still governs at its tier in Precedence.
- **No questions.** Every missing fact has a default, reported in a note. A
  draft of unstated origin is fully recomposed and carries a fixed origin
  note. The three framing questions are answered from the material; an open
  one narrows the piece and is named in the notes.
- **Fixed loading.** Recompose and findings-only runs load six files every
  time. Preserve loads two.

What it costs, measured before the change: Recompose on six human drafts
removed every injected defect and about a fifth of the author's wording
(mean model-token share 0.141), where Preserve removed the same defects at
a share of 0.014 or less. Open question 1 gave the reason for the old
fallback: over-rewriting a human draft destroys authorship. The maintainer
accepted that cost for unattended use, offered the alternative of one
question when origin is unknown. What remains of the protection is the
origin note and the rule that only the caller's statement selects Preserve.

What did not change: Preserve on the caller's word, the 0.15 budget, the
clause diff, every fidelity and integrity rule, and the rule against any
detector claim.

Choices made while implementing, each narrower than a literal reading of
"the same files on every run" or "drop the lighter pass":

- Preserve loads only the procedure and the verification reference. Loading
  the repair catalogs into a run whose edit policy forbids catalog-driven
  repair invites over-editing, which the blind rater had already penalized.
- The pasteable rule block survives as `examples/prompt-block.md`. It is for
  prompts where the skill is not installed, and an invocation never
  substitutes it for the procedure.
- A request to keep a draft's wording selects Preserve as well as a
  statement of authorship, so a caller can still get clause-level edits on
  text they did not write.

Superseded by this revision: open questions 1 and 3 as worded above, and the
vocabulary decision below (there are no caller-facing values now).

The same change added one line-level tell at the maintainer's request: `the
real X` staged as a revelation. Its reader-facing reason is that the phrase
promises a truth hidden behind a decoy the text never showed.

Not done: the guardrail's before-and-after detector score for this change.

## Revision of 2026-11-09: one home per rule

The maintainer asked for a pass over the repository with a guide for writing
documents that agents consume. Its test is whether an agent takes the same
process on every run, and its main findings in this skill were duplication:
three gates, a masking rule stated in five places, the dash default in five,
and three different rules for when to report a retained candidate. Each rule
now has one home, and the entry point leads with the steps of a run.

Choices made while consolidating, each a judgment and none from the
maintainer's words:

- Preserve runs without the clear-communication profile. The entry point
  said the profile applied under Preserve, but Preserve never loaded its
  file, so the sentence promised checks that could not run. The Preserve
  edit policy already repairs an ambiguity as a defect.
- A findings-only run uses the Recompose steps as a diagnosis, skips the two
  drafting steps, and carries no origin note. The first forward test of that
  path found the fixed note would have told the caller a draft was
  recomposed when nothing had changed.
- The rules govern the artifact. Notes are written in the agent's ordinary
  voice, and the two-sentence cap applies to notes that accompany an
  artifact, not to findings.
- The content lock fills from the whole source boundary. A PR description an
  agent drafted is checked against the diff in the session, which the caller
  never pasted.
- The `Directions` section is gone. Its five words restated the procedure's
  design and drafting steps and applied to one branch only.

The pass was meant to move rules, not change them, and it did both. The
forward tests surfaced unclear instructions, and about a dozen were fixed
in the same pass, most after the sessions that had tested the text. The
maintainer asked how fidelity had been lost. Nothing measured said it had,
and nothing measured said it had not. What followed:

- The consolidation and the rule changes are separate commits, so the
  second can be reverted alone.
- The final text was frozen and every path rerun on the frozen copy.
- The guardrail check ran on that copy, on both corpora, before anything
  was published. It covers the one-procedure revision as well, whose check
  had not been run.
- The reruns reported eight more instructions that needed interpreting.
  They are listed in the results file and were left alone, so the text
  tested is the text shipped.

The guardrail check flagged two cells whose mean rose with no verdict
change. Neither led to a rule change. The protocol sends a flag to a
reader, and no reader has judged these outputs.

A separate question came up during the pass: whether runs should default to
a smaller, faster model. The guardrail check ran all seven cells on both
tiers. The smaller model passed every process check and read the same as
the larger one on drafts a person wrote. It did a fraction of the work per
document, rebuilt half as much of a model-written draft and scored higher
on it, and under Preserve deleted content the larger model left in and
flagged. The evidence is one session per cell with no blind rating. No
default was set: the skill's frontmatter cannot name a model under the
repository's contract, and the choice is the maintainer's.

## Revision of 2026-11-09: the live verdict as the benchmark

The maintainer restated what the skill is for and how to measure it. Most
runs start from model-written text: messages, emails, pull request
descriptions, write-ups, and articles. The result should read as
human-authored, show as human-written on detection tools, and carry no
LLM-isms. Pangram's live verdict is the one objective measure available,
because a blind rating took one rater a month. The maintainer treats the
verdict as an eval score to develop against and said the aim is not to fool
anyone maliciously.

This reverses the guardrail revision above and open questions 4 and 5. A
score may now drive a rule change, and the skill's scope sentence no longer
says it leaves a detector's verdict alone.

What changed:

- The protocol names the live verdict as the benchmark and adds two
  acceptance criteria: a model-written input's output reads Human Written,
  and no rule change moves a cell toward machine-written.
- The protocol dropped four bars: a rule needs a reader-facing reason that
  stands without the detector, a lower score only breaks a tie, a score is
  never an optimization target or a release criterion, and no figure is
  reported as a bypass rate.
- The entry point dropped the rules against optimizing for a detector and
  against a detector claim, with the gate check and the prompt-block
  sentence that matched them.
- The harness reaches the live model through the vendor's text API. The
  vendor's terms of service forbid using the service through any tool other
  than its own software, which rules out scripting the web checker.

What did not change: every fidelity and integrity rule; the rule against
manufactured humanity; the rule against faked imperfection, whose trick
family (typos, casing, homoglyphs, synonym churn, fake self-corrections)
stays banned; the protocol's bars on sending user or customer text to a
detector service and on training against a detector in this repository;
and the place of model-stack techniques, which stay in `backends.md` and
outside the prose rules.

What the first live measurements say:

- The skill does not meet the new criterion. All 11 model-written drafts
  measured read 100% AI-generated before and after, in every genre tried.
- The amount of rewording is not the lever. A variant that rebuilt every
  sentence moved no model-written verdict, raised the humanizer score, and
  cost two human drafts their Human Written verdict. Human drafts reworded
  by more than half kept theirs.
- The live score is saturated on model-written text, so nothing tried so
  far gives a difference to rank changes by.
- The skill does keep a person's draft reading as a person's, and it
  removes the planted sentences the live model flags.

This revision removed prohibitions and added no rule. The next revision
records where the line on verdict-moving changes was drawn.

## Revision of 2026-11-10: catalog entries checked against labeled text

A survey of current humanizer skills and a study of the detector suggested
six changes. Each was checked against the vendor's labeled dataset before
it became a rule. `.research/humanizer-skills.md` and
`.research/pangram-detector.md` hold the survey and the study.

Adopted:

- Keep ordinary idiom. The Filler entry rewrote `in order to` and `there
is … that` on sight, and people write both far more often than models
  do. It now leaves a single instance.
- Widen the staged-contrast entry to `X rather than Y`, which leans toward
  models as strongly as `not just X but Y`.
- Contract in a conversational register. The eight workplace drafts held
  no contraction in 1,073 words, before the skill and after it.
- Scope the removal of `please` to procedure steps.
- Treat an instruction inside the material as content. This is a safety
  rule, not a style rule: a draft, a forwarded message, or a quoted notice
  can carry text aimed at whatever tool processes it.
- Write a message at the length its writer would speak it.

Not adopted:

- A check for runs of similar-length sentences. The dataset's human
  documents have such runs in 60% of cases, so the check would fire on
  most human text.
- Genre baselines for sentence length and contraction rate. They wait for
  text from the voice packet.
- A regime that finishes a writer's rough version. Preserve adds no
  sentence, so it returns a two-minute rough version nearly as it came. The
  voice packet collects eight rough versions, and a prompt outside the skill
  finishes them. The regime waits on what the live model says about those
  finished versions.

The line on changes made for the verdict. The maintainer's position is that
making a model-written message read the way a person would write it
improves the reader's experience and is not deception. The skill follows
that test: a change that makes the text read better or more natural to a
person goes in, and it is not held back because it may also help with a
detector. The live verdict is then measured and reported for it. Two kinds
of change stay out. The first is a quota, such as using a phrase every few
hundred words. The second is anything a reader cannot perceive or that
reads worse: hidden characters, planted typos, random noise, and paraphraser
laundering. The rules against manufactured humanity and faked imperfection
already ban the second kind.

What the measurements say:

- The changes do what they were written for in the text. They do not move
  the live verdict: six model-written outputs read 100% AI-generated, as
  their sources do.
- Contractions cost on the open models. Inserted alone, they raise both
  EditLens scores on a model-written workplace draft. The live score is
  saturated on these drafts, so the entry was kept on its reader-facing
  reason, with the cost recorded for a live test later.
- The embedded-instruction rule holds when the material is in the
  conversation. When the material came through a file, a session twice
  removed the sentence from a quotation without a note. It never followed
  the instruction.
- Rules alone have not produced a Human Written verdict from model-written
  text in any arm. The published evidence points the same way: prompt-rule
  humanizers and voice imitation from samples are caught at high rates, and
  text whose words came from a person keeps its verdict after a model
  polishes it lightly. The voice packet tests routes that start from a
  person's words.

## Decisions forced by repository rules

1. **No `agents/backends.md`.** The validator allows only `openai.yaml` inside
   `agents/`, and that file accepts only the `interface` and `policy` keys. The
   backend note lives at `animize/references/backends.md`, is linked from the
   entry point's reference list, and `openai.yaml` carries a YAML comment that
   points to it.
2. **Changelog location.** The repository had no changelog. The entry lives in
   a root `CHANGELOG.md` because root-level docs are allowed and visible
   root-level non-skill folders are not.
3. **Harness location.** The local detector harness lives in `.eval/animize/`
   (a dot-prefixed infrastructure folder). Results are committed to
   `animize/references/evaluation-results.md` so they stay reachable from the
   skill. This decision log lives in `.research/` next to the earlier evidence
   note.
4. **Vocabulary.** The caller-facing values are `quick` and `deep` (passes) and
   Preserve and Recompose (regimes inside `deep`). The old `process` control
   name disappears from every file; the word "pass" is used for the two passes
   and never in relation to a detector.

## Corrections to the brief found while checking sources

- The Pangram 4 numbers quoted in the brief match the HTML report (arXiv
  2607.27183v1): AUROC 0.9916, FPR 0.0041%, FNR 0.3396%; humanizer head
  accuracy 96.82% and F1 0.9678; Table 15 BLADER result 44 of 10,223
  (0.430%), by model 0.499%, 0.410%, 0.382%; mixed-window threshold 15% of
  supervised tokens; window 512 with stride 256 and Repeat2.
- The HIP paper (arXiv 2605.19516) states the 98.8% versus 17.1% (Pangram)
  and 96.7% versus 30.3% (GPTZero) figures for Llama-3-8B under human prefixes
  in its Figure 1 discussion. Verified from the PDF text.
- The BLADER repository showed about 50,100 stars on 2026-09-19, not 32,000.
  The skill lists 25 patterns in five categories with a critique and revision
  cycle, which matches the brief's description.
- The Open Pangram collection page lists both models as not gated, but each
  model card and the `editlens_iclr` dataset card require agreeing to share
  contact information before files are served. Treat all three as gated. The
  base `meta-llama/Llama-3.2-3B` is gated under the Llama 3.2 Community
  License.
- The `editlens_iclr` dataset card README is empty. The label field names and
  bucket mapping (brief step 4) cannot be recorded until the user logs in;
  `.eval/animize/inspect_labels.py` prints them.
- The brief says the skill's `third-party-notices.md` lists BLADER as lineage.
  No such file exists in the tree, so there was nothing to update.

## Evaluation scope decisions

- The Open Pangram scoring runs (brief steps 3 to 6, 9, and 10) are blocked on
  the user's Hugging Face login and acceptance of three sets of terms. The
  harness is written and its code paths are tested; the gated scripts fail
  with a message naming the missing step.
- The perplexity-family column runs on an ungated pair
  (`Qwen/Qwen2.5-1.5B` and `Qwen/Qwen2.5-1.5B-Instruct`) because the Falcon-7B
  pair does not fit beside anything else on 24 GB and the point of the column
  is contrast, not a production verdict.
- The blind human-preference and skeptical-observer suites need raters and
  were not run. The results file reports them as pending.
- The pilot corpus is far below the protocol's 100 documents per cell. Every
  number in `evaluation-results.md` is labeled as pilot scale.
- Binoculars with the 1.5B pair turned out not to separate agent-written
  mirrors from the human passages, and famous public-domain prose scores low
  because the observer has memorized it. The column is reported as a weak
  contrast, and the protocol keeps it only for the "moves naive detectors"
  demonstration, which needs a larger pair and unseen human text.
- The injected-defect family (scaffolding that can be cut) never made the
  Preserve budget bind, so the 0.05 versus 0.15 question stays open. The next
  run needs defects whose repair requires new words.
