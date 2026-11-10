# Skill Style Guide

Use this guide when creating or updating any skill in this repository.

## Core Principles

- Optimize for a predictable process, not identical output.
- Keep every skill easy to scan and execute.
- Prefer concrete instructions over abstract advice.
- Match specificity to risk: fragile work needs tighter guardrails; contextual
  work needs room for judgment.
- Separate facts, guesses, and recommended next steps.

## Naming And Layout

The [automated skill contract](#automated-skill-contract) fixes names,
required files, and permitted folders. Within it:

- `SKILL.md` with frontmatter `name` and `description` is the portable
  contract. `agents/openai.yaml` carries picker metadata and the
  harness-specific invocation policy.
- Store supporting material in the folder that matches its job:
  - `references/` for longer factual or background material
  - `assets/` for static resources consumed by the skill's output, such as
    document templates, images, fonts, fixtures, or boilerplate
  - `helpers/` for smaller helper Markdown files
  - `templates/` for substantial reusable output skeletons
  - `examples/` for concrete sample inputs or outputs that improve trigger
    behavior, output expectations, or forward-testing
- Keep the structure minimal. Add a folder only when the skill uses it.

## Invocation And Frontmatter

Choose invocation deliberately and follow [the invocation
contract](.agents/invocation.md). Keep the portable frontmatter and machine
metadata synchronized.

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
- A portable name matches its folder and is unique.
- A package contains `SKILL.md`, `agents/openai.yaml`, and optional files only
  in `references/`, `assets/`, `helpers/`, `templates/`, or `examples/`.
  Packages contain no symlinks.
- Agent metadata has a nonempty display name, a 25-64 character short
  description, and an invocation policy synchronized with portable
  frontmatter.
- Every support file is reachable from `SKILL.md` through one or more real
  Markdown links, and local links stay inside their package. Code-span paths do
  not establish reachability.
- `SKILL.md` has at most 500 lines and 50,000 UTF-8 bytes. Reference Markdown
  over 100 lines includes an H2 `Contents` or `Table of contents` section with
  at least one same-document link. Any supporting Markdown file has at most
  100,000 UTF-8 bytes.
- A template name uses the parent skill name as its uppercase stem, keeps the
  kebab-case, and keeps the format's normal extension:
  `skill-name/templates/SKILL-NAME.ext`.
- README contains exactly one complete install command per skill folder in a
  `ruby` display fence containing no other commands.
- Rendered skill prose omits the unambiguous vendor terms configured in
  `.config/skills/validation.json`. Installation commands are exempt.

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

## Neutral Language

Keep skill instructions tool- and vendor-neutral, so the guidance still makes
sense when the skill runs in a different tool:

- Keep product-specific names inside installation instructions, machine
  adapter paths, and documentation that defines those adapters.
- Prefer neutral terms such as `coding agent`, `caller`, `workflow`,
  `workspace`, or `session`.
- Depend on no named product or model.

## Output Quality

Every skill must define enough output guidance to prevent generic filler. Make
clear:

- the expected final-output shape
- what evidence, verification, and material uncertainty to report
- when to continue independently, batch decisions, stop, refuse, or ask
- how to omit unsupported sections and placeholders

Keep simple adaptive reports inline. Use a template only when the skill produces
a substantial, rigid artifact whose exact structure matters.

## Updating An Existing Skill

- Preserve the original purpose unless the change is intentional.
- Start from concrete successes and failures observed in real use.
- Clean up stale or contradictory wording instead of layering exceptions onto
  it.
- Keep examples, pointers, supporting material, and the README entry
  synchronized with the instructions.
- Forward-test substantial or behaviorally subtle revisions with independent,
  highest-capability workers. Give them the skill and realistic raw artifacts,
  not the intended answer or diagnosis.

## Review Checklist

`mise run standards:check` confirms the automated contract. Before finishing
a change, confirm what it cannot decide:

- invocation mode and description match the intended reach
- every step has an appropriate completion criterion
- instructions every branch needs are inline, and each pointer says when to
  follow it
- each behavior has one source of truth and no obvious no-op wording
- every support file is used by the skill
- the README entry still describes the skill
- substantial revisions were forward-tested when practical
