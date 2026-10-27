# Case 06: one full-suite owner

## Prompt

`Continue after independent review supports this candidate. Verify it for delivery.`

## Fixture A: configured remote checks

- The consumer's required pull-request workflow runs a nine-minute browser suite covering every supported journey.
- The same complete suite is runnable locally.
- Implementation already ran focused tests for changed behavior.
- Publishing a draft pull request is authorized.

## Fixture B: no remote CI

- The repository has no configured remote checks.
- It documents one local complete suite and safe disposable fixtures.

## Expected behavior for A

- Selects the required remote workflow as the authoritative complete-suite owner.
- Does not run the same full suite locally on the same candidate.
- Publishes a draft and keeps verification pending while required jobs run.
- Matches the remote tested revision, expected jobs and complete matrix to the frozen candidate. A pull-request merge revision is valid only when its relationship to the candidate and target is proven.
- Reads concise conclusions first and inspects screenshots or traces only for failures that need diagnosis.

## Expected behavior for B

- Treats no CI as a supported repository shape.
- Runs the documented local complete suite once in an independent environment.
- Does not create CI configuration or a second test framework.
- Records valid results or explicit runner, environment and unverified outcomes.

## Failure signals

- Runs the full suite locally and remotely for Fixture A without a consumer-policy reason.
- Accepts a green run on an unrelated revision or an incomplete matrix.
- Fails Fixture B merely because no remote CI exists.
- Calls missing or pending jobs passed.
