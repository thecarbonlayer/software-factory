# Software Factory efficiency and review design

## Intent

Make Software Factory cheaper and easier to review without weakening its evidence, permissions, or recovery guarantees.

The change is driven by five consumer factory runs from another machine. Those runs exposed repeated context loading, late merge-base surprises, blocked stage tools, ambiguous stage completion, duplicated focused reviews, and long artifacts that restated earlier work. The Visual PR skill is a useful reference for reviewer-first presentation, especially its reason-first summary, exceptional concerns, and optional structural views.

## Goals

- Start each ordinary task from a freshly fetched remote target revision, normally the remote default branch.
- Keep the user's current checkout unchanged and continue all implementation in a separate worktree.
- Detect runner, skill-access, permission, and required pre-commit-review failures before expensive stage work.
- Distinguish a completed stage report from a successful turn that is still waiting for checks.
- Preserve independent acceptance and code review while avoiding repeated focused reviews after unrelated changes.
- Make stage outputs and pull requests decision-first, concise, and useful to both people and later agents.
- Preserve requirement coverage, decision provenance, verification limits, risky-area coverage, and resume evidence.
- Prefer small contract changes over new orchestration infrastructure.

## Non-goals

- No model or reasoning-effort pinning.
- No new service, daemon, validator framework, artifact renderer, or harness-specific agent definition.
- No weakening of authorization boundaries, review independence, or the consumer's required checks.
- No automatic rebase, force-push, merge, deployment, or mutation of the user's local default branch.
- No consumer-repository copy of per-task intent, specification, or plan artifacts. The issue and pull request are the shared task record.
- No version bump until the complete change set and behavioral evaluations are accepted.

## Evidence from the audited runs

- Consumer runs 11, 12, and 15 began from local `main` revisions containing 15 or 16 commits absent from the fetched remote target. The mismatch was discovered near submission, after implementation and review.
- Run 12 recorded 257 unique permission denials. Refinement could not read its installed skill templates, and review stages often could not run basic Git boundary checks or planned test commands.
- Run 15 had 32 explicit Bash denials, nine implementation attempts, six pre-commit reviews, and three four-reviewer rounds.
- Run 13 repeated all four reviewers after a change limited to an image and task-log entry. Those four reviews processed about 9.6 million reported input tokens and produced about 40,000 output tokens.
- Several Claude stage streams emitted multiple successful result events. Early results said checks were still running, while later results contained the actual report. Selecting the last or longest result is not a reliable completion rule.
- The substantive stage reports for runs 12 and 15 each totaled about 265,000 characters. Requirements, prior findings, and check evidence were often restated across stages.
- Documentation review found inferred choices labeled as user decisions. The current policy already forbids this, but the handoff format did not preserve authority clearly enough.

## Design

### 1. Resolve the delivery base at task start

For a new task, resolve the intended pull-request target before planning:

1. Identify the remote and target branch from project rules or the remote default.
2. Fetch that target.
3. Record the remote target name and revision in `checkout.json` and `state.md`.
4. Compare the current checkout with the target and report unrelated local ancestors.
5. Create `factory/<id>` directly from the fetched remote-tracking revision.

Do not switch, pull, reset, or clean the user's checkout. If the remote cannot be refreshed, or the user intends unpublished local commits to be the base, stop for that specific decision. `continue` and `submit` compare against the recorded target as well as the task branch.

This uses the existing worktree flow. It does not add a synchronization service or a second branch-management abstraction.

### 2. Preflight the execution contract at two natural boundaries

Before the first stage, confirm the selected harness can:

- load the required factory skill;
- read its referenced skill files and task handoff files;
- run the baseline read-only Git boundary commands; and
- invoke any consumer-mandated pre-commit review command.

Planning selects the exact verification commands. After planning and before worktree implementation, preflight those commands and the checks/edit profiles. This avoids pretending the factory knows the checks before planning while still failing before expensive implementation.

Record the selected executable, profile, and execution fallback in `state.md`. Reuse that choice for the task. If the environment fails later for the same reason, do not repeat the unchanged attempt across stages. This execution fallback is independent of the single-source-of-truth rule for artifacts.

Keep permissions narrow. Add predictable read-only Git operations and exact planned checks to the profile instead of broad shell access. Put temporary commit-message files inside the authorized worktree.

### 3. Give stages an explicit completion state

A stage returns one of two states:

- `pending`: named checks or child jobs are still running, so the factory must resume the same stage and cannot advance;
- `complete`: all stage-owned work is joined, the candidate revision is final for that stage, and the documented report follows.

