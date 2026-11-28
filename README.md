# Agentic Software Engineering Toolkit

### Three ways to run an agentic software development lifecycle.

![Working design · language agnostic · human approval gates](assets/project-status.png)

Define the outcome, inspect the design, implement bounded work, and verify the result. Choose who drives the process and how much tooling the setting supports.

| Scenario | Who drives it | Tools and artifacts | Start here |
| --- | --- | --- | --- |
| **Factory** | Workflow engine, policies, and human gates | Factory Controls + Monitor; optional Fabric; configured agents, skills, hooks, and execution artifacts. | [Overview](workflows/factory/README.md) · [Setup](workflows/factory/SETUP.md) |
| **Human Is the Loop** | You assign work, evaluate evidence, and authorize each transition | Pi, your skills and project tools, Git worktrees; `spec.md`, `plan.md`, `progress.md`. | [Workflow](workflows/human-in-the-loop/README.md) · [Setup](workflows/human-in-the-loop/SETUP.md) |
| **AI coding interview** | You solve and explain the problem with permitted AI assistance | Pi or Claude in the supplied environment; one lightweight `task.md`. | [Workflow](workflows/interview/README.md) · [Printable cheat sheet](workflows/interview/cheat-sheet.pdf) |

## Repository layout

```text
workflows/
  factory/
    factory.yaml        reference workflow configuration
    install.sh          Controls + Monitor installer
    package*.json       Factory SDK / adapter dependencies
    agents/             worker bundles and per-agent installers
    classifiers/        task-readiness classifier
    scripts/            engine lifecycle hooks
    skills/             Factory hook guidance
    diagrams/           workflow diagrams
    README.md           overview, with setup and design alongside
  human-in-the-loop/    Pi workflow, setup, Markdown templates
  interview/            interview workflow and printable cheat sheet
skills/                 shared engineering methods and their bundled tools
assets/                 shared repository visuals
```

Factory-only configuration, dependencies, installation, and runtime resources live in `workflows/factory/`. Shared skills stay at the root and are linked into worker bundles. Agent-invoked scripts belong inside their owning skill; see [Factory script ownership](workflows/factory/scripts/README.md).

## Shared engineering contract

```text
INTENT     → agreed behavior and observable acceptance criteria
DESIGN     → implementation tasks with explicit verification
EXECUTION  → bounded changes and actual evidence
ACCEPTANCE → your decision about whether the result satisfies the task
```

Bug fixes demonstrate correction. Refactors demonstrate preservation. Performance work demonstrates measured improvement. Investigations produce supported conclusions and limitations. Reuse the [task-type guidance](skills/task-intake/references/task-briefs.md) without requiring every scenario to run a classifier.

## Shared capabilities

| Skill | Use |
| --- | --- |
| [Project verification](skills/project-verification/SKILL.md) | Establish or run real-interface verification with owned resources and persistent evidence. |
| [CI diagnostics](skills/ci-diagnostics/SKILL.md) | Inspect GitHub Actions failures and distinguish pending/unavailable checks from success. |
| [Performance measurement](skills/performance-measurement/SKILL.md) | Compare actual workloads, correctness, completed work, variation, and resource limits. |
| [Debugging](skills/evidence-based-debugging/SKILL.md) | Reproduce and minimize failures; discriminate causes with evidence. |
| [Code review](skills/critical-code-review/SKILL.md) | Challenge correctness and indirect-contract safety with concrete scenarios. |

Agent-called scripts stay inside their owning skill. Target-project [manual](workflows/human-in-the-loop/templates/AGENTS.md.template) and [interview](workflows/interview/templates/AGENTS.md.template) instruction templates are opt-in: merge verified project facts into existing guidance rather than copying task state or overwriting instructions. Factory worker roles remain in their bundles.

## The Pragma toolkit

| Component | Repository | Responsibility |
| --- | --- | --- |
| Runtime | [factory-controller](https://github.com/PragmaEngineering/factory-controller) | Workflow execution, routing, human decisions, and CLI. |
| Operator UI | [factory-monitor](https://github.com/PragmaEngineering/factory-monitor) | Execution graphs, messages, findings, and decisions. |
| Optional delegation | [factory-fabric](https://github.com/PragmaEngineering/factory-fabric) | Capability discovery and asynchronous specialist calls. |
| Registry | [factory-registry](https://github.com/PragmaEngineering/factory-registry) | Reference configurations, agents, and skills. |

The manual and interview workflows do not require Factory or Fabric. The Factory scenario documents the existing integration boundaries; Fabric is optional, not a replacement for workflow authority.
