# Backends

This note is for callers who control their model stack. It sits outside the
prose rules. Nothing in the skill's procedure depends on it, and no
prompt-level rule in the skill substitutes for it.

## What the evidence says

The only published detector-agnostic method with a real fidelity trade-off is
a base-model paraphraser applied iteratively. Xu, Zhong, Raghunathan, Fang, and
Kolter ("Base Models Look Human To AI Detectors", arXiv 2605.19516, May 2026)
report that with human-written prefixes, one commercial detector assigns
Llama-3-8B base-model continuations a 98.8% human probability and the
instruct model's continuations 17.1%. Their reading is that detectors track
artifacts of instruction tuning and local context rather than an invariant
property of machine text. Their pipeline, Humanization by Iterative
Paraphrasing (HIP), minimally fine-tunes a base model into a paraphraser and
applies it iteratively.

That is a model-stack choice. A skill made of prose rules cannot make it, and
the measured ceiling for prose-rule humanizers against a trained classifier is
a false negative rate under half a percent (Pangram 4 Technical Report, arXiv
2607.27183, Table 15). Animize's rules neither require HIP nor replace it.

## Running Animize on top of a paraphrase

A caller who runs a base-model paraphrase first can use Animize as the
editing layer on top of it. By default the run recomposes the paraphrase like
any other model-written draft. A caller who wants clause-level edits instead
states that the paraphrase is the draft to keep, and the Preserve regime
applies: edits under budget, with the clause diff in the notes.

Say plainly what this stacks: an honest constraint (the model adds few tokens
to a draft) on top of a technique whose purpose is evasion. The caller owns
that choice. The skill's own claim stays the same: it repairs reader-facing
defects and says nothing about any detector's verdict.

## The arms-race tax

The detector vendor benchmarks popular repositories by name, retrains on hard
negatives, and ships a classification head for whatever tactic gets traffic.
The base-versus-instruct gap is a target for their next release, so treat it
as a moving window rather than a fixed hole. Any technique that measurably
moves a detector decays within about one release cycle. The only workflows
that survive that loop are the ones a vendor cannot train against without
raising false positives on real human writing, which is why the skill's
Preserve regime is defined by what the human wrote rather than by what a
detector sees.
