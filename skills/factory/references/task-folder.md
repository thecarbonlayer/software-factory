# Task folder

```text
<main checkout>/.factory/                    excluded via common Git info/exclude
  <id>/
    state.md                                 current state, resume boundary and recent log
    checkout.json                            source, target, task base and worktree evidence
    capabilities.json                        observed runner, permission and environment capabilities
    intent.md                                original sources, motivation and constraints
    spec.md                                  current requirements and decisions with stable R/D IDs
    answers.md                               supplied answers and authority, newest last
    triage.md                                readiness evidence
    plan.md                                  approach, exact commands and R/D-to-proof map
    evidence.md                              append-only check ledger with stable E IDs
    implementation-<round>.md                builder changes and new evidence references
    documentation.md                         durable-context reconciliation
    review-<round>.md                        independent review and stable F IDs
    verification-<round>.md                  independent black-box verification
    summary.md                               local sign-off artifact
    logs/<context-attempt>.jsonl             raw independent-context output
    history/                                 superseded canonical artifacts when needed
<main checkout>/../<repo>.factory/<id>/       separate worktree, branch factory/<id>
```

The issue owns shared intent, discussion and clarification. The PR owns shared delivery evidence. These local files preserve working state and recovery evidence. Do not commit a second per-task intent, specification or plan tree to the consumer. Existing durable documents change only when the implementation changes knowledge they own.

## Artifact ownership

Each fact has one canonical owner:

| Fact | Owner |
| --- | --- |
| Original request and sources | `intent.md` |
| Accepted behavior and authority | `spec.md` |
| Approach, prerequisites and full rerun commands | `plan.md` |
| Observed check result | `evidence.md` |
| Current runner and environment capability | `capabilities.json` |
| Independent findings | `review-<round>.md` |
| Final black-box result | `verification-<round>.md` |

Other artifacts reference the owner by stable IDs rather than copying long instructions or results. Requirements use `R-001`, decisions `D-001`, evidence entries `E-001`, and findings `F-001`. Never reassign an ID. A material decision records authority as **user-agreed**, **delegated implementation choice** or **unresolved proposal**, with its source. Silence is not agreement.

Canonical `spec.md` and `plan.md` may be updated as the task evolves. Archive an earlier canonical copy under `history/` only when it cannot be recovered from version history or raw logs. Round reports are immutable. A retry uses a new attempt or round filename.

## Capability snapshot

Capability discovery happens after task reservation and before expensive work. Record observed facts in `capabilities.json`, for example:

```json
{
  "observed_at": "<timestamp>",
  "builder": {"host": "<host>", "skills_readable": true},
  "independent_context": {"route": "<runner or agent>", "profile": "<flags>", "status": "available"},
  "commands": {"<exact command or family>": {"status": "allowed", "evidence": "<probe>"}},
  "timeout": {"mechanism": "<host-native mechanism>", "status": "available"},
  "constraints": ["<network, service, data or permission limit>"],
  "retry_after": "<environment change, or null>"
}
```

Probe capability, not product correctness. Confirm that the chosen route can start, load required skills, read task handoffs and consumer instructions, and perform baseline read-only Git operations. Inspect consumer-mandated review hooks without triggering unsafe mutations. After planning, probe only newly required exact commands or setup. Do not run a stateful full suite as preflight.

Prefer host-native execution limits and cancellation. Never assume an operating-system utility such as `timeout` exists. A denied command, missing executable or unavailable network is a capability result, not a product test failure. Record it once. Retry only after a concrete change named in `retry_after`.

If the preferred independent route fails, preflight a supported fallback with the same isolation and permissions. A fallback cannot waive a required consumer check or make a review independent if it inherits the builder's private context.

## Evidence ledger

`evidence.md` is append-only. One entry records one observation:

```markdown
## E-001: <short claim>

- Owner: builder | reviewer | verifier
- Candidate: <exact full commit and tree plus dirty-content hash when applicable>
- Tested revision: <candidate commit, or integration commit and proven relationship to candidate and target>
- Execution source: local | <remote provider, workflow and run id/url>
- Command or method: `<exact command or remote job>`
- Matrix: <complete dimensions, selected row, or not applicable>
- Environment: <relevant versions, fixtures, services, roles and isolation>
- Result: passed | failed | not run | blocked
- Observed: <concise output or artifact link>
- Limits: <what this does not prove>
- Time: <timestamp>
```

