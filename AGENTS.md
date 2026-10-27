# Working notes

## Context index

- [README](README.md): read for product behavior, installation, consumer context conventions and runtime evidence before changing the plugin.
- [Self-hosting](docs/self-hosting.md): read before developing Software Factory with its own released skills.
- [Review policy](REVIEW.md): required review, deterministic PR verification and local behavioral-qualification ownership.
- [Qualification](README.md#qualify-the-plugin): read before verification; prerequisites, commands, manual checks and execution limits.
- [Durable-context procedure](skills/document/references/durable-context.md): read when changing consumer documentation or instruction guidance.
- [Task artifacts](skills/factory/references/task-folder.md): read when changing factory handoffs or resume state.

## How we know a change helped

- Test a stage change by running it on one real task, ideally a replay: a shipped issue at the revision before its spec, scored against what actually shipped.
- Write the checks before the run. Mark anything added after it as post-hoc.
- Record the result in the commit message: what was run, which harness, the checks that held or missed, and the limits. One run is a likely improvement, not proof.
- A passing `plugin validate` proves packaging, not that a harness runs the stage.
- Do not build test harnesses, validators or expected-answer machinery for the plugin without a concrete product need.

## Self-hosting

- Use the installed stable `software-factory:factory` skill for non-trivial work on this repository. The released plugin operates the task; the edited checkout is the candidate.
- Never replace the running task's instructions with candidate skills. Load the candidate only in fresh evaluation sessions that are explicitly testing it.
- Keep `.factory/` task artifacts local and ignored. Follow [REVIEW.md](REVIEW.md) for independent review and verification ownership.
- Behavioral evals run on a trusted machine with configured coding agents, never in PR CI. After merge, refresh and reinstall the plugin before starting work under the new release.
- Starting or continuing an authorized Factory task here also authorizes committing the independently reviewed candidate, pushing its task branch and opening or updating a draft pull request for remote verification. Do not ask again at that boundary.

## Rules

- Skills are the contract. Every stage must work from its skill alone in every supported harness. Do not add harness-specific agent definitions.
- Keep the plugin generic. Consumer context, access policy and delivery policy stay in the consumer; the consumer or the person decides when `submit` runs.
- No consumer names in skills, references or examples: no repository, user or file path from a project the plugin was tried on.
- Do not pin models or effort in skills; the host chooses.
- A change meant for users needs a version bump in both `plugin.json` and `.claude-plugin/plugin.json`. Hosts cache by version and keep the old copy otherwise.
- A person or separately authorized outer workflow owns ready state, approval, merge and deployment. Factory never extends its standing draft-publication authority to those actions.

## Verification

During Factory work, run only affected local checks before draft publication. The candidate-bound `PR quality` job owns the complete deterministic matrix described in [REVIEW.md](REVIEW.md). Use these commands locally to reproduce or diagnose that matrix:

- Repository quality: `python3 -m unittest discover -s tests`, then `python3 scripts/validate_repository.py --base-ref <target revision>`
- Claude Code: `claude plugin validate .`
- Codex: after pushing, `codex plugin marketplace add thecarbonlayer/plugin-marketplace`, `codex plugin add software-factory@thecarbonlayer`, then `codex plugin list --json` shows the new version. If `codex` is not on PATH, use the CLI bundled with the ChatGPT app.
- `git diff --check`

Report command exits and warnings separately from behavioral evidence, and say which harness each behavior claim was checked in.

## Before committing

- Exclude local drafts and evaluation artifacts; check new content for absolute filesystem paths and personal details.
- Verify visibility before publishing and keep private names out of public artifacts.
