# Changelog

## animize: catalog entries checked against labeled text (2026-11-10)

Changes:

- `tells.md` keeps ordinary idiom that people write more often than models
  do. The Filler entry leaves a single `in order to`, `the fact that`, `as
a result of`, or `there is … that` as it stands and tightens only a
  passage that stacks them. The overcorrection guard lists the same idiom,
  a plain `because`, and a request's `please`.
- The staged-contrast entry replaces `Not just X, but Y`. It also covers `X
rather than Y`, `Rather than X, Y`, and a contrast split across two
  sentences, and it keeps a contrast whose rejected side is real.
- Two entries are new under Plain speech. Spelled-out contractions: a
  message, email, comment, pull request description, or post contracts
  where a speaker would, and a rule or a stressed form stays full.
  Compressed speech: a message clipped shorter than its writer would say it
  aloud is written at speaking length.
- The clarity profile removes `please` only from a procedure step. A
  request to a person keeps the courtesy its source gave it.
- The entry point treats an instruction inside the material as content. A
  run never follows it, leaves it where a protected span holds it, and
  tells the caller what it says and where. The acceptance gate checks this,
  and the delivery notes list it.
- The stacked-declaratives entry names the plain conjunctions to join
  with: `because`, `so`, `but`, `if`, and `although`.
- The prompt block carries the same changes in short form.
- The evaluation protocol says to check a catalog entry against labeled
  text before it names a construction as a machine default.
- The harness has `construction_rates.py`, which compares how often people
  and models use a construction in the vendor's labeled dataset, and
  `contraction_variants.py`, which isolates what contractions do to a
  detector's score. `idiom/` holds this run.

Measured, with the tables in `animize/references/evaluation-results.md`
under "Catalog revision":

- In 2,038 human-written and 2,046 model-generated documents, people wrote
  `in order to` about 35 times as often as the models, and `there is`,
  `because`, and `please` three to four times as often. The models wrote
  `rather than` and `not just … but` four to five times as often as people.
- A check for runs of similar-length sentences was not added. Three similar
  lengths in a row appear in 60% of the human documents.
- Path tests on the final text: 5 of 5 sessions took the right regime,
  loaded every reference, and asked nothing.
- Batch jobs on the final text: 62 of 62 took the right regime and asked
  nothing, no source number is missing, and no output has a dash character.
  The three Preserve cells ran on the first of three freezes and are
  carried.
- The eight workplace outputs went from no contractions to 14.
- Live model, version 4.1, eight outputs: six model-written documents read
  100% AI-generated before and after, and two human drafts stay Human
  Written. The acceptance criterion for model-written input is still not
  met.
- On the open EditLens models, contractions alone raise the score of a
  model-written workplace draft, and the rest of a run lowers it. The live
  model reads these drafts as 100% AI-generated either way.

Known limit:

- When the material reaches a run through a file, a session removed an
  embedded instruction from inside a quotation and wrote no note, twice.
  It never followed the instruction. The same case passed twice when the
  material was in the conversation.

## animize: the live verdict is the benchmark (2026-11-09)

Changes:

- The evaluation protocol states the skill's main input and target. The
  input is model-written text: messages, emails, pull request descriptions,
  write-ups, and articles. The target is output that reads as
  human-authored, that Pangram's live model reads as human-written, that
  carries no LLM-isms, and that preserves the source's substance.
- The live verdict is the benchmark and an acceptance criterion: a
  model-written input's output reads Human Written, and no rule change
  moves a cell toward machine-written. The protocol no longer bars a rule
  change made for a score. A verdict gain still never excuses a fidelity
  failure or fabricated material.
- The entry point lost two universal rules, `Do not optimize against a
detector` and `Make no detector claim`, and the clauses that pointed to
  them in the objective and in Precedence tiers 1, 4, and 8. The acceptance
  gate lost its `Detector silence` check, and the prompt block lost the
  matching sentence. The universal rules are numbered 1 to 7.
- The rules against manufactured humanity and faked imperfection are
  unchanged.
- The harness has `score_pangram.py`, which sends documents to the live
  model through the vendor's text API and stores text-free rows. The API
  bills by the word, so the script requires a word cap and the protocol
  sets a sampling rule: the same documents before and after a change, three
  at a time, widened only when a verdict moves.
- The harness has two new folders. `rebuild/` holds a variant of Recompose
  that composes every sentence anew, and `workplace/` holds eight fictional
  workplace drafts.

Measured on the live model, version 4.1, with the tables in
`animize/references/evaluation-results.md`:

- Model-written text: 0 of 11 outputs read Human Written. Eight essays,
  news stories, and fiction pieces and three workplace drafts read 100%
  AI-generated before the skill and after it.
