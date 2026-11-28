# Human Is the Loop: AI Coding Interviews

[Printable cheat sheet (PDF)](cheat-sheet.pdf) · [Other scenarios](../../README.md)

Use Pi or Claude Code to solve the interview problem while you explain the reasoning, inspect changes, and decide what happens next. Confirm permitted AI assistance and submission requirements with the interviewer. Use the supplied environment; no skill installation is required.

**Clarify → task.md → your approval → one implementation task → feedback → verify and demonstrate.**

If repository instruction files are permitted, the optional [AGENTS.md template](templates/AGENTS.md.template) supplies short standing guidance. Merge it with existing project instructions and fill verified commands; keep authorization and current results in task.md. No template or shared skill installation is required to use this interview workflow.

## Establish the workspace

Use the supplied checkout. If a separate worktree is appropriate, start from the agreed base:

```sh
git worktree add -b interview/123 ../project-interview main
cd ../project-interview
```

Replace the branch and paths as needed. Record the absolute workspace path from `pwd -P` and the expected branch. Launch agents from there. Keep one active writer; settle tool activity before handing work to another session. Worktrees isolate working files and indexes, not access to the host filesystem.

Keep one `task.md` at the workspace root, unless project instructions specify another location or the file already exists. It holds the specification, plan, and a short checkpoint. Use an existing suitable task document rather than overwriting it or creating competing copies.

## Clarify and draft

Choose one author:

| Agent | Start from the interview workspace |
| --- | --- |
| Pi | `pi --name interview-design` |
| Claude Code | `claude --name interview-design --permission-mode plan` |

Claude's Plan Mode is useful for investigation and discussion. Leave it before requesting file writes. Its native plan does not replace the agreed task document. [Claude Plan Mode](https://code.claude.com/docs/en/common-workflows#plan-before-editing)

Give the agent the original question and this prompt, replacing the workspace details:

```text
Workspace: /absolute/path/to/project-interview
Expected branch: interview/123
Confirm and report your working directory, Git worktree root, and branch.
Stop if they differ from this assignment. Keep repository work in this workspace.

Inspect the supplied instructions and relevant code. Identify questions that change
required behavior, scope, or compatibility. Ask before settling those decisions.
Draft task.md using the template below. Keep it brief; omit inapplicable sections.
Do not invent requirements, repository facts, or results. Do not implement or commit.
Stop for my review and approval.

# [Task title]
Design revision: 1

## Spec
### Problem
[Required change. For a bug: reproduction, observed behavior, and expected behavior.]
### Acceptance criteria
- AC-001: [Observable outcome, including a concrete example where useful.]
### Constraints and exclusions
[Required interfaces, compatibility, limits, and behavior outside scope.]
### Open questions and assumptions
[Consequential uncertainty requiring confirmation.]

## Plan
### Approach
[Chosen algorithm/design, affected files, tradeoffs, and complexity where relevant.]
### Tasks
| ID | Outcome / intended changes | Depends on | Acceptance | Verification |
| --- | --- | --- | --- | --- |
| P-001 | [Coherent result] | — | AC-001 | [Check and expected result] |

## Progress
Approved design revision: none
Authorized task: none
Status: awaiting design approval
Feedback / decisions: none
Actual checks and results: none
Open findings / blockers: none
Next action: human review
```