The report keeps the existing first-line skill declaration and adds a machine-recognizable state line. Claude stream parsing selects the single complete report and rejects conflicting complete reports. It never selects authority by message length. Codex continues to use its final-output file and exit status, with the same report-state check.

### 4. Reuse review evidence only when its boundary is unchanged

Acceptance and code review remain mandatory for every changed candidate.

Security or UX review may carry forward only when the orchestrator verifies all of the following:

- the requirements and risky-area classification for that focus are unchanged;
- no relevant source, test, configuration, asset, or migration changed since that review;
- the verification environment and known limits are unchanged; and
- the earlier report names the reviewed revision and has no unresolved finding in that focus.

The aggregate review records the carried verdict, earlier revision, and boundary evidence. Filename similarity alone is insufficient. If the boundary is uncertain, rerun the focused review.

Checks have owners. Acceptance reviews validate requirement coverage, code reviews own general code/test verification, security reviews own adversarial checks, and UX reviews own real user journeys. A reviewer reruns shared suites only when existing evidence is missing, stale, or insufficient for its focus.

Findings state whether their trigger is reachable through a supported user workflow, through an API only, or is inferred from source. This keeps speculative low-severity cases from consuming a fix round without losing API correctness coverage.

### 5. Use one task record and make local artifacts delta-based

Use one shared information path for every task:

- When a GitHub issue exists, it is the source for the original intent, discussion, and clarified requirements.
- The excluded `.factory/<task-id>/` directory contains working copies, resume state, intermediate reports, and raw logs. It is not a second shared knowledge base.
- The submitted pull request is the concise shared delivery record. It links to the issue and submitted commits.
- Existing repository documents change only when the implementation changes durable project knowledge owned by those documents.

Do not offer a second mode that commits a per-task `intent/`, `spec/`, or `plan/` directory to the consumer repository. For an ad hoc request without an issue, the pull request carries the necessary intent and accepted scope.

Align the local working artifacts with the AI-native SDLC vocabulary while retaining the evidence needed to resume:

- `intent.md` replaces `request.md`. It preserves the source request and records what is wanted, why, affected users or systems, constraints, open questions, and the authoritative issue when one exists.
- `spec.md` replaces the numbered refinement files as the current accepted requirements and design. Raw stage logs preserve earlier attempts. Requirements and material decisions have stable IDs and explicit authority: user-agreed, delegated implementation choice, or unresolved proposal.
- `plan.md` maps the accepted IDs to files, order of work, risks, rejected alternatives, and proof. It does not restate the full specification. Material implementation departures update the local plan and are surfaced in the pull request.

Keep `checkout.json`, the short current `state.md`, implementation and review evidence, the final local `summary.md`, and raw JSONL logs. Do not add an evidence database or generated dashboard.

- Fix-round implementation reports contain the changed finding IDs, resulting commits, new evidence, and complete rerun instructions. They do not repeat unchanged behavior narratives.
- Individual review reports lead with `supports next step`, `blocks next step`, or `not assessable`, followed by findings, changed coverage, checks, and limits.
- `review-<round>.md` keeps the merged decision and finding table. Individual final reports are stored separately and referenced instead of being appended verbatim to the aggregate file.
- `summary.md` remains the complete sign-off artifact, but its first screen contains only the decision, open items, unverified required behavior, and outcome. Its requirement matrix uses the stable IDs and concise evidence references.
- `state.md` remains short and current.

Compactness comes from one owner per fact and references to stable IDs. It does not come from rigid word limits or omitted evidence.

### 6. Make the pull request useful outside `.factory`

The draft pull request body follows this order:

1. Why and what changed, in one or two sentences.
2. Reviewer attention: open findings, unverified required behavior, migrations, compatibility effects, accepted risks, or deliberate omissions. Omit when empty.
3. A compact change outline. Add one structural view only when it clarifies ownership, order, state, or an API/data contract better than prose.
4. Verification on the submitted revision, including material failures and skips.
5. A collapsible acceptance-evidence and rerun section when the code host supports it; otherwise use a normal final section.

The consumer's pull-request template still takes precedence. Local `.factory` paths are not valid remote evidence. Translate them into accessible issue, commit, code, test, or CI references, or include a concise observed result with the tested revision and limitation.

Discover a consumer `REVIEW.md` and apply it as the repository's review policy. It owns review passes, severity meanings, exclusions, and noise limits. Do not duplicate that policy in `AGENTS.md` or the pull request. When no `REVIEW.md` exists, use the factory's review policy without creating one unless the consumer change explicitly establishes durable repository review guidance.

Visual PR contributes the selection rule and reviewer hierarchy. Its HumanLayer-specific files, upload hooks, and PR mutation workflow are not adopted.

## Verification

