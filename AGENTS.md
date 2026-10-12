# Working notes

## Context index

- [README](README.md): read for product behavior, installation, consumer context conventions and runtime evidence before changing the plugin.
- [Qualification](README.md#qualify-the-plugin): read before verification; prerequisites, commands, manual checks and execution limits.
- [Durable-context procedure](skills/document/references/durable-context.md): read when changing consumer documentation or instruction guidance.
- [Task artifacts](skills/factory/references/task-folder.md): read when changing factory handoffs or resume state.

## How we know a change helped

- Test a stage change by running it on one real task, ideally a replay: a shipped issue at the revision before its spec, scored against what actually shipped.
- Write the checks before the run. Mark anything added after it as post-hoc.
- Record the result in the commit message: what was run, which harness, the checks that held or missed, and the limits. One run is a likely improvement, not proof.
- A passing `plugin validate` proves packaging, not that a harness runs the stage.
- Do not build test harnesses, validators or expected-answer machinery for the plugin without a concrete product need.

## Rules

- Skills are the contract. Every stage must work from its skill alone in every supported harness. Do not add harness-specific agent definitions.
- Keep the plugin generic. Consumer context, access policy and delivery policy stay in the consumer; the consumer or the person decides when `submit` runs.
- No consumer names in skills, references or examples: no repository, user or file path from a project the plugin was tried on.
- Do not pin models or effort in skills; the host chooses.
- A change meant for users needs a version bump in both `plugin.json` and `.claude-plugin/plugin.json`. Hosts cache by version and keep the old copy otherwise.

## Verification

From the repository root:

- Claude Code: `claude plugin validate .`
- Codex: after pushing, `codex plugin marketplace add thecarbonlayer/plugins`, `codex plugin add software-factory@thecarbonlayer`, then `codex plugin list --json` shows the new version. If `codex` is not on PATH, use the CLI bundled with the ChatGPT app.
- `git diff --check`

Report command exits and warnings separately from behavioral evidence, and say which harness each behavior claim was checked in.

## Before committing

- Exclude local drafts and evaluation artifacts; check new content for absolute filesystem paths and personal details.
- Verify visibility before publishing and keep private names out of public artifacts.
