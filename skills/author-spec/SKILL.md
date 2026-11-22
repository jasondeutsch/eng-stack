---
name: author-spec
description: Author or revise a software specification from a brief and repository evidence, defining behavior and observable acceptance criteria without planning implementation or granting approval.
license: MIT
---

# Author a software specification

Use the content-only [spec body](assets/spec.body.html) and [document helper](scripts/document.mjs); remove irrelevant sections. The helper preserves the shared visual shell without loading its CSS into your context. Output to the assignment's path, defaulting to `spec.html`.

Inspect the brief, relevant code, and actual project rules before drafting. Establish intended behavior, users or callers, included/excluded scope, external contracts, compatibility, and material failure cases. Ask only questions whose answers change behavior, scope, or a consequential decision; look up repository facts yourself. Record uncertainty rather than inventing an answer or conducting an unbounded interview.

Write measurable acceptance criteria with representative inputs and expected outcomes. Distinguish required behavior, observed current behavior, assumptions, and proposed constraints. Include sourced architecture or coding constraints only where they affect the task. Keep implementation choices and work ordering in the plan.

When revising, address findings individually and preserve stable IDs. Before handing off, check that every material part of the brief is covered or explicitly excluded, criteria are observable, source claims are grounded, and related document revisions agree. Report unresolved decisions with their impact. Publish the document and a concise summary of changes and limitations; the assignment owns handoff and approval policy.

Adaptation sources and notices: [planning sources](references/SOURCES.md).

## Content-only editing

Write content sections to a temporary body file, then render the deliverable:

```sh
node /path/to/this-skill/scripts/document.mjs render spec \
  --body /path/to/private/body.html --output /assigned/spec.html \
  --title "Change title" --revision 1 --companion-revision 1
```

Use `node /path/to/this-skill/scripts/document.mjs read /assigned/spec.html` to inspect the current metadata and content for revision, without CSS. Edit body sections only; the metadata header is supplied through the render options. Resolve the script from this skill's directory. Keep temporary body files in private runtime storage or the system temporary directory; publish only the assigned deliverables. Write a coherent draft early, then patch the affected sections. Do not repeatedly regenerate the full document or copy its style markup through tool output.

## Specification responsibilities

The spec defines intended behavior, scope, external contracts, sourced constraints, and observable acceptance criteria. Implementation sequence belongs in the [plan skill](../author-plan/SKILL.md); execution progress belongs in the assigned progress/result artifact. Default to `spec.html`; use another path when assigned. Do not introduce a separate requirements document.

The assignment controls authorship and workflow policy controls approval. A draft or clean review is not approval. Read the spec and plan together; report exact conflicts rather than silently changing either. Preserve accepted document identities when proposing scope revisions.

## Identity and change tracking

Use stable identifiers within an artifact: `AC-001` for acceptance criteria, `P-001` for work items, `C-001` for constraints, and `D-001` for consequential design decisions. Keep an identifier when revising the same requirement; do not reuse a retired identifier for different behavior. These are references, not a new task hierarchy.

Record the document revision, source brief/reference, relevant source versions, and the related document revision. Use a content digest or a recorded revision when available; Git is not required. Do not claim approval unless the assignment supplies its recorded decision and document identity. When accepted scope changes, preserve the old identity and report the proposed revision for whatever decision process the assignment defines.

## Project guidance and evidence

Inspect project instructions and the smallest relevant set of architecture documents, standards, source, and tool configurations. Search for the project's actual guidance rather than assuming a particular filename exists. Common examples include `AGENTS.md`, `CONTRIBUTING.md`, architecture/decision records, coding standards, lint configuration, and module/toolchain configuration.

The spec records applicable binding constraints. The plan records how the change meets them. Use a compact table:

| ID | Source and version | Applicable rule | Effect on this change | Verification |
|---|---|---|---|---|
| C-001 | Repository-relative path + section; revision/digest if known | Concrete rule, not a pattern name | Boundary or implementation consequence | Check or review evidence |

Preserve the actual authority of each source. Explicit instructions and established project rules take precedence over generic skill preferences. Existing code establishes current behavior; it is not permission to ignore a documented rule. Surface conflicting authoritative sources instead of inventing precedence between them. Record missing guidance as unknown, not as a mandatory new standard.

A named pattern such as DDD is not a sufficient requirement or justification. State the actual ownership, invariants, allowed dependencies, and failure behavior that matter. New patterns or exceptions are proposed decisions, with alternatives and consequences. Do not silently turn them into binding constraints. Keep project-wide manuals canonical; include only relevant rules and enough context to understand the artifact independently. Repository-relative source paths may be shown as text when the HTML output has no reliable link to the source checkout.

## Spec content

- Objective and scope: concise objective; included/excluded behavior.
- Behavior: scenario, input or condition, expected result; cover material errors and boundaries.
- External contracts: API, event, data, interface, or compatibility expectations where relevant.
- Constraints and invariants: sourced rules and concrete conditions that must hold.
- Acceptance: stable ID, observable requirement, representative case, verification method. Define required results, not fabricated evidence.
- Uncertainty: assumption or question, its source/status, impact, and decision needed.

## Presentation

Use the [spec template](assets/spec.html). The [plan template](../author-plan/assets/plan.html) uses the same [shell](assets/document.html), [stylesheet](assets/document.css), and [renderer](scripts/document.mjs). The plan skill links to this implementation instead of copying it. Edit body sections, not presentation markup.

Use technical tables, contracts, examples, and short decision rationales. Add diagrams when they explain a boundary, interaction, or state transition; small changes may need none. Charts require actual measurements and labeled units. Remove inapplicable sections and keep small changes small.

Outputs work offline: embedded CSS and SVG, semantic headings and table headers, SVG titles/descriptions, escaped literal text/code, and no scripts, external fonts, CDNs, or remote images. Explain status through text as well as color. Preserve narrow-screen and print layouts. Companion links must not be rendering dependencies.

Completed examples: [small change](examples/small/spec.html) and [service change](examples/service/spec.html). These illustrate document structure, not executed or approved work.

## Execution file locations

When the assignment supplies an execution files directory, resolve workflow documents and review/progress artifacts there. Project source remains in the launcher-selected workspace. Use the assigned absolute paths for renderer inputs/outputs; relative Factory publication names are relative to the execution files directory, not the source checkout. Standalone assignments without this context retain their explicit/default document paths.
