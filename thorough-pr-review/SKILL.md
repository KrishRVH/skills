---
name: thorough-pr-review
description: Exhaustive, adversarially verified pull request review for high-consequence changes.
disable-model-invocation: true
---

# Thorough PR Review

A slow, evidence-bound review for changes where a miss is expensive. Discovery
fans out across single-lens specialists, a refuter attacks what they return,
every dismissal is logged with its deciding evidence, and only high-consequence
findings are publishable.

**Review one pull request per invocation.** When the caller supplies several,
ask them to invoke the skill separately for each. Batching splits attention, and
the last change tends to receive the thinnest pass.

## Contract

- Hold dismissals to the bar findings get. Refute a candidate only with deciding
  evidence, recorded in the ledger; carry ambiguous candidates as uncertainties.
- Publish only Critical, High, and the publishable tier of Medium defined in Step 8. Report everything else to the caller.
- Write comments as a colleague's reading. Severity lives in the evidence, not
  in the tone.
- An empty publishable set is a legitimate outcome. Report it as one rather than
  promoting a weak finding to fill the review.
- Treat publishing as a separate authorization. Post only when the caller
  explicitly asks; otherwise return review-ready drafts. Approve, request
  changes, merge, resolve, push, or open issues only on a separate specific ask.

## Steps

### Step 1: Gather

Resolve exactly one pull request identifier or URL. Fetch the review platform's
metadata and canonical diff through its available CLI or API, then fetch the
head revision so surrounding code can be read at the exact revision under
review. Keep the caller's active checkout untouched: read the fetched objects
directly or use an isolated worktree, and save transient artifacts outside the
repository. If the metadata, canonical diff, or head revision is unavailable,
stop and report the missing access or artifact.

Read the repository's workspace instructions and whatever standards or workflow
documents they route to; repository rules outrank this skill's defaults. Then
read the diff in full, paging rather than sampling.

Read the branch's commit history too. Where a predicate, join, filter, or guard
changed shape across commits, use the earlier form and replacement rationale to
understand intent. Verify every conclusion against the final revision.

```sh
git log -p <base>..<review-head> -- <path-of-interest>
```

**Complete when:** the whole diff and the commit history have been read, the head
ref is local, and the repository's applicable standards are known.

### Step 2: Inventory the change

List every behavior the diff introduces or alters, with what it now depends on
and what newly calls it.

Invert that into the **consumer map**: for each pre-existing query, function,
column, config value, or contract the diff points a **new consumer** at, record
what that consumer needs from it. This is the highest-yield artifact in the
review — the defects that survive a careful read live in unchanged code whose
requirements moved.

Then pin what the change was _asked_ for. Look for the originating issue or spec
in the pull request body, branch name, commit messages, or a document the caller
names; if none exists, record that and skip the axis rather than inventing
requirements. Compare in both directions: asked for but missing, and present but
unasked-for.

Keep the spec axis separate all the way to the report. Code can meet every
requirement while being defective, or be flawless while implementing the wrong
thing; ranking the two together lets one hide the other.

Maintain two ledgers from this point onward: defect candidates and spec
observations. Spec observations never enter defect severity or publication.

**Complete when:** every changed behavior is inventoried, every new consumer of
pre-existing code is in the consumer map, and the spec axis is populated in both
directions or recorded as unavailable.

### Step 3: Trace each change to its real data

Follow the actual values end to end: who produces them, which fields are
populated, by what code, for which subset of records. Read the producer; never
infer it from what the consumer expects.

Where a query, filter, or predicate is involved, test its **satisfiability**:

1. List every field in the `WHERE`, `JOIN`, filter, or match.
2. Name the code that writes each one.
3. Confirm it is written for **every class of record** the new consumer needs
   back — not just the class that motivated the original query.

The shape this catches: a table written by both a local path and a webhook, where
only the local write populates the filtered columns. A query on those columns
served its original consumer for years. A change bolts a new consumer onto it
that needs the webhook rows, inherits the filter unchanged, and returns nothing
forever. Nothing in the diff looks wrong.

**Complete when:** every inventory entry has a traced producer, and every
predicate field has a named writer confirmed for each record class the new
consumer needs.

### Step 4: Execute and verify the behavior

Run every check mandated by the repository instructions and the narrowest
relevant tests for each changed behavior. Exercise integration, authorization,
error, and side-effect paths in an isolated test environment; keep real external
systems untouched. Record any check that cannot run, why, and how that limits the
review.

