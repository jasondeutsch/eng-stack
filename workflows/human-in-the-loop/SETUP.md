# Set up Human Is the Loop

[Workflow](README.md) · [Templates](templates/) · [Repository scenarios](../../README.md)

This macOS setup uses Pi directly with this repository's skills. Factory services, worker installers, SDK packages, and `npm install` in ai-eng are not needed.

## Pi and project tools

Use an existing Pi installation when available:

```sh
command -v git
pi --version
pi --help
```

If Pi is absent, use its [official installer](https://github.com/earendil-works/pi/tree/main/packages/coding-agent#getting-started):

```sh
curl -fsSL https://pi.dev/install.sh -o /tmp/pi-install.sh
sh /tmp/pi-install.sh
```

Follow the installer's PATH instructions, then verify `pi --version`. This standalone workflow does not impose the Factory adapter's Pi version pin. Do not replace a shared Factory runtime without checking that adapter's requirements.

Install and verify the target project's actual compiler, package manager, check tools, and service dependencies using its own setup instructions. Nothing here requires a particular language. Keep credentials in Pi/provider configuration or the environment, not task documents.

## Locate the shared skills

Use your existing checkout. For a new machine, clone the repository from `main`:

```sh
git clone --branch main https://github.com/jasondeutsch/eng-stack.git ai-eng
cd ai-eng
export AI_ENG_DIR="$(pwd -P)"
```

For an existing checkout, set `AI_ENG_DIR` to its absolute path instead. Keep the variable available in each terminal used for the workflow. Reference skills in place; do not copy them into every project.

## Authenticate and check skill access

From the target project:

```sh
pi --skill "$AI_ENG_DIR/skills/evidence-based-debugging"
```

Use `/login` to connect an available provider when needed. Choose the model in Pi; model/provider selection is not part of this workflow. Ask Pi to read the debugging skill and summarize its failure-diagnosis method without editing files. Confirm there is no missing-skill or provider error, then exit. Explicit `--skill` paths make a skill available; stage prompts explicitly request reading the relevant methods. [Pi skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md)

## Standing project instructions

Optionally adapt [AGENTS.md.template](templates/AGENTS.md.template) into the target project's root AGENTS.md. Merge with existing guidance; do not overwrite it or a more specific instruction file. Fill in actual project commands and boundaries, remove placeholders, and have the agent confirm which applicable guidance it read. Keep task IDs, absolute worktree paths, approval revisions, and progress in the assignment/task documents, not this standing file. Pi discovers context files from its working directory and parents; see [configuration](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/configuration.md#context-files).

The template preserves the manual workflow's one-task authorization and Markdown assignments. Do not install it into a Factory-run project as a generic policy: Factory's engine and worker assignments own those transitions. The separate [interview template](../interview/templates/AGENTS.md.template) is smaller and optional when the setting permits it.

## Optional verification and diagnostic tools

The shared helpers require Python 3.10+; CI diagnostics also requires authenticated [GitHub CLI](https://cli.github.com/manual/). Provision those on the operator's machine only when using the capability. No new Python package is required by either helper. Browser/API/CLI automation continues to use the target project's own tools.

For a project without a repeatable application check, load `--skill "$AI_ENG_DIR/skills/project-verification"` in an assigned discovery session. Ask it to inspect setup and propose a project-local verification skill; authoring or running that procedure must stay within the assignment. The output belongs in the target project's `.agents/skills/verify-<project>/`, with its own helpers. Read it and run one real scenario before treating it as usable; record an unexecuted procedure as a draft.

## Prepare the first task

From the target repository, check its current work and create an independent worktree:

```sh
git status --short
git worktree list
git worktree add -b task/123 ../project-123 main
cd ../project-123
mkdir -p docs/tasks/123
pwd -P
```

Replace the ID, paths, and base branch. Existing uncommitted changes in the original checkout are not copied. Record the absolute worktree path and branch. If any task documents already exist, inspect and reuse them; do not overwrite them with templates.

For a new task directory:

```sh
cp -n "$AI_ENG_DIR/workflows/human-in-the-loop/templates/"*.md docs/tasks/123/
```

Start with the [specification assignment](README.md#specify-and-plan). Launch Pi from this worktree, use the stage-specific skill flags, and supply the original request. The workflow prompts select Markdown explicitly; they override the shared authoring skills' HTML presentation defaults without modifying those skills.

## Scripts and resource ownership

The [Factory scripts](../factory/scripts/README.md) directory contains Factory hooks that expect engine context. Do not invoke those hooks from manual Pi assignments. Use ordinary Git commands for this workflow's lifecycle. Agents may invoke a script bundled inside an assigned skill when its instructions require it; HTML renderers are unnecessary for these Markdown artifacts.

Keep extensions and MCP services you need for project work. Reviewer commands in the workflow disable extensions and allow only reading/search tools for design review. Code-review commands permit Bash for checks; they do not create a filesystem sandbox.

Pi command behavior can vary by installed version. Check `pi --help` against the [CLI reference](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/cli.md), especially before reusing a Factory-pinned installation.
