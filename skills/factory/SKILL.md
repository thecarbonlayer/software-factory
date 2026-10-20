---
name: factory
description: Use when starting a software request through Software Factory, resuming a factory task, checking factory task status, or submitting a finished task as a pull request, with start, continue, status or submit.
---

# Factory

You are the orchestrator in the main session. You own stage dispatch, task state and evidence boundaries. Each stage runs separately and loads its skills. Do not delegate orchestration to a stage. Use the [task-folder contract](references/task-folder.md) for artifacts, completion parsing, preflight and recovery.

Commands take free text:

- **start** `<issue link, number or request>`: reserve a task, establish its remote base and worktree, then run until a stop.
- **continue** `[task id] [answers, decisions or notes]`: validate saved evidence, then resume. Omit the id only when one task is open.
- **status** `[task id]`: report saved task state, read-only.
- **submit** `[task id] [notes]`: run `software-factory:submit` on a finished task. A yes to the final submit question has the same effect.

## Boundaries

- **Files are the handoff.** The excluded `.factory/<id>/` contains local working artifacts and raw stage logs. The issue owns shared intent and discussion; the PR owns shared delivery evidence. For an ad hoc request, put necessary intent and accepted scope in the PR. Do not commit a per-task intent, specification or plan directory to the consumer.
- **The source checkout stays unchanged.** Record its boundary, fetch the delivery target and create `factory/<id>` from that remote revision. All stages inspect or edit the task worktree. Do not switch, pull, reset, clean or incorporate unpublished source changes.
- **People decide external actions.** `start` authorizes implementation within the plan's scope. Posting, issue changes, push and PR creation need existing authorization, `submit`, final consent or the consumer's automatic-submit policy. Never merge or deploy. Wider scope needs a decision.

## start