Where the change adds pure or near-pure logic — resolver, comparator, sort,
parser, state machine, threshold, money calculation — exercise the actual
implementation through the repository's test or runtime entry points. If no
entry point exists, use a scratch harness that imports the implementation and
the repository's installed dependencies. Feed it inputs the real producer can
emit.

Reading a comparator tells you what it does with the cases you thought of.
Running it tells you what it does with the cases you did not. Exercise each
applicable dimension below and record why the others do not apply:

- records arriving out of order, and a later one contradicting an earlier one
- two entries tied on the primary sort key
- null in every field the producer declares nullable
- each threshold's boundary value, from both sides

Keep scratch artifacts outside the working tree.

**Complete when:** every extractable piece of logic has been run against real
dependencies on every applicable out-of-order, tied, null, and boundary input;
each inapplicable dimension has a reason, and each result is either expected or
recorded as a review candidate. Repository-mandated checks and targeted tests
have also passed or are recorded as evidence limits.

### Step 5: Sweep the defect classes

Walk every row. Each names a class whose evidence sits outside the changed lines,
which is why a diff-focused read misses it. Record an outcome for every row —
including "not applicable", which needs the same explicit note as a finding.

The **Lens** column is also the partition Step 7 fans out along.

| Lens              | Class                   | Question that surfaces it                                                                                                                                                                                                  |
| ----------------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Data reachability | Requirement drift       | For each consumer-map entry, what does the new consumer need from this unchanged code that the old one did not?                                                                                                            |
| Data reachability | Field population        | Is every field the change filters, joins, matches, or reads populated for every record class it needs back?                                                                                                                |
| Data reachability | Pre-change data         | Does this work for records written before the change — old shape, old defaults, a column made nullable since?                                                                                                              |
| Silent failure    | Swallowed errors        | For every new or widened `catch`, what else can it swallow beyond the error it was written for? Then check every empty catch, catch-and-continue, error-swallowing default return, and retry that gives up quietly.        |
| Silent failure    | Green on empty          | Which paths report a benign state when they actually have no data, or failed? A feature that renders fine because its query returned nothing reads as working software, and is the most expensive thing a review can miss. |
| Silent failure    | Observability           | For an irreversible or externally-visible action, is there a record of who did it, and against what state?                                                                                                                 |
| Reachability      | Branch reachability     | For every new branch, what input reaches it, and can that input occur at all given upstream gates?                                                                                                                         |
| Reachability      | Guard over-reach        | What did each new guard start rejecting that legitimately succeeded before?                                                                                                                                                |
| Reachability      | Prescribed remedy       | If the change blocks a user and routes them somewhere to resolve it, what does that destination do to their data?                                                                                                          |
| Consistency       | Duplicated rule         | Is any rule the change introduces implemented in more than one place, and do the copies agree exactly?                                                                                                                     |
| Consistency       | Cross-path disagreement | Where two paths handle the same state, do they classify it the same way? A change claiming to unify paths gets checked against its own claim.                                                                              |
| Spec              | Unasked-for behavior    | What does the diff do that nothing asked for? Report as scope, not defect.                                                                                                                                                 |
| Spec              | Missing requirement     | What did the spec ask for that the diff omits or half-does?                                                                                                                                                                |
| Integrity         | Idempotency             | What happens when this runs twice, and which external side effect duplicates?                                                                                                                                              |
| Integrity         | Transaction boundary    | What stays committed if this fails halfway, and does anything inside commit independently of the outer transaction?                                                                                                        |
| Integrity         | Concurrency             | What does each lock actually protect, and which writes stay possible against it?                                                                                                                                           |
| Authorization     | Gate parity             | Which roles reach this, and does every branch, redirect, and endpoint it leads to carry an equivalent gate?                                                                                                                |
| Security          | Input trust             | Can untrusted input reach a query, command, path, template, parser, redirect, or interpreter without the encoding or validation that boundary requires?                                                                    |
| Security          | Sensitive data          | Can credentials, tokens, personal data, or internal state newly reach logs, telemetry, errors, caches, or responses?                                                                                                       |
| Arithmetic        | Clock and units         | Whose timezone, precision, and rounding — and does any money or threshold comparison turn on them?                                                                                                                         |
| Arithmetic        | Growth                  | What is unbounded: rows returned, queries per row, payload serialized into the page?                                                                                                                                       |
| Tests             | Test reachability       | Which branches, error paths, boundaries, and negative cases can the added, modified, or relied-upon tests not reach at all?                                                                                                |

