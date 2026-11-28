# Human Is the Loop: Agentic SDLC

[Setup](SETUP.md) · [Templates](templates/) · [Interview workflow](../interview/README.md) · [Other scenarios](../../README.md)

Drive Pi directly with your skills, project tools, and Git worktrees. You assign work, resolve scope, approve design, evaluate evidence, and integrate changes. No Factory or Fabric is involved.

**Brief → spec and plan → independent design review → your approval → one implementation task → feedback → code review → integration.**

## Workspace and records

Follow [setup](SETUP.md) to configure Pi, locate the shared skills with `AI_ENG_DIR`, and create the task worktree. Examples use branch `task/123`, worktree `/absolute/path/to/project-123`, and task documents under `docs/tasks/123/`. Substitute your actual values before assigning work.

Use one worktree per independent change and one active writer per worktree. Independent tasks may run in parallel in different worktrees; check shared services, ports, generated files, and test data for interference. Pause the author during review. If task B depends on A, wait for integration or explicitly base B on an A checkpoint and record that dependency; revalidate B when A changes. Worktrees do not enforce host access boundaries.

| Artifact | Responsibility |
| --- | --- |
| [spec.md](templates/spec.md) | Original intent, behavior, constraints, task-specific evidence, and observable AC- criteria. |
| [plan.md](templates/plan.md) | Design, consequential decisions, individual P- tasks, dependencies, and intended verification. |
| [progress.md](templates/progress.md) | Approved revisions, currently authorized task, human feedback, actual evidence, findings, and handoff. |

Maintain one canonical copy of each. Increment spec/plan revisions when their content changes; record approval of the exact pair in progress.md. Do not rewrite requirements to justify an implementation. Planned checks belong in the plan; observed results belong in progress.

When managing multiple worktrees, keep a short task register outside their branches:

```text
123 | /absolute/path/to/project-123 | task/123 | implementation
Authorized: P-002 | Pi: project-123-build | next: waiting for human feedback
Documents: /absolute/path/to/project-123/docs/tasks/123/
```

Keep detailed state in progress.md, not duplicated across the register and conversation.

## Select supporting capabilities

| Need | Shared skill / integration |
| --- | --- |
| No repeatable application check, or an assigned real-interface run | [project-verification](../../skills/project-verification/SKILL.md); use existing project procedures first. |
| Failed or unclear GitHub PR checks | [ci-diagnostics](../../skills/ci-diagnostics/SKILL.md); return diagnosis before an unassigned repair. |
| Performance claim or regression | [performance-measurement](../../skills/performance-measurement/SKILL.md); use it in planning, measurement, and review. |

Add the relevant `--skill "$AI_ENG_DIR/skills/<name>"` flag and explicitly request reading it. Pass the project's verification procedure path to implementation and code review when one exists. Loading a skill does not authorize installation, new source changes, or another P-task. Record its actual evidence in progress.md. See [setup](SETUP.md) for prerequisites and optional standing project instructions.

## Specify and plan

From the task worktree:

```sh
pi --name project-123-design \
  --skill "$AI_ENG_DIR/skills/author-spec" \
  --skill "$AI_ENG_DIR/skills/author-plan"
```

Give Pi the original request and the assignment below. These prompts reuse the shared skills' engineering methods. **Markdown templates and paths in this assignment override their HTML presentation instructions:** read and write Markdown directly; do not invoke the HTML renderer. Skills and their bundled scripts remain at the repository root.

```text
Authorized worktree: /absolute/path/to/project-123
Expected branch: task/123
Check and report the absolute working directory, Git root, and branch; stop on mismatch.
Keep repository work here. Read docs/tasks/123/progress.md and the original request.

Resolve AI_ENG_DIR from the environment. Read author-spec and author-plan under its skills/.
Use their engineering methods with the Markdown templates under
AI_ENG_DIR/workflows/human-in-the-loop/templates/. Do not use HTML assets or renderers.
Inspect project instructions, relevant source, callers, checks, and existing decisions.
Ask about unknowns that change required behavior, scope, or compatibility; investigate
repository facts yourself. Separate evidence, hypotheses, and assumptions.

Write docs/tasks/123/spec.md. Define required outcomes, exclusions, material failure cases,
interfaces and constraints, and AC- acceptance criteria. Include the task-specific evidence
called for by the template. Record revision 1. Do not implement or commit.
Update progress.md with unresolved questions and next action: human scope check. Stop.
```

