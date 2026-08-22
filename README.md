# Skills

A collection of reusable coding-agent skills for repository quality,
engineering workflows, visual communication, and prose.

Each visible top-level folder is a skill package with a required `SKILL.md`
entry point and optional supporting files such as references, assets, helpers,
templates, and examples.

See `AGENTS.md` for repository conventions and `STYLE.md` for authoring rules.

Skills are grouped below for browsing only. Each skill remains a visible
top-level folder so discovery and install paths stay predictable.

## Invocation

User-invoked skills run only when the caller names them: [ocd](ocd/SKILL.md),
[polish](polish/SKILL.md), and
[thorough-pr-review](thorough-pr-review/SKILL.md).

Model-invoked skills can also be selected automatically when the task matches:
[animize](animize/SKILL.md).

## Project Commands

Format the skills or run all repository checks through mise:

```sh
mise run standards
mise run skills:check
mise run standards:check
```

`skills:check` runs the skill-contract test suite and validates every
non-ignored package. `standards:check` includes that gate alongside Markdown,
link, spelling, and secret checks.

## Pre-Commit Quality

- **polish** - Exhaustive pre-commit code and documentation finishing pass.
  Defaults to current branch changes and pursues idiomatic elegance while
  preserving intended contracts, applying proportionate verification, and
  removing unwarranted ceremony from code and current documentation.

  ```sh
  npx skills@latest add KrishRVH/skills/polish
  ```

## Code Review

- **thorough-pr-review** - Evidence-bound pull request review for changes where
  a miss is expensive. Traces changed behavior to its real data, executes
  extractable logic, separates spec conformance from defects, and uses
  single-lens specialists plus per-candidate refuters before drafting or
  publishing only high-consequence findings introduced by the change.

  ```sh
  npx skills@latest add KrishRVH/skills/thorough-pr-review
  ```

## Writing And Editing

- **animize** - Combines clear communication with fidelity-safe prose
  recomposition. Its quick processing keeps ordinary
  replies direct, unambiguous, and ready for their destination. Explicit
  writing and rewrite requests can use deep processing to rebuild standalone
  artifacts such as PR descriptions, documentation, articles, and creative
  prose. The audit job reports prose-pattern or rewrite-fidelity findings
  without changing the source. Its clarity lineage includes Diátaxis, the
  Google developer documentation style guide, ASD-STE100, Kohl's _Global
  English Style Guide_, and Cursor's technical-writing skill.

  ```sh
  npx skills@latest add KrishRVH/skills/animize
  ```

## Repository Tidiness

- **ocd** - Behavior-preserving configuration ordering and project organization
  pass. Defaults to current branch changes and prioritizes semantic grouping,
  ecosystem convention, and deterministic ordering among true peers.

  ```sh
  npx skills@latest add KrishRVH/skills/ocd
  ```
