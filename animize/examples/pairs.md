# Paired examples by genre

Each pair shows a draft with a reader-facing defect and the same content after
a run. The source boundary is stated so a reader can check fidelity. None
of the rewrites adds a fact, a reaction, or a source. Model imitation of shape
is the point: read the pair, then write to the after-shape, not to the rule
list.

## Contents

- [1. Professional email (Recompose)](#1-professional-email-recompose)
- [2. Technical explanation (Recompose)](#2-technical-explanation-recompose)
- [3. Product copy (Recompose)](#3-product-copy-recompose)
- [4. Analytical newsletter (Recompose)](#4-analytical-newsletter-recompose)
- [5. Academic passage (Preserve)](#5-academic-passage-preserve)
- [6. Policy text (Recompose)](#6-policy-text-recompose)
- [7. Personal essay (Preserve)](#7-personal-essay-preserve)

## 1. Professional email (Recompose)

Source boundary: the vendor's invoice 4471 is 23 days overdue; the contract
allows a 1.5% monthly late fee after 30 days; the sender wants payment by
Friday, 2026-09-25; the recipient is the vendor's accounts contact.

### Before: email

> I hope this email finds you well. I wanted to reach out regarding invoice
> 4471, which, as you may be aware, is currently outstanding. We greatly value
> our partnership and understand that delays can happen. However, it is
> important to note that per our agreement, late fees may become applicable
> after 30 days. We would greatly appreciate it if payment could be arranged
> at your earliest convenience. Please do not hesitate to reach out with any
> questions.

### After: email

> Invoice 4471 is 23 days overdue. Under our contract a 1.5% monthly late fee
> applies after 30 days, so payment by Friday, 2026-09-25, avoids it. Reply
> if anything on the invoice needs correcting before you can pay it.

The rewrite leads with the fact, names the number and the date the source
supplies, and turns the vague "at your earliest convenience" into the real
deadline. It drops the wrappers and the "please do not hesitate" close.

## 2. Technical explanation (Recompose)

Source boundary: the service retries a failed webhook delivery five times
with exponential backoff starting at 2 seconds; after the fifth failure it
marks the endpoint unhealthy and stops delivering until an operator resets it
in the dashboard; retries stop early on a 410 response.

### Before: webhook

> Webhook reliability is a critical aspect of any modern integration
> platform. Our robust retry mechanism ensures that transient failures do not
> result in lost events. When a delivery fails, the system will intelligently
> retry using an exponential backoff strategy, significantly improving
> delivery success rates. In the event that repeated failures occur, the
> endpoint will be flagged accordingly, and manual intervention may be
> required.

### After: webhook

> A failed webhook delivery is retried five times with exponential backoff,
> starting at 2 seconds. A 410 response stops the retries early. After the
> fifth failure the service marks the endpoint unhealthy and stops delivering
> to it until an operator resets it in the dashboard.

The rewrite states the count, the starting delay, the early-stop condition,
and who has to act. "Intelligently", "robust", and "significantly improving"
are gone because the source gives no measure for them.

## 3. Product copy (Recompose)

Source boundary: the new export runs on a schedule the user sets; it writes
CSV to the user's own S3 bucket; exports over 2 GB are split into 2 GB files;
no customer quotes, adoption numbers, or performance comparisons are supplied.

### Before: exports

> Say hello to scheduled exports, the game-changing feature our customers have
> been waiting for. Seamlessly deliver your data exactly where you need it,
> when you need it, with zero hassle. Whether you're a data analyst or a
> growth marketer, scheduled exports empower you to unlock insights faster
> than ever.

### After: exports

> Scheduled exports write your data as CSV to your own S3 bucket on a schedule
> you set. Exports larger than 2 GB arrive as 2 GB files.

The source supports two facts and a limit. The rewrite states them. The
audience labels, the waiting customers, and the speed claim have no support
and are omitted rather than softened.

## 4. Analytical newsletter (Recompose)

Source boundary: the writer's position is that the city's new bus lane cut
average trip time on route 12 from 41 minutes to 29 minutes in its first
month; car travel time on the same corridor rose by 3 minutes; the writer
thinks the trade is worth it and says so; ridership data is not yet published.

### Before: bus lane

> Urban mobility is at a crossroads. The recent introduction of a dedicated
> bus lane has sparked considerable debate among stakeholders. On one hand,
> proponents argue that transit improvements benefit the community. On the
> other hand, critics raise concerns about the impact on drivers. Ultimately,
> the data will tell the story, and only time will reveal whether this bold
> experiment pays off.

### After: bus lane

> The bus lane took twelve minutes off a route 12 trip in its first month:
> 41 minutes down to 29. Drivers on the same corridor lost three. That is the
> whole trade, and I think it is a good one. What we do not know yet is
> whether more people ride the bus because of it; the city has not published
> ridership for the month.

The source owns a judgment, so the rewrite states it in first person at the
source's strength. The staged debate and "only time will tell" ending are
replaced by the numbers and the one open question the source names.

## 5. Academic passage (Preserve)

Source boundary: a human-written draft, stated by the caller. The claim, the
sample size, the effect, and the limitation are the author's. Regime:
Preserve, default budget.

### Before: sleep study

> In this study, we sought to investigate the relationship between sleep
> duration and recall performance in undergraduate students. It is worth
> noting that prior work in this area has been somewhat mixed. Our sample
> consisted of 212 participants. We found that participants who reported
> sleeping fewer than six hours performed worse on the recall task, with a
> mean difference of 4.1 items (95% CI 2.3 to 5.9). It should be noted,
> however, that sleep duration was self-reported, which is a limitation.

### After: sleep study

> We investigated the relationship between sleep duration and recall
> performance in 212 undergraduate students. Prior work in this area has been
> mixed. Participants who reported sleeping fewer than six hours performed
> worse on the recall task, with a mean difference of 4.1 items (95% CI 2.3
> to 5.9). Sleep duration was self-reported, which is a limitation.

Clause diff: 8 source clauses; 6 kept, 2 lexically edited, 1 deleted ("It is
worth noting that"), 1 merged ("Our sample consisted of 212 participants"
into the first sentence), 0 added. Model-added tokens: 1 of 63 output tokens
(share 0.02). The author's hedge "somewhat" was cut as a lexical edit; every
number, the confidence interval, and the limitation are unchanged.

## 6. Policy text (Recompose)

Source boundary: employees may work remotely up to three days a week; managers
may require attendance for named events with one week's notice; the policy
takes effect 2026-10-01; the prior policy allowed two days.

### Before: remote policy

> We are excited to announce an update to our flexible work policy. In
> today's evolving workplace, flexibility is more important than ever. Moving
> forward, team members will be empowered to work remotely for up to three
> days per week, subject to business needs. Managers may, from time to time,
> request in-office attendance. This policy will be effective October 1 and
> supersedes the previous guidance.

### After: remote policy

> From 2026-10-01, employees may work remotely up to three days a week. The
> prior limit was two. A manager may require attendance for a named event
> with at least one week's notice.

"Subject to business needs" had no support in the source and would have
widened the manager's authority; the rewrite states the actual condition,
which is a named event and a week's notice. The effective date and the prior
limit are kept because the reader needs both.

## 7. Personal essay (Preserve)

Source boundary: a human-written draft, stated by the caller. Regime:
Preserve, default budget. The caller asked for a tighter opening paragraph.

### Before: radio

> I have been thinking a lot lately about why I keep the broken radio. It
> doesn't work, obviously, and it takes up half the shelf. My grandfather
> built it in 1961 from a kit, and honestly I think it's the only thing he
> ever finished. Anyway, it sits there. I dust it sometimes. I have never
> once tried to fix it, which probably says something about me, though I'm
> not sure what.

### After: radio

> I keep the broken radio. It doesn't work, and it takes up half the shelf.
> My grandfather built it in 1961 from a kit, and honestly I think it's the
> only thing he ever finished. It sits there. I dust it sometimes. I have
> never once tried to fix it, which probably says something about me, though
> I'm not sure what.

Clause diff: 9 source clauses; 7 kept, 1 lexically edited ("I have been
thinking a lot lately about why I keep" to "I keep"), 1 deleted ("Anyway"),
0 added. Model-added tokens: 0. The asides, the "honestly", and the
unresolved ending are the author's and stay. A Recompose run would have been
wrong here: the roughness is the voice.
