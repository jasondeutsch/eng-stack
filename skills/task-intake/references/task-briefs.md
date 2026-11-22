# Task briefs

The shared envelope records the original request, objective, target, scope, constraints, acceptance criteria, assumptions, unknowns, and classification. Put the substantive brief in the selected `details` structure. Keep sections short and avoid repeating the same prose in several fields. Type-specific verification describes *how to establish* acceptance; the common acceptance criteria describe *what result must hold*.

Unknown text is `null`; unknown lists are empty. Explain consequential omissions in `unknowns`. Populate facts from the request and available evidence, not imagined answers. Reproduction, measurements, and design choices can be discovered after admission.

## Bug fix — issue report

- `issue.description`: explain the defect in context, including the operation, triggering conditions, and affected user or system. For example: "Exporting a report with no matching rows returns exit 0 but leaves a zero-byte CSV, so downstream import rejects it."
- `actual_behavior` and `expected_behavior`: state the observable difference. Cite an existing contract where available; distinguish a reporter's expectation from a confirmed requirement.
- `impact`: who is affected and the consequence. Record known reach or frequency; do not manufacture severity or urgency.
- `reproduction`: environment/version, preconditions, ordered steps, and frequency when known. An empty step list means unavailable, not unreproducible.
- `evidence`: supplied logs, error messages, screenshots, failing inputs, or references. Keep hypotheses out of factual evidence.
- `regression`: last known good and first known bad versions if supplied; these do not establish root cause.
- `known_workarounds`: observed mitigations, without treating them as the requested correction.
- `verification`: evidence that would establish correction and related regressions to cover. Do not prescribe a patch or invent the cause.

## Feature — problem and capability brief

- `problem_statement`: the unmet need and its context; explain why the capability is wanted.
- `users`, `desired_outcome`, `usage_scenarios`: who uses it, what changes for them, and concrete inputs/actions with expected outcomes. Include material failure scenarios when supplied.
- `external_contracts`: relevant API, CLI, event, storage, or UI behavior the feature must expose or respect; discovery is allowed.
- `compatibility`: existing behavior that must remain and migration constraints supplied by the request or repository.
- `success_measure`: how the requested value will be recognized, if known. Do not invent product metrics or require a business case for a straightforward feature.

## Refactor — structural improvement brief

- `motivation`, `current_design`: explain the concrete maintainability or structural problem, grounded in the current system.
- `design_pressures`: competing forces such as coupling, ownership, operability, performance, or compatibility. These are decision drivers, not a predetermined solution.
- `desired_properties`: the structural improvement sought. Preserve a supplied solution as a proposal unless it is an explicit constraint.
- `behavior_to_preserve`, `affected_interfaces`: state observable invariants and contracts that constrain the change.
- `existing_decisions`: references to relevant ADRs or approved choices; identify decisions potentially challenged by the task.
- `preservation_strategy`: how equivalence could be established. Design alternatives and the chosen implementation follow admission.

## Performance — measurement and optimization brief

- `problem_statement`: observable performance problem and its consequence, distinguishing a report from a measured result.
- `workload`: operation, representative data shape/size, and load/concurrency where known.
- `measurement`: baseline with units and statistic, improvement target, environment, and measurement method. Prefer "p95 <200 ms at 100 requests/s" over "faster" when the request supplies that target. A missing baseline is work to do, not a fabricated number.
- `correctness_invariants`: outputs, semantics, error behavior, or consistency that optimization must preserve.
- `trade_off_constraints`: limits on resource use, cost, latency, accuracy, compatibility, or operational complexity. Proposed optimizations belong in later design.

## Investigation — question and evidence brief

- `question`, `context`: the uncertainty to resolve and why the answer matters.
- `known_evidence`, `hypotheses`: separate observations from possible explanations. Hypotheses may be empty; do not invent a fixed number.
- `suggested_approach`: supplied investigative leads, recorded as suggestions unless explicitly constrained.
- `deliverable`, `completion_condition`: expected answer/artifact and what would constitute an adequate answer. An inconclusive result can be valid when it explains evidence limits and what would resolve them; never promise certainty without evidence.
- `read_only`: remains true. A finding that suggests a repair does not authorize implementation.

## What to borrow from decision records

[Michael Nygard's ADR practice](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) records context, a significant decision, its status, and consequences. [MADR](https://github.com/adr/madr/blob/4.0.0/template/adr-template.md) makes decision drivers, alternatives, and confirmation explicit.

At intake, borrow the concise problem/context, competing forces, and references to prior decisions. Apply these where the type needs them; a routine defect needs a clear issue report, not an ADR questionnaire. During design, use an ADR-style record for consequential choices: context/drivers, considered options, proposed choice and rationale, consequences/tradeoffs, and how to confirm the result. Keep it in the existing plan's decision section unless the target repository requires separate ADRs. Link existing records instead of copying them. Status follows recorded human decisions; an intake agent cannot mark a design accepted. Preserve superseded decisions and link their replacements when the project uses ADRs.
