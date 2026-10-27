# Durable project context

Use this after implementation and before the candidate is frozen for independent review. Prepare documentation in the same authorized task worktree as the code. For a manual stage, use the caller's authorized checkout. Detailed drafts and review iterations stay in the locally excluded `.factory/<task-id>/` when factory is running, or in the caller's designated local artifacts for a manual stage.

The issue owns shared intent and clarified requirements when one exists, and the PR owns the shared delivery record. Local `intent.md`, `spec.md`, `plan.md`, intermediate reports and raw logs support resume and review. Do not commit per-task copies or task directories to the consumer repository. For ad hoc work without an issue, the PR carries the necessary intent and accepted scope. Existing durable project documents change only where the reviewed work changes knowledge those documents own.

## Discover existing destinations

Find destinations as the document skill describes; do not assume a layout. When recommending names, prefer `README.md`, a root `DECISIONS.md`, and a tracked `TASK_LOG.md` as names to recommend; reuse existing equivalents and their locations and formats. A decisions file or task log elsewhere is an equivalent, not a reason to create a second one. Missing files are reported as context gaps; this convention does not authorize creating them. Respect a narrower edit scope or repository policy and report any updates it prevents.

Discover applicable `REVIEW.md` files. They own review passes, severity meanings, evidence expectations, exclusions and noise limits. Link to that owner from a context index when useful; do not duplicate its policy in `AGENTS.md`, a PR or task artifacts. When none exists, use the factory's review policy without creating `REVIEW.md` unless the authorized consumer change establishes durable review guidance. Report conflicting policies rather than silently rewriting them.

## Reconcile from the job's evidence

Use the original request/spec, refinement and sourced replies, plan, implementation evidence and any still-applicable findings from an earlier fix round. Update only the durable facts supported by these artifacts:

| Existing destination | What belongs there |
| --- | --- |
| README or product guide | Resulting product behavior, usage and relevant limitations. Describe what the change provides; do not imply it has shipped. |
| Decision records | Decisions actually agreed or made within the caller's delegated authority, with their source and rationale. Preserve prior entries. A proposed policy reversal needs explicit owner agreement; record an agreed supersession according to the project's format instead of rewriting history. |
| Tracked task log | Concise branch implementation evidence, known limits and the actual pending review, verification and delivery status. Do not predict later results. Preserve earlier entries; revise this job's entry only when another authorized candidate must be frozen. |
| AGENTS.md | Durable operating instructions and a concise context index, plus how to qualify/test the product. Link to REVIEW.md for review policy. Keep task history and per-run outcomes in the log and local artifacts. |
| REVIEW.md | Required review and verification classes, severity and evidence policy. Link to canonical test guides and any complete role, persona or journey matrix instead of copying commands and identities into policy. |

Ordinary implementation proposes new decision wording rather than changing recorded policy. **Durable-context reconciliation** may record a supported decision only when that documentation edit is in scope and the evidence establishes agreement or delegated decision authority. A recommendation in a plan, silence or a passing test is not agreement. Keep unresolved proposals in task artifacts and report them as open decisions.

Trace each recorded material decision to its stable `D-001` ID and source in the handoff, along with affected R IDs when useful. Preserve authority exactly: **user-agreed** requires an explicit user requirement or agreement; **delegated implementation choice** requires a named delegation and a choice within its limits; **unresolved proposal** remains outside tracked decisions. Do not relabel a delegated choice as user-decided. Use each destination's existing format and accessible sources for durable prose; local `.factory` links cannot serve as shared evidence. Reference the issue, PR, commit, code or a concise observed result with the tested revision and limitation instead. IDs aid traceability without turning the durable document into a copy of the task specification.

## Instruction files and product checks

When an existing `AGENTS.md` needs context or testing guidance and the edit is authorized:

- Add short relative Markdown links to the existing README, decision records, task log and other key context. Say when each is needed, for example before planning, before reversing a policy, or when checking completed work. Link only relevant existing destinations; do not paste their contents or eagerly import them.
- Explain or link to actual product setup prerequisites, commands/scripts and their locations, meaningful manual checks, and known execution limits. Use repository evidence such as scripts, CI configuration, documented setup and checks actually run. Distinguish a discovered command from an executed check. If setup or checks are unknown, report that gap rather than inventing instructions.
- If testing instructions are missing, add a concise section from that verified repository evidence. Preserve existing instructions and more specific child guidance. Keep each `AGENTS.md` and `CLAUDE.md` within 200 lines; move detailed check guidance to an existing suitable document when possible. Report a conflicting policy or an existing oversize file rather than deleting unrelated rules.
- Treat `AGENTS.md` as canonical. An existing `CLAUDE.md` should be a one-line `@AGENTS.md` include once any unique instructions are safely preserved within authorized scope. If consolidation is outside scope, report it; do not overwrite unique content or create missing instruction files.

## Hand off for review

Return the destinations updated or skipped, evidence for recorded decisions, exact checks and their outcomes, and missing or blocked context. Include the documentation diff with the code. Have the documentation diff reviewed against the code and evidence before finishing. A task-log statement such as “implemented on `job/csv`; focused check passed; integration unavailable; awaiting review and delivery” describes branch work without claiming merge or deployment.
