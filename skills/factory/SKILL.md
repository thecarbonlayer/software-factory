---
name: factory
description: Use when starting, resuming, checking or submitting a software task through Software Factory. Keeps discovery, planning, implementation and documentation in one builder loop, with independent review and verification.
---

# Factory

You are the task's main builder loop. Own orchestration, task state, decisions, implementation and evidence. Load stage skills progressively in this same context. Use fresh contexts only when independence or an isolated environment improves the result.

Use the [task-folder contract](references/task-folder.md) for artifacts, capability discovery, evidence, resume checks and recovery.

Commands take free text:

- **start** `<issue link, number or request>`: reserve a task, establish its remote base and worktree, then run until a decision or external action is needed.
- **continue** `[task id] [answers, decisions or notes]`: validate saved boundaries, incorporate new authority and resume the same builder loop.
- **status** `[task id]`: report saved task state without changing it.
- **submit** `[task id] [notes]`: run `software-factory:submit` to publish a reviewed candidate as a draft PR, including when the draft is needed to obtain remote verification. A direct yes to that question has the same effect.

## Boundaries

- **Files preserve task memory.** Keep local working artifacts in the excluded `.factory/<id>/`. The issue owns shared intent and discussion. The PR owns shared delivery evidence. Do not commit per-task planning artifacts to the consumer.
- **The source checkout stays unchanged.** Create a separate `factory/<id>` worktree from the fetched delivery target. Never silently include unpublished source changes.
- **People decide external actions and wider scope.** `start` authorizes implementation within the agreed plan. Posting, issue changes, pushing, PR creation, merge and deployment need their own authorization or an explicit consumer policy. Never merge or deploy.
- **The plugin remains consumer-neutral.** Discover commands, roles, workflows and policy from the consumer repository. Do not encode a consumer's names, paths, accounts or product assumptions in Factory artifacts.

## Context model

Use one persistent builder context for work whose next decision depends on what came before:

```text
triage -> refine -> plan -> implement -> document -> fix
                         |                         ^
                         +---- same builder ------+

frozen candidate -> independent review -> one authoritative verification route
                                      \-> draft PR first when remote checks own verification
```

Load `triage`, `refine`, `plan`, `implement` and `document` only when that capability is needed. Do not start a new context merely because the stage name changed. Keep the same builder context through scoped fixes so it retains tradeoffs, failed approaches and user decisions.

Create a fresh context only for one of these reasons:

1. independent review of a frozen candidate;
2. independent black-box verification in a clean or isolated environment;
3. self-contained research that can proceed without task-local reasoning;
4. a measured context-quality problem, or conflicting tools and permissions that cannot be isolated safely.

Record the reason. More contexts are not a default quality mechanism. Do not split work into role-playing agents when the roles need the same evolving state.

## Start and resume

1. Resolve the source identity and search existing tasks, including legacy names. Resume a match. A new run needs an explicit distinct suffix.
2. Reserve `.factory/<id>` atomically before writing. Record source branch, HEAD, status and dirty-content hashes in `checkout.json`. Add `.factory/` to the common repository's local exclude.
3. Resolve and fetch the intended remote target. Record remote, target ref and fetched SHA. Report source-only commits and divergence. Do not use a stale local ref or unpublished commit as the base without a decision.
4. Create `factory/<id>` in a separate worktree from the fetched SHA. Record branch, worktree, base and expected clean boundary.
5. Discover applicable project instructions, `REVIEW.md`, setup and test guidance, durable documentation owners and protected resources. Write `intent.md` and initial `state.md`.
6. Run capability discovery once. Save observed executables, profiles, skill access, allowed commands, timeout mechanism, fallback and environment constraints in `capabilities.json`. Prefer host-native time limits. Never assume GNU `timeout` exists. A denied or missing capability is recorded once and is retried only after a concrete environment change.
7. On `continue`, compare the saved base, target, branch, HEAD, status, relevant inputs and environment with reality before resuming. Preserve unexpected changes. Mark dependent evidence stale rather than blessing the new state.

## Builder loop

