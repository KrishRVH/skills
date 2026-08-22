# Recomposition examples

These examples demonstrate the default method: preserve the content boundary,
discard generic expression, design a new information hierarchy, and write from
that plan.

## Contents

- [1. Technical incident update](#1-technical-incident-update)
- [2. Thin source material](#2-thin-source-material)
- [3. Default rebuild versus explicit voice preservation](#3-default-rebuild-versus-explicit-voice-preservation)
- [4. Ending without a manufactured moral](#4-ending-without-a-manufactured-moral)
- [5. Quick reply](#5-quick-reply)
- [6. Negative scope and a real prohibition](#6-negative-scope-and-a-real-prohibition)

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

## 3. Default rebuild versus explicit voice preservation

### Personal source draft

> The migration was rough, honestly. We lost most of Tuesday to a schema issue
> that should have been obvious, then found a second one after the backfill
> started. The good news is that the rollback worked exactly as designed.

### Default `voice_mode: rebuild`

> The migration was rough. We lost most of Tuesday to a schema issue that should
> have been obvious and found another after the backfill began. The good news
> was that the rollback worked exactly as designed.

The source's conversational cadence is not protected by default, but its actor,
owned judgments, and evaluative force remain.

### Explicit `voice_mode: preserve`

> The migration was rough, honestly. We lost most of Tuesday to one schema issue
> that should have been obvious, then found another after the backfill started.
> At least the rollback worked exactly as designed.

Here the directness, aside, and rough emotional register are part of the
requested voice.

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
cause, change, and result without exposing an audit or invoking deep
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
