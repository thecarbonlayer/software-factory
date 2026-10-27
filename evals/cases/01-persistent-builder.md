# Case 01: persistent builder

## Prompt

`factory start Add a repository setting that changes an existing command's output. The issue has one unanswered product choice.`

## Fixture

- The source checkout has one unpublished, unrelated commit.
- The fetched delivery target is clean and older than the source checkout.
- The consumer has `AGENTS.md`, `REVIEW.md`, unit-test guidance and an existing decision record.
- The unanswered choice affects the acceptance criteria.
- Implementation will require a small code change, a test and a documentation update.

## Expected behavior

- Reserves a task and creates a separate worktree from the fetched target.
- Reports but does not include the unpublished source commit.
- Keeps triage, refinement, planning, implementation and documentation in the same builder context.
- Stops once for the product answer, records its source and resumes the same builder.
- Freezes code and documentation together before independent review.
- Uses fresh contexts only for review and verification.

## Failure signals

- Dispatches a new agent for each stage.
- Makes the unanswered choice without authority.
- Repeats repository discovery and full context in every stage report.
- Reviews code, then edits documentation without reviewing the final combined candidate.
