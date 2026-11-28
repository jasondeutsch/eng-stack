# Working in ai-eng

This repository contains reusable engineering methods and three workflow scenarios. Start with README.md and preserve the distinction between them.

- Shared methods and agent-called helpers belong in skills/<name>/, with scripts bundled beside their owning skill.
- Factory-only configuration, dependencies, agents, hooks, and installers belong in workflows/factory/.
- Human-driven Pi documentation/templates belong in workflows/human-in-the-loop/; interview material belongs in workflows/interview/.
- Keep one canonical document per purpose. Repair relative links, imports, and skill symlinks when moving files.
- Do not add a repository test suite. Exercise changed helpers in disposable temporary workspaces; check syntax, links, and observable behavior appropriate to the change.
- Preserve source attribution, reviewed revisions, and required license notices for borrowed material.
- Do not install these skills globally, change credentials, start Factory services, or modify another project as a side effect of maintaining this repo.

Workflow AGENTS.md.template files are opt-in target-project examples. They do not define the policy for editing this repository and must not be installed over existing project guidance.
