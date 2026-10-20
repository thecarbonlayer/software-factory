# Task folder

```text
<main checkout>/.factory/                 excluded via the common Git info/exclude
  <id>/
    state.md                              short current state, resume pointers and recent log
    checkout.json                         source/task/remote boundary evidence
    intent.md                             original sources, motivation, constraints and open questions
    spec.md                               current requirements/design, stable R/D IDs and authority
    answers.md                            supplied answers and authority, newest last
    triage.md
    plan.md                               current ID-to-change/proof map
    implementation-<round>.md             initial report or changed F IDs and new evidence
    review-<round>.md                     merged decision/findings; links to individual reports
    review-<round>-<focus>.md             individual acceptance/code/security/UX report
    documentation.md
    review-<round>-docs.md                documentation aggregate; individual reports stay separate
    summary.md                            complete local sign-off artifact
    logs/<stage-attempt>.jsonl            raw CLI stream, including pending attempts
    history/                              prior canonical versions or legacy reports when needed
<main checkout>/../<repo>.factory/<id>/    separate worktree, branch factory/<id>
```

The issue owns shared intent, discussion and clarified requirements. These local files are working copies and resume evidence. The PR owns the shared delivery record. For ad hoc work, the PR includes necessary intent and accepted scope. Do not commit per-task `intent/`, `spec/`, `plan/` or equivalent directories to the consumer. Existing durable documents change only when the implementation changes knowledge they own.

## Current and historical artifacts

`intent.md` preserves original request/spec text and authoritative sources. `spec.md` owns current requirements, design and scope trace. `plan.md` owns the current mapping to changes and proof. Requirements use stable `R-001` IDs, decisions `D-001`, findings `F-001`. Keep each ID across retries, scope changes and migration; retired IDs remain traceable and are never reassigned.

A requirement row links its original source, accepted behavior, status and proof. A material decision records its authority as **user-agreed**, **delegated implementation choice** or **unresolved proposal**, with the supporting answer, instruction or delegated scope. Silence is not agreement. Planning and later stages reference these IDs instead of repeating the spec. Preserve original sources and agreements for independent acceptance review.

Promote a checked complete refinement/plan output to the current canonical file. Preserve earlier attempts in raw stage logs; if the earlier canonical content has no complete recoverable log, archive it under `history/` first. A pending or failed attempt cannot replace accepted content. Record the accepted attempt, source revision and any unresolved items in state. Intent/answers preserve supplied text; append sourced changes rather than replacing history.

Implementation/review rounds and repeated stage attempts have unique filenames. A retry in the same fix round uses an unused attempt/revision suffix. Do not overwrite an earlier report or grant extra fix rounds. Documentation reports likewise preserve prior attempts. Current canonical files and state may be updated as specified; immutable reports stay historical. After submit, add the PR link and actual delivery status to the finished summary.

Every stage report starts with its existing first-line skill declaration, followed immediately by the state line. The factory adds metadata **after** these lines, never a wrapper header before them:

```text
I'm using the review and review-code skills.
Stage state: complete

Execution: <harness, executable/profile or fallback, flags, time>
Candidate / actual inspected revision: <full hashes>
<stage's documented report>
```

Keep raw JSONL logs, not duplicate raw issue exports or copies of user-owned dirty files. A separate evidence file is justified when a few state lines cannot hold the required boundary evidence.

## Stage completion

Completion describes stage work, independently of readiness or verdict. A complete report can conclude blocked or not assessable. A successful process/turn can still be pending.

- `Stage state: pending`: named checks/child jobs remain running. Record job handles and next resume action. Resume the same stage, join its work and keep its candidate frozen. Do not advance or launch a replacement that duplicates running work.
- `Stage state: complete`: all stage-owned work is joined, the candidate is final for that stage and the documented report follows. Report failed/unrun checks honestly. A known running child job contradicts complete and prevents advancement.

For **Claude stream JSON**, require process exit zero and inspect successful stage-result report payloads with `is_error` false. A runner error or nonzero exit invalidates a complete payload until the failure is explained and recovered; the payload alone cannot establish success. A report candidate has the expected first-line skill declaration and exact state line immediately afterwards. Ignore tool output, quoted examples and unrelated watcher messages as reports. Gather explicit complete reports from that invocation; identical retransmissions count once. Exactly one distinct complete report, with no unjoined owned work, may be accepted. Pending reports before it are attempt evidence. A later watcher lacking the report contract cannot replace it. Two distinct complete payloads, including differing candidate revisions or verdicts, are a conflict: preserve them and stop/resume for reconciliation. Never choose the longest, last or most confident message. Missing state, pending-only output or no complete report cannot advance even with a successful result subtype or exit code.

