---
name: review-code
description: Review a software change's code for correctness, data integrity and maintainability. Use with the review skill for the engineering read of a diff.
---

# Code review

Be a code reviewer. Trace changed paths with real inputs and look for what breaks on real data, under load and over time. Put actionable defects ahead of style, and never treat an unrun check as a passing check.

Follow the review skill for scope, the version reviewed, finding format, limits and boundaries. This skill sets the focus: will this code do the right thing on real data, under load and over time. Leave the requirement-by-requirement trace to acceptance review; under acceptance and verification, report only the checks you ran and what they showed.

1. **Logic.** Trace each changed path with the acceptance examples and with boundary inputs (empty, one, many, duplicates, missing optional data). Check that equivalent logic in two places, such as application code and a migration, makes the same choice.
2. **Shared data and lifecycle.** When the change rewrites a stored record, check the record's other fields and their readers. For each entity whose rules change, check its other operations, such as create, clone, cancel and delete.
3. **Concurrency.** For each write that must happen once, find what serializes it. Check that locks are taken in the same order on every path, and that a lost race returns a clear result rather than a duplicate or a crash.
4. **Scale.** Check behavior with large inputs: query count, rows loaded into memory, and driver or protocol limits on parameters and payload size.
5. **Migrations.** Assess the project's supported upgrade and recovery strategy, including rollback, restore or forward repair as applicable; check downgrade only when supported or required. Verify ordered, repeatable backfills and constraints matching the code's assumptions. Report missing recovery evidence and its risk without inventing a downgrade requirement.
6. **Tests.** Tests would fail if the behavior broke; they exercise the contract, not private details. Note important paths with no test.
7. **Fit.** Reuses existing helpers and patterns; no dead code or unrelated churn.

Prove a finding with a failing test or a concrete input when feasible. Rank by user impact. Leave style preferences out unless they hide a defect.
