# AI Software Engineering Stack

**Working draft · Updated November 23, 2026**

The stack turns a request into a typed task, assesses readiness, then routes change tasks through reviewed design and implementation, or investigations to a read-only report. Both require human acceptance. The [factory workflow](factory.yaml) begins with typed intake and readiness. Language, tools, models, agent packages, and verification commands are configuration choices.

## Workflow

| Step | Responsibility and result |
| --- | --- |
| Task intake | Convert a natural-language request from a user or system into a task with a formal type, using that type's template. Preserve the original request and unresolved information. |
| Readiness | Assess the resulting task against its type and template: is there enough information to begin meaningful work? Admit under the configured policy or request human admission. Preserve the assessment and any override reason. Provider failures remain execution errors. |
| Specification and plan | Inspect the repository and task. Define behavior, constraints, acceptance criteria, implementation steps, and verification. Produce a specification and plan proportional to the task. |
| Architecture review | Independently review both documents against the task and repository. Approve or return actionable findings with stable IDs and references to reviewed revisions. |
| Design approval | A human approves implementation, requests design changes, or rejects the work. |
| Implementation | Execute the approved plan. Produce source changes and evidence recording checks, results, progress, and limitations. |
| Code review | Independently evaluate the implementation against the approved design and acceptance criteria. Approve or return findings for repair. Recheck changed behavior and affected evidence. |
| Acceptance | A human accepts the result, requests implementation changes, or rejects the work. |

Design and implementation each contain a sequential author/reviewer loop. The current configuration allows three rounds per stage. A satisfactory review reaches its human gate early; exhausted rounds escalate with unresolved findings. Human requests for changes start another bounded series. Exhaustion alone never establishes success. Failed steps and human rejection route to blocked.

Execution hooks prepare an isolated worktree. Stage hooks commit approved project changes; specifications, plans, and reviews remain in execution storage. Release retains the workspace and branch for inspection. Commit, merge, deployment, and acceptance are distinct actions.

## Execution rules

**Agents propose. Policies validate. The workflow engine executes.**

- The engine owns authoritative workflow state, routing, limits, and history. Agents cannot bypass gates or expand their authority.
- Record task context, decisions, artifact revisions, findings, verification, failures, and usage outside conversational memory.
- First reviews establish independent coverage. Subsequent reviews inspect actual revisions and open findings, retaining evidence that remains valid.
- Diagnose failures before retrying. Separate infrastructure faults, invalid outputs, and engineering defects; preserve causal information and bound recovery.
- Task hierarchy expresses ownership; dependencies express prerequisites. Subtasks remain within parent scope. Parent completion requires integrated acceptance against the parent's criteria.
- Isolate conflicting writes and account for shared services and environment state. Delegate when its benefit exceeds coordination and integration costs.

Policies enforce encoded conditions. Requirement adequacy, design quality, and evidence sufficiency still require accountable judgment. Agent roles are responsibilities; they need not be permanent processes. Agent Fabric remains a separate, optional integration.

## Task intake and templates

**Natural-language request → task-intake skill → typed task → readiness classifier.**

The intake skill selects a formal task type and fills its template from the request and supplied context. Every task preserves the original request, source references, objective, target, scope, constraints, acceptance criteria, assumptions, and unknowns. Record uncertainty in the selected type; avoid inventing facts to complete fields.

Each type adds specific fields:

| Type | Template fields |
| --- | --- |
| Bug fix | Issue description, actual/expected behavior, impact, reproduction conditions and steps, evidence, regression history, workarounds, correction and regression checks. |
| Feature | Problem, users, desired outcome, usage scenarios, external contracts, compatibility and migration constraints, success measure. |
| Refactor | Motivation, current design, competing design pressures, desired properties, behavior and interfaces to preserve, relevant decisions, preservation strategy. |
| Performance | Performance problem, representative workload, baseline/target with units, environment and measurement method, correctness invariants, tradeoff constraints. |
| Investigation | Question and context, known evidence, separate hypotheses, investigative leads, deliverable, completion condition, read-only scope. |

The [brief guidance](../../skills/task-intake/references/task-briefs.md) explains each field. Borrow ADR context and decision drivers where useful; record consequential alternatives, choices, rationale, consequences, and confirmation during design in the existing plan, or in ADRs when the target project requires them.