The builder writes canonical task artifacts directly. It may call tools, but it does not dispatch a separate agent for each stage.

1. **Triage.** Load `software-factory:triage`. Assess readiness for refinement or the named target. Save the result in `triage.md`. Stop only for a real dependency, inapplicability or failed investigation.
2. **Refinement.** Load `software-factory:refine`. Maintain `spec.md` with stable requirement and decision IDs. If necessary information is missing, prepare one clarification request and stop. Append supplied answers and their authority to `answers.md`, then continue in the same builder context.
3. **Planning.** Load `software-factory:plan`. Maintain `plan.md` as the owner of approach, affected components, exact verification commands, prerequisites, resource effects and the R/D-to-proof map. Select one authoritative owner for the complete suite: configured remote checks bound to the candidate or a proven integration revision, or the independent verifier locally when no suitable remote route exists. Check planned commands against `capabilities.json` before editing. A material scope or policy choice needs authority; an ordinary implementation choice can proceed within delegated scope.
4. **Implementation.** Load `software-factory:implement`. Use behavior-focused checks, implement the smallest coherent change and append results to `evidence.md`. Commit when the consumer workflow and task authorization permit it. A fix round reports only changed findings, changed requirements, candidate commits and new evidence IDs.
5. **Documentation.** Load `software-factory:document` before freezing the candidate. Reconcile existing durable documentation against the implemented behavior and decisions. Documentation is part of the candidate reviewed below, not a post-review add-on.
6. **Freeze candidate.** Confirm the expected branch, HEAD, status, diff, declared resources and cleanup. Save the candidate revision and evidence boundary in state. Pause builder edits while external review and verification run.

If a stage is inapplicable, record why and continue. Do not simulate a handoff report to yourself. The canonical artifacts and `state.md` are the handoff.

## Independent review

Launch one fresh reviewer context for the frozen candidate. It must not receive the builder's private reasoning or conversational history. Give it only the original intent, accepted spec and decisions, plan, base-to-candidate diff, current documentation, evidence ledger, risky-area classification, consumer `REVIEW.md` and resource limits.

The reviewer loads `software-factory:review` and `software-factory:review-code` in the same context. Add `software-factory:review-security` when the change touches trust boundaries, access, untrusted input, money, secrets, shared data or migrations. Add `software-factory:review-ux` when screens, navigation, messages or role-visible behavior changed. Focus skills add lenses; they do not create more reviewer agents by default.

Review is read-only apart from declared isolated temporary tests. It may run a narrow check to establish a finding, but it does not own the consumer's complete regression or journey suites. Supply existing finding IDs and the next available ID. Save the complete report as `review-<round>.md` and preserve its IDs task-wide.

For an authorized scoped fix, resume the same builder context and preserve existing F and E IDs. The same reviewer context may recheck a narrow fix when the finding, requirements and affected surface remain bounded. Reuse verification evidence only when its candidate or integration tree, inputs, environment and limits still apply; rerun affected checks plus any consumer-mandated matrix that cannot be reused. Use a fresh full reviewer when scope, architecture, risk classification or the base-to-candidate diff expands materially.

## Independent verification

After review supports the next step, launch one fresh verifier context and load `software-factory:verify`. Do not give it the builder's reasoning. Give it the frozen candidate, `plan.md`, `capabilities.json`, `evidence.md`, consumer instructions, `REVIEW.md`, and remote-check metadata when applicable.

The verifier discovers the consumer's required checks and runnable user journeys, including any declared role or persona matrix. It selects one authoritative full-suite route according to consumer policy:

- **Suitable remote checks exist.** Do not run the same complete suite locally and remotely against an equivalent tree. Obtain authorization, use `software-factory:submit` to publish the reviewed candidate as a draft PR or equivalent remote candidate, and keep the task running with verification pending. The verifier reads concise conclusions first and opens failure artifacts only as needed. It consumes required remote jobs for the candidate head or a proven integration revision containing it, then records the candidate, tested revision, target relationship, workflow, matrix, environment, results and limits.
- **No suitable remote checks exist.** Run the documented complete local suite once in an isolated environment, or serialize shared resources. If only meaningful manual checks exist, run and record those. Do not create CI or a test framework without separate authorization.
- **No valid verification route exists.** Mark the affected requirements unverified. This is not a product failure, but it can block delivery or require a person's explicit risk decision.

