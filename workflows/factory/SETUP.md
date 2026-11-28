# Factory setup

[Workflow](README.md) · [Repository scenarios](../../README.md)

Run the commands below from `workflows/factory/` in the ai-eng checkout: `cd workflows/factory`. Requires Git, Go, Node.js, and npm; this installs the Factory system separately from your project's workflow.

## Install Controls and Monitor

```sh
./install.sh
export PATH="$HOME/.local/bin:$PATH"
```

The installer follows `main`, builds Controls and Monitor, and verifies the installed commands. Use `./install.sh --prefix /path/to/install` for another prefix. Re-running updates clean `main` checkouts and rebuilds both components. It does not start services.

## Define a project workflow

Create `factory.yaml` in your target project using the [configuration reference](https://github.com/PragmaEngineering/factory-controller/blob/main/docs/factory-yaml.md). This repository's [factory.yaml](factory.yaml) is one reference, not an installation requirement.

Provision the selected [agent bundles](agents/README.md) with their `install.macos.sh` files and configure provider credentials before starting the service. The per-agent installer installs this directory's SDK/adapter dependencies; do not run npm from the repository root. Keep shared root skills accessible through the bundle links. The reference configuration's `stack_root: .` resolves beside this factory.yaml. If copying the configuration into a project, set `stack_root` to the absolute path of this `workflows/factory/` directory and configure the workspace for that project.

## Project guidance and optional helpers

Keep target-project AGENTS.md focused on project facts, commands, boundaries, and conventions. Factory roles live in `agents/<bundle>/agent.md`; assignments, workflow state, and approval authority remain engine-owned. Do not install the manual/interview AGENTS templates into a Factory workflow: their stop-for-human rules are scenario-specific.

The optional shared server/CI helpers require Python 3.10+. CI inspection also requires operator-provisioned `gh` authentication for the repository. Agent installers do not configure those credentials or install optional helper prerequisites; provision them when selecting the capability. Workers must report unavailable tools instead of installing them during a task.

## Start and submit

```sh
factory start
factory monitor start -d
factory exec "Your task" -c /path/to/project/factory.yaml
```

Open the URL printed by Monitor to inspect execution and handle configured decisions. `factory stop --all` stops both services.

Fabric is a separate optional integration. See [factory-fabric](https://github.com/PragmaEngineering/factory-fabric) when a workflow needs its capabilities; neither this installer nor the reference configuration provisions a Fabric integration.
