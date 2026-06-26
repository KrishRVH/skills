---
name: ocd
description: Idiomatic config ordering and clean project organization pass.
disable-model-invocation: true
---

# OCD

Run an OCD pass only when the caller explicitly invokes `/ocd` or `$ocd`. An
OCD pass is idiomatic polish: extreme sorting, clean grouping, and tidy layout
with behavior preserved.

## Contract

- Preserve behavior. Neatness loses to semantics.
- Treat existing formatters, linters, package-manager normalizers, and project
  task wrappers as authoritative.
- Sort within meaningful groups, not across boundaries where order carries
  priority, execution, override, or cascade semantics.
- Define clean as easier scanning: conventional order, stable sections, short
  comments, no duplicate entries, no gratuitous churn.
- Leave generated, vendored, dependency, build, cache, coverage, and lock output
  alone unless the repo's own command updates it during verification.

## Steps

1. Map the repo.
   Read local instructions, task files, package scripts, formatter/linter
   configs, and the dirty diff. Complete when the canonical commands,
   generated-output exclusions, and candidate files are known.
2. Classify candidates.
   Mark each candidate as tool-owned, safe-to-sort, semantic-order, or skip.
   Complete when no candidate is unclassified.
3. Polish safe areas.
   Run canonical normalizers first; hand-sort only where no tool owns the order.
   Complete when every safe candidate is sorted, grouped, deduplicated,
   formatted, or explicitly left unchanged because it is already idiomatic.
4. Audit the diff.
   Review normal and whitespace-ignored diffs. Complete when changed values,
   removed entries, reordered arrays, and moved blocks are all accounted for as
   behavior-preserving or explicitly intentional.
5. Verify and report.
   Use `templates/OCD.md` as the final-report skeleton when a structured report
   helps. Run the narrowest useful checks, then the repo's normal gate when
   reasonable. Complete when the final response names cleaned categories,
   verification, intentional semantic changes or none, and skipped
   semantic-order files.

## Reference

- JSON/JSONC: keep schema/root metadata first; sort keys inside logical groups;
  preserve JSONC comments.
- TOML: group tables in conventional order; sort simple keys inside tables;
  preserve arrays whose order documents priority or execution.
- YAML: assume arrays may be semantic; sort maps only when clearly safe.
- Package manifests: use ecosystem normalizers when available; otherwise keep
  metadata, dependencies, scripts, tooling config, and package-manager metadata
  in idiomatic order.
- Linter/editor config: co-locate defaults, language overrides, naming/style
  rules, diagnostics, and file overrides; sort independent rule names and
  diagnostic codes.
- Ignore files: group by source or ecosystem; preserve negation ordering.
- Shell/config scripts: format and group aliases/functions, but preserve
  initialization order, PATH precedence, side effects, and command availability
  checks.
- Docs: align lists and layout descriptions with the repo, but do not style-edit prose unless asked.
- Semantic-order danger zones: CSS cascade, Dockerfile layers, CI steps,
  migrations, route registration, plugin arrays, override lists, shell startup
  code, and any include/exclude list where first match wins.
