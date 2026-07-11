---
name: polish
description: Exhaustive pre-commit code and documentation polish pass.
disable-model-invocation: true
---

# Polish

Polish is a relentless, file-by-file finishing pass over the caller's requested
scope. Default to current branch changes; honor explicit paths, commits, ranges,
or repo-wide scope.

Pursue idiomatic elegance with proportionality. Prefer the clearest conventional
expression of the real problem, with abstraction, validation, strictness, and
commentary proportional to actual contracts and risk.

## Contract

- Preserve intended behavior. Treat tests, task requirements, public
  documentation, types or schemas, and authoritative specifications as contract
  evidence. Apply a narrow defect fix when the contract is unambiguous and add
  focused verification; ask before choosing between plausible contracts.
- Remove unwarranted ceremony: helpers, wrappers, guards, abstractions,
  indirection, strictness, or commentary whose cost exceeds the clarity,
  contract, or risk they carry. Preserve trust-boundary validation, meaningful
  error handling, security controls, and useful domain structure.
- Keep specialist audits separate. Address correctness, security, performance,
  and architecture concerns encountered during the pass without claiming a
  dedicated threat model, profile, or architecture review.
- Treat explicit defaults, disabled rules, and other effective no-op
  configuration as possible policy. Use comments, nearby patterns, history,
  tests, and repository standards to establish intent; preserve and report
  genuinely ambiguous cases.
- Prefer direct current implementations over compatibility layers. Preserve a
  layer when affirmative evidence shows a supported external or persisted
  contract. Remove unsupported residue after tracing visible consumers; ask
  when evidence conflicts or the cost of being wrong is substantial.
- Polish comments for signal. Keep or tighten comments that improve
  understanding or preserve durable rationale. Remove narration, conversational
  justification, implementation archaeology, and change-history tombstones
  that carry no live value.
- Write living, current-state documentation in present tense. Preserve ADRs,
  changelogs, release notes, active migration guides, and archived decisions as
  historical records; correct them only when inaccurate in their stated context.
- Make unambiguous fixes directly. Record path-local decisions and continue
  independent work; interrupt only when a decision changes scope or a shared
  contract, creates material security or data risk, or would invalidate
  substantial downstream work.
- Preserve unrelated dirty work and generated, vendored, dependency, build,
  cache, coverage, and lock output. Allow repository tools to update owned
  output during verification, and account for it explicitly.
- Commit only when the caller asks. Keep broad sorting, grouping, and
  layout-only churn in the OCD pass; when both are invoked, finish Polish first.

## Steps

1. Establish scope and build the ledger.
   Read local instructions, task documentation, package scripts, formatter,
   linter, and test configuration, plus the current status and diff. Honor an
   explicit scope and base. Otherwise compare `HEAD` with the merge base of the
   repository's default integration branch, then include staged, unstaged, and
   untracked work. Repo-wide scope includes every active human-maintained path.
   Inspect base and diff content for deletions and renames. Record generated,
   vendor, tool-owned, and unrelated dirty paths without editing them.

   For a large scope, delegate only substantial, reasoning-heavy, disjoint
   slices whose value exceeds coordination cost. Use the highest-capability
   workers available, keep canonical files with their mirrors, share one ledger,
   and retain policy and final-diff ownership with one coordinator. Do not
   delegate menial work. Complete when every candidate path has exactly one
   disposition: edit, already polished, skip with reason, or caller decision.

2. Inspect each candidate end to end.
   Read the whole current file and relevant surrounding flow, not only changed
   hunks. Check correctness, security, and performance risks, local idiom,
   naming, data flow, abstraction weight, error handling, tests, comments,
   documentation impact, sediment, and unwarranted ceremony. Prefer existing
   local helpers and ecosystem conventions over new machinery. Complete when
   every ledger disposition is resolved or recorded for the caller.
3. Align contracts, tests, and documentation.
   Trace externally consumed and persisted surfaces before removing
   compatibility. Give every intentional behavior fix contract evidence and
   focused verification. For branch scope, inspect every documentation surface
   affected by the work; for repo-wide scope, inspect every living
   current-state document. Complete when implementation, tests, comments, help
   text, examples, and normative documentation agree, while historical records
   retain their intended context.
4. Verify and audit the result.
   Run the narrowest checks that meaningfully prove the edits. Follow
   repository-mandated gates and use broader checks when scope or risk warrants
   them. Review the normal diff and a whitespace-insensitive diff when useful.
   Complete when every resulting change is accounted for, material verification
   gaps are known, and excluded dirty work remains intact.
5. Report adaptively.
   Report material changes, verification, skipped areas, and unresolved
   decisions. For repo-wide or blocked passes, also report scope, comparison
   base, and coverage. Omit empty sections, placeholders, and the internal file
   ledger. Complete when the caller can commit or resolve the named decisions
   without another audit summary.