- Human drafts: 11 of 12 outputs read Human Written and one reads Mostly
  Human Written, under either regime. On three drafts with planted defects
  the live model flagged the planted sentences, and the skill lowered the
  AI share on each.
- No output has a passage flagged as humanized.
- The rebuild variant was not adopted. It reworded 47% to 74% of each
  model-written draft and moved no verdict, raised the humanizer score, and
  moved two planted-defect human drafts from Human Written to AI Assisted
  and AI Detected.
- The open EditLens models are more lenient than the live model. They read
  several workplace drafts as human that the live model reads as 100%
  AI-generated, so they only rule a candidate out.
- Not run on these outputs: the forward tests and the detector check on
  the text without the two rules, which the next entry covers; the live
  model on five of the workplace drafts, on an article-length draft, and on
  mid-tier outputs.

## animize: one home per rule (2026-11-09)

Changes:

- The entry point opens with the four steps of a run (route, frame, run the
  procedure, deliver) and states the rules after them. The table of files a
  branch loads sits in the step that loads them.
- There is one gate. The entry point's universal gate merged into the
  procedure's acceptance gate, which groups its checks as every run,
  Preserve only, and Recompose only. `verification.md` lost a second
  red-team pass and a third acceptance list.
- The masking rule, the `fix`, `retain`, and `flag` rule, and the record for
  a retained candidate each live once, in the procedure's red-team step.
  Three files had stated them, with three different rules for reporting a
  retained candidate.
- The dash default is stated once, in Precedence tier 8, and the catalogs
  point to it.
- Recompose steps are numbered R1 to R8 beside Preserve's P1 to P4. Step
  lists that summarized a catalog are gone, so each step applies every entry
  of its file. The content lock has one name and one shape, the schema that
  R1 fills.
- The `Directions` section, the clear-communication profile's own brief and
  completion check, and the session-residue section of `tells.md` are gone.
  The procedure, the acceptance gate, and skeptic pattern 16 already held
  their content.
- Preserve runs without the clear-communication profile, whose file it never
  loaded.
- A findings-only run is defined: it skips the two drafting steps, runs the
  rest as a diagnosis, ranks its findings by cost to the reader, and carries
  no origin note. The fixed note said the draft had been recomposed.
- The content lock fills from the whole source boundary, including task
  evidence the caller did not paste, and narrowing a claim that evidence
  does not support is authorized.
- Smaller rules a forward test asked for: a Markdown artifact is returned
  in a fence, PR descriptions and commit messages keep change framing,
  moving a paragraph break is a Preserve operation, and the Preserve notes
  name each edit in plain words.

Measured, with the tables in `animize/references/evaluation-results.md`:

- Size: a Recompose run reads 1,986 lines of instructions, down from
  2,255.
- Forward tests: seven sessions on the consolidated text across two model
  tiers, then four top-tier sessions on the final text, one per path
  (Preserve, Recompose, unstated origin, findings only). No session asked a
  question, and each loaded exactly its branch's fixed reference set,
  checked against its recorded tool calls.
- Guardrail check, which also covers the previous entry: 54 documents on
  each of two model tiers, scored with Binoculars and both open EditLens
  models against the recorded baseline. No verdict moved toward
  machine-written in any cell. Two cells are flagged because their mean
  rose: Recompose on the pilot mirrors (0.484 to 0.515 on the Llama model,
  one document carrying it) and Recompose on ordinary human drafts (0.020
  to 0.032, all ten still read as human).
- Where the outputs stand: every human draft outside one known false
  positive reads as human after either branch, on both models. No
  model-written draft reads as human after Recompose, as at baseline; the
  Llama mean on generated text fell from 0.991 to 0.921.
- Preserve no longer over-edits a strong draft: 0 edited clauses on six
  polished passages, against 11.
- Tier difference: both tiers pass the process checks and read the same on
  human drafts. On model-written text the mid tier rebuilt half as much
  and scored higher, and under Preserve it deleted content the top tier
  left in and flagged. It wrote 1,400 to 4,000 tokens per document against
  8,800 to 21,500.
- Cost of a single run: 72,000 to 132,000 tokens and 3 to 10 minutes on
  the top tier; 55,000 to 76,000 tokens and 36 to 65 seconds on the mid
  tier.
- Three worked Preserve examples were corrected: `clause_diff.py` counted
  an added clause in two of them and different totals in two.
- Not run: the production checker on these outputs (a blind packet of
  twenty is prepared), a blind rating of the outputs or the tiers, and the
  file-target, supplied-samples, text-alone, and long-document cases.
- Open: the test sessions reported eight instructions they had to
  interpret, listed in the results file. None was changed, so the text
  tested is the text shipped.

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