Templates define the task brief. Detailed specifications and plans follow admission. Root causes, exact code locations, measurements, and other discoverable facts may remain unknown at intake. Readiness distinguishes those unknowns from missing objectives or constraints that prevent progress. Template completion alone does not establish readiness.

The [task-intake skill](../../skills/task-intake/SKILL.md) supplies five JSON templates: `bug-fix`, `feature`, `refactor`, `performance`, and `investigation`. Readiness validates the task structure and original source, then assesses type fidelity and actionability. Uncertain or mismatched types require human admission. New versus follow-up is a separate attribute. A material type mismatch found later is recorded and reassessed; classification cannot silently change scope or remove approvals. Investigations route to a read-only agent and `investigation.md`, followed by human acceptance; requests for changes revise the report. Other types follow the design and implementation loops.

## Proposed execution metrics

Measure a **task** as an objective, an **execution** as one workflow run, and an **attempt** as one invocation of a step. Keep retries, review rounds, and repeat executions distinct.

| Metric | Definition |
| --- | --- |
| Accepted completion | Accepted executions divided by admitted executions in a fixed cohort. Show blocked, failed, cancelled, and unfinished outcomes separately; report admission exclusions. Also track eventual task acceptance across repeat executions. |
| Escaped defects | Accepted results requiring a defect correction or rollback within a declared observation window, divided by accepted results with that full window. Record severity; distinguish defects from new requirements. |
| First-review pass | Design and code reviews returning approval on their first completed review, each divided by that stage's initial completed reviews. Report stages separately and pair with escaped defects. |
| Rework | Additional author/reviewer rounds, reopened findings, and human requests for changes per execution. Distinguish implementation repair from requirement changes and infrastructure retries. |
| Cycle time | Submission to acceptance or other terminal outcome. Report median and p90 by outcome, with queue, active execution, and human-wait time separated. Track the age of unfinished work. |
| Cost per accepted result | Total model and execution cost across the admitted cohort, including failed attempts and repeat executions, divided by accepted tasks. Missing usage or pricing remains unknown; configured zero rates are not evidence of free execution. |
| Human effort | Active review and decision minutes plus unplanned interventions per task. Separate required admission/design/acceptance decisions from rescue work; waiting time belongs in cycle time. |

Record task and execution IDs, parent IDs, type, risk, configuration identity, artifact revision, stage/attempt timestamps, outcomes, finding IDs, human decisions, and resource usage. Compare like task types and difficulty, report sample sizes and incomplete telemetry, and use a declared defect observation window. Agent activity, token volume, and test counts alone do not establish quality.

## Proposed skill set

Skills must provide a concrete method, useful knowledge, tooling, or verification procedure. Reuse the [registry skills](https://github.com/PragmaEngineering/factory-registry/tree/main/skills) before adding new ones.

| Skill | Purpose | Starting point |
| --- | --- | --- |
| `task-intake` | Select a formal type, fill its template, preserve the source request and unknowns. | Implemented with five templates and structural/source validation. |
| `author-spec` | Define behavior, scope, constraints, and observable acceptance criteria. | Existing. |
| `author-plan` | Define implementation items, interfaces, dependencies, and verification. | Existing. |
| `review-spec`, `review-plan` | Independently challenge coverage and feasibility; track findings against revisions. | Existing. |
| `follow-plan` | Implement assigned items, record actual checks, and resolve findings. | Existing. |
| `critical-code-review` | Challenge source and verification claims against acceptance criteria. | Existing. |
| `behavioral-verification` | Design meaningful checks and assess acceptance evidence. | Generalize the existing `go-testing` method; configure language tools separately. |

Load `evidence-based-debugging`, `software-architecture`, `domain-modeling`, and language-specific skills when relevant. Task templates supply type-specific expectations to authoring, implementation, and review. Performance measurement, refactor equivalence, and read-only investigation may warrant dedicated methods; validate those needs through example tasks before creating more skills.

Implementation and review share verification guidance; this adds no workflow stage. Keep readiness in the classifier, authority in workflow policy and human decisions, Git lifecycle in hooks, and metric collection in instrumentation. Share handoff and finding formats across skills.

Next: exercise intake and readiness on representative requests for each type, and generalize verification. The configuration includes typed intake, aligned readiness, and a read-only investigation route. Runtime services remain external dependencies.