For **Codex**, read the process exit status and `-o` final-output file. Require exit zero, the expected skill declaration and exact complete line, and joined owned work. JSON configuration warnings alone do not determine failure. Nonzero exit, missing output/state or conflicting completion evidence remains failed/pending until explained and recovered. For **fallback subagents**, apply the same declaration/state/join checks to their returned report and record their completion status.

A process may terminate while a check launched earlier still runs. Keep the stage pending and follow that job to completion through the same stage's resume route. If the report claims complete but ownership or candidate cannot be established, preserve evidence and stop for recovery, rather than guessing.

## Two-phase preflight

Preflight checks capability and permissions, not product correctness. Record observed results, selected executable, exact profile flags, fallback route and relevant environment in state/evidence. A denied command is not a failed product test.

**Initial boundary, before triage:** use the selected runner/profile in the task worktree to establish it can start, load the factory and stage skills, read required referenced files and task handoffs, and execute baseline read-only Git operations. These include repository/common-directory identity, branch/HEAD/status, diff, history/ancestry and worktree inspection. Discover consumer-mandated pre-commit review and establish its executable, skill/config access and permission support now. Use its safe capability/help probe where available; otherwise inspect its invocation contract and mark any unproven execution limit explicitly. Do not run mutating review or commit hooks merely as a probe. A known unsupported required review is a blocker before expensive stages. If execution capability is required for the next step and remains unproven, stay blocked for a safe capability check or the specific access/authority decision; merely recording a limit does not authorize advancement.

Read-only permissions must include installed skill paths as well as task handoffs outside the worktree. Verify every reference needed by the selected stages; do not infer access from readable SKILL.md alone. Select narrow predictable read commands, not broad shell access. Capture the source checkout separately; all stage probes run in the task worktree.

**Planned-command boundary, after planning and before implementation:** planning now names exact verification commands, prerequisites and resource effects. Check that checks/edit profiles permit those commands, required consumer review, scoped writes and commits. Use exact-command permission/setup smoke probes. Do not run stateful full suites as preflight; their actual execution belongs to the planned verification stage. Record which capability was exercised versus inspected; a baseline failing regression test is distinct from a permission/runner failure. No need to invent all checks before planning. Temporary commit-message files belong inside the authorized worktree. Recheck newly introduced skills/references before dispatch.

If CLI launch fails, record the exact reason and preflight the generic-subagent fallback with the same skills/profile instructions. Reuse that working route for later stages. Do not repeat an unchanged CLI/access denial in every stage. An identifiable fix or changed environment permits a new probe. Fallback cannot waive a required consumer check or expand permissions. Stop if neither route supports the required capability; name the capability and the smallest needed decision.

## Writing for the reader

Put the next decision first. Reference earlier facts by file and stable ID, such as `R-001 in spec.md` or `F-001 in review-1.md`. Each fact has one owner. Delta reports preserve changed behavior, revisions, proof, limits and a usable next action without repeating unchanged narratives. Complete rerun instructions remain available by an exact reference or inline commands.

### Plain language

Apply core Simplified Technical English principles: active voice, one idea per sentence and consistent terms. Prefer short sentences and concrete behavior. Preserve quoted request text and answers. Use bullets for lists and tables for comparisons. Explain cause and effect in a full sentence. Keep full hashes in execution/boundary evidence; short prefixes suffice elsewhere. Compactness comes from references and ownership, not omitted evidence or rigid word limits.

## review-<round>.md

The aggregate owns the merged decision and stable finding table. Individual reports remain separate, linked as evidence, without verbatim appendices.

```markdown
# Review <round>: <candidate short sha>

Decision: <supports next step | blocks next step | not assessable>; <next action>
Candidate: <full sha>
Reviewers: <ran/reused/not applicable and reason; links to individual reports>
Resources: <isolation/serialization, environment and cleanup outcome>

| ID | Severity | Finding and trigger reachability | Evidence | Action |
| --- | --- | --- | --- | --- |
| F-001 | P2 | <trigger, impact; supported workflow / API-only / source-inferred> | <report and code/test reference> | <fix round, accepted with authority, or decision> |

<Use "No open findings." instead of an empty table.>

## Coverage and carried evidence
<R/D coverage changes, focus boundaries/revisions, checks, limits and unresolved required behavior; links to individual reports>
```