Never rewrite a failed or stale result into a pass. Append a new entry and mark the relationship. A result applies only to its candidate and tested tree, workflow or command, complete matrix, relevant inputs and environment. A branch name, pull request number or earlier green run is not a candidate identity. A remote integration commit is valid only when event metadata or commit relationships prove that it contains the candidate and recorded target. Raw output may live in `logs/`, remote checks or consumer test artifacts; the evidence entry points to it.

`plan.md` remains the single owner of complete rerun commands, prerequisites, resource effects and expected outputs. Implementation, review and verification reports cite the plan and E IDs. They add full commands only when the plan proved wrong and must be updated.

## Builder checkpoints

The persistent builder updates `state.md` at meaningful boundaries: reservation, refinement stop, plan approval, candidate freeze, review result, verification result and finish. It does not manufacture separate agent-style completion reports for its internal stage transitions.

Before each checkpoint, record expected branch, HEAD, status and relevant resource state. A clean Git status does not prove databases, services, fixtures or ignored inputs are unchanged. Preserve unexpected state and investigate it. Never adopt a discrepancy by updating the expected boundary.

An implementation round report contains changed R/D/F IDs, base and candidate commits, changed files at a useful level, new E IDs, deviations and remaining risks. A fix report references unchanged evidence. It does not repeat the entire request, plan or command list.

Documentation runs in the builder before candidate freeze. Its report names files updated, files checked and left unchanged, decisions recorded with authority, missing destinations, verification and commit. The independent reviewer then reviews code and documentation together.

## Independent context completion

Review and verification reports start with their skill declaration, followed immediately by the state line:

```text
I'm using the review and review-code skills.
Stage state: complete

Candidate: <full hash>
<report>
```

`Stage state: pending` means owned checks or child work still run. Keep the same context and join that work. `Stage state: complete` means all owned work is joined and the named candidate is final for that context. A complete report can still conclude blocked or not assessable.

For a non-interactive runner, require exit zero, exactly one distinct complete report, expected skill declaration, expected candidate and no unexplained tracked mutation. A later watcher message or the longest payload is not authoritative. Conflicting complete reports require reconciliation. Preserve raw output in `logs/`.

## Independent review

The reviewer receives evidence, not the builder's private reasoning. It independently reads the base-to-candidate diff, surrounding code, tests and documentation. By default one context loads `review` and `review-code`; it loads security and UX focus skills in that same context when applicable.

The report owns:

- decision: **supports next step**, **blocks next step** or **not assessable**;
- actual base and candidate inspected;
- consumer policy followed;
- stable findings with severity, trigger, impact, location and evidence;
- requirement, decision and risky-area coverage;
- evidence reused or newly produced, with limits;
- cleanup and the next action.

Review may run a targeted check to establish a finding. It does not need to rerun the whole consumer suite when the verifier will own it. It must not call an unrun workflow passed.

The same reviewer context may check a scoped fix only when requirements, risk classification and affected surface remain bounded. Use a new full review after material scope, architecture, risk or diff expansion. Record why a context was reused or replaced.

## Independent verification

The verifier starts from the frozen candidate and consumer-owned instructions. It discovers required suites from `REVIEW.md`, test guides, configured remote checks and project instructions. If the consumer defines supported roles, personas or journeys, treat that declared matrix as the verification scope. The plugin never supplies product-specific identities or workflow names.

Select one authoritative full-suite route for each candidate. When configured remote checks cover the full matrix, publish the reviewed candidate as a draft only with authorization, then consume results bound to the candidate head or a proven integration revision containing it. Do not also run the same full matrix locally against an equivalent tree. When no suitable remote checks exist, run the complete documented local suite once. When only manual checks exist, record them. When no valid route exists, keep the affected behavior unverified instead of creating CI or tests without authorization.

