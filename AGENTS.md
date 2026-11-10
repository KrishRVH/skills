# Repository Guide

This repository stores reusable skills.

## What Lives Here

- Each visible top-level folder is one skill, entered through the `SKILL.md`
  at its root. Supporting material lives inside the skill folder.
- Dot-prefixed root folders are repo infrastructure, not skills. Give every
  non-skill root folder a dot prefix.
- Skill categories exist only in `README.md`. Every skill stays a top-level
  folder; grouping folders such as `quality/` or `workflow/` break discovery
  and install paths.
- Root-level docs explain repository-wide expectations:
  - `README.md` lists the published skills.
  - `STYLE.md` defines how to create and update skills: layout, naming,
    frontmatter, the automated contract, and writing rules.
  - `AGENTS.md` explains how to work in this repository.

## Working In This Repo

- Start by reading the target skill's `SKILL.md`.
- Read [`STYLE.md`](STYLE.md) before creating or changing any file inside a
  skill folder.
- Read [`.agents/invocation.md`](.agents/invocation.md) when adding a skill or
  changing whether an agent may invoke one implicitly.
- Update `README.md` when adding, renaming, or removing a top-level skill.
- Preserve user work in the dirty tree. Do not revert unrelated changes.

## Commands

- Run every tool through its mise task; `mise run tasks` lists them. Call a
  package manager or quality tool directly only when fixing the mise task
  that wraps it.
- Run `mise run standards` after editing Markdown. It formats and lint-fixes.
- Run `mise run standards:check` before handoff. It scans for secrets, checks
  Markdown structure and formatting, validates skills and local links, and
  checks prose and filenames for typos.
- Run `mise run skills:check` or `mise run secrets` for a focused pass on
  skill packages or secrets.

## Git

- Keep generated and local-only files out of commits.
- Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/#specification)
  for every commit message.