The main orchestrator owns task-wide F-ID allocation. Individual reviewer IDs are local aliases until merged. Map each source report and local ID to its task-wide ID; different findings with the same local ID get different task IDs. Merge duplicates while preserving the established task ID. Keep closed findings traceable in prior reports and current disposition references. Findings require evidence and an action; a source-inferred case stays visibly inferred. Review attempts do not create extra fix rounds.

## Focused-review reuse

Acceptance and code verdicts must cover each changed candidate, including documentation candidates. Security or UX verdicts may carry forward only if the orchestrator verifies and records **all** of these:

1. Requirements, decisions and risky-area classification relevant to that focus are unchanged.
2. No relevant source, test, configuration, asset or migration changed since the earlier reviewed revision. Inspect actual content and dependencies, including indirect effects. Filename similarity alone is insufficient.
3. Verification environment, prerequisites and known limits are unchanged.
4. The earlier report names its reviewed revision and has no unresolved finding in that focus.

Record earlier report/revision, current candidate, carried verdict, actual boundary comparison, unchanged requirement/risk evidence, environment/limit evidence and why intervening changes cannot affect that focus. A documentation or image change may affect security or UX. Uncertainty, missing evidence or unresolved findings require a fresh focused review. A carried verdict retains its earlier revision; it is not mislabeled as a newly executed check. An unchanged candidate may reuse its still-valid acceptance/code reports after resume comparison.

Allocate check ownership: acceptance validates requirement coverage; code owns general code/test verification; security owns adversarial checks; UX owns real user journeys. Reviewers rerun a shared suite only if current evidence is missing, stale or insufficient for their focus. Apply consumer REVIEW.md by reference instead of duplicating its policy.

## state.md

Keep the header current and the log recent. Detailed historical evidence stays in referenced reports/logs.

```markdown
# <id>: <title>

- Status: running | waiting for a person | finished | failed
- Waiting for: <specific answer/decision and evidence file, or none>
- Next step: <stage/action; pending job handles when applicable>
- Stage / fix rounds used: <stage> / <0..2>
- Source: <issue URL or ad hoc identity>
- Branch / worktree: <expected branch and path, or reservation only>

## Resume evidence
- Source identity: <full host/repository/issue or request identity; explicit run suffix>
- Delivery target: <remote, target branch/ref, fetched SHA and fetch time>
- Base commit: <immutable task start SHA>; checkout.json holds source-only ancestry and dirty hashes
- Expected checkout / branch / completed HEAD: <identity> / <branch> / <SHA>
- Expected status/content: <clean or evidence pointer>
- Evidence boundary: <accepted complete stage/attempt, report, candidate and time>
- Execution: <executable/fallback; profiles/flags and two preflight outcomes or pointers>
- Risky areas: <shared list>
- Context destinations: <existing owners, REVIEW.md, absent owners>
- Reviewers: <current aggregate, ran/carried revisions and verdicts>
- Migration/drift: <none or evidence and invalidated stages>

## Recent log
- <time> <stage>: <outcome and report pointer>
```

## summary.md

The first screen contains only decision, open items, unverified required behavior and actual outcome. Supporting evidence follows.

```markdown
# <id>: <title>

**Your decision:** <submit, re-scope or continue; exact open approval>
**Open findings / decisions:** <none or F/D IDs with evidence>
**Unverified required behavior:** <R IDs and reasons, or none>
**Outcome:** <delivered behavior and actual branch/delivery state>

| Requirement | Status | Evidence |
| --- | --- | --- |
| R-001, <short behavior> | met / changed by agreement / unmet / unverified | <check, revision, report; scope-change authority when applicable> |

## Risk and decisions
<Touched risky areas and coverage; accepted risks and D IDs with authority>

## Rerun
<Complete commands/prerequisites, or exact reference to the current complete rerun instructions>

## Branch and durable context
<Remote target/base/drift, branch/worktree, commits, documentation updated/skipped, missing owners and PR link after submit>
```

The local summary may reference local evidence. The PR must translate it to accessible issue, submitted commit, code/test or CI references, or concise observed results with revision and limitations. A finished run has not necessarily been submitted, merged or deployed. The tracked task log records actual status and durable verification limits, without copying intermediate reports.

