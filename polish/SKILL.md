---
name: polish
description: Exhaustive pre-commit code and documentation finishing pass.
disable-model-invocation: true
---

# Polish

Polish is a relentless, file-by-file finishing pass over the caller's requested
scope. Default to current branch changes; honor explicit paths, commits, ranges,
or repo-wide scope. Leave no sediment anywhere in scope.

Pursue proportionate, idiomatic elegance. Prefer the clearest conventional
expression of the real problem. Keep abstraction, validation, strictness, and
commentary proportional to actual contracts and risk.

## Contract

- Preserve intended behavior. Treat tests, task requirements, public
  documentation, types or schemas, and authoritative specifications as contract
  evidence. Apply a narrow defect fix when the contract is unambiguous and add
  focused verification; ask before choosing between plausible contracts.
- Treat every affected test as discriminating contract evidence under the
  contract defined in Step 4.
- Remove unwarranted ceremony: helpers, wrappers, guards, abstractions,
  indirection, strictness, or commentary whose cost outweighs its benefits to
  clarity, contract enforcement, or risk reduction. Preserve trust-boundary
  validation, meaningful error handling, security controls, and useful domain
  structure.
- Keep specialist audits separate. Address correctness, security, performance,
  and architecture concerns encountered during the pass without claiming a
  dedicated threat model, profile, or architecture review.
- Treat explicit defaults, disabled rules, and other effective no-op
  configuration as possible policy. Use comments, nearby patterns, history,
  tests, and repository standards to establish intent; preserve and report
  genuinely ambiguous cases.
- Polish comments for signal. Keep or tighten comments that improve
  understanding or preserve durable rationale. Remove narration and
  conversational justification that carry no live value.
- Make unambiguous fixes directly. Record path-local decisions and continue
  independent work; interrupt only when a decision would change scope or a
  shared contract, create material security or data risk, or invalidate
  substantial downstream work.
- Preserve unrelated dirty work and generated, vendored, dependency, build,
  cache, coverage, and lock output. Allow repository tools to update owned
  output during verification, and account for it explicitly.
- Commit only when the caller asks. Broad sorting, grouping, and layout-only
  churn are out of scope for this pass. When OCD is also invoked, leave that
  work to the OCD pass and finish Polish first.

## Sediment

The living tree states only the current system; version control and historical
records hold its past. **Sediment** is anything in the living tree that exists
because of that past rather than the current contract. It falls into four
classes:

- **Compatibility residue**: shims, aliases, re-exports, deprecated wrappers,
  dual code paths, fallback reads of old keys, formats, or paths, flags that are
  fully rolled out, and version checks, polyfills, or workarounds for runtimes,
  dependencies, or platforms below the supported floor.
- **Version theater**: names and prose that define something by its
  predecessor, such as `v2`, `new`, `old`, `legacy`, `improved`, `unified`,
  "now", "no longer", "instead of", and release-note voice ("as of 2.3") in
  living documentation. A version that names a live contract, such as an API,
  schema, protocol, or published release, is current state.
- **Provenance narration**: comments and prose that tell how the code got here,
  such as "moved from", "previously", "refactored to", dated notes, ticket or
  review references that stand in for rationale, tombstones for deleted code,
  and commented-out code. Durable rationale for why the current code must be
  this way, and license or attribution notices, are current state.
- **Dead weight**: unreachable branches; unused exports, parameters, options,
  dependencies, files, and fixtures; configuration keys and environment
  variables that nothing reads or nothing sets; superseded copies such as
  `*_old` or `*.bak`; tests and documentation for retired behavior; and TODOs
  for finished work.

Remove sediment when a reader or consumer who knows only the current state
loses nothing. A consumer the repository cannot show is no consumer: keep a
compatibility layer only when affirmative evidence shows a supported external
or persisted contract, such as a published package's public API, a documented
external interface, or data and configuration persisted outside the
repository. Ask when the evidence conflicts.

The release stage decides what can hold a contract. A **pre-release** project
has no users, so nothing it ever exposed protects a consumer: every
compatibility layer, deprecation, migration guide, and name or prose that
points at an earlier version is sediment, and code and documentation state only
the current, idiomatic, stable design. In a released project, compatibility with a shape that never reached
the default integration branch or a release protects no consumer; remove it.

Historical records keep their past by design: ADRs, changelogs, release notes,
active migration guides, migration histories that tooling replays, and archived
decisions. Correct them only when they are inaccurate in their stated context.
Write living documentation in present tense.

Sediment outside scope stays in place; name it in the report so the caller can
run a repo-wide pass.

## Steps

