---
name: follow-plan
description: Execute assigned software plan items against their specification, preserving scoped progress, verification evidence, and responses to findings without rewriting the design or controlling the workflow.
license: MIT
---

# Follow a software plan

Read the [spec guidance](../author-spec/SKILL.md) and [plan guidance](../author-plan/SKILL.md), the assignment's spec and plan revisions, applicable project instructions, prior findings, and current progress. Confirm any decision the assignment actually requires; do not introduce an approval requirement of your own. Missing or contradictory design information is a question to resolve, not permission to invent requirements.

Inspect the current source before editing and preserve unrelated work. Implement the assigned items in dependency order using the relevant language and project skills. Acknowledge changed document revisions or material scope differences before acting on them. Do not amend design documents to match your implementation without an explicit document-authoring assignment.

Record durable progress in the assigned result/progress artifact: plan-item and acceptance IDs, changes made, actual commands and outcomes, limitations, and remaining work. Keep planned checks distinct from executed evidence. Do not claim success from an agent message, a listed command, or a predicted test result. On resumption, inspect source and evidence rather than assuming conversation memory is complete.

For each review finding, verify its trigger and evidence before repairing it. Resolve demonstrated defects, explain counterevidence when it does not apply, and surface design/scope disagreements for the assigned decision process. Preserve finding IDs. If blocked, report the cause and affected items; continue only independent authorized work.

Finish with a factual handoff and evidence. Completion means the assigned work is ready for the next configured action, not that the entire execution is approved. Commits, tool installation, other agents, review scheduling, retries, and deployment require their own authorization or workflow configuration.

Adaptation sources and notices: [planning sources](../author-spec/references/SOURCES.md).

Read HTML document content with the [document helper](../author-spec/scripts/document.mjs) rather than repeatedly loading style markup. Keep a compact record of current revisions, assigned items, open findings, and evidence. Search for relevant symbols, read bounded sections, and implement coherent items before repeating broad checks. Preserve useful check output (command, outcome, counts, failing excerpt); expand it when diagnosing a failure. Communicate milestones, concrete questions, and consolidated handoffs rather than routine tool narration.

## Execution file locations

When the assignment supplies an execution files directory, resolve workflow documents and review/progress artifacts there. Project source remains in the launcher-selected workspace. Use the assigned absolute paths for renderer inputs/outputs; relative Factory publication names are relative to the execution files directory, not the source checkout. Standalone assignments without this context retain their explicit/default document paths.
