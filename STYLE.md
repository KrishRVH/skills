# Skill Style Guide

Use this guide when creating or updating any skill in this repository.

## Core Principles

- Optimize for a predictable process, not identical output.
- Keep every skill easy to scan and execute.
- Prefer concrete instructions over abstract advice.
- Match specificity to risk: fragile work needs tighter guardrails; contextual
  work needs room for judgment.
- Separate facts, guesses, and recommended next steps.
- Keep skills agent-agnostic. Do not depend on a named product or model.

## Naming And Layout

- Use a lowercase kebab-case folder name for each skill.
- Match the folder name and frontmatter `name` unless there is a strong reason
  not to.
- Put the required `SKILL.md` at the root of the skill folder.
- Treat `SKILL.md` plus frontmatter `name` and `description` as the required
  portable contract.
- Keep visible root-level directories reserved for skills.
- Store supporting material in well-named subdirectories:
  - `references/` for longer factual or background material
  - `assets/` for static resources consumed by the skill's output
  - `helpers/` for smaller helper Markdown files
  - `templates/` for substantial reusable output skeletons
- Use `examples/` only when concrete sample inputs or outputs improve trigger
  behavior, output expectations, or forward-testing.
- Keep the structure minimal. Add folders only when they serve the skill.
- Use the parent skill name as each template's uppercase stem, preserve
  kebab-case, and keep the format's normal extension:
  `skill-name/templates/SKILL-NAME.ext`.

## Invocation And Frontmatter

Choose invocation deliberately:

- Use `disable-model-invocation: true` for an expensive or judgment-heavy skill
  that should run only when the caller names it. Keep its description brief and
  human-facing; do not repeat invocation conditions in the body.
- Keep model invocation enabled only when the agent must discover the skill
  autonomously or another skill must reach it. Front-load a strong task word in
  its description and include one trigger per genuinely distinct branch.

Every `SKILL.md` must include:

1. YAML frontmatter with `name` and `description`, plus the intentional
   invocation setting when needed.
2. A clear title.
3. Concrete steps, reference, or both, arranged by when the agent needs them.
4. A quality and output contract strong enough to execute without generic
   filler.

## Automated Skill Contract

`mise run skills:check` tests the validator, then checks tracked and untracked
non-ignored skill files. The deterministic contract is:

- Frontmatter accepts only `name`, `description`, and the optional
  `disable-model-invocation` field. Names are lowercase kebab-case with at most
  64 characters, descriptions are nonempty strings with at most 1,024
  characters, and the invocation field is boolean when present. Duplicate YAML
  keys are invalid.
- A portable name matches its folder and is unique. A hash-locked comparison
  control may declare its original portable name in
  `.config/skills/validation.json`.
- A package contains `SKILL.md` plus files only in `references/`, `assets/`,
  `helpers/`, `templates/`, or `examples/`. Packages contain no symlinks.
- Every support file is reachable from `SKILL.md` through one or more real
  Markdown links, and local links stay inside their package. Code-span paths do
  not establish reachability.
- `SKILL.md` has at most 500 lines and 50,000 UTF-8 bytes. Reference Markdown
  over 100 lines includes an H2 `Contents` or `Table of contents` section with
  at least one same-document link. Any supporting Markdown file has at most
  100,000 UTF-8 bytes.
- Template names use the uppercase parent skill name, README contains exactly
  one complete install command per skill folder in a shell fence containing no
  other commands, and rendered skill prose omits the unambiguous vendor terms
  configured in `.config/skills/validation.json`. Installation commands are
  exempt from the vendor-term check.

Frozen comparison controls are protected by an exact SHA-256 file manifest and
excluded from mutating Markdown and spelling tasks. Local-link checks still
cover them.

These checks enforce portable structure, bounded context, and discoverable
resources. They do not decide whether a completion criterion is genuinely
checkable, whether a description triggers at the right time, whether an
invocation setting fits the skill's intended reach, or whether an output is
good. Review and forward-test those behavioral properties.

## Information Hierarchy

- Put ordered actions in steps and end each step with a checkable completion
  criterion. Make the criterion exhaustive when the work must account for every
  item in a scope.
- Keep instructions every branch needs in `SKILL.md`. Move only substantial,
  branch-specific reference behind a clearly worded pointer.
- Keep definitions, rules, and caveats for one concept together.
- Keep each behavior in one authoritative place. Remove duplicated guidance,
  stale sediment, and instructions that do not change agent behavior.
- Use a concise leading word when it steers behavior more reliably than a list
  of near-synonyms.

## Writing Style

- Use direct, imperative language.
- Prefer short sections with descriptive headings.
- Optimize for the next reader to act quickly without extra interpretation.
- Make uncertainty and decision boundaries explicit.
- State the desired behavior positively; reserve prohibitions for necessary
  guardrails and pair them with the intended alternative.
- Keep examples realistic and aligned with the actual workflow.

## Output Quality

Every skill must define enough output guidance to prevent generic filler. Make
clear:

- the expected final-output shape
- what evidence, verification, and material uncertainty to report
- when to continue independently, batch decisions, stop, refuse, or ask
- how to omit unsupported sections and placeholders

Keep simple adaptive reports inline. Use a template only when the skill produces
a substantial, rigid artifact whose exact structure matters. Do not create an
empty `templates/` directory.

## Updating An Existing Skill

- Preserve the original purpose unless the change is intentional.
- Start from concrete successes and failures observed in real use.
- Clean up stale or contradictory wording instead of layering exceptions onto
  it.
- Keep examples, pointers, and supporting material synchronized with the
  instructions.
- Update `README.md` when adding, renaming, or removing a top-level skill.
- Replace product-specific references with neutral language.
- Forward-test substantial or behaviorally subtle revisions with independent,
  highest-capability workers. Give them the skill and realistic raw artifacts,
  not the intended answer or diagnosis.

## Review Checklist

Before finishing a change, confirm:

- the folder name matches the skill name
- invocation mode and description match the intended reach
- `SKILL.md` exists at the skill root with valid frontmatter
- every step has an appropriate completion criterion
- required instructions are inline and every relative pointer resolves
- each behavior has one source of truth and no obvious no-op wording
- support folders are useful and non-empty
- templates, when justified, use the parent skill's uppercase name
- README entries and install commands are current
- substantial revisions were forward-tested when practical
