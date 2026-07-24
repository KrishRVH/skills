# Skills

A collection of reusable coding-agent skills for repository quality,
engineering workflows, visual communication, and prose.

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

## Demos And Communication

- **demo-html** - Single-file before/after HTML demo of UI changes, with
  screenshots captured from the running app and a technical vs non-technical
  language toggle for mixed stakeholder audiences.

  ```sh
  npx skills@latest add KrishRVH/skills/demo-html
  ```

## Writing And Editing

- **animize-candidate** - Fidelity-first prose editing, auditing, and drafting.
  Uses contextual review cues to remove generic performance, evasion, and
  flattening without inventing facts, erasing the writer's voice, or inferring
  authorship.

  ```sh
  npx skills@latest add KrishRVH/skills/animize-candidate
  ```

- **animize-v1** - Frozen original Animize workflow, retained as the comparison
  control for the candidate.

  ```sh
  npx skills@latest add KrishRVH/skills/animize-v1
  ```

## Repository Tidiness

- **ocd** - Behavior-preserving configuration ordering and project organization
  pass. Defaults to current branch changes and prioritizes semantic grouping,
  ecosystem convention, and deterministic ordering among true peers.

  ```sh
  npx skills@latest add KrishRVH/skills/ocd
  ```
