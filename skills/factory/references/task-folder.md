# Task folder

```text
<main checkout>/.factory/            excluded via .git/info/exclude
  <id>/
    state.md                         person's view first, then resume evidence and a short log
    request.md                       the request, issue text and comments (the only copy)
    checkout.json                    source checkout boundary: branch, HEAD, status, hashes of dirty files
    triage.md
    refinement-1.md                  one per refinement pass; the highest number is current
    answers.md                       answers supplied with continue, newest last
    plan.md
    implementation-1.md              one per round
    review-1.md                      one per review round: merged findings first, then each reviewer
    documentation.md                 the documentation stage's report, after the last code review
    review-<round>-docs.md           the documentation check
    summary.md                       written at the end; the pull request link is added after submit
    logs/<stage file>.jsonl          each stage's JSON log (CLI stream), kept for evidence
<main checkout>/../<repo>.factory/<id>/   the task's git worktree, branch factory/<id>
```

Each stage file starts with one line naming the stage, the skills loaded, how it ran (harness and CLI profile, or fallback subagent), the commit it looked at and the time, followed by the stage's output as returned. Do not edit an earlier stage file; a later round gets its own file. A repeated stage or review within the same fix round uses an unused attempt/revision suffix rather than overwriting its earlier output. Review attempts do not grant additional fix rounds.

Apart from stage logs in `logs/`, do not save raw tool output (for example the issue as JSON) or copies of the person's own uncommitted changes. Record a blocker in `state.md`; add a separate file only when its evidence will not fit in a few lines there.

## Writing for the reader

Every file has a first reader: the person at a stop or sign-off, or the next stage. Each stage's own format puts what its reader needs first. You bring anything that needs a person to the top of `state.md` (**Waiting for**), with the file that holds the evidence.

### Plain language

Use the core rules of Simplified Technical English (ASD-STE100), not its full dictionary:

- Write one idea per sentence.
- Keep sentences to 20 words for instructions and 25 words for descriptions.
- Use the active voice.
- Use the same term for the same thing in every file. Keep the project's own names for code, roles and features.
- Do not change quoted request text or quoted answers.

Short means fewer items, not fewer words per item. Never write glued or telegraphic text.

- Use bullets for lists of facts.
- Use tables to compare items such as requirements, findings or reviewers.
- Write a sentence when there is cause and effect, for example a finding's trigger, impact and evidence.
- Write each bullet and table cell as a full short phrase or sentence.

Refer to an earlier file and item (for example "criterion 3 in refinement-2.md") instead of restating it. Restate only what changed. Full commit hashes belong in stage header lines and `state.md`; elsewhere an 8-character prefix is enough.

## review-<round>.md

One file per review round. You write the top; the reviewers' reports follow as returned.

```markdown
# Review <round>: <candidate short sha>

Reviewers: <who ran and why; who was skipped and why; verdicts carried over from an identical tree, with the revision>
Resources: <independent reads, isolated or serialized checks, cleanup outcome>
Decision: <fix round N | stop for a person | finish>

| # | Severity | Finding | Reviewer | Action |
| --- | --- | --- | --- | --- |
| 1 | P2 | one line, file:line | code review | fix in round N, or the person's decision needed |

(Write "No open findings." instead of an empty table.)

## <reviewer>
<header line, then the report as returned>
```

The table is the merged, de-duplicated finding list from **Decide**. A fix round works from it and reads a reviewer's section only for the evidence behind a row.

## state.md

Keep it short and current. Update it after every step so another session can resume. The first block is for the person and for `status`; the second is for resume.

```markdown
# <id>: <short title>

- Status: running | waiting for a person | finished | failed
- Waiting for: <the decision or answers needed, with the file that holds the evidence, or none>
- Next step: <what continue will do>
- Stage / round: <stage> / <fix round, 0 before the first review>
- Request: <issue link or "text">
- Branch / worktree: factory/<id> at <path>, or not created yet

## Resume evidence
- Source identity: <issue host/repository/number or request identity; distinct run suffix when requested>
- Base commit: <sha>; source checkout evidence in checkout.json
- Expected checkout: <source checkout before worktree creation, task worktree afterward>
- Expected branch / last completed HEAD: <branch> / <sha>
- Expected status: <clean, or short status; hashes in checkout.json>
- Evidence boundary: <last completed stage, output file and time>
- Risky areas: <the task's list, built at start>
- Context destinations: <existing README/product guide, decisions, tracked task log, instructions; name missing files>
- Reviewers: <latest round: who ran on which revision, verdicts; details in review-<round>.md>

## Log
- <time> <stage>: <one-line outcome> (<file>)
```

Log lines are one sentence each: the outcome and the file. Leave hashes, check counts and resource details in the stage files. Rewrite the header fields in place; only the log grows.

## summary.md

The person signs off from this file. The first screen says what they must decide and why; evidence follows.

