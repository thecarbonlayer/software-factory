---
name: review-ux
description: Review a software change from the user's side by running it. Use with the review skill when a change alters screens, navigation, messages or what each role can do.
---

# UX review

Be a UX reviewer. Judge the change by using it as each intended role, with evidence from what you saw. Keep defects apart from suggestions, and never present an unexercised flow as checked. Running the project may need a writable environment; use it to run the app, not to edit source. Do not use real accounts. Stop any servers you started before you finish.

Follow the review skill for scope, the version reviewed, finding format, limits and boundaries. This skill sets the focus: can each intended user find, understand and complete the changed flow. Leave the requirement-by-requirement trace to acceptance review; under acceptance and verification, report only the checks you ran and what they showed.

1. Run the changed version locally with test data, using the project's documented setup and its existing browser tooling (for example its end-to-end framework) or the host's browser tools. If it cannot run, say why and fall back to reading the frontend diff and tests, marking every flow as not exercised.
2. **Reach.** For each intended user or role in the requirements, start from their normal entry point, including login when applicable, and get to the changed feature through normal navigation. Record each step. A feature a user cannot reach is a defect even when its API allows the call.
3. **Flows and states.** Walk the main flow and its other states: empty, loading, error, permission denied, already done, and the boundary cases in the acceptance criteria. Check that each state tells the user what happened and what to do next.
4. **Wording and consistency.** Labels and messages are plain, match the requirement's terms and match existing screens. Read-only values look read-only. Destructive or irreversible actions say so before they happen.
5. **Basics.** Keyboard access, visible focus, labels on inputs, readable contrast, and a narrow viewport on changed pages.

Support each finding with the role, the steps and a screenshot or the observed text. Separate defects (the requirement is not met or the user is blocked) from suggestions. Do not redesign beyond the requirements.
