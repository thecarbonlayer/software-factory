# Refinement comment template

Keep this proportionate to the request. Combine short sections when useful; mark unknown or unresolved items explicitly rather than filling them with assumptions.

## Problem and desired outcome
Who is affected, what happens today, and what should improve?

## User requirements and scope
Use one concise row per stable `R-001` requirement: observable behavior and scope, authority (**user-agreed**, **delegated implementation choice**, or **unresolved proposal**), and source. Preserve existing IDs across revisions. Include relevant scenarios and exclusions without repeating the source request in full.

Record material choices with stable `D-001` IDs, their authority, source and rationale. A delegated choice must cite the delegation; unresolved proposals remain open. Silence never establishes user agreement.

## Original request/spec trace
Map each material original requirement to its R ID. List changes with their agreement source, unresolved items, additions and exclusions with their authority, and any superseded IDs with their disposition. Group retained requirements by source reference and IDs rather than restating them. Keep this brief for small requests.

## Factual context and evidence
Only facts the triage assessment does not already give; refer to triage for the rest. Distinguish observations from claims and inferences. These facts are not prescriptive requirements.

## Constraints
Known compatibility, operational or project constraints, with their source. Identify assumptions.

## Success and acceptance criteria
Concrete examples of observable outcomes ("given … when … then …" or a worked case), including meaningful failure, boundary and existing-data cases. Link each to its R ID so later stages can refer to it. When the request already states concrete, testable criteria, adopt them by source reference and add examples only for gaps. Identify criteria awaiting agreement.

## Completion measurement and checks
How each outcome can be demonstrated; appropriate existing tests, manual checks or other evidence. Note required access or test data without exposing sensitive content.

## Open decisions
Unanswered questions or conflicting replies that affect the requirements, with affected R/D IDs and who can resolve them if known. If none, say so.

## Next steps
Ready for planning, awaiting specified answers, or blocked by a named prerequisite. This judgment does not authorize implementation or publication.