After checking scope, request the plan:

```text
Read the current spec.md and progress.md under docs/tasks/123.
Use author-plan's method with the assigned Markdown plan template; no HTML renderer.
Inspect existing patterns and boundaries. Recommend the smallest adequate design;
explain consequential alternatives and tradeoffs, not routine coding choices.
Write plan.md with revision and spec revision, coherent P- tasks, dependencies, affected
files, interface details, AC coverage, and checks with expected results and prerequisites.
Every AC needs coverage; each task needs a reason to exist and a verifiable outcome.
Keep decisions here unless project rules require separate ADRs.
Update progress.md; stop for independent design review. Do not implement or commit.
```

Use `software-architecture` or `domain-modeling` when the actual design needs those methods. Add only relevant language skills. Small changes need short documents; read-only investigations can end with supported findings and human acceptance without implementation or merging.

## Review and approve the design

Pause the author. Start a fresh Pi session in the same worktree:

```sh
pi --name project-123-design-review \
  --skill "$AI_ENG_DIR/skills/review-spec" \
  --skill "$AI_ENG_DIR/skills/review-plan" \
  --no-extensions --tools read,grep,find,ls
```

Provide the original request independently of the author. Ask:

```text
Read review-spec and review-plan under AI_ENG_DIR/skills. Read Markdown directly;
do not invoke their HTML helper. Review docs/tasks/123/spec.md and plan.md against
the original request, actual repository, and applicable project decisions.
Read progress.md for revisions and prior findings; form an independent assessment.
Check ambiguity, contradictions, unsupported assumptions, missing behavior, unnecessary
scope, interface consistency, dependencies, and AC-to-task-to-verification coverage.
Return consolidated F- findings with severity, reviewed revision/location, evidence,
triggering case, impact, and correction needed. Separate spec defects from plan defects.
A clean review is valid. Do not edit documents or source, delegate, or commit.
```

You record confirmed findings in progress.md and assign revisions to the author. The reviewer rechecks actual changed sections and unresolved findings, retaining valid evidence. Do not loop for cosmetic preferences. If review stops producing new evidence, decide the unresolved issue or narrow the task.

Approve only when behavior and design are acceptable and tasks are executable. Record the exact spec/plan revisions and agreed limitations. Review agreement is a recommendation; your approval authorizes the next stage.

## Implement one task, then get feedback

Start or resume the implementation owner in the task worktree:

```sh
pi --name project-123-build \
  --skill "$AI_ENG_DIR/skills/follow-plan"
```

Add a relevant project/language skill with another `--skill` flag. For a diagnosed failure, use `evidence-based-debugging`; do not repeat identical attempts without new evidence.

```text
Authorized worktree: /absolute/path/to/project-123
Expected branch: task/123
Before editing, check and report working directory, Git root, and branch; stop on mismatch.
Keep repository reads, edits, and verification here. The shared skill library is read-only.
Do not switch branches, modify another checkout, create a worktree, or delegate.

Read follow-plan under AI_ENG_DIR/skills and docs/tasks/123/{spec.md,plan.md,progress.md}.
These artifacts are Markdown; do not use HTML helpers. I approve spec revision 1 and
plan revision 1, and authorize P-001 only. Confirm revisions and prerequisites match.
Implement that task using project conventions and its verification method.
Read the existing project verification procedure if assigned; use performance-measurement
for a performance task and ci-diagnostics for an assigned CI failure. Do not bootstrap
a new harness or expand the repair without authorization.
Raise blocking ambiguity or any required scope/design decision before proceeding.
Self-review for missing requirements, unintended changes, and ineffective assertions.

Update progress.md, preserving approvals and useful evidence. Record authorization,
changes/files, actual commands and results with relevant source state, AC coverage,
findings, and remaining uncertainty. A reproduction task may correctly demonstrate a failure;
explain that outcome without claiming the defect is fixed.
Report results and stop for my feedback. Do not commit or begin another P- task.
Only my explicit instruction authorizes continuation.
```

Inspect the diff and evidence. Request corrections to the same task, or explicitly advance:

```text
P-001 is accepted. Implement P-002 only under the same worktree and approval constraints.
Record the authorization and results in progress.md, then stop for my feedback.
```