1. Establish scope and build the ledger.
   Read local instructions, task documentation, package scripts, formatter,
   linter, and test configuration, plus the current status and diff. Honor any
   explicit scope and comparison base. When no base is given, compare `HEAD`
   with the merge base of the repository's default integration branch. Include
   staged, unstaged, and untracked work. Repo-wide scope includes every active
   human-maintained path. Record generated, vendored, tool-owned, and unrelated
   dirty paths without editing them.

   Establish the release stage from the caller's statement, repository
   instructions, and release evidence: package metadata marking a published
   package, release tags, production deployment configuration, and released
   changelog entries. Without such evidence the project is pre-release.

   Sweep the scope for sediment. The sweep costs what the remaining sediment
   costs, so a clean scope sweeps cheaply.

   - **Ripple**: when the scope is a change, collect every identifier, path,
     option, key, and user-visible value it removes, renames, or stops using,
     then search the whole repository for survivors: stale references to what
     is gone and definitions left without callers. Search distinctive forms
     such as qualified names, full paths, and exact keys; use reference-aware
     tooling for generic names. Survivors are in scope because the change
     created them.
   - **Census**: search every candidate path outside historical records for
     sediment signatures: `legacy`, `deprecated`, `compat`, `shim`, `polyfill`,
     `fallback`, `backward`, "kept for", "no longer", "previously", "formerly",
     "used to", "moved from", "renamed", `old`, `new`, and version-number
     affixes on names, TODOs that name a migration or removal, runtime and
     dependency version checks, and commented-out code. Run any configured
     unused-code tooling and keep its in-scope findings.

   Batch terms into few searches, count hits per file before reading, and open
   each hit with its surrounding context rather than its whole file. Add every
   survivor and hit to the ledger as a sediment site.

   For a large scope, delegate only substantial, reasoning-heavy, disjoint
   slices whose value exceeds coordination cost. Use the highest-capability
   workers available, keep canonical files with their mirrors, share one ledger,
   and retain policy and final-diff ownership with one coordinator. Do not
   delegate menial work.

   Complete when every ripple term and census signature is searched and every
   candidate path and sediment site has exactly one disposition: edit, already
   polished, current state with reason, skip with reason, or caller decision.

2. Inspect each candidate end to end.
   Read the whole current file and relevant surrounding flow, not only changed
   hunks. Check correctness, security, and performance risks, local idiom,
   naming, data flow, abstraction weight, error handling, tests, comments,
   documentation impact, sediment, and unwarranted ceremony. Prefer existing
   local helpers and ecosystem conventions over new machinery. Settle each
   sediment site from its surrounding context and, before removing it, its
   consumers. Complete when every ledger disposition is resolved or recorded
   for the caller.
3. Align contracts, tests, and documentation.
   Give every intentional behavior fix contract evidence and focused
   verification. For branch scope, inspect every documentation surface
   affected by the work; for repo-wide scope, inspect every living
   current-state document. Complete when implementation, tests, comments, help
   text, examples, and normative documentation agree.
4. Verify and audit the result.
   Under the discriminating-evidence contract, every affected test has these
   properties:

   - It goes red for a specific production-side fault that violates its
     maintained behavioral claim.
   - It stays green for claim-preserving behavior.
   - It serves a justified coverage role.

   For each added, materially changed, removed, or replaced test, establish
   claim-specific red evidence using this fallback hierarchy:

   1. Against the base.
   2. Otherwise, against a minimal production-side fault.
   3. Otherwise, through a falsifiable trace naming the execution obstacle,
      fault, and failing assertion.

   For broad assertion surfaces, also observe a relevant claim-preserving
   variation stay green. Focused assertions may establish specificity from
   their bounded dependencies. Removing or replacing a test preserves its
   claim, boundary role, and fault sensitivity elsewhere, or cites affirmative
   evidence that the claim is no longer maintained.

   Run the narrowest checks that meaningfully prove the edits. Follow
   repository-mandated gates and use broader checks when scope or risk warrants
   them. Review the normal diff and a whitespace-insensitive diff when useful.
   Complete when every affected test satisfies the discriminating-evidence
   contract, every resulting change is accounted for, material verification gaps
   are known, and excluded dirty work remains intact.

5. Report adaptively.
   Report material changes, verification, skipped areas, and unresolved
   decisions, and name sediment seen outside scope. When the release stage
   decided a removal, state the stage and its evidence. For repo-wide or blocked
   passes, also
   report scope, comparison base, and coverage. Omit empty sections,
   placeholders, and the internal file ledger. Complete when the caller can
   commit or resolve the named decisions without another audit summary.
