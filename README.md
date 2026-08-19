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

- **animize** - Rebuilds AI-generated, AI-assisted, or generic prose into
  deliberately authored, genre-native writing, for standalone artifacts such
  as PR descriptions, documentation, articles, and creative prose. Audits
  prose patterns and rewrite fidelity, recomposes structure and stance, and
  sweeps a line-level tell catalog adapted from Cursor's unslop skill,
  preserving facts, substance, and attribution throughout.

  ```sh
  npx skills@latest add KrishRVH/skills/animize
  ```

- **simple-writing** - Clear, direct communication from the coding agent to
  the user: replies, explanations, status updates, summaries, and review
  reports, guided by George Orwell's writing rules, Diátaxis response modes,
  Google developer documentation style, ASD-STE100 Simplified Technical
  English, and Global English disambiguation, while preserving meaning,
  necessary precision, and deliberate voice.

  ```sh
  npx skills@latest add KrishRVH/skills/simple-writing
  ```

## Repository Tidiness

- **ocd** - Behavior-preserving configuration ordering and project organization
  pass. Defaults to current branch changes and prioritizes semantic grouping,
  ecosystem convention, and deterministic ordering among true peers.

  ```sh
  npx skills@latest add KrishRVH/skills/ocd
  ```
