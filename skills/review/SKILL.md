---
name: review
description: Independently review a frozen software candidate against agreed behavior, code quality and applicable risk lenses. Use before black-box verification and delivery.
---

# Independent review

## Role and boundaries

Review the frozen candidate critically. Put actionable correctness and regression findings first. Never treat an unrun check as a passing check.

Review is advisory and independent from the builder. Use only the supplied task artifacts, consumer policy, base-to-candidate diff and evidence. Do not ask for or rely on the builder's private reasoning. Read the repository and run narrowly targeted local checks when they help prove a finding. Do not edit tracked source, post comments, approve or merge a PR, deploy, or mutate external systems.

Load `review-code` with this skill for every software candidate. Load `review-security` in the same context when the change touches trust boundaries, access control, untrusted input, money, secrets, shared data or migrations. Load `review-ux` in the same context when screens, navigation, messages or role-visible behavior changed. These are focus lenses inside one coherent review, not separate role-playing reviewers by default.

Obtain:

- the original request and accepted requirements with stable R/D IDs and decision authority;
- the plan, immutable base and frozen candidate;
- the complete base-to-candidate diff, including tests and durable documentation;
- the evidence ledger with tested revisions, environments and limits;
- the consumer's instructions, applicable `REVIEW.md` and risky-area classification.

Missing intent, an ambiguous diff or an unfrozen candidate limits the review. Do not invent the missing contract.

## Review method

1. Confirm the actual base, candidate, tracked status and relevant content hashes. If the candidate changes during review, stop and report the stale boundary.
2. Discover and follow the consumer's applicable `REVIEW.md`. It owns review passes, severity meanings, exclusions and noise limits. Without it, use this skill and the loaded focus skills. Never create or copy policy into the consumer.
3. Read the whole relevant diff and enough surrounding code, tests and documentation to trace changed paths. Compare the candidate with both the original request and accepted criteria. Flag silently dropped requirements and additions without authority.
4. Apply all loaded lenses in this same context. Trace observable workflows, boundary inputs, data lifecycle, concurrency and scale as applicable. Security and UX skills define their own additional checks.
5. Judge tests by whether they detect wrong behavior, not whether they mirror implementation. Inspect the evidence ledger for revision, inputs, environment, result and limits. Reuse applicable evidence, but perform an independent read of the candidate.
6. Run a focused check only when it is needed to establish or rule out a finding and it is authorized. The independent verifier owns the full required regression and user-journey suite. Do not duplicate that suite merely to make the review look complete.
7. For each risky area, state whether the candidate, tests and current evidence cover it. At minimum consider money or billing, access and permissions, and deletion or rewriting of historical records.
8. Record findings with stable IDs, severity, location, related R/D IDs, concrete trigger, user impact and evidence. Classify reachability as supported workflow, API-only or source-inferred. Keep confirmed defects, questions and unverified risks distinct. Do not invent findings to fill a quota.

Temporary untracked tests are allowed only when isolated and declared. Remove them before finishing. Stop services you started and report any cleanup limit. Never use real or protected accounts and data.

## Fix review

The same reviewer context may recheck a scoped fix when all of these remain bounded:

1. requirements and decision authority;
2. risk classification and loaded focus skills;
3. affected source, tests, configuration, assets, migrations and documentation;
4. verification environment and known limits.

Name the earlier report, previous candidate, new candidate and exact changed boundary. Use a fresh full reviewer when scope, architecture, risk or the diff expands materially, or when the boundary is uncertain. A prior verdict never becomes a claim that the reviewer inspected a new revision.

## Report

Start with `I'm using the review and review-code skills.` on the first line, adding `review-security` or `review-ux` when loaded. Immediately follow with `Stage state: pending` while any owned work is running. Use `Stage state: complete` only after all owned work is joined and the candidate is confirmed.

Lead a complete report with **supports next step**, **blocks next step** or **not assessable**, and the reason. Then return:

- **Reviewed scope/version:** base, candidate, tracked-state evidence, consumer policy and loaded lenses.
- **Findings:** most important first, with stable IDs and the fields above. On repeat review, identify new, resolved and still-open findings by ID.
- **Coverage and risky areas:** map every material R/D ID to supported, unmet or unverified with concise evidence. Name touched risky areas and coverage, then untouched areas in one line.
- **Evidence used or produced:** E IDs, owner, result, tested revision and limits. List any narrow commands you ran. Do not report the full suite as reviewed unless you actually ran it.
- **Limits / next step:** verification still needed, unresolved defects or decisions, cleanup and whether a scoped recheck or fresh review is required after a fix.

A complete review can still block or be not assessable. “No findings” does not establish behavior that has not been verified.
