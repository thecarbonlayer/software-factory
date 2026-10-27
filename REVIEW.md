# Review and verification policy

This repository develops Software Factory with the released Software Factory plugin. Follow [the self-hosting procedure](docs/self-hosting.md) and keep the installed stable release separate from the candidate being edited.

## Independent review

- Review the frozen code-and-documentation candidate in one fresh context with `software-factory:review` and `software-factory:review-code`.
- Add the security lens only for trust boundaries, permissions, secrets, untrusted input, shared data or workflow-token changes. Add the UX lens only for changed user-visible interaction.
- Give the reviewer the request, accepted requirements and decisions, base-to-candidate diff, documentation and evidence. Do not provide builder-private reasoning as evidence.
- Report actionable correctness, compatibility, evidence and maintainability findings. Do not report style-only preferences.

## Deterministic verification

The required complete deterministic suite is the pull request job `PR quality / Validate plugin repository`. It must pass on the exact candidate head or a proven integration revision containing that candidate and its target.

The job runs:

- validator unit tests;
- `scripts/validate_repository.py` against the pull request base;
- `git diff --check` for the pull request patch;
- `claude plugin validate .` with the workflow's pinned validator version.

Implementation and review may run affected checks needed to build or prove a finding. Do not duplicate the complete deterministic matrix locally and remotely on an equivalent tree without a recorded policy reason.

## Behavioral qualification

When shipped skill behavior or orchestration changes, run the applicable [behavioral evals](evals/README.md) on a trusted machine with configured coding agents. This is local release evidence, not a GitHub Actions job. Keep model credentials, raw transcripts and consumer traces out of the repository.

Documentation, eval prose and repository-infrastructure changes may omit behavioral qualification when they do not change shipped skill behavior. Record that classification and its limits in the task evidence and pull request.

## Delivery

Starting or continuing an authorized Factory task in this repository includes authority to commit the independently reviewed candidate, push its task branch and open or update a draft pull request so remote verification can run. Factory does not ask again at that boundary.

A person or separately authorized outer workflow still owns ready state, approval, merge and deployment. After merge, refresh and reinstall the plugin before using the new release for another task.
