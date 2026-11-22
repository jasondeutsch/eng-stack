---
name: task-intake
description: Convert a user or system request into a typed engineering task using a per-type template, preserving its source and uncertainty for readiness assessment.
---

# Task intake

Read the assignment's original `task` input (brief and captured document metadata), the captured documents, and supplied context. Select the type by the requested outcome, not the technique used to reach it:

| Type and template | Select when | Type-specific obligation |
| --- | --- | --- |
| [bug-fix](assets/bug-fix.json) | Existing behavior is incorrect. | Observed versus expected behavior and evidence of correction. Diagnosis is part of the fix. |
| [feature](assets/feature.json) | Add or intentionally change behavior. | Consumers, acceptance scenarios, exclusions, compatibility. |
| [refactor](assets/refactor.json) | Change structure while preserving behavior. | Intended improvement and checks for behavioral preservation. |
| [performance](assets/performance.json) | Improve or assess a performance target by changing the system. | Workload, target, measurement conditions, baseline when available. |
| [investigation](assets/investigation.json) | Answer a question or diagnose without implementing a change. | Question, evidence, expected answer/artifact; read-only scope. |

For a bug fix, write `details.issue.description` as a clear account of what is wrong, who or what is affected, and under which conditions. Separate actual behavior from expected behavior; a title such as "fix export" is not an issue description. Summarize supplied evidence and put missing details in `unknowns`.

A request to fix a bug remains `bug-fix` even when its root cause is unknown. A request only to explain the bug is `investigation`. A benchmark-only assessment is an investigation; an optimization request is performance. For mixed requests, choose the principal acceptance outcome and preserve secondary requirements. If outcomes require incompatible routes, record that in `unknowns` and mark classification uncertain; do not silently drop work or split it into executions.

Read the selected type in [brief guidance](references/task-briefs.md), then load its JSON template. Each type has a different problem/evidence structure; keep the shared envelope for source, scope, and routing. Use the template's exact keys. Common fields:

- `source`: copy the original brief verbatim and captured document metadata unchanged (normalize absent or null documents to an empty list). Keep additional evidence locations in `references`.
- `relationship`: `new` or `follow_up`, independent of type. Record missing prior-task context in `unknowns`.
- `objective`, `target`, `scope`, `constraints`, `acceptance_criteria`: capture requested outcomes and limits. Criteria are observable results, not implementation plans.
- `assumptions`, `unknowns`: distinguish inferences from supplied facts; state consequential omissions explicitly.
- `classification`: explain the type selection. Set `uncertain` and list plausible alternative type IDs when the choice would change scope or routing.
- `details`: fill the selected type's nested sections with sourced text; use `null` for unknown text. Lists may be empty when no items are supplied. Explain missing objectives, targets, or criteria in `unknowns` rather than inventing them. An empty value never means readiness.

Do not require root cause, code locations, reproduction commands, or measurements that later work can discover. Do not turn intake into specification, implementation, or an interview. Unsupported or non-engineering requests retain their original text, use a tentative investigation template with uncertain classification, and state why admission needs human review.

Write `task.json` in the assigned files directory. Validate its structure using the helper bundled with this skill:

```sh
node /path/to/task-intake/scripts/task.mjs validate /assigned/files/task.json
```

`template TYPE` prints a fresh template. `validate FILE ORIGINAL_INPUT_JSON` additionally checks source preservation. Resolve the helper from this skill's location; do not copy it into a target repository.

Complete with the assignment's `completed` outcome and `data: {"task": <the same task object>}`. The downstream classifier validates the contract and source against captured execution input before assessing readiness. Intake does not grant admission, alter permissions, or select workflow transitions. Never claim a structural check proves the classification or requirements correct.
