---
name: author-plan
description: Author or revise an implementation plan for a software specification, defining design decisions, work dependencies, interface contracts, and verification without implementing the work.
license: MIT
---

# Author an implementation plan

Use the content-only [plan body](assets/plan.body.html) and [document helper](scripts/document.mjs); remove irrelevant sections. The helper preserves the shared visual shell without loading its CSS into your context. Output to the assignment's path, defaulting to `plan.html`.

Read the applicable spec revision and inspect relevant components, interfaces, tests, tool configuration, and project rules. Identify the smallest adequate change. Explain consequential choices with evidence, alternatives, and costs; a pattern name alone is not a design. Surface spec defects or conflicts rather than silently resolving them through implementation choices.

Define coherent work items with stable IDs, dependencies, affected components or files where known, consumed/produced interfaces, acceptance coverage, and verification. Give enough precision for another engineer to execute the work without reproducing the investigation. Avoid speculative filenames, full implementation transcripts, arbitrary tiny task counts, or blanket refactoring. Include data migration and recovery only when needed.

Map every applicable acceptance criterion and constraint to work and a check or explicit review method. State expected evidence separately from results; planning does not prove that a check passes. Identify tool/environment prerequisites and material failure paths.

Before handing off, check coverage, dependency order, consistency of names/contracts across work items, compatibility with project rules, and proportion to the actual change. Address prior findings individually. Publish the plan with unresolved decisions and limitations. Do not implement, create tracker issues, commit, launch reviewers, or choose workflow transitions merely because a plan contains work items.

Adaptation sources and notices: [planning sources](../author-spec/references/SOURCES.md).

## Content-only editing

Write content sections to a temporary body file, then render the deliverable:

```sh
node /path/to/this-skill/scripts/document.mjs render plan \
  --body /path/to/private/body.html --output /assigned/plan.html \
  --title "Change title" --revision 1 --companion-revision 1
```

Use `node /path/to/this-skill/scripts/document.mjs read /assigned/plan.html` to inspect the current metadata and content for revision, without CSS. Edit body sections only; the metadata header is supplied through the render options. Resolve the script from this skill's directory. Keep temporary body files in private runtime storage or the system temporary directory; publish only the assigned deliverables. Write a coherent draft early, then patch the affected sections. Do not repeatedly regenerate the full document or copy its style markup through tool output.

## Plan responsibilities

The plan explains implementation of the applicable specification: changes, interfaces, dependencies, decisions, and verification. It does not invent requirements or record execution progress. Default to `plan.html`; use another path when assigned. A planned check is not evidence that it passed, and a draft or clean review is not approval.

Use `P-001` for stable work-item IDs and `D-001` for consequential decisions. Retain IDs across revisions and never reuse retired IDs for different work. Record document revision, source reference, and related spec revision; Git is not required. Link acceptance and constraint IDs to the [spec's identity and guidance rules](../author-spec/SKILL.md#identity-and-change-tracking). Report contradictions rather than silently resolving them by changing scope.

## Plan content

- Change overview: affected components and current/proposed relationships, where meaningful.
- Design decisions: for consequential choices, use a compact ADR-style record with stable `D-` ID, context and decision drivers, considered options, proposed choice and rationale, consequences/tradeoffs, and a confirmation method. Status reflects recorded human approval; authoring alone cannot mark a choice accepted. Reference relevant existing ADRs and preserve supersession links. Keep records in this plan unless project conventions require separate ADRs; omit decision ceremony for routine implementation choices. See [task brief and decision guidance](../task-intake/references/task-briefs.md#what-to-borrow-from-decision-records).
- Work items: stable ID, intended change, dependencies, acceptance coverage, and observable verification. Prefer coherent, verifiable increments; a broad mechanical change need not be forced into artificial vertical slices.
- Interfaces and data: enough exact contract detail to coordinate affected components without writing the entire implementation in the plan.
- Verification: criterion or constraint, check, expected evidence, and environment prerequisites.
- Risks: failure condition, impact, mitigation or recovery, and unresolved decision where relevant.

Remove inapplicable sections. Small changes should produce small documents. Include deployment, migration, or rollback work only when the actual change requires it. Keep progress separate; work-item checkboxes in an approved document must not become the execution ledger.

## Presentation and project rules

Use the [plan body](assets/plan.body.html), [plan template](assets/plan.html), and [renderer](scripts/document.mjs). Rendering uses the spec skill's shared shell and CSS; [presentation rules](../author-spec/SKILL.md#presentation) apply to both documents. The renderer dependency is explicit and has one implementation.

Cite applicable project rules and source versions, and describe how the proposed change satisfies them. Project manuals remain canonical. A named pattern is not sufficient justification: specify actual boundaries, invariants, allowed dependencies, and failure behavior. Missing guidance is unknown, not authorization to invent a standard. Keep documents proportional to the change; avoid repeated inventories, speculative options, and textbook explanations.

Completed examples: [small change](examples/small/plan.html) and [service change](examples/service/plan.html). These illustrate document structure, not executed or approved work.

## Execution file locations

When the assignment supplies an execution files directory, resolve workflow documents and review/progress artifacts there. Project source remains in the launcher-selected workspace. Use the assigned absolute paths for renderer inputs/outputs; relative Factory publication names are relative to the execution files directory, not the source checkout. Standalone assignments without this context retain their explicit/default document paths.
