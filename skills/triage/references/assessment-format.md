# Assessment format

Keep it short. Use plain words and short sentences. Use a table when there is more than one finding. Omit empty sections. Do not add detail that does not change the verdict.

## Verdict

Two lines first:

**Readiness for <stage>:** Ready, Needs information, Blocked by a dependency, Needs a decision, or Not applicable.
**Primary blocker:** The main thing preventing the next stage, if any; explicitly say None when ready. Then at most two sentences on why. Include other independently blocking items when present.

If evidence is insufficient to assess readiness, say so instead of choosing a verdict or inventing a project blocker. Explain the investigation gap under Limits.

## Missing decisions

Put genuine human decisions immediately after the verdict when needed: preferences, tradeoffs, authorization or genuinely unavailable information that changes the next step. Resolve discoverable facts through investigation first; keep investigation limits separate.

Name each decision; do not write it as a question to users. Refinement turns these into the one clarification comment, so the user is asked once. Rank by what blocks most and merge decisions that one answer settles. If the request would reverse a recorded decision, say so and name the decision.

1. **Decision needed.** What it affects, and the evidence that leaves it open.

## What the request asks

Only when the request has two or more separate asks. One row per ask.

| Ask | State in code | Where |
| --- | --- | --- |
| Short restatement | built, partly built, not built, conflicts, or unverified | file or doc |

## Evidence

At most eight rows. Pick the ones that decide the verdict.

| Claim | Source | Depth | Finding |
| --- | --- | --- | --- |
| What you checked | file:line, link or revision | read in full, read in part, or search match only | What it shows, or what contradicts the request |

Conclude only from what you read. A search match is a lead, not proof. Support implementation claims with the relevant behavior paths, not comments alone.

## Dependencies

Real prerequisites only, with status if known. An unread TODO is not an established dependency.

## Limits

List only what you could not verify and could change the verdict, with the reason, such as source access failing. Do available, verdict-relevant reads before returning. Access-blocked verification is an investigation limit, not a product decision. Skip the rest.

## Showing structure

- Use a before/after table when the request changes a mapping, such as a status or label by audience.
- Use a small flow only when the request describes a multi-step process or states.
- Otherwise use no diagram.
