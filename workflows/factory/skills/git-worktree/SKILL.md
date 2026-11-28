---
name: git-worktree
description: Configure and diagnose deterministic per-execution Git worktree preparation and release without assigning Git lifecycle operations to agents.
license: MIT
---

# Execution worktrees

Use the [worktree utility](../../scripts/git-worktree.py) as an execution `before` hook. It reads version 1 hook context from stdin; pass `--repository`, `--workspace` and an optional `--base` explicitly. The factory's frozen variables and execution ID determine one worktree path and `execution/<id>` branch. The utility creates both in one operation.

Preparation records the source repository, path, base commit and invocation under Git's common directory. A retry verifies the owned worktree and preserves dirty work; it never resets, stashes, switches the source checkout, adopts an unowned branch/path or silently recreates a missing prepared worktree. Separate executions can use separate active worktrees in the same repository. Uncommitted source changes remain untouched and are not copied.

Pass the same workspace to every agent launcher and the [commit utility](../../scripts/git-commit.py). A factory may use a project subdirectory within the worktree; commit paths are then scoped to that directory. Project source and [execution documents](https://github.com/PragmaEngineering/factory-controller/blob/main/docs/execution-files.md) are separate.

On successful execution, invoke the utility with the same repository/workspace/base arguments and `--release` in an execution `after` hook. Release marks the receipt complete and retains files, branch and history. Failure/cancellation does not run success hooks. Inspect active processes before an explicit release; never remove another active execution's worktree. After inspection, ordinary `git worktree remove PATH` can remove an unneeded clean worktree; branch deletion is a separate deliberate action. This utility has no force-delete or automatic cleanup mode.

[Git's worktree documentation](https://git-scm.com/docs/git-worktree) describes shared repository metadata and independent working checkouts. Worktrees isolate changes between executions, not host privileges or concurrent writers inside one execution.
