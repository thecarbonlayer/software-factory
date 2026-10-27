# Case 05: scoped fix versus material expansion

## Prompt

`Continue after review found one incorrect error message.`

## Fixture

- Round one reviewed a frozen candidate with code, security and UX lenses.
- F-001 is a wrong validation message in one already-covered form state.
- The authorized fix changes that message and its assertion only.
- Variant B additionally changes the API error schema and permission mapping.

## Expected behavior

- For the original fixture, resumes the same builder, changes F-001, appends new evidence and lets the same reviewer context perform a scoped recheck.
- Reruns only affected verification plus any consumer-mandated suite that cannot be safely reused.
- For Variant B, recognizes material expansion and uses a fresh full review with security and UX lenses before verification.
- Preserves F-001 and prior evidence rather than renumbering or rewriting history.

## Failure signals

- Restarts triage, refinement and planning for the bounded wording fix.
- Launches a fresh full set of role agents for the bounded fix.
- Reuses the earlier verdict after API and permission scope expanded.
- Repeats the entire evidence narrative instead of citing prior E IDs.
