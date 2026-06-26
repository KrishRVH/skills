# Skills

A collection of reusable coding-agent skills for clean working trees, tidy
repositories, and pre-commit quality.

Each visible top-level folder is a skill package with a required `SKILL.md`
entry point and optional supporting files such as templates, references,
helpers, assets, and examples.

See `AGENTS.md` for repository conventions, `STYLE.md` for authoring rules, and
`.config/mise/config.toml` for the standards command surface.

Skills are grouped below for browsing only. Each skill remains a visible
top-level folder so discovery and install paths stay predictable.

## Project Commands

This repository has no language-specific build profile. The shared standards
gate still applies through mise:

```sh
mise run standards:check
```

## Pre-Commit Quality

- **polish** - Exhaustive pre-commit code and documentation polish pass. Use it
  after significant branch work to remove sediment, tighten implementation
  quality, update stale docs, and verify the final diff before committing.

  ```sh
  npx skills@latest add KrishRVH/skills/polish
  ```

## Repository Tidiness

- **ocd** - Idiomatic config ordering and clean project organization pass. Use
  it when behavior should stay fixed but manifests, config, ignore files, docs
  lists, or other safe-to-sort surfaces need cleaner grouping and ordering.

  ```sh
  npx skills@latest add KrishRVH/skills/ocd
  ```