For remote evidence, record provider, workflow revision, event, run identifier or URL, candidate head SHA and tree, exact tested SHA and tree, target SHA, their proven relationship, expected jobs, matrix and conclusions. Missing, skipped, cancelled, pending or unrelated-revision jobs do not pass. Read summary results first and inspect only failure artifacts needed for diagnosis.

Before mutable local checks, identify databases, fixtures, services, ports and files. Use existing isolation or serialize conflicts. Never target protected or production data. Temporary tests and services must be removed or stopped by their owner. A failed cleanup limits the result.

Verification owns the complete required matrix and records every result in `evidence.md`. A report distinguishes:

- product failure: the candidate violates expected behavior;
- runner failure: the host could not execute an otherwise required check;
- environment failure: prerequisites or isolation were unavailable;
- unverified behavior: no valid observation exists.

Only a product failure becomes an implementation finding automatically. Other failures may still block delivery, but they do not prove a code defect. Draft publication may precede remote verification; it never converts pending or missing checks into a pass.

## Target drift and parallel branches

Worktrees isolate files but do not synchronize branches. Refresh the recorded target at candidate freeze, before draft publication and before final delivery or queue entry. Classify target movement:

| Class | Meaning | Default response |
| --- | --- | --- |
| unchanged | target SHA matches | continue |
| conflict-free | target advanced without a dependency or known semantic overlap | preserve the task base; let a configured merge queue or equivalent validate the combined revision |
| semantic overlap | Git may merge, but target changes affect assumptions or behavior | require combined-revision evidence; use the queue or an authorized branch update, then repeat affected review and verification |
| conflict | source changes cannot combine cleanly | resolve only in the task worktree under the consumer's update policy; never silently rebase |
| dependency | this task relies on another unmerged task | use the consumer's stacked-PR convention or serialize delivery |

A merge-queue or integration-group SHA differs from the task candidate. Required checks on that combined SHA are new integration evidence, not a duplicate same-candidate run. Without a queue, follow the consumer's documented merge, rebase or retarget policy. Missing policy or unclear ownership needs a decision.

## Resume comparison

Before continuing:

1. confirm source identity, common repository, worktree, branch, immutable base and recorded delivery target;
2. refresh the target and classify drift without rebasing;
3. compare actual HEAD, status, relevant content hashes, capabilities and check prerequisites with the expected boundary;
4. compare any remote evidence by candidate and tested tree relationship, workflow and complete matrix;
5. trace differences to affected requirements, plans, evidence, review or verification;
6. preserve unexpected changes and request a decision when ownership is unclear.

Missing evidence stays unknown until recovered from immutable commits, reports and logs. Do not switch, stash, reset, clean or incorporate changes automatically. Legacy tasks may map older artifacts into the current owners, but migration must preserve original sources, authority, accumulated fix rounds and stale limits.

## state.md

Keep the header current and the log short:

```markdown
# <id>: <title>

- Status: running | waiting for external checks | waiting for a person | finished | failed
- Waiting for: <specific answer or decision, or none>
- Next step: <action>
- Stage / fix rounds used: <stage> / <0..2>
- Source: <issue URL or ad hoc identity>
- Branch / worktree: <branch and path>
- Base / candidate: <full SHAs>
- Delivery target: <remote, ref, fetched SHA and time>
- Expected boundary: <HEAD, status and resource evidence>
- Capabilities: <capabilities.json and changed facts>
- Evidence boundary: <latest applicable E IDs>
- Review / verification: <reports, exact SHAs, execution owners, workflows/matrices and verdicts>
- Draft PR / remote checks: <link and pending/completed jobs, or none>
- Risky areas: <classification>

## Recent log
- <time> <boundary>: <outcome and artifact>
```

## summary.md

The first screen contains the decision, open items, unverified required behavior and actual outcome. Then map every material requirement to its status and evidence ID. Include risky areas, accepted risks, decision authority, branch/base/candidate, target drift, documentation status and the `plan.md` rerun reference. Finished means the run ended. It does not imply submission, merge or deployment.

The local summary may reference local artifacts. A PR must translate them into accessible issue, commit, code, test or CI references, or concise observed results with revision and limits.
