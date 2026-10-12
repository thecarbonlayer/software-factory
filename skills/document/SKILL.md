---
name: document
description: Update a project's existing documentation after a reviewed change. Use when finished code needs its README, guides, decision records, task log or agent instructions brought up to date.
---

# Document

## Role and boundaries

Keep the project's documentation true to the reviewed change. Find what the project already has, change only what is now wrong or missing, and never record a decision nobody agreed.

Edit documentation only, inside the caller's authorized edit scope. Do not change code or tests. Return the result to the caller. Publication, merges, deployment and external delivery need their own authorization.

Use the original request/spec, agreed requirements and decisions with their sources, plan, final implementation report, review results and the authorized checkout. Do not assume a repository layout; find what this project actually has.

## Find the documentation

1. Read the project's instruction files (for example `AGENTS.md`, `CLAUDE.md` or their equivalents) and follow their links to context files.
2. List the documentation the repository tracks: README files, documentation folders, guides, changelogs, decision records, task logs and specifications, wherever they are.
3. Search those files for what the change touches: feature and screen names, routes, commands, settings, messages, error text and roles taken from the requirements and the diff.
4. Keep a short list: each file, why it is relevant, and whether it needs an edit. A file that only mentions a term but does not describe the changed behavior needs no edit.

## Update

Follow [durable-context reconciliation](references/durable-context.md) for what belongs where and for decision records. Edit only statements the change makes wrong or incomplete, in each file's existing format and voice. Describe what the change provides; do not imply it has merged or shipped. Record only decisions already agreed or made within delegated authority, with their source, and preserve history. Keep unresolved proposals out of tracked files; report them as open decisions. Report missing destinations; do not create new files unless the caller authorizes it.

Commit the documentation on the task branch when the caller permits, separate from code changes. Do not change code or tests. If a fact cannot be confirmed from the code, the requirements or the review evidence, leave it out and report it.

## Return

Return **Files updated** (one line each: what changed and why), **Files checked and left unchanged** (one line each), **Decisions recorded** (with source) or none, **Missing or blocked destinations**, and **Commits**. Keep it short; the documentation diff carries the detail.
