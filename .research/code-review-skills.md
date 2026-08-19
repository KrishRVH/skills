# Evidence note for the thorough-pr-review skill

Date: 2026-08-18

## Question and method

What do the best publicly available code-review skills, prompts, and AI
reviewer designs actually do, and which techniques are worth absorbing into
[thorough-pr-review](../thorough-pr-review/SKILL.md)? Sources were read in the
primary form — the actual SKILL.md/command/agent files on GitHub, official
vendor docs and engineering posts, and the papers themselves (two fetched as
PDFs and text-extracted). Techniques already in the skill (full-diff+history
reading, consumer map, producer tracing, execution of extractable logic, the
22-row sweep, the reasoning self-audit, one-lens-per-specialist fan-out with a
separate refuter, severity tiers with a publishable/report-only split, comment
drafting verification, the four-part comment shape) are treated as baseline and
not restated as findings.

## Anthropic: `/code-review` plugin (claude-code repo)

The command file is a 9-step orchestration: precondition triage by a cheap
agent (skip closed/draft/trivial/already-reviewed PRs), CLAUDE.md discovery,
a PR summary agent, four parallel review agents (two CLAUDE.md-compliance, two
bug hunters), then **one validation subagent per flagged issue, in parallel**,
each given only the PR context plus that single issue and asked to confirm it
"with high confidence"; unvalidated issues are dropped.
([code-review.md](https://github.com/anthropics/claude-code/blob/main/plugins/code-review/commands/code-review.md))

Distinctive mechanisms:

- **A hard high-signal bar stated as positives and negatives.** Flag only:
  fails to compile/parse, "will definitely produce wrong results regardless of
  inputs," or a CLAUDE.md violation "where you can quote the exact rule being
  broken." Do not flag: style, "potential issues that depend on specific
  inputs or state," subjective improvements. "If you are not certain an issue
  is real, do not flag it."
- **An explicit false-positive list** used at both generation and validation:
  pre-existing issues, looks-like-a-bug-but-correct, pedantic nitpicks,
  anything a linter will catch, general quality concerns not in CLAUDE.md,
  issues explicitly silenced in code.
- **Comment mechanics:** one comment per unique issue; committable suggestion
  blocks only "UNLESS committing the suggestion fixes the issue entirely";
  code links must use the full SHA permalink format with ≥1 line of context.
- The README describes 0–100 confidence scoring with an 80 threshold
  ([README](https://github.com/anthropics/claude-code/blob/main/plugins/code-review/README.md)),
  though the current command file implements filtering through per-issue
  validation subagents rather than numeric scores — the README lags the
  prompt.

## Anthropic: `pr-review-toolkit` plugin

A conditional fan-out: `code-reviewer` always runs; `pr-test-analyzer`,
`comment-analyzer`, `silent-failure-hunter`, `type-design-analyzer`,
`code-simplifier` dispatch only when the diff touches their material.
([review-pr.md](https://github.com/anthropics/claude-code/blob/main/plugins/pr-review-toolkit/commands/review-pr.md))
The interesting content is in the aspect agents:

- [silent-failure-hunter](https://github.com/anthropics/claude-code/blob/main/plugins/pr-review-toolkit/agents/silent-failure-hunter.md)
  asks, for every catch block, to "list every type of unexpected error that
  could be hidden by this catch block" — same class as the skill's swallowed-
  errors row, with the output shape made explicit.
- [pr-test-analyzer](https://github.com/anthropics/claude-code/blob/main/plugins/pr-review-toolkit/agents/pr-test-analyzer.md)
  rates each _recommended_ test 1–10 for criticality and requires "specific
  examples of failures it would catch" — recommendations priced, not listed.
- [comment-analyzer](https://github.com/anthropics/claude-code/blob/main/plugins/pr-review-toolkit/agents/comment-analyzer.md)
  cross-references every claim in a code comment against the implementation
  (comment rot as a reviewable defect class).
- [type-design-analyzer](https://github.com/anthropics/claude-code/blob/main/plugins/pr-review-toolkit/agents/type-design-analyzer.md)
  scores encapsulation / invariant expression / usefulness / enforcement 1–10.

These are review-the-work-in-progress agents, not adversarially verified PR
review; there is no refutation stage and severity is by assertion.

## Anthropic: claude-code-security-review (GitHub Action)

The strongest false-positive machinery found anywhere in this survey, in
[security-review.md](https://github.com/anthropics/claude-code-security-review/blob/main/.claude/commands/security-review.md):

- Two-stage generate-then-validate: one sub-task finds vulnerabilities, then
  **one parallel sub-task per finding** filters false positives; anything with
  validator confidence < 8/10 is dropped.
- **Hard exclusions** (17 rules): DoS, rate limiting, memory safety in
  memory-safe languages, regex injection/ReDoS, SSRF that controls only the
  path, findings in markdown files, lack-of-hardening, etc. A deterministic
  regex layer implements part of this in
  [findings_filter.py](https://github.com/anthropics/claude-code-security-review/blob/main/claudecode/findings_filter.py)
  before any model-based filtering.
- **Precedents encoding a trust model**, not just noise rules: "Environment
  variables and CLI flags are trusted values"; "A lack of permission checking
  ... in client-side JS/TS code is not a vulnerability"; "React and Angular
  are generally secure against XSS" absent `dangerouslySetInnerHTML`; UUIDs
  are unguessable. These kill the classic LLM security false positives by
  naming the boundary assumption instead of asking for generic confidence.
- Scope rule stated flat out: "focus ONLY on security implications newly added
  by this PR. Do not comment on existing security concerns."
- Calibration sentence worth keeping: "Better to miss some theoretical issues
  than flood the report with false positives."

## cursor/plugins: `interrogate` (pstack)

A multi-reviewer adversarial review where "the adversarial signal comes from
model diversity, not assigned personas": the same prompt + rubric goes to
reviewers on different frontier models (Fable, sol, Grok, Opus by default), and
"agreement across models is high-confidence signal; lone-model findings are
worth reading but lower confidence."
([SKILL.md](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/SKILL.md))
Supporting references:

- The [reviewer prompt](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/references/reviewer-prompt.md)
  locks intent: "Do NOT question the intent itself... challenge the
  execution," demands evidence per finding, and legitimizes the empty review
  ("If you have zero findings, say so").
- The [rubric](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/references/rubric.md)
  has two lenses the skill's table does not name as such: **root cause vs
  symptom** (is the fix at the right layer; "if you see a workaround, ask why
  the workaround is needed") and **check-the-real-thing verification** (mtime
  vs actual value; trusting self-reports of async work).
- [lead-judgment.md](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/references/lead-judgment.md)
  is a filtering doctrine for the aggregator: **nitpick gravity** ("reviewers
  tend to fill their review... if a reviewer's findings are all nits, the code
  is probably fine"), **hypothetical vs actual** (trace the call site before
  accepting "what if null"), **"I would have done it differently" is the most
  common false positive**, an Act-On budget ("more than 5 items, you're
  probably not filtering hard enough"), and the Dismissed section framed as
  "a trust mechanism," letting the user override the filter.

The companion `thermo-nuclear-code-quality-review`
([SKILL.md](https://github.com/cursor/plugins/blob/main/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md))
is a deliberately maximalist maintainability lens ("code judo," 1k-line file
gate, spaghetti-growth blockers). It is the mirror image of
thorough-pr-review's out-of-scope section — useful as a separate finishing
skill, not as material for this one.

## obra/superpowers

Three related skills.
[requesting-code-review](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md)
dispatches a reviewer subagent with "precisely crafted context... never your
session's history," partly to keep the coordinator's context window free. The
[reviewer template](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/code-reviewer.md)
reviews a SHA range against a stated plan, forbids the reviewer from spawning
its own subagents, requires a read-only checkout (worktree for other
revisions), and ends in a mandatory verdict: "Ready to merge? Yes | No | With
fixes."
[receiving-code-review](https://github.com/obra/superpowers/blob/main/skills/receiving-code-review/SKILL.md)
is the author-side mirror: verify feedback against the codebase before
implementing, no performative agreement, a YAGNI grep before "implementing
properly," and clarify all unclear items before implementing any. It is a
different skill's territory (responding to review, not producing one), but its
verification-before-action stance matches the skill's dismissal bar.

## Greptile: "How we made the AI reviewer shut up"

The most honest engineering post in the set
([make-llms-shut-up](https://www.greptile.com/blog/make-llms-shut-up)).
Baseline: ~19% of generated comments were addressed; the rest were mostly
technically-correct nits. Three attempts:

1. Prompting against nits — failed.
2. **LLM-as-judge severity scoring (1–10, cut below 7) — failed because "the
   LLM's judgment of its own output was nearly random."** This is a directly
   measured negative result against the confidence-score pattern that several
   other tools advertise.
3. Embedding clustering of past team-labeled comments — block a candidate
   comment if cosine similarity > 0.7 to ≥3 downvoted comments — worked;
   address rate rose past 55%.

The working mechanism depends on longitudinal per-team feedback data, which a
stateless skill does not have. The transferable lesson is the negative one:
self-reported severity/confidence from the same model is weak evidence, and
filtering should rest on checkable properties (the skill's deciding-evidence
bar) rather than scores.

## cubic: learnings from three architecture revisions

([learnings-from-building-ai-agents](https://www.cubic.dev/blog/learnings-from-building-ai-agents))
claims a 51% false-positive reduction and half the median comments per PR from
three changes: (1) **explicit reasoning logs** — the agent must state its
reasoning before the finding, which made failure patterns diagnosable and
"forced structured thinking before conclusions"; (2) **fewer tools** — cutting
the toolset to a simplified LSP plus a terminal reduced confusion; (3)
**specialized micro-agents** (planner, security, duplication, editorial)
replacing one mega-prompt full of edge-case rules. The companion post
([the-false-positive-problem](https://www.cubic.dev/blog/the-false-positive-problem-why-most-ai-code-reviewers-fail-and-how-cubic-solved-it))
is mostly mechanism-free marketing (its numbers are industry citations, not
measurements) — the one concrete item is using static type information to
check whether a flagged issue can occur.

## CodeRabbit

The [context engine post](https://www.coderabbit.ai/blog/explainable-reviews-coderabbit-review-context-engine)
describes: a code graph tracing how the change connects cross-file; context
assembly per PR (linked issues, standards, past PRs, "learnings") filtered to
the change; signals from 40+ linters/SAST tools run in sandboxes; and a
two-tier agent design where "review agents surface candidate comments;
verification agents filter suggestions against code guidelines and team
preferences before output" (see also
[agentic code validation](https://www.coderabbit.ai/blog/how-coderabbits-agentic-code-validation-helps-with-code-reviews),
which is thin on mechanism). Marketing gloss aside, the load-bearing ideas —
generate-then-verify, deterministic tooling as evidence, repo-owned learnings
— are corroborated elsewhere. Independent field data: a study of 31,073
CodeRabbit comments found **36.4% accepted, 56.3% rejected**, with rejections
driven by invalid findings, redundancy, out-of-scope suggestions, and
intent misalignment ([arXiv:2607.03316](https://arxiv.org/abs/2607.03316)).
Even a context-heavy commercial reviewer is majority-rejected in the wild,
which supports the skill's high publication bar.

## Graphite Diamond

Public material on the reviewer itself is feature-level
([graphite.dev/reviewer](https://graphite.dev/reviewer)); the mechanism is in
the eval writeup ([Braintrust case study](https://www.braintrust.dev/customers/graphite)):
ground truth harvested from real accept/reject and upvote/downvote actions on
Diamond's own comments, scored by line-range intersection, semantic
similarity across pipeline versions, and binary user feedback, with acceptance
rate as the primary quality metric. That is an ops practice for a product with
telemetry, not a prompt technique; nothing here transfers directly to a
stateless skill beyond "measure against real dispositions if you ever can."

## OpenAI Codex review

Codex "flags only P0 and P1 issues so review comments stay focused on
high-priority risks" on GitHub
([docs](https://developers.openai.com/codex/integrations/github)) — the same
publishable-tier idea the skill already has. Two mechanisms stand out:

- **Repo-owned review rules**: an AGENTS.md `## Code Review Rules` section,
  scoped by directory, with guidance to "encode a check reviewers repeatedly
  explain," scope narrowly, state the safe path, and "describe outcomes, not
  function names that may change." Their eval: rule-guided review found 98% of
  required custom findings vs 58.3% baseline
  ([custom rules post](https://developers.openai.com/blog/custom-code-review-rules-for-codex)).
- **Execution as validation**: GPT-5-Codex review "navigates your codebase,
  reasons through dependencies, and runs your code and tests to validate
  correctness," and human graders found fewer incorrect/unimportant comments
  ([Introducing upgrades to Codex](https://openai.com/index/introducing-upgrades-to-codex/)).
  This is independent corroboration of the skill's Step 4 — one of the very
  few outside confirmations that running the code, not just reading it, is
  what moves comment correctness.

## Google eng-practices reviewer guide

The standard of review: approve "once it is in a state where it definitely
improves the overall code health of the system... even if the CL isn't
perfect"; "there is no such thing as 'perfect' code—there is only better
code" ([standard](https://google.github.io/eng-practices/review/reviewer/standard.html)).
[What to look for](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
is a breadth checklist (design, functionality, complexity, tests, naming,
comments, consistency, every line, context, good things).
[Comments guidance](https://google.github.io/eng-practices/review/reviewer/comments.html):
explain why; comment on the code, never the developer; label severity with
`Nit:` / `Optional (or Consider):` / `FYI:`; and — the sharpest rule — if the
author has to _explain_ code to the reviewer, the resolution is "rewrite the
code more clearly," because review-thread explanations are not durable.
This is a human-process document about sustained collaboration; its severity
labels and approval standard address problems (author relations, velocity)
the skill deliberately keeps out of scope.

## Academic work

- **Bacchelli & Bird 2013** (Microsoft, ICSE;
  [PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ICSE202013-codereview.pdf)):
  finding defects is the top _stated_ motivation, but in 570 classified review
  comments only 78 (14%) were defects, mostly "small logical low-level
  issues"; 29% were code improvements; understanding-seeking was the
  second-largest category, and "understanding is the main challenge when
  doing code reviews." Human review under-delivers on exactly the deep defect
  classes the skill's sweep targets — evidence that a mechanical sweep adds
  something humans demonstrably don't do, not that it imitates them.
- **Czerwonka, Greiler & Tilford 2015**, "Code Reviews Do Not Find Bugs"
  ([PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2015/05/PID3556473.pdf)):
  ~15% of reviewer comments indicate a possible defect; ≥50% concern
  maintainability. Reviewer usefulness is a function of familiarity — a
  reviewer new to the code averages 33% useful comments, rising to ~67% by
  their third review of the same area. Usefulness degrades with review size,
  noticeably from ~20 changed files.
- **SmartBear/Cisco study**
  ([best-practices page](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/)):
  review ≤200–400 LOC at a time; defect density drops sharply above 500
  LOC/hour; 200–400 LOC over 60–90 minutes yields 70–90% defect discovery.
  These are human-cognition limits, but they double as an honest prior: on a
  5,000-line PR, _any_ single pass — human or model — is operating past the
  regime where high discovery rates were ever measured.
- **Mäntylä & Lassenius 2009**
  ([IEEE TSE](https://dl.acm.org/doi/10.1109/TSE.2008.71)): 75% of
  review-found defects are evolvability, not functional — convergent with the
  two Microsoft studies.
- **Perspective-based reading** (Basili et al.,
  [PBR](https://www.cs.umd.edu/~mvz/handouts/emp_pbr.pdf)): assigning each
  reader one distinct perspective beats ad-hoc reading on team defect
  coverage because perspectives find complementary defects; later
  replications found PBR at least as effective as checklists and cheaper.
  This is the empirical ancestry of the skill's one-lens-per-specialist rule.

## Cross-source synthesis

Techniques that recur among the strongest sources:

1. **Generate wide, then independently validate each finding.** Anthropic's
   code-review and security-review both dispatch one validator per candidate
   finding; CodeRabbit runs verification agents over candidate comments;
   Codex validates by executing. Everyone serious converged on two-stage
   review with an isolated skeptic per claim.
2. **Noise control by enumerated exclusions, not by confidence scores.** The
   security-review's hard exclusions and trust-model precedents, Anthropic's
   false-positive list, Codex's P0/P1-only policy. Greptile measured why:
   self-judged severity was "nearly random," while categorical rules and
   external feedback worked.
3. **Scope to what the change introduced.** Pre-existing issues are excluded
   by Anthropic's FP list, security-review's objective, and are a top
   rejection cause in the CodeRabbit field study.
4. **Repo-owned review rules that get cited in findings** (CLAUDE.md quoting,
   AGENTS.md Code Review Rules, CodeRabbit learnings/path instructions), with
   measured effect in Codex's 98%-vs-58% eval.
5. **The reviewer's output budget is part of the design**: one comment per
   issue, Act-On ≤ 5, "few high-conviction comments over cosmetic notes"
   (Anthropic, cursor lead-judgment, thermo, Greptile).

Unique but compelling: model-diversity consensus as an orthogonal adversarial
signal (cursor interrogate); reasoning-before-finding logs as a debuggability
device (cubic); familiarity and size curves as quantified review-risk factors
(Czerwonka, SmartBear); the Dismissed section as a trust mechanism (cursor —
the skill already reports its dismissal ledger to the caller, which covers
this).

## Candidate ideas for thorough-pr-review

Ranked. Each excludes what the skill already does.

**1. Introduced-by-this-change scope rule.**
Sources: Anthropic code-review FP list; claude-code-security-review ("Do not
comment on existing security concerns"); arXiv:2607.03316 (out-of-scope is a
top rejection cause). Change: add to the Contract (or Step 8) that a
publishable defect must be introduced, activated, or materially worsened by
the diff; a pre-existing defect the review happens to uncover goes to the
caller report, never the publishable set. The consumer map already handles the
subtle case (unchanged code whose requirements moved counts as activated —
that distinction needs stating so this rule doesn't gut the skill's best
artifact). Cost: a few lines; closes a real gap — nothing currently stops a
Critical-severity pre-existing bug from being published onto an unrelated PR.

**2. Shard the refuter: one validator per candidate.**
Sources: Anthropic code-review step 5; security-review step 2; CodeRabbit
verification agents. Change: Step 7's single refuter pass over the merged list
becomes parallel per-candidate refuters, each briefed with one candidate and
the evidence pack, none seeing the others' candidates; the primary reviewer
keeps reconciliation. Rationale: a single refuter over a long list is exactly
the attention-dilution failure the fan-out exists to prevent, and every
production system that measured false positives converged on per-finding
isolation. Cost: more subagent invocations (bounded by candidate count); keep
the single-refuter form as the degraded fallback when worker slots are scarce.

**3. Trust-model precedents for the Security and Authorization lenses.**
Source: claude-code-security-review's precedents and hard exclusions. Change:
give the security specialist a compact precedent table (env vars/CLI flags are
trusted; client-side code needs no auth checks — the server does; framework
auto-escaping counts as encoding unless bypassed; path-only SSRF is not a
finding; memory-safety findings require a memory-unsafe language). Cost: ~10
lines in the specialist brief; risk is over-exclusion in unusual threat models
(e.g. a repo where env vars _are_ attacker-influenced), so precedents should
be stated as rebuttable defaults the repo's own docs can override.

**4. Re-review awareness.**
Source: Anthropic code-review step 1 (check whether Claude already commented;
never post duplicates). Change: Step 1 also fetches existing review threads;
Step 9/10 must not re-publish a finding an existing open or resolved thread
already covers — reference the thread instead — and repeated invocation on the
same PR must not double-post. Cost: one fetch plus a dedup check; without it
the skill misbehaves on its most likely real usage pattern (run, push fixes,
run again).

**5. Size-and-familiarity evidence limit.**
Sources: SmartBear/Cisco (defect discovery measured at 200–400 LOC, ≤500
LOC/h); Czerwonka et al. (usefulness degrades from ~20 files). Change: when
the diff is far past this regime, record it as a named evidence limit in the
report (and optionally suggest splitting), the same way unrunnable checks are
recorded. The numbers are human-cognition measurements, not model limits, so
use them as an honesty device, not a hard gate. Cost: trivial; keeps the
report from implying uniform confidence over a 10k-line diff.

**6. Cross-model refutation for unresolved candidates.**
Source: cursor interrogate (model diversity as adversarial signal; consensus
weighting). Change: not a full multi-model fan-out — the skill's lens
partition already buys coverage — but for candidates the refuter classifies
_unresolved_, offer a second opinion from an independent model as one of the
"cheapest settling checks" (this environment already has an authenticated
sol worker per user config). Cost: infra-dependent, so it must stay optional;
worth it only where the deciding evidence is genuinely ambiguous, since
model agreement is weaker evidence than a code trace.

**7. Quote-the-rule for repository-standard findings.**
Sources: Anthropic code-review ("quote the exact rule being broken", validate
the rule's scope covers the file); Codex custom rules (cite the rule in the
finding). Change: when a finding rests on workspace instructions rather than
behavior, the comment must quote the rule and link the governing document, and
the dismissal/validation check must confirm the rule's path scope applies.
Cost: one bullet in Steps 5/9; prevents the plausible-sounding-standard
failure mode.

**8. Suggestion-block discipline.**
Source: Anthropic code-review step 9. Change: in Step 10, a committable
suggestion block only when applying it alone fully resolves the finding;
otherwise describe the fix. Also adopt full-SHA permalinks for cross-file
evidence references. Cost: trivial; platform-mechanical but real (partial
suggestion blocks get committed as-is and break builds).

### Argued against absorbing

- **Numeric confidence scores as the publication filter** (Anthropic README,
  Greptile attempt 2, vendor marketing). Greptile measured LLM self-scoring
  as near-random; the skill's deciding-evidence bar is the stronger form.
  Adding scores would create an illusion of calibration.
- **Team-feedback memory / embedding filters** (Greptile attempt 3, CodeRabbit
  learnings, Graphite evals). The mechanism that actually moved vendor numbers
  requires longitudinal per-team disposition data a stateless skill lacks. A
  repo-local "previously dismissed patterns" file would be a stale, unowned
  imitation; if the repo grows real review conventions they belong in its
  workspace instructions, which the skill already reads.
- **Strengths/positive-findings sections** (obra template, Google "good
  things"). Directly conflicts with the skill's soundness-claim bar: praise is
  a positive claim the review usually has not verified, and Step 9 exists to
  stop exactly that. Right call for a collegial human process, wrong for this
  artifact.
- **`Nit:`/`Optional:`/`FYI:` severity prefixes** (Google). The skill does not
  publish nits, and its contract keeps severity in the evidence, not the
  label. Prefixes solve a human-team problem (authors triaging mixed-severity
  streams) the publishable-tier split already solves structurally.
- **The "code judo" ambition lens** (cursor thermo/code-quality). Explicitly
  the skill's out-of-scope territory; absorbing it would re-mix maintainability
  opinion into a defect-evidence pipeline. It belongs in a separate finishing
  skill.
- **Approve-on-net-improvement standard** (Google). The skill deliberately
  never approves/blocks without a separate ask; importing an approval standard
  would widen its authority, not its accuracy.

## Reliability notes

- Vendor numbers (cubic's 51%, Greptile's 19%→55%, Codex's 98% vs 58.3%) are
  self-reported on internal datasets; treat them as directional. cubic's
  false-positive-problem post and Graphite's public reviewer page are
  mechanism-free marketing and were weighted accordingly.
- The Anthropic code-review README describes a scoring design the current
  command no longer implements; the command file was treated as authoritative.
- The academic review-size and rate limits describe human reviewers;
  their application to a model-driven review (candidate 5) is an inference,
  flagged as such above.
