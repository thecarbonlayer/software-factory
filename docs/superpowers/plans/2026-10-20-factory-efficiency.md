# Factory efficiency implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Reduce repeated factory work while retaining independent review, safe task recovery and complete delivery evidence.

**Architecture:** Update the existing instruction contracts. The orchestrator owns checkout, execution and review boundaries. Local task artifacts own resume evidence; the issue and PR own the shared task record. No new runner or validation framework.

**Tech Stack:** Markdown skills and references, JSON plugin metadata, existing Git and host CLIs.

**Spec:** ../specs/2026-10-20-factory-efficiency-design.md

## Global constraints

- Work only in this isolated worktree. Preserve the user's source checkout.
- No model or reasoning-effort pinning, new services, harness-specific agents or consumer-specific examples.
- Preserve CLI-to-generic-subagent execution fallback and all authorization boundaries.
- Acceptance and code review remain mandatory on each changed candidate.
- Local `.factory/<id>/` working artifacts remain excluded. Issue and PR are the only shared task artifacts.
- Use `Stage state: pending` or `Stage state: complete` after the existing first-line skill declaration. Pending never advances a stage.
- Requirements use stable `R-001` IDs, decisions `D-001`, findings `F-001`. Preserve IDs and explicit authority across retries and migration.
- Keep version `0.7.0` until implementation, evaluations and full-diff review finish; then bump both manifests once.
- User explicitly requested this plan as a deliverable and authorized execution, commit, push and a separate draft PR.

## Review focus

- A remote target moves after task creation: record drift and reassess the submitted diff without resetting or rebasing automatically.
- A completed stream is followed by a watcher message: select completion by explicit state, reject conflicting complete reports.
- Asset or documentation edits affect security or UX indirectly: uncertain focus boundaries must rerun, regardless of filename.
- A legacy task has conflicting refinement attempts or missing checkout evidence: preserve history and ask only for unresolved authority or scope.
- A local summary contains inaccessible evidence or an inferred decision: translate evidence for the PR and preserve delegated versus user-agreed authority.

## Task 1: Orchestration and local task contract

**Files:** `skills/factory/SKILL.md`, `skills/factory/references/task-folder.md`; add focused reference files only if needed for clarity.

**Interfaces:** Produces remote target/ref/revision evidence, two-phase preflight, explicit stage completion, canonical intent/spec/plan, review evidence boundaries and migration rules. Tasks 2 and 3 consume these names.

- [x] Read existing stage dispatch, worktree, resume and review rules; identify contradictions against the approved design before editing.
- [x] Move worktree creation before stage work, directly from the freshly fetched target. Preserve source dirty-content evidence and report unrelated local ancestors. Record target remote, ref and SHA.
- [x] Specify first preflight for executable/profile/skills/references/Git/required consumer review; second for exact planned checks/edit profiles. Reuse chosen fallback and avoid unchanged launch retries.
- [x] Add explicit pending/complete parsing for Claude streams and Codex final output, including conflicts, missing reports and running child jobs.
- [x] Carry forward focused reviews only with requirement/risk, relevant-content, environment/limits and resolved-finding evidence. Keep acceptance/code mandatory, check ownership and resource isolation.
- [x] Replace request/refinement artifact guidance with current intent/spec, stable IDs, authority and separate individual review reports. Preserve historical attempts and fix-round count during legacy migration.
- [x] Check consistency with Tasks 2/3 contracts. Supply changed files and specific verification evidence; do not bump or commit.

## Task 2: Progressive stage artifacts and durable decisions

**Files:** `skills/refine/SKILL.md`, `skills/refine/references/refinement-comment.md`, `skills/plan/SKILL.md`, `skills/implement/SKILL.md`, `skills/document/SKILL.md`, `skills/document/references/durable-context.md`; clarification template only if required.

**Interfaces:** Consumes intent/spec/plan names, stable ID formats and stage-state line from global constraints. Produces requirements with authority, ID-based plans and delta fix reports. Does not own orchestration or task-folder schema.

- [x] Inspect existing outputs and locate duplicated facts and decision authority gaps.
- [x] Make refinement preserve original-source coverage using stable requirement/decision IDs and explicit user-agreed, delegated implementation choice or unresolved proposal authority. Silence cannot establish agreement.
- [x] Make plans reference accepted IDs with affected files, order, risks, alternatives and proof, without repeating the specification.
- [x] Make implementation fix reports identify changed findings, commits, new checks and complete rerun instructions; retain unchanged evidence by reference.
- [x] Ensure document reconciliation uses only durable existing owners. Prohibit committed per-task intent/spec/plan copies and inferred user decisions. Discover REVIEW.md as review-policy owner without duplicating it into AGENTS.md.
- [x] Keep standalone stage use viable and apply the explicit state line to stage outputs without imposing factory-only inputs.
- [x] Supply changed files and specific checks; do not bump or commit.

