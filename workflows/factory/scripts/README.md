# Factory scripts

The Factory runtime calls these scripts through lifecycle hooks in [factory.yaml](../factory.yaml). Agents do not invoke them.

This directory is for Factory-invoked scripts. Scripts invoked by agents must be bundled with their owning skill, under `skills/<skill-name>/scripts/`, alongside the instructions for using them.

Factory controls when these hooks run:

- Before execution: prepare the worktree.
- After design approval and final acceptance: commit project changes.
- After successful execution: release the worktree while retaining its files and branch.

| Utility | Responsibility |
|---|---|
| [git-worktree.py](git-worktree.py) | Prepare one worktree and branch per execution; `--release` retains both after success |
| [git-commit.py](git-commit.py) | Commit explicit workspace paths with deterministic Conventional Commit subjects and participant trailers |

Both read the [version 1 hook context](https://github.com/PragmaEngineering/factory-controller/blob/main/docs/hooks.md#standard-input). They require Python 3.9+ and Git on Unix; the committer preserves normal Git identity, hooks and signing. No utility pushes, merges, resets or force-deletes work. Paths/identity conflicts fail rather than adopting unrelated state.

Use [declared factory variables](https://github.com/PragmaEngineering/factory-controller/blob/main/docs/execution-files.md) to supply repository/workspace arguments consistently. Hook arguments resolve beside factory.yaml. Pass `--workspace` to the committer; agents independently accept the same directory through their launcher. Controls invokes commands and stores execution data; the utilities own Git behavior.

[Worktree guidance](../skills/git-worktree/SKILL.md) covers retries, release and cleanup. [Commit guidance](../skills/git-commit/SKILL.md) covers attribution and staging. Documents and evidence live under the execution files directory, outside the worktree's source commits. Keep the selected utility revision installed for the execution lifetime: utility scripts are not copied with hook settings.