```markdown
# <id>: <short title>, finished

**Your decision:** <merge, open a pull request, re-scope or continue; plus any open decision or accepted risk that needs their sign-off>
**Open findings / decisions:** <none, or a numbered list with the file holding the evidence>
**Not verified:** <the checks that did not run and why, one line each>

| Requirement (from request or refinement) | Status | Evidence |
| --- | --- | --- |
| criterion 1, short | met / changed by agreement / unmet / unverified | test or check, review-<round>.md |

## Risky areas
<each touched area and how it was covered; "none touched" otherwise>

## How to rerun the checks
<commands from the final implementation file, or a reference to it if unchanged>

## Branch and context
<branch, worktree, commits (short sha and one line each), documentation updated or skipped, missing context files, pull request link after submit>
```

`request.md` preserves the original request/spec. Refinement records material requirements and sourced scope changes; `answers.md` preserves supplied agreements. Pass these through implementation and review rather than passing only a summary. Consumer documentation is updated once in the task worktree after the last code review, then checked against the code. The tracked task log records completed work, verification, limitations and actual branch/delivery status; stage drafts and review iterations stay here. A `finished` state means the run ended, not that its branch merged or deployed. After `submit`, record the pull request link in `state.md` (Next step and log) and add it to `summary.md`; that is the one allowed edit to a finished stage file.

## Stage-boundary evidence

Use existing Git and agent-harness tools: record the checkout/common repository, branch, `HEAD` and tracked/untracked status at start and after each completed stage. Before task-worktree creation this describes the source checkout; afterward it describes the task worktree. If dirty, record a content hash for each changed tracked and relevant untracked file in `checkout.json`, not just filenames; hashes detect a change without copying the person's work into the task folder. Record relevant ignored inputs when the checks depend on them; a clean Git status does not establish database or service state. Keep detailed evidence in local task artifacts rather than bloating state.

For an authorized implementation, verify its reported commits belong to the expected task branch, preserve unrelated files and record its completed HEAD/status. A read-only stage cannot silently change tracked source or HEAD. Review reports name the candidate and actual revision inspected, relevant check environment, temporary effects and cleanup, briefly. Preserve old outputs; label results stale when their scope/version no longer matches. Before and after dispatch, compare with the expected boundary so a concurrent edit is not blessed by overwriting state. The factory's normal review candidate is committed and clean; unexplained dirty files are a discrepancy, not task output.

## Review scheduling

Independent code reading may run in parallel. Before starting mutable checks, identify shared databases, fixtures, service state, ports and files, including temporary tests. Use the project's or agent harness's existing isolation (for example separate test databases, fixture copies, ports and temporary directories), or serialize conflicting checks through the caller. Separate Git worktrees alone do not isolate databases, ports or external services. If independence is unknown, serialize the checks while allowing independent reads to proceed.

Give reviewers the candidate revision, assigned resource arrangement and cleanup responsibility. Keep implementation paused; reviewers do not edit tracked source or change the reviewed branch. Temporary tests must be isolated from other reviewers' discovery or run serially, removed after use and listed in the report. Restore only resources created/changed by that check; do not erase existing user data or stop another session's services. Confirm cleanup before the next conflicting check. If cleanup fails or shared state changed unexpectedly, stop affected checks and report the limit; do not count contaminated or incomplete evidence as passing. Compare HEAD and tracked diff before and after the review batch, and repeat affected reviews if the candidate changed.

## Resume comparison

1. Confirm the saved base and expected checkout belong to the task's repository; verify the registered task branch/worktree when one exists. A task legitimately paused before worktree creation compares its source checkout evidence instead.
2. Compare actual branch, HEAD and relevant status/content with the saved boundary. A matching path or base commit is insufficient. Also re-establish check prerequisites that may drift, such as service state or test inputs, before relying on earlier runtime results.
3. On a mismatch, preserve the expected evidence and unexpected edits, and record observed facts plus which earlier results are now stale. Trace the difference: changed requirements/decisions may need refinement/planning again; code or documentation changes need scope reassessment, implementation verification and fresh review. An independently verifiable, authorized task commit from an interrupted stage may be recovered with fresh checks. An unexplained branch switch, rewrite or user-owned dirty change needs a specific decision before implementation resumes. Do not automatically incorporate it, switch branches, reset, stash or clean it away.
4. For older state missing expected branch, last HEAD or status evidence, mark that evidence unknown. Recover only what immutable stage outputs, task commits and worktree registration establish independently. Inspect the present diff and repeat affected checks/stages to establish a new verified boundary before resuming; if ownership or scope cannot be established, stop for that decision. Saving the current checkout as expected without checking it is not recovery. Keep prior results historical and retain the accumulated fix rounds; if the count cannot be established, ask rather than starting a new allowance.

Repeated review or resume validation does not reset the two-fix-round limit. Status can report stale or missing evidence read-only; it must not repair state or imply that a previous pass covers the current checkout.
