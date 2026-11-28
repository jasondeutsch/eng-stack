---
name: git-commit
description: Create deterministic Conventional Commits at workflow hook boundaries, with execution and multi-agent attribution and duplicate-effect protection.
---

# Workflow commits

Use [commit utility](../../scripts/git-commit.py) as a stage `after` hook, paired with the [execution worktree utility](../git-worktree/SKILL.md). A stage commit includes successful agent invocations across its loops and runs after its configured human gate. For concurrent work, prefer a stage hook so all writers have finished.

```json
{"name":"commit-work","command":"python3","arguments":["/path/to/ai-eng/workflows/factory/scripts/git-commit.py","--workspace","/execution/worktree","--type","chore","--scope","implementation","--description","complete implementation stage","--path","."]}
```

The script generates the Conventional Commit header from explicit arguments, without a model. Trailers identify the execution, hook invocation, stage or step, and each participating agent invocation. Participation is attribution, not proof of authorship, independent review, or human approval. Use the [Conventional Commits skill](../../../../skills/conventional-commits/SKILL.md) for choosing meaningful types and descriptions when authoring configuration.

Choose `--path` deliberately; repeat it for multiple paths. `--path .` explicitly includes every nonignored change in the workspace, including additions and deletions. Paths resolve from the workspace root and cannot escape it; a workspace may be a subdirectory of the enclosing Git repository. Prefer narrower paths where unrelated work may exist. The script cannot infer ownership of shared files, detect every secret, or separate concurrent human edits. Configure ignore rules and review scope before running it. While managed hooks own commits, agents should leave their work unstaged and must not commit independently.

The utility refuses unrelated staged changes, unmerged files, an unexpected branch, and conflicting retries. It preserves normal Git hooks and signing. Hook failures leave the utility's staged tree intact for diagnosis; a retry accepts it only when it matches its recorded tree. Successful retries return the prior commit instead of committing twice. No changed files produces a recorded no-change result rather than an empty commit. A retry of that no-change invocation also remains a no-op; new work requires a new hook invocation.

It never pushes, amends, merges, disables hooks, changes Git identity, or discards working files. Requirements: Python 3 and Git, configured commit identity, and any signing credentials required by the repository.

Use `--workspace` to select the project directory in the prepared worktree while the hook itself starts beside factory.yaml. The utility verifies worktree ownership and refuses commits after release. Workflow documents in execution storage are not staged by project commits.