The specification draws on [GitHub Spec Kit](https://github.com/github/spec-kit/blob/main/templates/spec-template.md); the plan draws on [Superpowers](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md). The combined file and smaller template are adaptations for this interview workflow. Keep tasks meaningful and verifiable; do not turn every edit into its own task. Drafting should help you explain the solution, not become a separate deliverable to polish.

Read `task.md` in your editor and explain the approach to the interviewer. Check the examples, edge cases, and verification yourself. Resolve important questions before approving the design.

## Review and approve

For a short exercise, review the design directly with the interviewer. When complexity and time justify another review, pause the author and launch a fresh session:

| Reviewer | Start from the same workspace |
| --- | --- |
| Claude Code | `claude --name interview-design-review --permission-mode plan` |
| Pi | `pi --name interview-design-review --no-extensions --tools read,grep,find,ls @task.md` |

Give it the original question as well as the document:

```text
Read task.md and the original interview problem. Compare them with the supplied code.
Check ambiguous or contradictory behavior, unsupported assumptions, algorithm/data choices,
complexity claims, task dependencies, and AC-to-task-to-verification coverage.
Report only material F- findings with location, counterexample or evidence, and correction needed.
Do not invent additional requirements, edit files, or implement. A clean review is valid.
```

This review adapts [GitHub Spec Kit — Analyze](https://github.com/github/spec-kit/blob/main/templates/commands/analyze.md). Judge findings yourself, return accepted corrections to the author, and recheck them. Approve a specific design revision and authorize one P- task explicitly. Approval of the plan does not authorize executing the entire plan.

## Implement one task

Continue with the author or start a new session in the same workspace:

| Agent | Start |
| --- | --- |
| Pi | `pi --name interview-build @task.md` |
| Claude Code | `claude --name interview-build --permission-mode default` |

Use this assignment, adapted from the [Superpowers implementer prompt](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/implementer-prompt.md):

```text
Authorized workspace: /absolute/path/to/project-interview
Expected branch: interview/123
Before editing, confirm and report your absolute working directory, Git worktree root,
and branch. Stop if they differ. Keep repository reads, edits, and checks here.
Do not switch branches, modify another checkout, or delegate.

Read task.md, including Progress. I approve design revision 1 and authorize P-001 only.
Confirm its prerequisites are satisfied. Use existing project patterns and tools.
Explain important decisions concisely. Raise blocking ambiguity or a required design change.
Implement and verify this task; inspect your diff for missing or unintended behavior.
Update Progress with my approval and authorized P-ID, changes, actual commands/results,
open findings, and next action: waiting for human feedback. Preserve earlier decisions
and relevant evidence. Distinguish an expected reproduction failure from an unfixed defect.
Report results, then stop. Do not start another P- task, change requirements, or commit.
Only my explicit instruction authorizes the next task.
```

Inspect the changes and actual results. Explain the important code yourself. Request corrections to the same task or authorize the next one:

```text
P-001 is accepted. Implement P-002 only under the same workspace and approval constraints.
Update Progress with the results, then stop and wait for my feedback.
```

If the approach changes, revise the Spec and Plan, increment the design revision, and confirm the new direction before proceeding. Keep intended verification in the plan and actual results in Progress. These prompts govern behavior; enforcing filesystem boundaries requires permissions or a sandbox.

## Verify and demonstrate

Inspect the complete task change, including new and uncommitted files. Exercise representative, boundary, and failure cases. Check that assertions establish the ACs, rather than merely showing a successful exit. Explain complexity and tradeoffs where relevant.

If time permits a fresh code review, pause the author and launch Claude in a new session or Pi with `--no-extensions --tools read,bash,grep,find,ls`. Give it the original question and this prompt, adapted from [Anthropic — Code Reviewer](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/feature-dev/agents/code-reviewer.md):

```text
Read task.md. Review the complete task change against the approved Spec and Plan,
including committed, staged, unstaged, and new files relative to the agreed base.
Find concrete correctness, edge-case, complexity, or acceptance-coverage defects.
Inspect assertions and affected callers; run focused checks where useful.
Report F- findings with severity, locations, triggering examples, and evidence.
Separate observed results from author claims. Skip style preferences; a clean review is valid.
Do not edit, repair, delegate, or commit. Return findings to me.
```

Shell verification can write; this review assignment is not a filesystem sandbox. Evaluate findings, ask the author for specific repairs and verification, then recheck affected behavior.

Demonstrate the final solution to the interviewer. State remaining limitations and agreed scope reductions. Submit or commit only as the interview requires. Avoid spending the remaining round on local branch housekeeping.

## Pause, resume, or hand off

Before stopping, ask the author to update Progress with the current authorization, completed tasks, your feedback, actual checks, open issues, and next action. Keep a short current checkpoint, not a transcript; link substantial evidence instead of copying logs. Persistent notes support continuity across context resets. [Anthropic: structured note-taking](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

Resume the recorded session with `pi --resume` or `claude --resume interview-build` (use the design session name if you continued with that author). Instruct the agent to read `task.md`, repeat the workspace/root/branch check, and reconcile Progress with actual files before editing. A new agent needs the original brief, workspace path, expected branch, task document, and explicit current authorization. Session memory supplements this checkpoint.

If you created a worktree and a local merge is required, first commit accepted changes on the interview branch. From a clean target checkout:

```sh
cd ../project
git switch main
git merge --no-ff --no-commit interview/123
```

Verify the combined result in this target checkout before committing the merge. Resolve any failures first, or use `git merge --abort` to abandon it. After acceptance, stop task-owned processes and preserve required evidence before cleanup:

```sh
git commit -m "Merge interview/123"
git worktree remove ../project-interview
git branch -d interview/123
```

For sustained work with your installed skills and project tools, use the separate [Human Is the Loop: Agentic SDLC](../human-in-the-loop/README.md).
