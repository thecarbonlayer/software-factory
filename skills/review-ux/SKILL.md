---
name: review-ux
description: Review a changed user experience from the diff, product contract and available evidence. Use with the review skill when screens, navigation, messages or role-visible behavior changed.
---

# UX review lens

Judge whether each intended user can find, understand and complete the changed flow. Keep defects apart from suggestions, and never present an unexercised flow as checked.

Follow the review skill for independence, scope, version, finding format, evidence and boundaries. This skill adds a UX lens to the same reviewer context. The separate verify skill owns black-box execution of the consumer's complete role, persona and journey suites.

1. **Reach.** Trace each intended role from its normal entry point to the changed feature through routes, navigation, permissions and state. A feature that has no supported path is a defect even when its API allows the call.
2. **Flows and states.** Inspect the main path plus relevant empty, loading, error, permission-denied, already-complete and boundary states. Check that each state explains what happened and the next action.
3. **Wording and consistency.** Labels and messages use the product's terms and existing patterns. Read-only values look read-only. Destructive or irreversible actions state their consequence before confirmation.
4. **Interaction basics.** Inspect keyboard path, visible focus, input labels, semantic structure, contrast cues and narrow-layout behavior for changed UI.
5. **Evidence.** Use current screenshots, artifacts or test results only when their revision and environment match the candidate. A screenshot or test name is supporting evidence, not proof of an unobserved journey.

You may run one narrow local interaction to establish a suspected finding when authorized and isolated. Do not duplicate the full end-to-end matrix. If runtime evidence is absent, label journey conclusions source-inferred and hand the exact roles, states and suspected gaps to verification.

Support each finding with the role, path, trigger, user impact and evidence. Do not redesign beyond the requirements. Suggestions that are not defects stay separate and do not block the candidate unless consumer policy says otherwise.
