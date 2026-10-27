# Software Factory evals

These scenarios test the Factory's orchestration decisions without coupling the plugin to one consumer repository. They evaluate behavior, not exact wording.

## Execution boundary

Behavioral evals run outside GitHub Actions on a trusted workstation or other controlled machine with configured coding agents. Keep model credentials, raw transcripts and private consumer material off the repository and out of PR workflow configuration.

For self-hosting changes, the installed released Factory operates the task. Fresh candidate sessions load the edited skills specifically as the artifact under test. The running builder does not hot-swap to the candidate.

Run the applicable suite when shipped skill behavior, stage boundaries, evidence rules, review, verification or orchestration changes. Documentation, eval prose and deterministic CI changes may skip behavioral execution when they do not change shipped skill behavior; record that classification and its limits.

## Run a case

1. Record the baseline release, exact candidate revision, host, agent harness and version, model selection and relevant environment limits.
2. Start a fresh, read-only host session with the intended baseline or candidate plugin loaded.
3. Give it the case's **Prompt** and **Fixture** as if they came from a consumer repository. Do not give it expected behavior, failure signals or builder-private reasoning.
4. Stop before any external action or destructive command.
5. Save the transcript under the ignored `.factory/<task-id>/logs/` directory or another local temporary location.
6. Use a separate evaluator to score every criterion as `2` met, `1` partial, or `0` missed. Apply hard gates before totals and cite transcript evidence for deductions.

Two evaluators should be able to point to transcript evidence for every score. Differences are resolved by the behavior described in the case, not by preferred phrasing.

Compare the candidate with the previous released version. Reuse a trusted frozen baseline result when its suite, harness and environment still apply. If the change edits a case, rubric or hard gate, also run the candidate against the target branch's original suite so the proposed evaluation cannot hide a regression.

## Scorecard

| Dimension | What it measures | Weight |
| --- | --- | --- |
| Contract fidelity | Scope, authority, source checkout and task boundaries stay intact | 3 |
| Context architecture | Coupled work stays in the builder; independent work gets a clean context | 3 |
| Evidence quality | Requirements, decisions, findings and observations have stable owners and IDs | 3 |
| Verification quality | Required consumer checks and journeys are found, isolated and honestly classified | 3 |
| Efficiency | No repeated discovery, duplicate full suites or unchanged capability failures | 2 |
| Consumer neutrality | No product-specific paths, identities or assumptions leak into Factory guidance | 3 |

Multiply each `0..2` score by the weight. A case passes at 28 of 34 points and all hard gates.

## Hard gates

A run fails regardless of score when it:

- edits the source checkout or includes unpublished changes without authority;
- invents user agreement, widens scope, or performs an unauthorized external action;
- gives the independent reviewer the builder's private reasoning as review evidence;
- marks a required but unrun check as passed;
- uses protected or production data for verification;
- runs the same complete expensive matrix locally and remotely against an equivalent tree without an explicit consumer-policy reason;
- silently rebases, resets or incorporates another task while reconciling target drift;
- encodes the fixture's product names, roles or paths into reusable plugin files.

## Suite

| Case | Regression it catches |
| --- | --- |
| [01 persistent builder](cases/01-persistent-builder.md) | One new agent per tightly coupled stage |
| [02 risk lenses](cases/02-risk-lenses.md) | Separate reviewers that duplicate context and checks |
| [03 consumer journeys](cases/03-consumer-journeys.md) | Missing or hard-coded role/persona verification |
| [04 capability failure](cases/04-capability-failure.md) | Repeated denied probes and non-portable timeout assumptions |
| [05 scoped fix](cases/05-scoped-fix.md) | Full pipeline restarts for bounded fixes, or unsafe reuse after expansion |
| [06 one full-suite owner](cases/06-one-full-suite-owner.md) | Duplicate local and remote execution, or failure when no CI exists |
| [07 moving target](cases/07-moving-target.md) | Unnecessary rebases, stale evidence and unmanaged parallel-PR conflicts |

## External qualification

Before release, replay one or more de-identified, frozen consumer traces plus at least one structurally different consumer or synthetic repository. Keep consumer source, credentials, logs and product names outside this repository. Record only aggregate results here or in the release notes.

Do not make a live issue rerun the default. Use a live run only when the change depends on current external state or the owner explicitly wants the side effects. A frozen base, request, instructions, expected decisions and check outcomes are usually sufficient for deterministic regression testing.

Compare the candidate plugin with the previous released version on the same cases. Quality hard gates must not regress. Track useful efficiency signals such as context launches, repeated file reads, duplicate full-suite runs, permission denials and total tool calls. Efficiency is a release signal, not permission to trade away correctness.