The exported logs are the baseline failures. Validate the revised skills with fresh agents and isolated temporary artifacts:

1. A start scenario where local `main` is ahead of the fetched remote target. The factory must branch from the recorded remote revision without changing local `main`.
2. A runner scenario with an unreadable skill reference or unsupported mandatory pre-commit review. The factory must fail during preflight and must not repeat the same launch failure across stages.
3. A multi-result stage stream with pending messages before the final report and a later watcher message. Only the explicit complete report may advance the task.
4. A review round whose only new change is documentation or an asset. Acceptance and code review rerun; unchanged focused verdicts carry forward only with recorded boundary evidence.
5. A submit scenario with a long local summary. The PR body must remain self-contained, surface reviewer attention first, and preserve requirement status and rerun evidence without linking to inaccessible local artifacts.
6. A decision-provenance scenario where silence is the only support. Documentation must not label the choice as user-decided.
7. An issue-backed task where local intent, specification, and plan remain excluded while the pull request is self-contained and links the issue and submitted revision. No per-task artifact directory may appear in the consumer diff.
8. A consumer with `REVIEW.md`. Review must apply its passes, severity thresholds, exclusions, and nit limit without copying the policy into task artifacts.

Also run plugin validation, JSON parsing, link checks, and `git diff --check`. Compare the revised outputs with the audited examples for missing facts and material length reduction. A shorter artifact fails if a future agent cannot recover scope, candidate revision, checks, limits, and next step.

## Implementation scope

Expected files are the existing factory, submit, refine, plan, implement, review, document, task-folder, and durable-context instructions, plus README updates when behavior changes. Avoid changing focused review skills unless a tested gap requires it.

Keep the version at `0.7.0` during implementation and evaluation. Choose and apply the next version only after the user accepts the complete verified change set.

## Separate consumer change

After the plugin behavior and version are finalized, make a separate consumer branch and pull request. That change will:

- turn `AGENTS.md` from an “always read” list into a compact context index with task-based routing;
- keep the essential day-one build, test, and lint commands in `AGENTS.md`, while routing prerequisites and specialized checks to their existing owners;
- keep the must-preserve product, security, data, and delivery constraints visible without requiring every stage to load the full product, design, and decision corpus;
- map each kind of durable information to one canonical document, replace duplicate current-state guidance with links, and move misplaced guidance to its natural owner;
- preserve dated task-log and decision history even when current-state duplication is removed elsewhere;
- add a root `REVIEW.md` as the canonical review-policy owner, including review passes, consequence-based severities, evidence expectations, exclusions, a cap on nits, and the existing Codex pre-commit-review requirement;
- do not create a generic development document. Reuse existing setup, testing, operations, and architecture documents, and create a new owner only if the cleanup proves a specific uncovered gap;
- move detailed local accounts to `docs/local-real-data.md` and route optional fixture instructions to their existing executable or testing owners, preserving the protect-unless-requested rule;
- verify that linked status, decision, testing, review, and task-log documents contain the guidance removed from `AGENTS.md`;
- repair current-authority conflicts exposed by the new index, including tablet support, manual-only CI, staging state, and superseded RBAC guidance;
- add current-authority notices or links to historical plans and records without rewriting their dated content;
- preserve `CLAUDE.md` as the canonical include;
- verify the finalized Software Factory version in both supported hosts and record the completed update in the task log; the current consumer config is intentionally unpinned, so do not invent a version field or add changing version data to `AGENTS.md`;
- record the completed consumer work in its existing task log.

The consumer context owners will be:

| Information | Canonical owner |
| --- | --- |
| Task routing and must-preserve boundaries | `AGENTS.md` |
| Review passes, severity, evidence, and exclusions | `REVIEW.md` |
| Current scope and pending decisions | `product_spec/STATUS.md` |
| Decision history and supersession | `docs/architecture/decisions.md` |
| Setup, verification, development safety, and factory usage | Existing repository guides selected by the task-based index |
| Local accounts, protected data, and recovery | `docs/local-real-data.md` |
| Persona journeys | `design/personas/*`, routed by `design/README.md` |
| Visual and language rules | `design/system/design.md` and `design/system/style-guide.md` |
| Deployment state and procedure | deploy logs and operator guides |
| Completed work history | `docs/TASK_LOG.md` |

Also verify broader stale or misplaced guidance found during the audit, such as historical-plan CI promises, obsolete architecture source links, old issues, manual-testing role tables, and broken index links. Fix it in the consumer PR only when the current authority is independently clear. Otherwise record the specific follow-up instead of guessing.

Keep this consumer patch limited to context organization, verified documentation reconciliation, and the plugin upgrade. Do not mix product or application changes into it.
