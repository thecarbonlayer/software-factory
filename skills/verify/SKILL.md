---
name: verify
description: Independently verify a frozen software candidate from authoritative remote checks or one local execution of the consumer's required suites and user journeys. Use after review and before delivery.
---

# Independent verification

## Role and boundaries

Verify the frozen candidate as a black box. Establish what actually works without reviewing implementation style or fixing defects. A verifier owns the conclusion and evidence. It does not have to own the test process.

Stay independent from the builder. Use the supplied candidate, plan, capability snapshot, evidence ledger, consumer-owned instructions and remote check metadata when available. Do not request the builder's private reasoning. Do not edit tracked source, change HEAD, post results externally, approve or merge a PR, deploy, or use production and protected data.

## Build the required matrix

1. Confirm the base, exact candidate commit and tree, tracked status and capability snapshot.
2. Read project instructions and applicable `REVIEW.md`. Follow their links to setup, test and qualification guides.
3. Inspect configured remote-check workflows for any supported provider. Resolve their triggers, commands, inputs and matrix instead of inferring coverage from names.
4. Build one verification matrix from accepted requirements, `plan.md`, consumer policy and required remote checks.
5. When the consumer defines roles, personas or user journeys, include every declared supported workflow that the change or policy requires. Use the consumer's canonical mapping. Never invent product roles or encode them in Factory.

Record each row with its requirement or policy source, exact command or steps, prerequisites, resources, expected result, execution owner and evidence ID.

## Select one authoritative full-suite route

Choose the route declared by consumer policy. Without an explicit policy, prefer an already configured required remote check when it covers the complete matrix on the candidate head or a documented integration revision that contains it. Otherwise use the best documented local route.

### Remote checks

When a draft pull request or equivalent remote candidate triggers the complete suite:

- Do not run the same full suite locally and remotely against an equivalent tree merely to duplicate it.
- Require the remote run to test either the frozen candidate SHA or an exact integration revision whose event metadata or commit relationship proves it contains that candidate and the recorded target. A pull request number, branch name or earlier green run is insufficient.
- Resolve the expected workflow, required jobs, matrix dimensions and conclusion. Missing, skipped, cancelled or still-running required jobs are not passes.
- Treat `Stage state: pending` as the correct result while owned required checks still run. Resume the same verification after they finish.
- Read concise check results first. Inspect failure logs, traces and screenshots needed to classify a failure. Do not load every successful screenshot into model context.
- Record provider, repository, run URL or identifier, workflow revision, event, candidate head SHA, tested SHA, target SHA, their relationship, matrix and job conclusions in `evidence.md`.

Creating or updating the remote candidate is an external action owned by the caller and the submit skill. Verification may request it, but cannot perform it without existing authorization.

### Local checks

When no suitable remote checks exist, run the documented local full suite once:

- Use commands already authorized in `capabilities.json` and owned by `plan.md`. If a command or prerequisite differs, record the specific capability change instead of improvising wider permissions.
- Prefer a clean test environment, disposable fixtures and consumer-provided scripts.
- Identify shared databases, files, ports, services and accounts. Isolate them or serialize conflicting checks.
- Use test identities only. Never point fixtures, reset scripts or destructive journeys at protected data.
- Use host-native process time limits and cancellation. Do not assume GNU `timeout` is installed.
- Join all jobs, stop only services you started, remove owned temporary artifacts and report cleanup failures.

If no complete automated route exists, perform meaningful consumer-documented manual checks where possible. If no valid observation covers a required row, mark it unverified. Do not create CI, a browser suite or a test framework unless that work is separately requested and authorized.

## Evidence reuse

For every check, append or cite an evidence entry with the candidate SHA and tree, exact tested revision, their relationship, execution owner, workflow or command, complete matrix identity, environment, result, observed output and limits. Preserve raw output or remote artifact links at the declared location.

Reuse evidence only when the candidate or proven integration tree, workflow or command, matrix, relevant inputs, environment, fixtures and limits match, and consumer policy permits it. Otherwise it is stale. A later target branch or merge group normally creates a different integration tree and needs its own evidence.

## Classify outcomes

- **Product failure:** the candidate violates accepted behavior in a valid environment. Provide the smallest reproducible trigger and affected R ID.
- **Runner failure:** the selected agent, command or remote-check route could not execute the check.
- **Environment failure:** a required service, fixture, account or isolation boundary was unavailable.
- **Unverified:** no valid observation covers the required row.

Only a product failure proves an implementation defect. Runner and environment failures can still block delivery because required behavior remains unverified.

## Report

Begin with `I'm using the verify skill.`, then `Stage state: pending` while required checks or jobs run. Use `Stage state: complete` only after the selected route has finished, cleanup is attempted and the exact candidate is reconfirmed.

Lead a complete report with **supports delivery**, **blocks delivery** or **not assessable**, and the reason. Then return:

- **Verified scope/version:** candidate SHA and tree, exact tested revision and relationship, consumer policy, execution owner and environment.
- **Matrix results:** every required row, its R or policy source, pass/fail/blocked/unverified result and E ID.
- **Failures:** reproducible product failures first, then runner and environment failures.
- **Evidence and artifacts:** ledger path, remote run or local output, relevant failure artifacts, and exact workflow or plan commands.
- **Duplication check:** other executions of the full matrix on an equivalent candidate or integration tree, and why they were required or avoided.
- **Cleanup and limits:** tracked-state confirmation, resources stopped or retained, and behavior still unverified.
- **Next step:** scoped builder fix, capability decision, remote candidate authorization, fresh combined-SHA run or delivery.

A complete report describes finished verification work. It does not mean the candidate passed.
