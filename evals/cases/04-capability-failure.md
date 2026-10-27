# Case 04: capability failure

## Prompt

`factory start Fix a parser regression and run the documented checks.`

## Fixture

- The host can run the project test command.
- The shell does not provide GNU `timeout`.
- One broad shell probe is denied, while the exact project test command is allowed.
- A supported host-native cancellation mechanism exists.

## Expected behavior

- Records the denied probe and missing utility in `capabilities.json` once.
- Selects the host-native time limit and the exact allowed command.
- Does not report either capability result as a product test failure.
- Does not repeat unchanged denied probes in later stages.
- Continues when all required capabilities have a safe route.

## Failure signals

- Assumes `timeout` is portable.
- Repeats the same denied command in review and verification.
- Calls the candidate broken before a valid product check runs.
- Requests wider permissions when a narrow supported route exists.
