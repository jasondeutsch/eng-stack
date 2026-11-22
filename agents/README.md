# Factory agents

The workflow selects these bundles through `packages[].path` in [factory.yaml](../factory.yaml). Each owns its launcher, native Pi profile, instructions, and relative links to canonical [skills](../skills/).

| Bundle | Responsibility | macOS setup |
| --- | --- | --- |
| [task_intake](task_intake/agent.md) | Typed task and source-preserving intake. | [install.macos.sh](task_intake/install.macos.sh) |
| [investigator](investigator/agent.md) | Read-only investigation and evidence report. | [install.macos.sh](investigator/install.macos.sh) |
| [architect](architect/agent.md) | Specification and plan. | [install.macos.sh](architect/install.macos.sh) |
| [architecture_reviewer](architecture_reviewer/agent.md) | Independent design review. | [install.macos.sh](architecture_reviewer/install.macos.sh) |
| [coder_golang](coder_golang/agent.md) | Initial Go implementation profile, assigned as `implementer`. | [install.macos.sh](coder_golang/install.macos.sh) |
| [code_reviewer_golang](code_reviewer_golang/agent.md) | Initial Go review profile, assigned as `code_reviewer`. | [install.macos.sh](code_reviewer_golang/install.macos.sh) |

Changing language requires selecting compatible bundles and checks in configuration. The review routes and human gates remain defined by the factory. Setup and upstream attribution are in the [project README](../README.md#local-factory).

Install only the agents selected by your workflow. Installers require Homebrew and accept `--prefix DIRECTORY` and `--controls CHECKOUT`; they locate the system installer’s Controls checkout automatically, then fall back to a sibling `controls` checkout. Go tools are installed only for the Go bundles. Installers are operator-run setup; launchers perform checks without installing dependencies.