1. Find the main checkout through the common Git directory. Resolve the source identity first: issue host/repository/number, or the ad hoc request identity. Resolve a bare issue number against the intended repository. Search existing tasks, including legacy `gh-<number>` records. A match resumes through **continue**; ambiguous legacy identities need clarification. New issue ids are `gh-<host>-<owner>-<repo>-<number>`, lowercased with unsafe characters replaced by hyphens. Free text uses a stable short slug. Only a caller-requested new run gets a distinct suffix.
2. **Reserve before writing.** Check `.factory/<id>`, `factory/<id>`, registered worktrees and `<root>/../<repo-name>.factory/<id>` for collisions. Preserve any collision; stop for continuation or an explicit new-run id. Create only the parent `.factory/` as needed, then claim the task directory with atomic `mkdir`, without `-p`. Failure permits no writes there. Add `.factory/` to the common repository's local `info/exclude`. Record source branch, HEAD, status and dirty-content hashes in `checkout.json`; these changes are outside task scope.
3. **Resolve the delivery base now.** Discover the intended remote and target from consumer rules, otherwise the remote default branch. Clarify competing targets. Fetch that exact target and record remote name, target branch/ref and fetched SHA in `checkout.json` and `state.md`. Compare source HEAD with it: report source-only ancestors and both sides of divergence. Source-only commits are excluded from the task. If refresh fails or the person intends unpublished commits as the base, stop for that specific decision. Do not silently use the local branch or stale remote ref.
4. Recheck branch, registration and destination collisions. Create the worktree directly from the fetched SHA: `git worktree add -b factory/<id> <root>/../<repo-name>.factory/<id> <fetched target sha>`. Stop on failure, preserving the reservation. Record expected branch, initial HEAD, status and worktree. A source-only local ancestor cannot become the task base implicitly.
5. Discover consumer instructions and context destinations in the task worktree: existing product guide, decision records, tracked task log, setup/check guidance and `REVIEW.md`. Record paths or absence in state. `REVIEW.md` owns consumer review passes, severity meanings, exclusions and noise limits. Apply it without copying policy into task artifacts or AGENTS.md; absence uses factory policy and does not authorize creating one. Build the shared risky-area list: money/billing, access/permissions, rewriting historical records, recorded decisions and consumer must-preserve rules.
6. Write `intent.md`, preserving the original request/spec and sources, issue body and relevant discussion. Record what is wanted, why, affected users/systems, constraints and open questions. Do not retain a duplicate raw issue export. Write initial `state.md`, then run [initial preflight](references/task-folder.md#two-phase-preflight) before the first stage.
7. Run **Stages**, saving output and updating state after each boundary. A reserved task stopped before stages remains resumable; a later `start` never overwrites it.

## Running a stage

A stage is a skill, a prompt and a permission profile. There are no named stage agents.

| Stage | Skills to load | Profile | Runs in |
|---|---|---|---|
| Triage, refinement, planning | `triage`, `refine`, `plan` | read-only | task worktree |
| Acceptance review, documentation check | `review` | checks | task worktree |
| Code, security, UX review | `review` plus `review-code`, `review-security` or `review-ux` | checks | task worktree |
| Implementation, documentation | `implement`, `document` | edit | task worktree |

**Preferred: one CLI call per stage**, using the current harness unless consumer instructions or the person choose another. Name skills at the start of the prompt: `/software-factory:<skill>` in Claude Code, `$software-factory:<skill>` in Codex. Focused reviews name both skills. Require the existing first-line skill declaration, immediately followed by `Stage state: pending` or `Stage state: complete`. Do not pass a model or reasoning effort; the host chooses.

| Profile | Claude Code | Codex |
|---|---|---|
| read-only | `claude -p "<prompt>" --output-format stream-json --verbose --permission-mode dontAsk --disallowedTools Edit,Write,NotebookEdit --allowedTools "<preflighted read operations>"` | `codex exec -C <dir> -s read-only --json -o <output file> -` (prompt on stdin) |
| checks | `claude -p "<prompt>" --output-format stream-json --verbose --permission-mode acceptEdits --allowedTools "<preflighted reads and exact planned checks>" --disallowedTools Edit,Write,NotebookEdit` | `codex exec -C <dir> -s workspace-write --json -o <output file> -` |
| edit | checks profile without its edit-tool prohibition; add scoped edit tools and `Bash(git add *),Bash(git commit *)` to allowed tools | as checks |

Run in the task worktree. Keep temporary commit-message files inside that authorized worktree. Read-only and checks prompts prohibit changes to HEAD or tracked files; checks may create only declared, isolated temporary effects. Add precise commands and readable skill/handoff paths during preflight instead of granting broad shell access. A new worktree may not inherit the source checkout's trust or allow rules.

- **Wait for owned work.** Run long stages in the background when needed. Join stage-owned checks and child jobs. A successful turn with checks running is pending, never a completed stage. Schedule independent reviewers under [review scheduling](references/task-folder.md#review-scheduling).
- **Parse explicit completion.** Follow [stage completion](references/task-folder.md#stage-completion). Claude streams may contain multiple successful results and later watcher messages. Neither the last result nor the longest text determines authority. Codex uses exit status and its final-output file, plus the same state check.
- **Preserve output.** Keep each JSON stream in `logs/<stage-attempt>.jsonl`. Save individual complete reports separately with execution/revision metadata after the first two lines. Pending output is attempt evidence, not a canonical accepted report.
- **Record permissions.** Save executable, profiles, exact flags and fallback choice in state. Consumer-authorized container/VM isolation may permit wider flags; record that authority. A Codex main session needs network access to launch `codex exec`.

**Execution fallback remains available.** If the CLI is absent or cannot start, use a generic subagent (`general-purpose` in Claude Code, `default` in Codex) with the same prompt. It loads named skills before work and observes the same completion contract. Record the launch failure and preflight the fallback. Its profiles are instructions within inherited permissions. Reuse the selected working route for later stages; retry the failed route only after a concrete capability change. This execution choice does not change artifact ownership. If neither route can load skills or perform required work, stop with the specific blocker; do not perform stage work in the main session.

**Check every profile afterwards.** Compare expected branch, HEAD, status and relevant hashes before and after each stage. Unexpected tracked edits or HEAD changes invalidate read-only/checks output. Preserve changes and investigate; do not adopt them by updating the expected boundary.

## Stages

Supply original sources in `intent.md`, current accepted `spec.md` when available, source agreements and the necessary preceding artifacts by reference. Planning onward receives the scope trace, stable `R-001` requirement and `D-001` decision IDs, and authority evidence. IDs remain stable across retries. The original source stays available; later summaries do not replace it. Ask for each skill's documented format in [plain language](references/task-folder.md#plain-language). Save returned output for stages that cannot write files.

1. **Triage** (`triage`, target refinement) → `triage.md`. Stop on inapplicability, dependency blockage or failed investigation.
2. **Refinement** (`refine`) → current `spec.md`, after complete output is checked. Preserve prior attempts in raw logs; the [artifact rules](references/task-folder.md#current-and-historical-artifacts) govern replacement. Keep accepted requirements separate from unanswered proposals. Awaiting answers stops the run: show the clarification comment for the person to post or answer here. `continue` appends supplied answers and their source to `answers.md`, then resumes refinement until ready for planning. Silence never establishes user agreement.
3. **Planning** (`plan`) → current `plan.md`. Map accepted R/D IDs to changes, order, risks, alternatives and proof. Stop for blocking product decisions. Delegated technical choices can proceed with explicit authority. Before implementation, run [planned-command preflight](references/task-folder.md#two-phase-preflight) for exact checks and edit/check profiles. Worktree creation has already happened.
4. **Implementation** (`implement`) → `implementation-<round>.md`. Supply original intent, accepted spec/agreements, plan, only the task worktree as edit scope, and permission to commit on the task branch. Verify reported commits belong to that branch and the worktree is clean. Consumer documentation waits for **Documentation**. Material plan departures update the local plan and must reach the PR. Fix reports identify changed F IDs, commits and new evidence, referencing unchanged facts and giving complete rerun instructions.
5. **Review** → `review-<round>.md` plus separate individual reports. Freeze the committed candidate and pause edits. Acceptance and code review are mandatory on **every changed candidate**. Determine security and UX applicability from the full base-to-candidate diff and consumer review policy:
   - Security: trust boundaries, access control, untrusted inputs, money, secrets or shared-data migrations. A single-user tool reading its own files alone does not qualify.
   - UX: changed visual interface, pages, screens, forms or navigation. Acceptance covers command-line output.
   Carry an applicable earlier security/UX verdict only under the full [focused-review reuse test](references/task-folder.md#focused-review-reuse). Uncertain source, test, config, asset or migration effects require rerun. Record selection reasons, earlier and current revisions, boundary evidence, environment and limits. Filename similarity alone proves nothing.
   Discover and supply consumer `REVIEW.md` by reference. Give all reviewers intent, spec/trace, sourced agreements, implementation rerun instructions, risky areas, candidate and resource arrangements. Allocate shared checks: acceptance owns requirement coverage, code owns general code/test checks, security owns adversarial checks, UX owns real journeys. Reuse adequate current check evidence; rerun missing, stale or focus-insufficient checks. Apply [review scheduling](references/task-folder.md#review-scheduling). Reports identify supported-workflow, API-only or source-inferred triggers. Preserve reviewers' actual inspected revisions and cleanup evidence; reject stale acceptance/code verdicts.
6. **Decide.** Allocate task-wide finding IDs in the main session. Merge and deduplicate reviewer-local findings into stable `F-001` rows with source-report aliases, actions and evidence links. Distinct findings that reviewers both call F-001 receive distinct task IDs; preserve the alias map. Reuse the same F ID for the same finding across rounds. Fix in-scope defects or missing checks first, within two fix rounds, then return to **Review**. Review attempts and resume do not reset the count. Stop for a person when a risky-area finding, missing required check, decision reversal or proposal remains beyond authorized repair. After two fix rounds, unresolved findings need a person's decision. Covered risky areas and delegated technical choices go in the summary without repeated approval.
7. **Documentation** (`document`) → `documentation.md`, once after code review supports the next step. Supply intent, accepted spec/decisions with authority, current plan, implementation and aggregate review. Permit edits and commits only in the task worktree and existing durable documentation owners. Do not turn proposals or silence into user decisions, create missing owners by default, or commit per-task working artifacts. Verify documentation-only commits and clean status.
8. **Documentation check** → `review-<round>-docs.md` plus individual reports. Compare non-documentation tree hashes with the last code-reviewed candidate. If changed, return to **Review**. For a changed documentation candidate, rerun acceptance and code review on that candidate; inspect documentation accuracy and continued requirement coverage, reusing adequate non-documentation check evidence. Apply the focused-review reuse test again. A documentation error gets one documentation repair and recheck; further errors remain open for the person. Documentation repairs do not grant extra implementation fix rounds.
9. **Finish** → `summary.md`, then stop for sign-off unless automatic submit applies. First screen: required decision, open findings/decisions, unverified required behavior and actual outcome. Follow with R-ID coverage, agreed scope changes, risky-area evidence, accepted risks, rerun instructions and branch/context details. Individual stage reports retain detailed history. Finished means the run ended, without implying merge or deployment. Ask whether to submit, re-scope or continue.

## submit

Run `software-factory:submit` in the main session. Validate the task boundary and freshly fetched recorded target as in **continue**. Target drift must be recorded and its effect on the proposed diff and review/check evidence assessed before submission; do not silently reset, rebase or change the target. Supply the remote/ref/base evidence, summary and accessible evidence for a self-contained PR. The submit skill pushes `factory/<id>` and opens a **draft** PR targeting the recorded branch. Record its link in state and summary.

Automatic draft submission requires consumer opt-in, no open findings/decisions, no risky area touched and no required check unverified. Otherwise obtain final consent. Existing explicit submission authorization stays valid.

## continue

Before saving answers or launching a stage, read state and the [resume comparison](references/task-folder.md#resume-comparison). Compare recorded remote target, base, checkout identity, branch, last completed HEAD and status/content evidence with reality. Refresh the recorded target; record drift and reassess scope/diff and affected checks/reviews, without automatically rebasing or switching branches. Preserve unexpected changes, prior expectations and stale results. Recover only an independently established authorized boundary; ownership or scope uncertainty needs a specific decision. Use [legacy migration](references/task-folder.md#legacy-task-migration) for old task names or missing evidence. Preserve fix rounds, stable IDs and authority. If answers do not resolve the saved stop, name the remaining gap and stay stopped.

## status

Report id, title, stage, status, waiting decision, next step, branch and worktree. For several tasks use a table. Report missing/stale evidence read-only; status does not repair or migrate tasks.

## When something fails

Recover proportionately within existing permissions: correct arguments, use an allowed read tool, or use the preflighted execution fallback. Retry only after an identifiable correction or useful new evidence. Record error, recovery and outcome. Repeating the same denied capability across stages is not recovery. New installs, access changes, data writes or wider scope need existing authority or a specific decision.

An unavailable required capability stops the task. A skill's limited fallback, such as static UX assessment, may complete with explicit limits; unexercised required behavior stays unverified and can still block progression. Never count failed or unrun checks as passed. Keep user messages short: outcome, artifact location and next decision.
