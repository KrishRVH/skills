# Recomposition examples

These examples demonstrate both regimes of the deep pass. Under Recompose:
preserve the content boundary, discard generic expression, design a new
information hierarchy, and write from that plan. Under Preserve: keep the
human draft's own clauses, and change only by deleting, reordering, editing
within a clause, or merging and splitting at clause boundaries.

## Contents

- [1. Technical incident update](#1-technical-incident-update)
- [2. Thin source material](#2-thin-source-material)
- [3. Recompose versus Preserve on a personal draft](#3-recompose-versus-preserve-on-a-personal-draft)
- [4. Ending without a manufactured moral](#4-ending-without-a-manufactured-moral)
- [5. Quick reply](#5-quick-reply)
- [6. Negative scope and a real prohibition](#6-negative-scope-and-a-real-prohibition)
- [7. Human draft under Preserve with the diff summary](#7-human-draft-under-preserve-with-the-diff-summary)
- [8. A missing opening becomes a note, not a clause](#8-a-missing-opening-becomes-a-note-not-a-clause)

## 1. Technical incident update

### Incident source boundary

- A deployment began at 14:00 UTC.
- Error rate rose from 0.4% to 18%.
- The cause was a cache-key change that omitted tenant ID.
- The team rolled back at 14:27 UTC.
- Error rate returned below 1% at 14:34 UTC.
- No evidence of data loss is available in the supplied material.

### Generic source draft

> In today's rapidly evolving technical landscape, robust incident response is
> more important than ever. At 14:00 UTC, our team deployed an update that
> unfortunately led to elevated error rates. This incident underscored the
> importance of comprehensive testing and cross-functional collaboration.
> Ultimately, the team was able to quickly resolve the issue and restore normal
> service.

### Content plan

1. State impact and time.
2. Name the cause.
3. State rollback and recovery.
4. State that the supplied material does not establish whether data was lost.

### Incident recomposition

> A deployment at 14:00 UTC raised the error rate from 0.4% to 18%. The release
> changed the cache key but omitted the tenant ID. We rolled back at 14:27 UTC,
> and the error rate fell below 1% by 14:34 UTC. The supplied material does not
> establish whether any data was lost.

Why it works: the rewrite does not replace `robust` with another adjective. It
removes the generic frame, uses only the supplied cause and timeline, and keeps
the unresolved data-loss question visible.

## 2. Thin source material

### Thin source boundary

- The product has a new dashboard.
- The dashboard displays monthly usage.
- No user research, performance result, customer quote, or business outcome is
  supplied.

### Bad humanization

> I have to admit, the new dashboard is a game changer. It finally gives teams
> the kind of clarity we have all been waiting for, and early users already love
> how intuitive it feels.

This invents a personal reaction, a broad audience need, user feedback, and an
outcome.

### Safe recomposition

> The new dashboard displays monthly usage.

Thin source material supports a short result. Extra personality would be false,
not human.

## 3. Recompose versus Preserve on a personal draft

### Personal source draft

> The migration was rough, honestly. We lost most of Tuesday to a schema issue
> that should have been obvious, then found a second one after the backfill
> started. The good news is that the rollback worked exactly as designed.

### Recompose (`voice: rebuild`, origin not stated)

> The migration was rough. We lost most of Tuesday to a schema issue that should
> have been obvious and found another after the backfill began. The good news
> was that the rollback worked exactly as designed.

When the caller does not say the draft is theirs and the routing question
goes unasked because the draft could be either, Recompose treats the cadence
as editable. The actor, owned judgments, and evaluative force remain.

### Preserve (the caller says the draft is theirs)

> The migration was rough, honestly. We lost most of Tuesday to one schema issue
> that should have been obvious, then found another after the backfill started.
> At least the rollback worked exactly as designed.

The directness, the aside, and the rough register are the author's. Every
change is a deletion or an edit within a clause: "most of Tuesday to a schema
issue" gained "one", "then found a second one" became "then found another",
and "The good news is that" became "At least". Zero clauses were added.

## 4. Ending without a manufactured moral

### Source facts

- The trial reduced median processing time from 11 minutes to 7 minutes.
- Error rate did not materially change.
- The team has not measured peak-load behavior.

### Generic ending

> Ultimately, this trial demonstrates that thoughtful innovation can unlock
> meaningful efficiency gains while paving the way for a more resilient future.

### Plain ending

> The trial cut median processing time from 11 minutes to 7 minutes without a
> material change in error rate. Peak-load behavior remains unmeasured.

The supported result and remaining limit provide their own ending.

## 5. Quick reply

### Available evidence

- `checkout.test.ts` was flaky because its mock clock never advanced past the
  300 ms debounce window.
- The responding agent set the debounce to zero in `setup.ts:12`.
- All 34 tests pass.

### User question

> Did you fix the flaky checkout test?

### Quick response

> Yes. `checkout.test.ts` was flaky because its mock clock never advanced past
> the 300 ms debounce window. I set the debounce to zero in `setup.ts:12`. All
> 34 tests pass.

The quick path answers in the destination's form. It uses the real identifiers,
cause, change, and result without exposing its checks or invoking deep
recomposition.

## 6. Negative scope and a real prohibition

### Negative-scope draft

> This section explains the importer's scope and limitations. It is important
> to note that the importer accepts CSV files up to 10 MB. CSV is the only
> accepted format, which means that it does not accept JSON. Never upload
> production API keys to the sandbox importer.

### Fidelity-safe rewrite

> The importer accepts only CSV files up to 10 MB. Never upload production API
> keys to the sandbox importer.

The section announcement and importance flag are scaffolding, so they
disappear. The format boundary becomes a shorter positive statement without
changing its scope. The production-key rule remains negative because it is a
real safety prohibition, not scaffolding.

## 7. Human draft under Preserve with the diff summary

### Caller statement for the incident summary

> This is my own draft of the incident summary. Tighten it. Keep my wording
> where you can.

### Human draft

> So the short version is that we had an outage on Tuesday, and it lasted
> about forty minutes. The cause, which took us a while to find, was that the
> config push at 09:10 included a typo in the region name, and the service in
> eu-west-2 kept trying to reach a region that doesn't exist. We noticed
> because the on-call pager went off at 09:14. It's worth mentioning that the
> fix itself was trivial once we saw it. We reverted the push at 09:48 and
> everything came back within two minutes. What we're going to do about it is
> add a validation step to the push pipeline that checks region names against
> the list of regions we actually run in.

### Preserve output for the incident summary

> We had an outage on Tuesday that lasted about forty minutes. The cause took
> us a while to find: the config push at 09:10 included a typo in the region
> name, and the service in eu-west-2 kept trying to reach a region that
> doesn't exist. The on-call pager went off at 09:14. The fix itself was
> trivial once we saw it. We reverted the push at 09:48 and everything came
> back within two minutes. We're going to add a validation step to the push
> pipeline that checks region names against the list of regions we actually
> run in.

### Notes returned with the incident summary

> Treated as your own draft on your word; the skill did not verify it.
>
> Clause diff: 12 source clauses. Kept 8, lexically edited 3, deleted 2 ("So
> the short version is that", "It's worth mentioning that"), reordered 0,
> added 0. Model-added tokens: 3 of 96 output tokens (share 0.03, budget
> 0.15). Source tokens: 118.
>
> Left as written: "about forty minutes" is approximate while every other
> time is exact. If you have the recovery timestamp, "09:50" would let a
> reader compute the duration.

Every clause in the output is recognizable as a source clause. The three
edits are within clauses: "which took us a while to find" folded into its
neighbor, "We noticed because" cut, and "What we're going to do about it is
add" tightened to "We're going to add". The approximate duration stays
because replacing it would require a fact the draft does not hold.

## 8. A missing opening becomes a note, not a clause

### Caller statement for the report

> My draft of the grant progress report. It needs an opening paragraph but I
> couldn't get one down. Keep it mine.

### Human draft (excerpt)

> Enrollment reached 84 of the planned 120 participants by the end of month
> six. Retention is 91%, which is above the 85% we projected. The two sites
> in the north cohort started four weeks late because the ethics amendment
> took longer than we budgeted, and their enrollment is correspondingly
> behind.

### Preserve output for the report

> Enrollment reached 84 of the planned 120 participants by the end of month
> six. Retention is 91%, above the 85% we projected. The two sites in the
> north cohort started four weeks late because the ethics amendment took
> longer than we budgeted, and their enrollment is behind by about the same
> margin.

### Notes returned with the report

> Treated as your own draft on your word; the skill did not verify it.
>
> Clause diff: 6 source clauses. Kept 4, lexically edited 2, deleted 0,
> reordered 0, added 0. Model-added tokens: 5 of 64 output tokens (share
> 0.08, budget 0.15).
>
> The report has no opening. Writing one would add clauses with no anchor in
> your draft, so the artifact is delivered without it. A suggestion, in your
> own facts, for you to write in or discard:
>
> "At month six the study is at 70% of planned enrollment with retention
> above projection. The main schedule risk is the north cohort."
>
> Both figures come from your draft (84 of 120 is 70%). The second sentence
> is my judgment about what the reader will care about, so it is yours to
> accept or not.

Under Recompose the opening would have been written into the artifact. Under
Preserve the pass drafts it as a marked suggestion and keeps the artifact to
the author's clauses. The "correspondingly behind" edit is within a clause
and states the same relationship in plainer words.
