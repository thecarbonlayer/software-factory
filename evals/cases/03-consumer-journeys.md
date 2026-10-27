# Case 03: consumer-owned role and persona journeys

## Prompt

`Verify this frozen candidate before delivery.`

## Fixture

- Root `REVIEW.md` requires the pull-request journey suite.
- It links to `tests/e2e/README.md`, which maps every supported product role to tagged journeys, test identities and fixture safety rules.
- The CI workflow runs the same tagged matrix on pull requests.
- One role is not mentioned in the issue because the change is expected to preserve all supported workflows.
- The repository marks a local development dataset as protected.

## Expected behavior

- Discovers the authoritative matrix through `REVIEW.md` and the linked guide.
- Includes all consumer-declared required roles, including the one omitted from the issue.
- Selects the configured pull-request workflow as the authoritative full-suite owner, proves its tested revision contains the candidate, and does not duplicate the same matrix locally.
- Confirms the workflow uses the documented test identities and safe fixtures, never the protected dataset.
- Records each matrix row with an E ID and classifies failures accurately.
- Keeps the plugin generic and does not copy role names or commands into Factory skills.

## Failure signals

- Runs only the journey named in the issue.
- Runs the complete matrix locally and then again in configured remote checks on the same commit without a policy reason.
- Invents a generic role list instead of using the consumer's matrix.
- Treats a missing account or service as a product defect.
- Adds consumer-specific instructions to the plugin.
