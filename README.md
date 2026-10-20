# Software Factory

Software Factory is a reusable set of stage skills for taking software work from an unclear request to a reviewed change. It gives each step a clear purpose: understand what is needed, agree on the behavior, plan the change, implement it and check the result.

The goal is to use these pieces on real work, observe where they fall short and improve them iteratively. Start with one issue and the stage it needs. You do not need to adopt a new development platform or run every stage for every change.

## What lives here

This repository is the **Software Factory plugin**. It is listed in the [thecarbonlayer marketplace](https://github.com/thecarbonlayer/plugins), the catalog through which a host discovers installable plugins. The plugin contains nine stage skills, a submit skill and an orchestrator skill. Your own project is the **consumer**: it supplies the request, code, project rules and access to relevant discussion.

```mermaid
flowchart LR
    M["thecarbonlayer marketplace"] -->|lists| P["This repository: Software Factory plugin"]
    P --> S["Stage skills: role, method and output guidance"]
    S --> H["Claude Code or Codex session"]
    C["Your project: request, code and rules"] --> H
```

A **stage** is a step in the flow, such as triage or review. Each stage loads a **skill**: its role and boundaries, then the reusable procedure and output guidance. Stage reports name the loaded skills first, then declare `Stage state: pending` or `Stage state: complete`. Pending checks keep the same stage open. A focused review loads two. The same skills run in Claude Code and Codex. There are no agent definitions to install or copy. Models inherit the environment's choice.

The host runs the stages and enforces permissions. This plugin supplies the working methods, an explicitly triggered orchestration skill and a submit skill that opens a draft pull request when the person (or the consumer's own instructions) allows it; it does not start jobs on its own, watch issue replies, merge or deploy changes.

## Follow one request

Suppose a user reports: “Saving my notification preference does not stick.” Triage first checks the discussion and current code: is this still a bug, what evidence exists, and what prevents the next step?

If the desired behavior is unclear, refinement asks only the questions that matter—for example, whether the preference should apply across devices. It drafts **one comment containing the necessary questions**. A person or separately authorized host workflow can post it. When replies arrive, you supply them to a resumed refinement session, which produces requirements and acceptance criteria without guessing unanswered decisions.

Planning turns those agreed requirements into a scoped technical approach. Once the edit is authorized, implementation makes the change and checks its observable behavior. Review compares the final changed version with the acceptance criteria and identifies defects or remaining verification gaps.

```mermaid
flowchart TD
    R["Request and current evidence"] --> T["Triage: assess readiness"]
    T -->|proceed when prerequisites allow| F["Refinement: clarify desired behavior"]
    F --> Q{"Necessary answers missing?"}
    Q -->|yes| D["Draft one clarification comment"]
    D --> H["Authorized delivery; human replies"]
    H -->|caller supplies replies and resumes| F
    Q -->|no| P["Planning: technical approach and checks"]
    P --> G["Human gate: resolve decisions and authorize scope"]
    G --> I["Implementation: change and verify behavior"]
    I --> V["Review: inspect final diff and acceptance evidence"]
    V -->|changes needed within authorized scope| I
    V -->|ready for next step| O["Document: update existing docs, then check them"]
    O --> N["Human decision: submit a draft pull request?"]
```

The arrows describe stage handoffs: you can control them individually or use the `factory` skill below to sequence them. Stop the review-and-fix loop after two fix rounds: if findings remain, a person decides whether to accept, re-scope or continue. A blocked stage returns its specific gap. Existing authorization remains valid; the human gate is a decision boundary, not a mandatory repeated approval prompt. Larger or riskier plans need an approach review before implementation. Merge, publication and deployment remain separately authorized actions outside this flow.

For a small fix, refinement may need no questions and planning may be a few sentences. A large feature may need an interactive developer conversation before asynchronous refinement can finish. Pass along existing decisions instead of making each stage rediscover them.

## What each stage needs and returns

All stages accept ordinary text, links and files. Include relevant discussion, current repository context and project rules. There is no required input schema.

| Stage | Question it answers | Useful input | Output to carry forward |
| --- | --- | --- | --- |
| **Triage** | Is this ready for the named next stage? | Request, discussion, current evidence and target stage | Readiness, cited rationale, missing information, decisions and dependencies |
| **Refine** | What should users experience? | Triaged request, code context and any replies | One clarification-comment draft, or structured requirements with acceptance criteria and open decisions |
| **Plan** | How should we make and verify the change? | Refined requirements, constraints and current code | Scoped technical approach, dependencies, risks and verification plan |
| **Implement** | Does the authorized change deliver that behavior? | Agreed criteria, appropriate plan and edit scope | Reviewable changes, check results and remaining risks |
| **Review** | Does this final version meet the agreement? | Requirements, final diff and verification evidence | Actionable findings, acceptance assessment and limits |
| **Document** | Do the project's docs match the reviewed change? | Requirements, decisions, final code and review results | Updated existing docs, files left unchanged, missing destinations |
| **Submit** | Is the branch ready for people to review as a pull request? | Finished, reviewed branch and summary; the person's approval | Pushed branch and a draft pull request link |

Triage defaults to assessing readiness for **pilot implementation** when no stage is specified. Name another stage when that is the decision you need. A failed investigation is reported separately from a request that is not ready.

Triage names missing decisions; refinement owns the questions, so users are asked once. Refinement starts from triage's evidence, asks through one [clarification comment](skills/refine/references/clarification-comment.md) with concrete examples and proposed answers, and separates factual code evidence from desired behavior. Its [requirements template](skills/refine/references/refinement-comment.md) covers scope, constraints, success criteria, completion measurement, appropriate checks and unresolved decisions.

Implementation uses proportionate **red-green-refactor** checks: demonstrate the behavioral failure, make it pass, then improve the changed code while preserving behavior. Tests should exercise workflows or observable contracts rather than mirror private implementation details. Review distinguishes passed, failed and unrun checks, and ties its conclusion to the final version it actually inspected. Every changed candidate gets independent acceptance and code review. Security and UX reviews run when applicable, with UX exercising the app as each role. Each focused reviewer loads `review` plus its focus skill. Security or UX evidence may carry forward only when requirements, risks, relevant content, environment and limits remain unchanged, with no unresolved focused finding. The aggregate names the earlier revision and the boundary evidence. Uncertain boundaries require a fresh review. Reviewers use the consumer’s applicable `REVIEW.md` for review passes, severity, exclusions and noise limits. Acceptance owns requirement coverage, code review owns general code and test verification, security owns adversarial checks, and UX owns user journeys. Shared suites rerun when their evidence is missing, stale or insufficient for that focus.

## Keep consumer context current

After the last code review, the documentation stage [reconciles existing durable context](skills/document/references/durable-context.md) from the request, agreed requirements, decisions, implementation, verification and review results. It finds the project's documentation without assuming a layout, prepares the updates in the task worktree, and the acceptance reviewer checks the documentation diff:

| Existing consumer file | Update |
| --- | --- |
| README or product guide | Resulting behavior, usage and limitations |
| Root DECISIONS.md or existing decision records | Supported decisions and rationale, with agreement/authority evidence and preserved history |
| Tracked TASK_LOG.md or existing equivalent | Completed work, verification, limitations and actual branch/delivery status |
| AGENTS.md | A concise context index saying when to read relevant files, plus actual setup prerequisites, check commands/scripts and locations, manual checks and execution limits, or links to that guidance |

These are recommended destinations, not mandatory new files. Reuse the consumer's existing equivalents and formats. Report absent destinations or blocked edits without creating files by default. Preserve existing instructions; AGENTS.md is canonical and an existing CLAUDE.md uses a one-line `@AGENTS.md` include once unique instructions are safely preserved within scope. Keep both concise and within 200 lines. Use relative Markdown context links instead of eager imports of every document.

Unresolved decision proposals stay in task artifacts. Reconciliation records only decisions already agreed or made within delegated authority; it does not turn a plan recommendation into permission to reverse policy. The issue holds the original discussion and clarified requirements; the PR holds the shared delivery record. Ad hoc work puts necessary intent and accepted scope in the PR. Local `intent.md`, `spec.md`, `plan.md`, stage drafts and review iterations remain in the excluded `.factory/<task-id>/`. Do not commit a second per-task record to the consumer repository. Requirements, decisions and findings keep stable `R-001`, `D-001` and `F-001` IDs. Decision authority distinguishes user agreement, delegated implementation choices and unresolved proposals. A completed run may still await review or delivery; the tracked task log must not imply a merge or deployment that did not happen.

Refinement traces each material original request/spec item to an agreed criterion, a sourced scope change or an unresolved gap. Planning, implementation and review receive that trace and the original sources. Acceptance review checks both the original request/spec and the refined agreed criteria on the final code and documentation, distinguishing agreed changes from unmet or unverified items.

## Install in your host

Add the [thecarbonlayer marketplace](https://github.com/thecarbonlayer/plugins), then install the plugin from it.

### Claude Code

```text
/plugin marketplace add thecarbonlayer/plugins
/plugin install software-factory@thecarbonlayer
```

Check that the `software-factory:` skills appear, for example `/software-factory:factory`.

### Codex

```bash
codex plugin marketplace add thecarbonlayer/plugins
codex plugin add software-factory@thecarbonlayer
codex plugin list --json
```

This installs the skills; nothing else is needed. 

## Run the stages automatically

The `factory` skill runs the whole sequence from the main session, which owns stage dispatch and task state. In Claude Code:

```text
/software-factory:factory start <issue link, number or request>
/software-factory:factory continue [task id] [answers or decisions]
/software-factory:factory status [task id]
/software-factory:factory submit [task id]
```

In Codex, mention `$software-factory:factory` with the same commands, for example `$software-factory:factory start <issue>`.

For a new task, it fetches the intended remote target and creates a separate `factory/<task id>` worktree directly from that revision before the first stage. It reports local commits outside the target and leaves the source checkout unchanged. A failed refresh or a request to include unpublished local commits needs a specific decision. Resume and submission compare the recorded target and task boundaries; target drift does not authorize an automatic rebase.

The first preflight checks the selected runner, required skills and references, read-only Git operations and any required consumer pre-commit review. Planning chooses the exact verification commands. A second preflight checks those commands and the checks/edit profiles before implementation. The task records and reuses the working executable, profile and fallback. An unchanged launch failure does not get retried across stages.

Each stage runs separately and loads its skill by name. The preferred way is one CLI call per stage (`claude -p` in Claude Code, `codex exec` in Codex) with a permission profile: read-only, checks or edit. If the CLI cannot start, the factory tries a generic subagent with the same prompt and records the fallback. The [factory skill](skills/factory/SKILL.md#running-a-stage) has the commands and report-state rules. Claude streams advance only on one explicit complete report, regardless of later watcher messages; conflicting complete reports require recovery. Codex requires a successful exit and a complete final-output file.

The excluded `.factory/<task id>/` holds current `intent.md`, accepted `spec.md`, an ID-based `plan.md`, short state and immutable stage attempts. Individual reviews stay separate from the aggregate decision and finding table. Fix reports describe changed finding IDs and new evidence, with complete rerun instructions. The final summary preserves requirement coverage, verification gaps and sign-off evidence. [Legacy migration](skills/factory/references/task-folder.md#legacy-task-migration) preserves old request/refinement files, decision sources, checkout evidence and accumulated fix rounds.

`start` preserves existing tasks and reserves a new identity before writing artifacts. It authorizes implementation within the plan’s scope. Independent checks can run in parallel; checks sharing mutable resources are isolated or serialized. `continue` compares saved branch, commit, worktree and check-environment evidence before resuming. It preserves unexpected changes and marks affected results stale.

At sign-off, the factory asks whether to submit unless submission is already authorized or the consumer permits automatic draft PRs under the skill’s conditions. It fixes within two rounds, reconciles existing durable documentation and stops for unresolved decisions or required verification gaps. It never merges. The draft PR explains why and what changed, puts exceptional reviewer concerns next, outlines the change, and gives verification on the submitted revision. A final acceptance-evidence and rerun section preserves the details, collapsible where supported. Consumer PR templates take precedence. Remote evidence uses issue, commit, code, test or CI references, or a concise observed result with its tested revision and limits; local task paths cannot serve as PR evidence.

## Try a stage, then hand off

Start in your consumer project with one request. Name the stage skill at the start of the prompt: `/software-factory:triage` in Claude Code, `$software-factory:triage` in Codex.

> /software-factory:triage Assess this issue for pilot implementation. Check current code and the latest discussion. Return readiness, evidence and gaps here.

To keep the stage's context separate from your session, run it as its own call, for example `claude -p "/software-factory:triage …"` or `codex exec -s read-only "$software-factory:triage …"`.

For a clarification round, use `refine`:

> Refine this triaged request. Batch only necessary unanswered questions into one proposed GitHub comment. Return the draft here.

After collecting replies:

> Resume refinement with this earlier draft and these replies. Produce the structured refinement comment; keep unanswered decisions visible.

Use the matching skill for the remaining handoffs:

- **Planning (`plan`):** “Plan the smallest sound change for these agreed requirements. Include scoped changes, risks and verification.”
- **Implementation (`implement`):** “Implement this agreed plan within the following authorized edit scope. Verify the acceptance criteria and report the actual check results.”
- **Review (`review`):** “Review this final diff against these acceptance criteria. Report actionable findings and distinguish verified behavior from unrun checks.”
- **Documentation (`document`):** “Update this project's existing documentation for this reviewed change. Report files updated, files left unchanged and missing destinations.”
- **Focused review:** run `review` together with `review-security`, `review-ux` or `review-code` on the same version with the same input, then combine their findings.

Advisory stages draft comments for the caller. Posting them, changing tracker state or sending messages requires authorization and host delivery capabilities.

## Find the reusable pieces

Skills use the `software-factory:` namespace:

| Stage | Skills |
| --- | --- |
| Triage | [triage](skills/triage/SKILL.md) |
| Refinement | [refine](skills/refine/SKILL.md) |
| Planning | [plan](skills/plan/SKILL.md) |
| Implementation | [implement](skills/implement/SKILL.md) |
| Documentation | [document](skills/document/SKILL.md) |
| Acceptance review | [review](skills/review/SKILL.md) |
| Security review | review + [review-security](skills/review-security/SKILL.md) |
| UX review | review + [review-ux](skills/review-ux/SKILL.md) |
| Code review | review + [review-code](skills/review-code/SKILL.md) |
| Main session only | [submit](skills/submit/SKILL.md), [factory](skills/factory/SKILL.md) |


```text
plugin.json                          Portable metadata
.claude-plugin/plugin.json           Claude metadata
skills/*/SKILL.md                    Stage skills: role, method and output
skills/refine/
  references/clarification-comment.md  Refinement question format
  references/refinement-comment.md   Refinement output template
skills/factory/                      Orchestration skill (start, continue, status, submit)
  references/task-folder.md          Task folder layout and state format
```

The repository root is the plugin; the marketplace catalogs live in [thecarbonlayer/plugins](https://github.com/thecarbonlayer/plugins). Contributor guidance and authoring references live in [AGENTS.md](AGENTS.md); [CLAUDE.md](CLAUDE.md) imports that same guidance.


## Qualify the plugin

This repository contains instructions and packaging, not a runnable consumer product. From the repository root, with Claude Code on PATH, validate the plugin:

```bash
claude plugin validate .
```

Validation can pass with metadata warnings. Read the exit status and warnings; validation does not prove native stage execution or behavioral quality. For a syntax smoke check:

```bash
python3 - <<'PY'
import json
from pathlib import Path
for path in Path('.').rglob('*.json'):
    json.loads(path.read_text())
print('JSON parsed')
PY
git diff --check
```

Manually check changed skill links and native skill references. Use the host installation steps above for loading checks, and exercise changed guidance on a scoped real task or isolated scenario for behavioral evidence. For context reconciliation, inspect the documentation diff and task-log delivery status as well as code; review any dropped original requirement explicitly. Keep drafts and evaluation artifacts local. Record which agent harness, version and checks were used, and distinguish a simulation or supplied skill text from native plugin execution. 

## Standards and authoring practices

We use the [Agent Plugins standard](https://agent-plugins.org/specification) for portable packaging and the [Agent Skills specification](https://agentskills.io/specification) and authoring practices for shared methods. This package ships only skills, the portable core. Stage dispatch uses each host's documented non-interactive CLI ([Claude Code](https://code.claude.com/docs/en/headless), [Codex](https://learn.chatgpt.com/docs/non-interactive-mode)) and generic subagents ([Claude Code](https://code.claude.com/docs/en/sub-agents), [Codex](https://learn.chatgpt.com/docs/agent-configuration/subagents)) as the fallback. Format compliance alone does not establish runtime compatibility.

We follow the official instruction guidance from [OpenAI](https://developers.openai.com/codex/guides/agents-md) and [Anthropic](https://code.claude.com/docs/en/memory): open each skill with role and judgment, then give the procedure, load supporting detail when needed and keep checks proportional to the work. These choices make the baseline easier to use and revise as real tasks reveal what needs improvement.
