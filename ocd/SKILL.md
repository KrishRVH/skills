---
name: ocd
description: Idiomatic config ordering and clean project organization pass.
disable-model-invocation: true
---

# OCD

OCD is a behavior-preserving organization pass over the caller's requested
scope. Default to current branch changes; honor explicit paths, commits, ranges,
or repo-wide scope. When both skills are invoked, run OCD after Polish.

Use semantic grouping first, conventional ordering second, and deterministic
sorting only among true peers.

## Contract

- Preserve runtime, priority, execution, override, cascade, and match-order
  semantics. Keep behavior-changing opportunities outside the OCD diff and
  report them separately.
- Choose order by this precedence: explicit runtime or schema constraints;
  canonical normalizer output for the region it owns; dominant repository or
  ecosystem convention; lifecycle, dependency, and reading order; semantic
  groups; then deterministic lexical order among true peers.
- Establish peerhood before lexical sorting. True peers have the same role and
  no dependency, priority, override, narrative, lifecycle, cascade, or
  match-order relationship.
- Enter through project task wrappers. A formatter or normalizer owns only the
  regions it actually rewrites; its silence creates no ordering rule.
- Reorder only when the result improves a higher rung of the precedence. Remove
  duplicates only when a canonical normalizer does so or the collection is
  demonstrably set-like. Keep comments attached to the entries they explain.
- Preserve unrelated dirty work and generated, vendored, dependency, build,
  cache, coverage, and lock output. Allow repository tools to update owned
  output during verification, and account for it explicitly.
- Commit only when the caller asks.

## Steps

1. Establish scope, baseline, and inventory.
   Read local instructions, task definitions, package scripts, formatter and
   linter configuration, plus the current status and diff. Honor an explicit
   scope and base. Otherwise compare `HEAD` with the merge base of the
   repository's default integration branch, then include staged, unstaged, and
   untracked work. Repo-wide scope inventories every active human-maintained
   configuration file, manifest, task, ignore rule, structured list,
   source-ordering region, and layout surface. Complete when scope, canonical
   commands, exclusions, and the candidate inventory are fixed.

   For a large scope, delegate only substantial, reasoning-heavy, disjoint
   slices whose value exceeds coordination cost. Use the highest-capability
   workers available, keep canonical files with their mirrors, share one
   inventory, and retain policy and final-diff ownership with one coordinator.
   Do not delegate menial work.
2. Classify ordering regions.
   Classify regions, not whole files, as normalizer-owned, semantic or
   conventional order, true-peer sort, order-sensitive, already idiomatic,
   layout Tier 1, layout Tier 2, or excluded. Complete when no candidate region
   is unclassified.
3. Normalize and organize.
   Run canonical normalizers for the regions they own, then hand-order the
   remaining regions using the contract precedence. Apply a Tier 1 move only
   when it is mechanical and convention-backed, preserves the file's identity,
   has discoverable repository references, shows no external path contract, and
   can be verified. Record architectural, competing-convention, or externally
   visible Tier 2 moves without applying them. Complete when every candidate
   region is normalized, improved, or intentionally preserved.
4. Audit and verify.
   Review normal and whitespace-insensitive diffs. Account for every changed
   value, removal, reorder, deduplication, and move introduced by the pass as
   behavior-preserving. Run the narrowest checks that meaningfully prove the
   edits, follow repository-mandated gates, and use broader checks when scope or
   risk warrants them. Recheck normalizer convergence when doing so adds useful
   evidence rather than ceremony. Complete when the diff is fully accounted for
   and material verification gaps are known.
5. Report adaptively.
   Report material organization changes, preserved semantic-order regions,
   verification, skipped areas, and separately discovered semantic concerns.
   For repo-wide or blocked passes, also report scope, baseline, and coverage.
   After completing unambiguous work, present all Tier 2 layout proposals in one
   follow-up batch. Omit empty sections and placeholders. Complete when the
   caller can accept or reject the proposals without another repository audit.

## Ordering Reference

- Within a block, put identity, selector, and control keys before parameters
  they govern; defaults before overrides; declarations before use; and context
  before policy.
- JSON/JSONC: keep schema and root metadata first; sort true-peer keys inside
  logical groups; keep comments with their entries.
- TOML: use conventional table order and sort true-peer keys inside tables;
  preserve arrays that express priority, execution, or narrative order.
- YAML: treat arrays as semantic until proven otherwise; sort maps only within
  established peer groups.
- Package manifests: prefer ecosystem normalizers and conventions; otherwise
  keep metadata, dependencies, scripts, tooling, and package-manager data in
  their conventional groups.
- Linter/editor configuration: put analysis context before diagnostic policy;
  within policy, put baseline enables before exceptions or disables and
  reporting severity. Sort only independent rule names and diagnostic codes.
- Ignore files: group by purpose or ecosystem; preserve every match-order
  relationship, including negation; sort only positive true-peer patterns.
- Shell and configuration scripts: group aliases and functions while preserving
  initialization, PATH precedence, side effects, and command-availability
  checks.
- Source code: prefer repository convention, public API and lifecycle order,
  dependency, conceptual grouping, and reading flow. Lexically sort only
  established true peers.
- Documentation: reorder factual peer lists and layout descriptions; leave
  prose wording to a prose-polish pass.
- Danger zones include CSS cascade, Dockerfile layers, CI steps, configuration
  cascades, migrations, route registration, plugin arrays, override lists,
  shell startup code, and every include or exclude collection whose match order
  affects the result.