## Task 3: Review and reviewer-first submission

**Files:** `skills/review/SKILL.md`, `skills/submit/SKILL.md`; focused review skills only for a demonstrated gap.

**Interfaces:** Consumes stable R/D/F IDs, explicit stage-state line, focused-review reuse boundaries, remote target evidence and separate reviewer reports.

- [x] Discover applicable consumer REVIEW.md and honor passes, severity, exclusions and noise limits. Preserve mandatory independent acceptance/code review and report policy conflicts.
- [x] Lead reports with supports next step, blocks next step or not assessable, then ID-based findings, changed coverage, owned checks and limits. Findings distinguish supported workflow, API-only or source-inferred reachability.
- [x] Assign check ownership and reuse valid shared-suite evidence. Never claim an earlier focused report inspected a new revision.
- [x] Make submission compare the saved target and reviewed branch, report target drift and never silently rebase. Preserve authorization and existing consumer template precedence.
- [x] Define reason-first PR order: why/change, exceptional reviewer attention, outline, submitted-revision verification, collapsible acceptance and complete rerun evidence. Translate local references into accessible issue/commit/code/test/CI evidence.
- [x] For issue-backed work link the issue; for ad hoc work include accepted scope in the PR. Prohibit publishing local task directories. Supply checks; do not bump or commit.

## Task 4: Integration, evaluation and publication

**Files:** `README.md`, both plugin manifests; this plan's checkboxes. Scenario artifacts and raw reports remain excluded.

- [x] Reconcile README with early worktree creation, preflight, stage states, focus reuse, local artifacts/migration, REVIEW.md and PR presentation. Inspect cross-file links and output contracts.
- [x] Run fresh-agent scenarios with checks specified before dispatch: remote-ahead local branch; unavailable runner capability; pending/complete/watcher/conflicting stream; asset/docs focus reuse; self-contained PR; silence provenance; issue-only shared record; consumer REVIEW.md. Use isolated temporary Git fixtures when commands can prove behavior. Record simulation limits and host.
- [x] Compare revised reports with old template expectations: retain scope, revision, checks, limits and next step while removing duplicated narratives. If audited source logs are unavailable, say so and avoid a measured reduction claim.
- [x] Run `claude plugin validate .`, parse both JSON manifests, check changed local Markdown links and run `git diff --check`. Read each exit status and report warnings separately.
- [x] Obtain independent full-diff review against design and scenario evidence. Verify findings and fix confirmed gaps, then perform scoped re-review.
- [x] After intended changes and evaluations complete, bump both manifests once to the next compatible minor version. Rerun packaging and diff checks on final content, scrub publication artifacts and verify remote visibility.
- [ ] Commit with harness, behavioral checks and limits in the message. Push this branch and open a separate draft PR with concise evidence. Report version, PR and limits to parent session; do not merge.

## Execution record

- Plan self-review: all eight verification scenarios and six design sections have owning tasks. Tasks 1–3 have disjoint file ownership and may run in parallel; Task 4 joins them.
- Authority: the dispatched request explicitly authorizes implementation and publication after evaluation. No repeat plan approval is required.

- Implementation complete: Tasks 1–3 and integration passed independent full-diff review with no actionable findings.
- Qualification: fresh Codex supplied-skill scenarios covered all eight prespecified groups. The remote-base scenario used an actual isolated Git fixture. Other scenarios used controlled inputs, generated outputs and a synthetic completion selector.
- Packaging and relative links passed. Native Claude stage execution was attempted but blocked before execution by an expired OAuth session; no unchanged retry or account change was made. Native Codex installed-plugin execution remains unverified.
- Limits: no production replay, overall token/cost reduction or elapsed-time improvement is claimed. The changed skill instructions grew; output compactness was demonstrated only on synthetic reports.
- Release preparation: both manifests move once from 0.7.0 to 0.8.0 after evaluations and independent review. Final delivery evidence and submitted revision will be recorded in the draft PR.
- Publication hygiene: consumer identity is generalized in the public design. Original design history will be preserved on a local archive branch before publishing one reviewed commit.