**Complete when:** every row has a recorded outcome or an explicit
not-applicable, and every finding carries a file and line.

### Step 6: Audit your own reasoning

The table hunts defects in the code. These three hunt them in the review, and
they are why a careful pass still misses things.

**Question substitution.** For every question raised and then closed in Steps
2-5, write the question asked beside the question the evidence answered. Reopen
any pair that does not match. The recurring form is answering "does path A behave
like path B" when the question was "does either path work" — shared mechanism
never establishes correct mechanism.

**Fixture shape.** For every added or modified test, and every existing test
relied on as coverage, check whether it builds the unit's inputs by hand.
Hand-built inputs leave the input _shape_ untested however many cases follow, so
trace the real producer and confirm it emits that shape. Read a test comment
explaining why the real source could not be used as evidence the boundary is
unverified. Judge behavioural coverage: a test asserting a state production can
never produce is a fixture agreeing with itself.

**Dismissal bar.** Re-read every candidate killed so far; each needs deciding
evidence such as a code location, an authoritative contract, or observed runtime
behavior. A dismissal resting on a search hit, a naming convention, or absent
contrary evidence returns to the candidate list.

**Complete when:** every closed question has a matched pair, every hand-built
fixture has a traced producer, and every dismissal cites its deciding evidence.

### Step 7: Fan out the lenses, then refute

**Give each specialist one lens in a clean context.** This is the load-bearing
part. Two lenses and a specialist reverts to a generalist, whose attention goes
uneven across the surface — the failure the shape exists to prevent. A single
narrow mandate lets independent workers search reliably while the primary
reviewer retains reconciliation and final judgment.

Dispatch one specialist per lens holding at least one applicable row in Step 5's
table. Its brief contains the review metadata and spec, repository path and head
revision, canonical diff, applicable repository instructions, relevant
consumer-map entries and producer traces, and only that lens's rows. Withhold
the candidate list — a specialist that knows what has been found narrows to
confirming it.

If independent workers are unavailable, stop and tell the caller this skill
cannot provide its claimed adversarial verification. Offer an ordinary local
review as a separate, explicitly degraded alternative.

Require each to filter its own output before returning: only what it can prove
from the code with a file and line, and nothing it would not defend under
push-back. Fan-out without that filter trades one uneven pass for many noisy
ones.

Then run the refuter, separately and last, over the merged list:

- try to disprove each candidate
- classify it as confirmed, refuted, or unresolved
- cite the deciding evidence for confirmed and refuted candidates
- name the cheapest check that would settle each unresolved candidate

Preserve each candidate's defect or spec ledger throughout refutation.

Keep the refuter away from the specialists so its skepticism cannot dampen their
search. Treat every returned claim as evidence rather than verdict: verify it
against the code yourself, and say plainly when one does not survive.

**Complete when:** every applicable lens has run, every skipped lens is
documented as having no applicable rows, the refuter has passed over the merged
list, and every returned claim is confirmed or refuted with deciding evidence or
recorded as unresolved with a settling check.

### Step 8: Reconcile and rate

Reconcile the defect ledger across the primary pass, non-Spec specialists, and
the refuter. Fan-out makes duplicates normal — several lenses reach one defect
from different directions. Keep the finding with the wider blast radius, note
the narrower one as subsumed, and carry the strongest evidence from either.

Where two lenses disagree about the same code, reopen the candidate. Resolve it
against the code rather than averaging the claims or trusting the more confident
worker. If the evidence remains ambiguous, classify it as unresolved rather
than as a defect.

Rate confirmed defects from the top down and stop at the first matching tier:

| Severity             | Test                                                                                                                                                                                                      |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Critical             | An exploitable security or authorization bypass; broad or irreversible data loss or corruption; materially wrong money across a nontrivial scope; a critical function that is structurally unable to work |
| High                 | Materially incorrect behavior on a common or critical path, an ineffective safety guard, or a destructive side effect, when the consequence is neither Critical nor narrow and readily recoverable        |
| Medium — publishable | A normal-use defect with narrow, recoverable monetary or data-integrity harm, or a duplicate external side effect, that does not meet a higher tier                                                       |
| Medium — report only | A bounded defect without demonstrated operational harm: path disagreement, maintainability, duplicated rules, performance without a demonstrated ceiling, or missing logging                              |
| Low                  | Everything else                                                                                                                                                                                           |

Publish the first three tiers, rank them by consequence, and fold a child finding
under the parent that subsumes it.

