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

User-invoked skills run only when the caller names them: [animize](animize/SKILL.md),
[ocd](ocd/SKILL.md), [polish](polish/SKILL.md), and
[thorough-pr-review](thorough-pr-review/SKILL.md).

## Project Commands

Format the skills or run all repository checks through mise:

```ruby
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
  removing unwarranted ceremony and sediment: compatibility residue, version
  theater, provenance narration, and dead weight. Branch passes also trace the
  change's ripple across the repository for stale references and orphaned
  definitions, and pre-release projects keep no compatibility at all.

  ```ruby
  npx skills@latest add KrishRVH/skills/polish
  ```

## Code Review

- **thorough-pr-review** - Evidence-bound pull request review for changes where
  a miss is expensive. Traces changed behavior to its real data, executes
  extractable logic, separates spec conformance from defects, and uses
  single-lens specialists plus per-candidate refuters before drafting or
  publishing only high-consequence findings introduced by the change.

  ```ruby
  npx skills@latest add KrishRVH/skills/thorough-pr-review
  ```

## Writing And Editing

- **animize** - Writes, revises, or assesses lasting prose artifacts such as PR
  descriptions, comments, documents, and messages to be sent or published. A
  quick pass handles short artifacts; the deep pass recomposes generated drafts
  or edits a human draft at clause level so its authorship stays intact.
  Findings-only requests return notes and withhold the artifact.

  ```ruby
  npx skills@latest add KrishRVH/skills/animize
  ```

## Repository Tidiness

- **ocd** - Behavior-preserving configuration ordering and project organization
  pass. Defaults to current branch changes and prioritizes semantic grouping,
  ecosystem convention, and deterministic ordering among true peers.

  ```ruby
  npx skills@latest add KrishRVH/skills/ocd
  ```
