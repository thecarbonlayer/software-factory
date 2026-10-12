---
name: review-security
description: Review a software change for security defects. Use with the review skill when a change touches access control, user input, money or other sensitive state, data exposure, migrations or secrets.
---

# Security review

Be a security reviewer. Think like a wrong-role user, another tenant and a concurrent request. Report defects you can show, ranked by impact, and never treat an unrun check as a passing check. Run local checks against test data only.

Follow the review skill for scope, the version reviewed, finding format, limits and boundaries. This skill sets the focus: what an attacker, a curious user or a concurrent request could do with this change. Leave the requirement-by-requirement trace to acceptance review; under acceptance and verification, report only the checks you ran and what they showed.

1. List the entry points the change adds or alters: routes, background jobs, migrations, file exports, client-side checks. For each, name who may call it and what it may touch.
2. **Access.** For each entry point, check role, tenant and object ownership on the server, not only in the UI. Try the wrong-role, other-tenant and other-user cases (for example, another user's record by id or number). A hidden button is not access control.
3. **Input and output.** Trace user-controlled values into queries, file paths, templates, generated files (CSV, PDF) and logs. Check escaping for each sink, including spreadsheet formulas. Check that error messages and responses do not reveal records the caller may not see.
4. **State that must not be duplicated or lost** (money, issued documents, counters, permissions). Check concurrent requests, retries and partial failure: what stops two callers from acting on the same rows, and what happens when a step fails midway.
5. **Data layer.** Check new tables and columns for tenant isolation, grants and row-level policies matching existing patterns. Check that migrations and backfills cannot widen access or rewrite records meant to be fixed.
6. **Secrets and audit.** No credentials in code, fixtures or logs. Sensitive changes leave an audit record that names who acted.

Prove a finding when feasible with a focused test or a local request against test data; otherwise label it unverified and state the trigger. Do not probe production or real accounts. Rank findings by impact and likelihood; do not pad with generic advice.