Plan approval, passing checks, and native agent task lists do not authorize another task. If design changes, return to revision/review and approve the new document pair. A prompt guides behavior; use permissions or a sandbox when access boundaries must be enforced.

## Review the implementation

Pause the author. Start a fresh reviewer:

```sh
pi --name project-123-code-review \
  --skill "$AI_ENG_DIR/skills/critical-code-review" \
  --no-extensions --tools read,bash,grep,find,ls
```

Bash enables verification and can write. The reviewer assignment prohibits modifying source; the command is not a filesystem sandbox.

```text
Read critical-code-review under AI_ENG_DIR/skills, the original brief, and current
spec.md, plan.md, and progress.md under docs/tasks/123. Read Markdown directly.
Review the complete task change against its recorded base, including committed, staged,
unstaged, and new files. Report the base and source state reviewed; flag unavailable evidence.
Trace affected callers, contracts, failure paths, and compatibility. Check AC coverage
and whether assertions actually establish behavior. Run focused existing checks as useful.
Report actionable F- findings with severity, file/line, triggering scenario, evidence,
consequence, and required correction. Distinguish observed results from author claims;
mark unverified risks explicitly. A clean review is valid; skip preference-only changes.
Do not edit source or documents, repair findings, delegate, or commit. Return findings to me.
```

Return confirmed findings to the author by ID. Require a correction with evidence, counterevidence, or an explicit blocker. Recheck affected behavior and remaining ACs. You decide ready to integrate, needs changes, or blocked. An incomplete criterion stays open unless you explicitly change scope.

## Commit and integrate

After acceptance, authorize the implementation owner to commit reviewed changes and the agreed task documents. Inspect included files, then stop its writes. Follow the project's PR process where required. For a local merge, use a clean target checkout:

```sh
cd ../project
git switch main
git merge --no-ff --no-commit task/123
```

Resolve conflicts against intended behavior. Launch Pi in this **target checkout** to verify the combined result:

```text
Read the approved task documents. Verify the pending merge against acceptance criteria
and affected behavior, accounting for changes now on main. Report actual commands/results
and unresolved failures. Do not edit source or commit the merge.
```

Task-worktree evidence does not verify the merged state. Resolve failures before completing the merge; `git merge --abort` abandons it. After acceptance:

```sh
git commit -m "Merge task/123"
git worktree remove ../project-123
git branch -d task/123
```

Stop task-owned processes and preserve needed evidence before cleanup. If already merged, skip the merge commit. Record where work landed and agreed follow-up in the external task register.

## Pause and resume

At a task boundary, have the author update progress.md with the current authorization, approvals, useful evidence, open findings, running processes, and next action. Keep one active writer; reviewers return findings to you rather than racing to update the shared checkpoint.

From the intended worktree, use `pi --resume` and select its recorded session. Pi resumes a session in its stored working directory, which may differ from your terminal's directory. Before edits, repeat the worktree/root/branch check, read the current documents, and reconcile progress with actual files. [Pi sessions](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/sessions.md)

For a fresh session, provide the original brief, absolute worktree path, expected branch, document paths, and currently authorized P-ID. Conversation history and compaction supplement the checkpoint. Do not infer authorization from an agent's proposed next action.

## Prompt sources

These are adaptations for a human-driven Pi workflow, not a published benchmark of this combination:

- Specification: [GitHub Spec Kit — Specify](https://github.com/github/spec-kit/blob/main/templates/commands/specify.md).
- Design and task planning: [Anthropic — Code Architect](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/feature-dev/agents/code-architect.md), [Superpowers — Writing Plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md), and [Spec Kit — Tasks](https://github.com/github/spec-kit/blob/main/templates/commands/tasks.md).
- Design review: [Spec Kit — Analyze](https://github.com/github/spec-kit/blob/main/templates/commands/analyze.md).
- Implementation: [Superpowers implementer](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/implementer-prompt.md).
- Code review: [Anthropic — Code Reviewer](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/feature-dev/agents/code-reviewer.md).

Adaptations retain the engineering methods, use local Markdown artifacts, and give assignment, approvals, review scheduling, and integration to you. They omit upstream trackers, hooks, automatic delegation, commits, and numerical confidence cutoffs.
