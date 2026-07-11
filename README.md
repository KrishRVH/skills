# Skills

A collection of reusable coding-agent skills for clean working trees, tidy
repositories, and pre-commit quality.

Each visible top-level folder is a skill package with a required `SKILL.md`
entry point and optional supporting files such as references, assets, helpers,
templates, and examples.

See `AGENTS.md` for repository conventions and `STYLE.md` for authoring rules.

Skills are grouped below for browsing only. Each skill remains a visible
top-level folder so discovery and install paths stay predictable.

## Project Commands

Format the skills or run all repository checks through mise:

```sh
mise run standards
mise run standards:check
```

## Pre-Commit Quality

- **polish** - Exhaustive pre-commit code and documentation finishing pass.
  Defaults to current branch changes and pursues idiomatic elegance while
  preserving intended contracts, applying proportionate verification, and
  removing unwarranted ceremony from code and current documentation.

  ```sh
  npx skills@latest add KrishRVH/skills/polish
  ```

## Repository Tidiness

- **ocd** - Behavior-preserving configuration and project organization pass.
  Defaults to current branch changes and prioritizes semantic grouping,
  ecosystem convention, and deterministic ordering among true peers.

  ```sh
  npx skills@latest add KrishRVH/skills/ocd
  ```