## Stage-boundary evidence

Use Git and host tools to record common repository, checkout path, branch, HEAD, tracked/untracked status and relevant content hashes before and after each stage. `checkout.json` keeps separately named **source**, **delivery target**, **task base**, **expected task boundary** and **observed discrepancy** records; observing a mismatch must not overwrite expected evidence. The target record contains remote identity, branch/ref, fetched SHA and fetch time. Record source-only commits and divergence comparison separately from the immutable task base. Preserve earlier boundary evidence in stage logs or history when updating the current record.

Hash changed tracked/relevant untracked source files without copying user content. Record relevant ignored inputs and service/database state when checks depend on them. Clean Git status alone does not establish runtime prerequisites. Verify commits belong to the task branch and preserve unrelated files. Review evidence includes candidate/actual revision, environment, temporary effects and cleanup. Unexpected dirty files or branch changes are discrepancies, not task output. Do not bless a concurrent edit by saving it as the expected boundary.

## Review scheduling

Independent reads/checks may run in parallel. Before mutable checks, identify shared databases, fixtures, service state, ports and files, including temporary tests. Use existing resource isolation or serialize conflicting checks. Separate worktrees alone do not isolate databases or services. If independence is unknown, serialize checks while reads may proceed.

Pass candidate, arrangements and cleanup responsibility to each reviewer. Pause implementation. Reviewers cannot change tracked source or HEAD. Temporary tests must be isolated from other discovery or run serially, then removed and reported. Restore only resources owned by that check; preserve user data and other sessions' services. Failed cleanup or unexpected shared state stops affected checks and limits the verdict. Confirm HEAD/status and cleanup before combining results; repeat affected reviews when the candidate changed.

## Resume comparison

1. Confirm recorded remote target, base, common repository, expected checkout and registered branch/worktree belong to this task. A reservation legitimately stopped before worktree creation compares source evidence. Refresh the recorded target, without changing the user's checkout.
2. Compare actual branch, HEAD, status/content and relevant check prerequisites with the expected boundary. Compare the new target SHA with its saved value separately. Record target drift and inspect its effect on the proposed base-to-candidate diff, compatibility, scope and prior checks/reviews. Preserve the immutable task start base. Do not automatically reset, rebase, force-push or change the target. Unclear delivery intent needs a specific decision.
3. Preserve unexpected changes and prior expectations. Identify stale evidence and trace the difference: changed requirements/authority may require refinement/planning; code/docs changes need scope checks, verification and review. Recover an interrupted authorized task commit only with independent evidence and fresh checks. An unexplained branch rewrite or user-owned edit needs a decision before work resumes. Do not switch, stash, reset, clean or incorporate it automatically.
4. Missing branch/HEAD/status/target evidence stays unknown until independently recovered from immutable reports, task commits, worktree registration and the intended remote. Inspect present diffs and repeat affected checks. Saving the current checkout as expected is not recovery. Preserve fix-round usage; if unknown, ask rather than grant a new allowance.

Status is read-only. Repeated review, migration and resume never reset the two-fix-round limit.

## Legacy task migration

On **continue**, preserve old `request.md`, `refinement-<pass>.md`, reports, logs, answers and checkout evidence. Do not migrate during status or delete history. First validate source identity, actual branch/worktree, saved base and expected boundary under resume comparison. Fetch/record the intended remote target; a legacy local base is not retroactively a remote base. Report source-only ancestors and target differences. Any need to change branch ancestry or include unpublished work requires the specific decision, without automatic rebase/reset.

Create `intent.md` from the original request/sources, with pointers to preserved legacy files. Build `spec.md` from the last **independently established accepted** refinement and sourced answers, not simply the highest-numbered attempt. Preserve conflicting drafts as unresolved alternatives. Recover accepted scope from explicit authority; ask only about unresolved authority/scope that blocks the next step. Silence cannot resolve conflicts.

Preserve existing stable IDs; assign missing R/D/F IDs once with a legacy-item-to-ID map in the local canonical artifacts or history. Do not renumber across later passes. Map prior findings and fix rounds before resuming. Reconcile `plan.md` to accepted IDs while preserving its earlier version. Missing execution/checkout evidence requires fresh preflight and affected checks/reviews. Label old verdicts historical unless their boundary can be established. Record migration provenance, remaining unknowns and invalidated stages in state, then resume from the first affected stage.
