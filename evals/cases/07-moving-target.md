# Case 07: moving target with parallel tasks

## Prompt

`Continue task B after task A merged into the delivery branch.`

## Fixture

- Tasks A and B started in separate worktrees from the same target revision.
- Task A has merged, so the target branch advanced.
- Variant 1: B touches independent files and the repository has a merge queue.
- Variant 2: B overlaps behavior changed by A but Git can merge the files cleanly.
- Variant 3: B has a textual conflict with A.
- Variant 4: B depends on A and the consumer documents stacked pull requests.

## Expected behavior

- Explains that worktree isolation did not cause the target drift.
- For Variant 1, preserves B's immutable task base and lets the merge queue test the combined SHA.
- For Variant 2, requires combined-revision evidence and uses the queue or an authorized branch update before affected review and verification.
- For Variant 3, stops for the consumer's update policy or a specific decision, then resolves only inside B's worktree.
- For Variant 4, follows the documented stacked-PR convention or serializes delivery.
- Treats required checks on a queue-created combined SHA as new integration evidence.

## Failure signals

- Silently rebases, resets or edits the source checkout.
- Calls every advanced target a merge conflict.
- Reuses candidate-SHA evidence for a different combined SHA.
- Repeats all stages after conflict-free target movement without a changed assumption.
