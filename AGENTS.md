# Repository Guide

This repository stores reusable skills.

## What Lives Here

- Each top-level folder is one skill.
- Every skill folder must contain a `SKILL.md` at its root.
- Supporting material should live inside the skill folder, not at the
  repository root.
- Dot-prefixed root folders are repo infrastructure, not skills.
- Root-level docs explain repository-wide expectations:
  - `README.md` lists the published skills.
  - `STYLE.md` defines how to create and update skills.
  - `AGENTS.md` explains how to work in this repository.

## Expected Shape

Use a simple, predictable structure:

```text
skill-name/
  SKILL.md
  references/
    REFERENCE.md
  assets/
    RESOURCE-FILE
  helpers/
    HELPER-NAME.md
  templates/
    SKILL-NAME.md
```

Optional examples may live in `examples/` when they support trigger behavior,
output expectations, or forward-testing.

## Structure Rules

- The folder name is the skill name and should be lowercase kebab-case.
- `SKILL.md` is required and is the entry point for the skill.
- `SKILL.md` frontmatter must include `name` and `description`; treat those
  fields as the portable skill-selection contract.
- Do not create visible root-level non-skill folders. Use dot-prefixed folders
  for repo infrastructure.
- Keep skill categories as README/catalog organization only. Do not create
  visible grouping folders such as `quality/`, `workflow/`, or `config/`.
- `references/` is for longer factual or background material the skill may lean on.
- `assets/` is for static resources consumed by the skill's output, such as
  document templates, images, fonts, fixtures, or boilerplate.
- `helpers/` is for smaller supporting Markdown files that belong to the parent skill.
- `templates/` is for reusable output skeletons when a skill needs them.
- `examples/` is optional and only for concrete sample inputs or outputs that
  improve trigger behavior, output expectations, or forward-testing.
- Template filenames must match the parent skill name in uppercase form,
  preserving kebab-case. Examples: `polish/templates/POLISH.md`,
  `ocd/templates/OCD.md`.
- Only create directories that the skill actually uses. Avoid empty scaffolding.

## Working In This Repo

- Start by reading the target skill's `SKILL.md`.
- Keep context and examples close to the skill that uses them.
- Update `README.md` when adding, renaming, or removing a top-level skill.
- Follow `STYLE.md` for naming, tone, structure, and update rules.
- Preserve user work in the dirty tree. Do not revert unrelated changes.

## Commands

- Use `mise run tasks` to list the available command surface.
- Use `mise run standards:check` before handoff. For this Markdown-only skill
  catalog, the standards gate runs shared checks and reports no detected
  language-specific build, lint, format, or test tasks.
- Use `mise run secrets` for a focused secret scan.

## Language Rules

Keep the repository tool- and vendor-neutral:

- Do not mention specific assistants, models, or products in skills or docs
  unless a file is documenting an installation command.
- Prefer neutral terms such as `coding agent`, `caller`, `workflow`,
  `workspace`, or `session`.
- Write guidance so it still makes sense if the skill is used in a different
  tool later.
