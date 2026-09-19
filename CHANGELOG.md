# Changelog

## animize: two passes and a Preserve regime (2026-09-19)

### What changed

- The skill now has exactly two passes. `quick` handles the agent's own
  replies and routine communication. `deep` handles bounded artifacts. The
  caller-facing `audit` job is gone; a request that forbids edits or asks what
  is wrong runs `deep` with `delivery: with_notes` and the artifact withheld.
  The verification reference survives as an internal step of every deep run.
- `deep` selects a regime from the source class. A draft the caller calls
  their own gets Preserve: clause-level editing under a token budget. An AI
  draft, an AI-assisted draft, or a bare brief gets Recompose, the existing
  full recomposition. A first-person, situated draft of unstated origin
  triggers one question; an unanswered question falls back to Preserve with a
  note.
- The controls table has three rows: `voice` (`auto`, `preserve`, `rebuild`,
  `match`), `clarity`, and `delivery`. The old `job`, `process`,
  `rewrite_depth`, and `factual_mode` controls are inferred from the request
  or stated as facts in the brief; the entry point documents where each went.
- The dash policy moved from a tier 4 hard rule to a tier 8 house-style
  default with a reader-facing rationale (repeated dash-aside syntax). A
  caller request, a controlling style guide, or a consistent sample habit now
  outranks it. Nothing in the skill claims a dash is evidence of authorship.
- Frame now asks three questions in `deep` when the brief lacks them (the one
  thing the reader must leave with, what the caller thinks, one real
  particular) instead of inferring "reasonable defaults", which is the
  averaging the skill exists to remove.
- New files: `references/backends.md` (model-stack note, outside the prose
  rules), `examples/quick-core.md` (a 47-line pasteable quick pass),
  `examples/pairs.md` (seven before-and-after pairs across genres), and
  `references/evaluation-results.md`. `examples/recomposition.md` gained two
  Preserve examples, one showing the clause-diff summary and one showing a
  missing opening delivered as a note rather than a clause.
- The description field states the scope: the skill improves reader-facing
  quality and makes no claim about any detector's verdict.

### What the Preserve regime does and does not do

Preserve keeps a human draft's own clauses. The model may delete, reorder,
edit within a clause, or merge and split at clause boundaries. It may not
regenerate a sentence from its meaning, add a clause with no lexical anchor in
the source, or add an opening, transition, or ending the draft lacks; those
become marked suggestions in the notes. Model-added tokens must stay under 15%
of the output and below the source's token count (`PRESERVE_BUDGET` in the
deep reference; a brief may tighten it, never loosen it). Before delivery the
pass computes a clause-level diff and reports kept, deleted, reordered,
lexically edited, and added clauses; any added clause is a violation.

Preserve does not verify that the draft is human. It takes the caller's word
and says so in its notes. It makes no claim about what any detector will say.
Its purpose is that the result stays honestly describable as human-written
with AI assistance, which is what callers in academic and editorial submission
need to be able to say.

### Measured numbers

Pilot run, 2026-09-19, 6 documents per cell; full tables in
`animize/references/evaluation-results.md`.

- Routing: 18 documents, 0 wrong guesses; the single question fired on the
  three first-person memoir subjects in both the human and the mirror cells.
- Preserve on defect-injected human drafts: all 5 injected defects removed in
  6 of 6 drafts at every budget; 0 added clauses; model-token share at most
  0.014 (0.05 and 0.15 budgets) and 0.000 (0.30). The budget never bound on
  this defect family.
- Preserve on strong human drafts: 11 edited clauses across 6 drafts, 0 added,
  share at most 0.032, every number and quotation intact. Over-editing is the open
  question; the preference test that decides it was not run.
- Recompose on the same human drafts (misrouting cell): defects removed, but
  a fifth of the length cut and model-token share up to 0.280.
- Detector: Binoculars with a 1.5B Qwen pair moved by less than the within
  cell spread in every cell and does not separate the mirrors from the human
  passages at this size. The trained-classifier column, calibration, and
  humanizer-head metric are blocked on gated weights until the maintainer logs
  in to Hugging Face.
- Production spot check, twenty documents by hand: Preserve outputs read as
  Human 10 of 10 (famous-source caveat applies); Recompose on fresh AI
  mirrors read as AI-generated 6 of 6; Recompose on human drafts read Human
  3 of 4 and AI-assisted 1 of 4.
- Quick core alone versus full skill on six routine replies: 25 of 25 injected
  defects repaired by each; the full skill read only `SKILL.md`.
