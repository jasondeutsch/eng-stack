---
name: review-spec
description: Independently review a software specification against its brief and repository evidence for ambiguity, missing behavior, contradictions, unintended scope, and observable acceptance criteria.
license: MIT
---

# Review a software specification

Read the [spec guidance](../author-spec/SKILL.md), the brief, the actual spec revision, and relevant project evidence. Do not begin from the author's summary or assume a previously clean review still applies to a changed document.

Check whether the spec describes the requested behavior and boundaries without silently adding policy. Construct representative success, error, and boundary scenarios; look for contradictory outcomes, missing external contracts, assumptions presented as facts, incompatible project rules, and acceptance criteria that cannot distinguish success from failure. Apply performance, security, concurrency, or recovery scrutiny only where the change makes it relevant.

Use precise questions to expose material uncertainty. Find discoverable facts yourself; do not turn every possible concern into a question for the user. A theoretical possibility without a credible trigger or material impact is not a confirmed defect. Separate required corrections, unresolved decisions, and optional suggestions.

Write evidence-backed findings in the assignment's review artifact using stable finding IDs. Recheck revised documents against original findings and name their resolutions. State explicitly when there are no blocking findings and what remains unverified. Review readiness is a recommendation, not approval. Do not edit the submitted spec or application source, seek a quota of findings, interview indefinitely, or start a review loop yourself.

Adaptation sources and notices: [planning sources](../author-spec/references/SOURCES.md).

For content-only reading, use the [document helper](../author-spec/scripts/document.mjs): `node /path/to/author-spec/scripts/document.mjs read /assigned/spec.html` (or `plan.html`). First review independently; on subsequent rounds inspect the actual changed sections and prior findings. Report one consolidated set of findings with the reviewed revisions, stable IDs, resolutions, and any affected contracts that were rechecked. Avoid rereading unchanged documents or issuing a separate message per observation.

## Findings and revisions

Each finding records a stable ID, artifact/criterion, severity, evidence or explicit uncertainty, triggering scenario, impact, and requested resolution. Blocking findings concern agreed behavior, correctness, safety, or feasibility; preferences remain suggestions. Retain IDs across rounds and close findings as addressed with evidence, unresolved, or withdrawn with a reason.

First establish independent coverage of the brief, submitted revisions, and affected boundaries. Later inspect actual changes, open findings, and affected contracts; reuse still-valid evidence. Finish with cross-document consistency and acceptance coverage. The author's summary is not a substitute for reviewing submitted evidence.

## Execution file locations

When the assignment supplies an execution files directory, resolve workflow documents and review/progress artifacts there. Project source remains in the launcher-selected workspace. Use the assigned absolute paths for renderer inputs/outputs; relative Factory publication names are relative to the execution files directory, not the source checkout. Standalone assignments without this context retain their explicit/default document paths.
