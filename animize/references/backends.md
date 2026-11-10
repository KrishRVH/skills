# Backends

This note is for callers who control their model stack. It sits outside the
prose rules. Nothing in the skill's procedure depends on it, and no
prompt-level rule in the skill substitutes for it.

## What the evidence says

The published methods that move a trained detector at a measured cost to the
text are model-stack choices. None has an independent measurement on the
detector's current version.

The first is a base-model paraphraser applied iteratively. Xu, Zhong,
Raghunathan, Fang, and Kolter ("Base Models Look Human To AI Detectors", arXiv
2605.19516, May 2026) report that with human-written prefixes, one commercial
detector assigns
Llama-3-8B base-model continuations a 98.8% human probability and the
instruct model's continuations 17.1%. Their reading is that detectors track
artifacts of instruction tuning and local context rather than an invariant
property of machine text. Their pipeline, Humanization by Iterative
Paraphrasing (HIP), minimally fine-tunes a base model into a paraphraser and
applies it iteratively.

The second is a model fine-tuned on one author's writing. Chakrabarty,
Ginsburg, and Dhillon (arXiv 2510.13939) fine-tuned thirty models, each on one
author's works. A commercial detector flagged 3% of their output, against 97%
for the same models prompted with examples of the author, and trained readers
preferred the fine-tuned output. The paper does not state the detector's
version.

A skill made of prose rules can make neither choice. The one published
measurement of a prose-rule humanizer against a trained classifier used a
single instruction repository with three models, and the classifier missed 44
of 10,223 rewritten texts, or 0.43% (Pangram 4 Technical Report, arXiv
2607.27183, Table 15). Animize's rules neither require these methods nor
replace them.

## Running Animize on top of a paraphrase

A caller who runs a base-model paraphrase first can use Animize as the
editing layer on top of it. By default the run recomposes the paraphrase like
any other model-written draft. A caller who wants clause-level edits instead
states that the paraphrase is the draft to keep, and the Preserve regime
applies: edits under budget, with the clause diff in the notes.

Say plainly what this stacks: an honest constraint (the model adds few tokens
to a draft) on top of a technique whose purpose is evasion. The caller owns
that choice. The skill's own rules stay the same: they repair reader-facing
defects.

## The arms-race tax

The detector vendor has benchmarked one popular instruction repository by
name, tests the commercial rewriting tools with the most traffic, and ships a
classification head that flags humanized text. Each release has shrunk the
measured effects. Between two versions, the miss rate on one author-imitation
benchmark fell from 5.05% to 2.86%, and the highest miss rate for any
generating model fell from 6.38% to 0.61% (Pangram 4 Technical Report, Tables
23 and 3). The base-versus-instruct gap is a target for the next release, so
treat it as a moving window rather than a fixed hole. The only workflows
that survive that loop are the ones a vendor cannot train against without
raising false positives on real human writing, which is why the skill's
Preserve regime is defined by what the human wrote rather than by what a
detector sees.
