# Case 02: risk lenses in one review

## Prompt

`factory continue The candidate changes an authorization check, a form and a tenant-scoped query. Review it.`

## Fixture

- The candidate is frozen and documented.
- `REVIEW.md` defines P0 through P3 severities and prohibits style-only findings.
- Builder evidence contains focused unit checks but not the full regression suite.
- The change affects access control, another tenant's data and a visible permission-denied state.

## Expected behavior

- Launches one fresh reviewer context with review, code, security and UX lenses.
- Gives the reviewer the contract, diff, evidence and policy, but not builder reasoning.
- Reviews server-side authorization, tenant isolation and the visible denied state coherently.
- Runs only narrow checks needed to prove findings.
- Leaves the complete regression and journey matrix to the verifier.

## Failure signals

- Starts separate acceptance, code, security and UX agents that reread the same repository.
- Treats a hidden UI action as sufficient authorization.
- Calls builder test results independent review.
- Duplicates the full suite in review and verification.
