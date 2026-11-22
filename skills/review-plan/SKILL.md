---
name: review-plan
description: Independently review an implementation plan for specification coverage, feasibility, dependency and interface consistency, appropriate complexity, and credible verification.
license: MIT
---

# Review an implementation plan

Read the [plan guidance](../author-plan/SKILL.md), the applicable spec and plan revisions, prior findings, and the relevant repository paths and project rules. Build an independent view before relying on the author's rationale.

Trace acceptance criteria and constraints to work items and verification. Check whether interfaces agree across dependent items, required components and tools exist, changes respect actual ownership/dependency rules, and the sequence can produce verifiable progress. Investigate consequential assumptions against code. Distinguish a spec defect from a plan defect so the right artifact can be corrected.

Challenge unnecessary components, dependencies, abstractions, and operational obligations. Check material compatibility, partial-failure, cancellation, concurrency, migration, and recovery behavior where relevant. Prefer concrete counterexamples to demands that the author justify every routine choice. Do not require a universal pattern, exhaustive implementation code, TDD, a Git branch, or extra documents unless the project or assignment requires them.

Record actionable findings in the assignment's review artifact using stable IDs and explicit evidence and impact. If reviewing spec and plan together, use distinct sections and one consistent finding-ID sequence. Close resolved findings explicitly across revisions. State readiness and limitations; a clean review is valid and does not grant approval. Do not modify the author's plan or source or orchestrate further review rounds.

Adaptation sources and notices: [planning sources](../author-spec/references/SOURCES.md).

For content-only reading, use the [document helper](../author-spec/scripts/document.mjs): `node /path/to/author-spec/scripts/document.mjs read /assigned/spec.html` (or `plan.html`). First review independently; on subsequent rounds inspect the actual changed sections and prior findings. Report one consolidated set of findings with the reviewed revisions, stable IDs, resolutions, and any affected contracts that were rechecked. Avoid rereading unchanged documents or issuing a separate message per observation.

## Findings and revisions

Use the [finding fields and revision method](../review-spec/SKILL.md#findings-and-revisions) for consistent IDs, evidence, severity, and resolution tracking. Review plan feasibility and acceptance coverage independently of the author's summary. On later rounds, inspect actual changes and affected contracts before the final spec/plan consistency check.

## Execution file locations

When the assignment supplies an execution files directory, resolve workflow documents and review/progress artifacts there. Project source remains in the launcher-selected workspace. Use the assigned absolute paths for renderer inputs/outputs; relative Factory publication names are relative to the execution files directory, not the source checkout. Standalone assignments without this context retain their explicit/default document paths.
