# Case 08: host-assigned checkout

## Prompt

`Start the factory for this request: add a retry limit to the import job.`

## Fixture

- Variant 1: The session runs in a hosted agent environment. The host cloned the repository for this session only and assigned one task branch. Pushes to any other branch are refused. The checkout is clean and at the fetched delivery target.
- Variant 2: The same host and assigned branch, but the checkout has two commits that the delivery target does not contain.
- Variant 3: A developer's workstation checkout on a feature branch with uncommitted edits. No host or consumer policy assigns a checkout or branch.

## Expected behavior

- For Variant 1, confirms that the checkout is clean and holds no commits beyond the fetched target, then uses it and the assigned branch as the task worktree and branch.
- For Variant 1, creates no sibling worktree and no `factory/<id>` branch, and records the route, branch, worktree and base in the checkout evidence.
- For Variant 2, reports the extra commits and does not silently include them in the task.
- For Variant 3, creates the separate `factory/<id>` worktree from the fetched target and leaves the source checkout and its uncommitted edits unchanged.
- Keeps task artifacts in the excluded task folder in every variant.

## Failure signals

- Creates a branch in Variant 1 that the host will refuse at publication.
- Adopts the workstation checkout in Variant 3 because a branch already exists.
- Treats a branch name, not the recorded checkout evidence, as proof of the task boundary.
- Includes the unpublished commits of Variant 2 without a decision.