Read concise remote conclusions first and open traces or screenshots only when they are needed to classify a failure. A branch name, pull request number or green result without an exact candidate-to-tested-revision relationship is not evidence. Any required job that is missing, skipped, cancelled or still running remains unverified or pending.

If verification exposes an implementation defect, resume the builder for a fix, refreeze the candidate, and repeat affected independent review and verification. A new commit invalidates the prior remote result. If verification exposes only an environment or runner gap, preserve the candidate and stop for the smallest needed decision.

## Moving targets and parallel tasks

Worktrees isolate files; they do not cause target drift and do not keep parallel branches synchronized. Drift comes from independent branch histories advancing. Refresh and compare the delivery target at candidate freeze, before publishing a draft, and before final delivery or queue entry. Classify drift before acting:

- **Target unchanged:** continue.
- **Target advanced without a dependency or conflict:** keep the immutable task base. A configured merge queue or equivalent integration check can validate the candidate against the latest target without rewriting the task branch.
- **Target advanced with possible semantic overlap:** require evidence on the combined revision. Prefer the consumer's merge queue. Otherwise obtain authority to update the task branch, then rerun affected review and verification.
- **Textual conflict or newly introduced dependency:** stop for the recorded update policy or a specific decision. Resolve only in the task worktree. Never rewrite the source checkout or silently rebase.
- **One task depends on another unmerged task:** use the consumer's stacked-PR convention or serialize them. Do not pretend they are independent.

Discover the host's merge queue or equivalent from consumer policy. A queue-created combined tree is a new integration revision, so rerunning required checks there is not duplicate verification. If no queue exists, follow the consumer's branch-update rule. The factory may propose merge, rebase or retargeting, but it performs none without existing authorization.

## Independent-context execution

Use the host's supported isolated agent or non-interactive runner. Do not require a particular provider. Preflight the chosen route once and record it in `capabilities.json`.

- Give each independent context an exact worktree, immutable base and candidate, allowed commands, resources and output path.
- Require the first line to name loaded skills and the second line to be exactly `Stage state: pending` or `Stage state: complete`.
- A successful process is not enough. Accept completion only when the expected candidate is named, all owned work is joined, tracked state is unchanged and exactly one complete report is returned.
- Preserve raw runner output in `logs/`. Do not repeat an unchanged launch or permission failure in later stages. Use a preflighted fallback only when it preserves the same independence and permissions.

## Decide, finish and submit

Use at most two implementation fix rounds unless a person authorizes more. Stop for a risky-area finding, missing required check, scope reversal or unresolved product choice that exceeds authorized repair.

When review supports the candidate, either verify locally or request draft publication for the selected remote route. Publishing a draft is not a claim that verification passed. Record the PR and pending jobs in state, then resume verification when their status changes.

When review and verification support the exact candidate, write `summary.md`. Lead with the requested decision, open findings or decisions, unverified required behavior and actual outcome. Then map requirements to evidence IDs, record accepted risks, and provide the branch, base, candidate and exact rerun commands by reference to `plan.md`. If a draft already exists, update its verification summary only when the existing submission authorization or consumer policy covers that external edit.

If local verification finishes before publication, ask whether to submit unless submission is already authorized or consumer policy allows automatic draft submission. On **submit**, load `software-factory:submit`, refresh and classify target drift, then push the task branch and open or update a draft PR. Never silently rebase, reset, merge or deploy.

## Status and failures

**status** reports task id, title, stage, state, waiting decision, next step, branch, worktree and candidate. It does not repair artifacts.

Recover proportionately: correct an argument, use a recorded fallback or rerun after a concrete capability change. Never count failed or unrun checks as passed. Preserve partial evidence and name the specific blocker. Keep user updates short and decision-oriented.
