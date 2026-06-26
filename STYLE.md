# Skill Style Guide

Use this guide when creating or updating any skill in this repository.

## Core Principles

- Keep every skill easy to scan and easy to execute.
- Prefer concrete instructions over abstract advice.
- Separate facts, guesses, and recommended next steps.
- Keep examples realistic and aligned with the actual workflow.
- Stay agent agnostic. Skills should not depend on a specific named product or
  model.

## Standards Scope

- Keep shared repository hygiene files aligned with the local standards catalog
  unless this repo needs a documented exception.
- Keep `.config/mise/config.toml` as the command surface for shared standards
  checks.
- Do not add language-specific standards files unless the repository gains that
  language surface.

## Naming And Layout

- Use a lowercase kebab-case folder name for each skill.
- Match the folder name and frontmatter `name` unless there is a strong reason not to.
- Put the required `SKILL.md` at the root of the skill folder.
- Treat `SKILL.md` plus frontmatter `name` and `description` as the required portable contract.
- Keep visible root-level directories reserved for skills.
- Store supporting material in well-named subdirectories:
  - `references/` for longer factual or background material
  - `assets/` for static resources consumed by the skill's output
  - `helpers/` for smaller helper Markdown files
  - `templates/` for reusable output skeletons
- Use `examples/` only when concrete sample inputs or outputs improve trigger
  behavior, output expectations, or forward-testing.
- Keep the structure minimal. Add folders only when they serve the skill.
- Template filenames must match the parent skill name in uppercase form, preserving kebab-case.

## Required SKILL.md Pieces

Every `SKILL.md` should include:

1. YAML frontmatter with at least `name` and `description`.
2. A clear title.
3. A short explanation of when to use the skill.
4. Concrete execution guidance.
5. Any quality bar, checklist, or template needed to apply the skill reliably.

## Frontmatter Guidance

- `name` should be short and stable.
- `description` should front-load trigger words, task intent, important
  boundaries, and intended outcome in plain language.
- Keep descriptions brief but not lossy.
- Keep descriptions vendor-neutral and reusable across tools and environments.

Example:

```md
---
name: polish
description: Exhaustive pre-commit code and documentation polish pass.
---
```

## Writing Style

- Use direct, imperative language.
- Prefer short sections with descriptive headings.
- Optimize for the next reader to act quickly without extra interpretation.
- Make uncertainty explicit.
- Use templates only when they improve consistency. Do not create a
  `templates/` folder for a skill that has no reusable output skeleton.

## Output Quality

Every skill must define enough output rules for a coding agent to produce
useful work without generic filler.

At minimum, each skill should make clear:

- the expected final-output shape, directly or through a template
- what evidence, verification, or uncertainty must be reported
- when the coding agent should stop, refuse, or ask for more context
- how to avoid unsupported sections, placeholders, or boilerplate
- what belongs in the skill instructions versus a template, helper, context file, or example

## Templates

Use `templates/` only for reusable output skeletons that the skill asks the
coding agent to follow. Name each template after the parent skill in uppercase
form, preserving kebab-case.

Examples:

- `polish/templates/POLISH.md`
- `ocd/templates/OCD.md`

Do not use generic names like `REPORT.md` or `SUMMARY.md` when the template
belongs to a specific skill. Do not create empty `templates/` folders.

## Updating An Existing Skill

When editing a skill:

- preserve the original purpose unless the change is intentional
- clean up stale or contradictory wording
- keep examples and templates in sync with the current instructions
- update `README.md` if the top-level skill list changes
- check for product-specific references and replace them with neutral language

## Review Checklist

Before finishing a change, confirm:

- the folder name matches the skill name
- `SKILL.md` exists at the skill root
- frontmatter has `name` and `description`
- support folders are useful and non-empty
- templates use the parent skill's uppercase name
- README catalog entries and install commands are current
- generated, vendored, dependency, build, cache, coverage, and lock output are
  untouched unless a repo tool intentionally updated them
