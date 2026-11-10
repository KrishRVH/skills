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
