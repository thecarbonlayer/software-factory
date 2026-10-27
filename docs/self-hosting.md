# Developing Software Factory with Software Factory

Software Factory is a consumer of its own released plugin. Non-trivial changes to this repository use the same `factory`, stage, review, verification and submit skills that another repository uses.

The installed stable release is the operator. The repository checkout is the product being changed, and its edited skills are the candidate under test.

```text
installed stable Factory
        |
        | creates and operates the task
        v
isolated factory/<task> worktree
        |
        | produces
        v
candidate Factory release
        |
        +--> independent review
        +--> local behavioral qualification when skill behavior changed
        +--> PR quality on the exact candidate
        v
human delivery decision, merge, then plugin refresh
```

## Start and operate a task

1. Confirm that a released Factory plugin is installed and record its version. The root manifests describe the candidate version; they do not change the running operator.
2. Start the request with the installed `software-factory:factory` skill. It reserves `.factory/<task-id>/`, creates a separate `factory/<task-id>` worktree from the fetched delivery target and keeps the source checkout unchanged.
3. Keep triage, refinement, planning, implementation, documentation and scoped fixes in the persistent builder. Use fresh contexts for independent review and verification.
4. Treat `.factory/` as local task state. It contains intent, plans, evidence and raw reports and is ignored by Git. Shared intent belongs in an issue when one exists; delivery evidence belongs in the pull request.

Do not load edited candidate skills into the running builder and pretend that the task changed versions. A task started under one installed release finishes under that release. Fresh evaluation sessions may load the candidate explicitly because the candidate is what those sessions are testing.

If the installed release cannot operate the task safely, use the last known-good installed release or carry out the smallest manual recovery. Record that departure and do not let an unreviewed candidate become its own control plane.

## Review and verification ownership

[REVIEW.md](../REVIEW.md) owns the repository's review and verification policy.

Implementation runs focused checks for the affected behavior. One fresh reviewer examines the frozen code-and-documentation candidate with code review and any applicable security or UX lens.

The pull request's `PR quality / Validate plugin repository` job owns the complete deterministic suite for the submitted revision. It runs the repository validator tests, repository validation, patch whitespace check and plugin packaging validation. A Factory task consumes that remote result rather than running the identical complete matrix locally first.

## Run behavioral qualification locally

Behavioral evals require a coding agent, so they run on a trusted workstation or other controlled machine where the selected agents are already configured. They do not run in GitHub Actions and no model credential belongs in repository or workflow configuration.

Run behavioral qualification when a change alters skill decisions, stage boundaries, evidence rules, review or verification behavior, or release-level orchestration. Documentation, evaluation prose and deterministic CI changes may skip it when they do not change shipped skill behavior; record the reason.

For qualification:

1. Keep the released plugin as the baseline and expose the candidate skills only to fresh candidate sessions.
2. Give each runner only the case prompt and fixture. Keep builder reasoning and expected answers out of the runner context.
3. Use a separate evaluator to score the saved output against the checked-in rubric and hard gates.
4. Record the baseline and candidate revisions, host, agent harness and version, model selection, environment limits, case results and evidence for each deduction.
5. Keep raw transcripts under the ignored task directory or another local temporary location. Commit only de-identified aggregate results.

If a pull request changes an eval case or rubric, run the candidate against the target branch's original suite as well as the proposed suite. The proposed test must not erase evidence of a regression against the earlier contract.

See [the eval guide](../evals/README.md) for the cases and scoring procedure.

## Deliver and adopt the next release

Starting or continuing an authorized Factory task in this repository grants standing authority to commit an independently reviewed candidate, push its task branch and open or update a draft pull request. Factory does not ask again before those actions. This lets the candidate-bound PR-quality job run without a redundant publication prompt.

That standing authority does not cover marking the pull request ready, approval, merge or deployment. After required local behavioral qualification and the candidate-bound PR-quality result support delivery, Factory stops for a person's decision on those actions.

After merge, refresh the marketplace, install the released plugin and confirm the installed version before starting the next Factory task. A task already in progress keeps the release it started with.