Reconcile and deduplicate the spec ledger separately. Report missing, partial,
and unasked-for behavior without a defect severity and without adding it to the
publishable set.

**Complete when:** every surviving finding carries a severity with its justifying
evidence, the publishable set is separated from the report-only set, and every
verified spec observation remains in the separate spec ledger.

### Step 9: Draft and verify the comments

Draft every comment before publishing any, then verify the drafts. Step 8
verified and rated the findings; nothing yet has checked the comments built on
them, and a comment can overstate or vouch for something the review never
established even when its finding holds.

- **Claim matches evidence.** Every assertion traces to an already-verified file
  and line. Anything that grew in the writing — a wider blast radius, an extra
  affected path, a confident mechanism — returns to Step 3 or leaves the comment.
- **Soundness claims carry the findings bar.** Saying part of the change is
  correct, safe, or an improvement is a positive claim. Verify it as rigorously as
  a defect or drop it: vouching for code the review never established tells the
  author which ground to skip.
- **Severity survives restatement.** Restate the consequence in one sentence and
  re-run it against Step 8's bar. A consequence that depends on an unverified
  assumption makes the candidate unresolved, not a lower-severity finding.
- **Uncertainty is stated where it exists.** A conclusion resting on a code trace
  rather than observed data says so, and names the check that would settle it.

Then have an adversary read the drafts against the diff, briefed to flag any
unsupported claim, any severity it would rate lower, and any assertion that
something is sound. Verify its objections rather than deferring to them.

**Complete when:** every claim traces to verified evidence, every soundness claim
is verified or removed, every severity survived restatement, and an adversary has
passed over the drafts.

### Step 10: Publish or prepare

Build each comment from these parts, in order:

1. The observation in one sentence, as your reading — "I don't think this branch
   can be reached", "I think this only fires for the primary recipient".
2. The minimum evidence chain, with file and line references, adding to what the
   anchored line already shows rather than repeating it.
3. The consequence in one sentence, in the terms someone operating the system
   would use.
4. The suggestion as an offer. Where the current behavior may be deliberate, give
   the alternative that assumes it is.

Keep each comment near 200 words or under. Let the comments in one review take
different shapes — a shared skeleton reads as generated and buries the finding
that differs.

Anchor each publishable finding inline on the line it concerns. Name the reviewed
scope, evidence limits, and unresolved questions in the review body.

When the caller explicitly authorized publishing, submit one non-blocking
comment review through the platform's CLI or API. Otherwise, return the same
inline comments as review-ready drafts with their intended anchors. Escalate the
review state only on a separate ask.

**Complete when:** every publishable finding is anchored on its line, each body
follows the four-part shape within the length limit, and the review is either
published under explicit authorization or returned as review-ready drafts.

### Step 11: Report to the caller

- what was published or drafted, at what severity, and where it is anchored
- findings held back as report-only, with severity
- the spec axis on its own: missing or partial requirements, and behavior nothing
  asked for, never merged into the defect list
- every dismissed candidate with the evidence that killed it
- any conclusion resting on a code trace rather than observed data, plus the
  cheapest check that would settle it

**Complete when:** the caller has the publishable set, the withheld set, the spec
axis, the dismissal ledger, the publication status, and every material
uncertainty with its settling check.

## Red flags

Each of these is the sound of a check being skipped. Treat it as a stop, not a
conclusion.

- "This filter is pre-existing, so it works."
- "The tests cover this" — about behavior whose inputs the tests construct.
- "Same mechanism as the existing path, so it's fine."
- "Obviously not applicable" — for a sweep row, without recording it.
- A dismissal whose evidence answers a narrower question than the one asked, or
  cites no deciding evidence.
- A specialist holding more than one lens, or holding the candidate list.
- Specialist output merged without each having filtered its own.
- An ambiguous candidate recorded as refuted rather than unresolved.
- A comment claiming more than the evidence gathered for it, or vouching for part
  of the change as sound.

## Out of scope

Style, naming, structural smells, simplification, and code-comment wording
belong to a finishing pass unless evidence connects them to behavior that meets
the severity bar.

## Cost

Full-diff and history reading, producer tracing, execution of extractable logic,
a twenty-two-class sweep, a reasoning audit, a parallel fan-out, a refuter, and a
pass over the drafted comments.

Dispatch specialists in small concurrent waves that stay within the available
worker limit. Preserve one slot for the primary reviewer so reconciliation can
continue between waves.

Use it when a miss is expensive; use an ordinary review otherwise.
