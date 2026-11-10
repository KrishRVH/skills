# Changelog

## animize: one unattended procedure (2026-11-09)

Changes:

- The skill has one procedure and no settings. The `quick` pass and the
  `voice`, `clarity`, and `delivery` controls are gone. Every invocation runs
  every step of its branch at every artifact length, so `run the skill on X
before sending it` always gets the full work.
- A run asks the caller nothing. A draft the caller says they wrote, or
  whose wording they ask to keep, gets the Preserve branch. Everything else
  is recomposed. A draft of unstated origin is recomposed too, and a fixed
  origin note after the artifact says so and says how to get the clause-level
  edit instead. The three framing questions are answered from the material;
  an open one narrows the piece and is named in the notes.
- Each branch loads a fixed set of references on every run: six files for
  Recompose and for findings-only runs, two for Preserve.
- The clear-communication profile is chosen by genre, and supplied writing
  samples steer expression, without a named control for either. A plain
  instruction in the request (a style guide, a length, a request for the text
  alone or for a change summary) still governs.
- A file whose origin is unstated is overwritten only when version control
  can restore the original. Otherwise the recomposed text comes back in the
  reply and the file is left as it was.
- `the real X` staged as a revelation is now a line-level tell, with its
  retain cases.
- `references/deep-recomposition.md` is now `references/procedure.md`, and
  `examples/quick-core.md` is now `examples/prompt-block.md`, a rule block
  for prompts where the skill is not installed.
- Two worked Preserve examples no longer trade the author's words for near
  synonyms, which the edit policy has not counted as a repair since the
  previous entry.
- The evaluation protocol replaces its control matrix with an unattended-run
  matrix: a question to the caller, a wrong regime, a missing note, a skipped
  step, or a wrong reference set each fails a run. The harness builds jobs
  from the caller's statement about authorship and counts those failures
  when it merges outputs.

Measured, with the table in `animize/references/evaluation-results.md`:

- Forward test, five independent sessions on bare requests: no session
  asked a question, and each loaded exactly its branch's fixed reference
  set, checked against its recorded tool calls. A PR description the agent
  had drafted was recomposed with three unsupported claims withheld. A
  first-person email introduced only as "my update email" was recomposed
  with the origin note, twice, on the same deciding sentence. A note the
  caller said they wrote got four edits at a model-token share of 0.014. A
  one-sentence release note ran every step.
- Cost: 96,000 to 145,000 tokens and 3 to 9 minutes per run, including the
  one-sentence artifact.
- Not run: the file-target, findings-only, supplied-samples, text-alone, and
  long-document cases, and the guardrail's before-and-after detector score
  for this change.

## animize: trained-classifier column and blind rating (2026-11-09)

Changes:

- The Preserve edit policy gained one sentence: a lexical replacement must
  repair a defect, and the author's diction, period idiom, spelling
  conventions, and register are not defects. A blind rater preferred the
  unedited draft where Preserve had swapped a period word for a modern near
  synonym or inserted a word. Nothing else in the skill changed.
- The evaluation protocol now says to show that a detector separates a
  corpus's own source classes before reading anything into an unchanged
  verdict, and describes the open models' training data and miss rate
  correctly.
- Detector scores became a bounded guardrail on rule changes. The protocol
  scores every cell before and after a change and flags one that makes
  output read as more machine-written. A rule still needs a reader-facing
  reason that stands without the detector, the trick family stays banned,
  and the skill still makes no claim about any detector's verdict. The
  Recompose criterion changed from "verdict unchanged" to "no more
  machine-written than the source."
- The harness scores with both open EditLens models the way the vendor's
  reference script does, checks its scores against the vendor's published
  ones, calibrates on one dataset split and verifies on another, samples a
  second corpus cell from the gated dataset without committing its text,
  and unblinds a rater's export.

Measured, with full tables in `animize/references/evaluation-results.md`:

- Reproduction: local scores match the published scores on 8,515 dataset
  rows with a mean absolute gap of 0.0004 (RoBERTa) and 0.0007 (Llama).
- Calibration, held out: 0.7% and 0.5% of human documents read as not
  human; 99.9% and 100% of generated documents read as not human; 33% and
  26% of AI-edited documents read as human.
- Pilot corpus: the RoBERTa model reads the agent-written mirrors as human,
  so it cannot test Recompose there. The Llama model reads them as
  AI-assisted before and after Recompose, reads four of six defect-injected
  drafts as AI-assisted, and reads all four as human after Preserve deletes
  the injected sentences. Preserve moved one draft (Paine) from human to
  AI-assisted.
- Second cell, ten generated and ten human documents from the detector's
  own test data: no Recompose output on generated text read as human on
  either model. On Llama nine of ten scored lower and three moved from
  AI-generated to AI-assisted. Preserve output on the human documents read
  as human ten of ten on both models, with no added clause after hand
  review of two flagged ones. Recompose output on the same human documents
  also read as human ten of ten, so a human verdict from these models does
  not certify an edit as light.
- Blind rating, one expert rater: the Preserve output preferred on 6 of 6
  defect drafts and 2 of 5 strong drafts; the Recompose output preferred on
  4 of 6 generated drafts; all 17 pairs judged the same in meaning;
  perceived authorship at parity with human controls. The rater's own edit
  of a defect draft used deletions only and removed 4 of the 5 injected
  defects; the skill's Preserve output removed 5.

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
