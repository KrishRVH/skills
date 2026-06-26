---
name: polish
description: Exhaustive pre-commit code and documentation polish pass.
disable-model-invocation: true
---

# Polish

Run a polish pass when the caller explicitly invokes `/polish` or `$polish`
before a commit after significant branch work. Polish is a relentless,
file-by-file pass over the branch: improve quality, remove sediment, and make
docs match the repo's current state.

## Contract

- Treat the current behavior as the target unless the caller says otherwise.
- Prefer the direct current implementation over compatibility shims, version
  branches, transitional wrappers, old names, and "previously/newly"
  explanations.
- Keep backward compatibility only when the repo is clearly a published library
  or API, the caller requested it, a migration requires it, or current
  tests/docs prove it is an intentional contract.
- Update docs to describe the repo as it is now, not the history of how it got there.
- Make safe fixes directly; report only decisions that genuinely need the caller.
- Preserve user work in the dirty tree. Do not revert unrelated changes.
- Do not commit unless the caller explicitly asks.
- Skip generated, vendored, dependency, build, cache, coverage, and lock output
  unless the repo's own tools update it during verification.
- Do not run an OCD pass. Avoid broad sorting, grouping, or layout-only churn;
  use `$ocd` for idiomatic ordering and project tidiness.

## Steps

1. Map the branch.
   Read local agent instructions, project task docs, package scripts,
   formatter/linter/test configs, and the dirty diff. Determine the comparison
   base from upstream or the main branch, then include committed branch changes,
   unstaged changes, staged changes, and untracked files. Complete when every
   candidate file is listed as in-scope, generated/vendor/tool-owned skip, or
   unrelated dirty work.
2. Build the file ledger.
   Inspect every in-scope file's current contents and diff context. For each
   file, check correctness risks, idioms, simplicity, naming, abstractions,
   error handling, tests, comments, stale code, and doc impact. Complete when
   no in-scope file is unexamined and each file has a disposition: edit,
   already polished, skip with reason, or needs caller decision.
3. Remove sediment.
   Delete dead code, unused exports, duplicate paths, obsolete comments, stale
   TODOs, compatibility shims, version gates, fallback adapters, migration
   prose, and old-vs-new explanations unless they satisfy the compatibility
   rule in the contract. Complete when every sediment candidate is either
   removed or justified by a live contract.
4. Polish the implementation.
   Make narrowly scoped edits that improve quality, elegance, and local idiom
   without inventing speculative abstractions. Update or add focused tests when
   behavior, contracts, edge cases, or stale paths changed. Complete when every
   edited file reads as the current implementation rather than a layered history
   of the branch.
5. Check documentation drift.
   Compare current behavior, commands, configuration, environment variables,
   public APIs, workflows, examples, and user-facing text against README files,
   docs directories, comments, help text, sample configs, and relevant issue/PR
   docs in the repo. Update or remove stale docs; write present-tense docs for
   the final state. Complete when every changed behavior or surface is
   documented accurately or intentionally undocumented with a reason.
6. Verify the result.
   Run the narrowest meaningful checks for touched areas, then the repo's
   normal gate when reasonable. Review the final diff, including
   whitespace-insensitive diff when useful, for accidental churn, missed docs,
   lingering sediment, and unrelated changes. Complete when verification
   results are known and the diff is fully accounted for.
7. Report concisely.
   Use `templates/POLISH.md` as the final-report skeleton when a structured
   report helps. Name the files or categories polished, docs updated, sediment
   removed, verification run, skipped generated/vendor/tool-owned areas, and
   any remaining caller decisions. Complete when the caller can commit or decide
   on the named blockers without needing another audit summary.

## Reference

- Quality: prefer boring, idiomatic code; standard library and local helpers
  before new dependencies; explicit data flow before hidden coupling; small
  tests that prove behavior.
- Elegance: delete unnecessary layers before refactoring them; collapse
  branch-only abstractions that no longer carry their weight.
- Sediment: stale code, stale comments, old names, transitional APIs,
  compatibility wrappers, versioned explanations, fallback paths, and docs that
  explain a prior state.
- Documentation drift: any mismatch between docs and the actual repo, including
  commands, screenshots, generated examples, env vars, config names, defaults,
  and setup flows.
- File ledger: keep the ledger in working notes; the final response should
  summarize outcomes, not dump every checked file unless the caller asks.
