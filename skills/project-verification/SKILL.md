---
name: project-verification
description: Establish or run a repository-specific procedure that launches the real application, exercises assigned acceptance scenarios, captures observable evidence, and cleans up owned resources. Use when project-level verification is missing or needs to be executed.
license: Apache-2.0 AND MIT
---

# Verify the real project

Use existing project checks and verification instructions first. Identify the assigned surface: CLI, service, browser, library, or desktop application. Find actual launch commands, configuration, data/auth prerequisites, user-visible entry points, readiness signals, and evidence locations from the repository. Ask only about consequential facts you cannot discover. This skill does not authorize tool installation, remote writes, or expanding the task.

## Establish a project procedure

When no adequate procedure exists and authoring is assigned, adapt the [project template](templates/project-verification.md) into the target project's `.agents/skills/verify-<project>/SKILL.md` or its existing skill location. Resolve exact commands and selectors; remove placeholders before handing it over. Keep this shared skill read-only. Store project-specific helpers alongside the generated skill, not in ai-eng or a global scripts directory.

Specify launch, a read-only health check, acceptance scenarios through real interfaces, evidence, isolated resources, and cleanup. A listening port does not establish application readiness; verify required migrations, fixtures, authentication, and a usable endpoint/state. Identify ports, data directories, and browser profiles that cannot be shared between worktrees. Do not adopt someone else's running instance implicitly.

Execute the authored procedure for at least one assigned scenario before calling it usable. If the environment prevents that, deliver a draft with the exact gap. Separate setup/harness failures from product defects. Subsequent runs use the established procedure rather than rediscovering setup. Update it when actual commands or behavior drift; do not rewrite expected outcomes to conceal a product regression.

## Run and preserve evidence

Read the applicable spec, plan, current authorization, and project procedure. Exercise the real public path and inspect outputs and side effects, not only process exit status or an attractive screenshot. Use stable interface handles and observable readiness conditions. In browsers, prefer locator assertions to fixed sleeps or a universal network-idle rule. Do not introduce a new browser stack when the project already has one.

Record source state, workspace, scenario/AC IDs, actions, actual results, and evidence paths in the assigned progress/result artifact. Keep secrets out of records. Report covered, failed, and unverified cases separately. Preserve evidence when cleaning up.

## Local server helper

For macOS/Linux projects that need disposable servers, use the bundled Python 3.10+ helper:

```sh
python /path/to/project-verification/scripts/with-server.py --help
python /path/to/project-verification/scripts/with-server.py \
  --cwd /absolute/task-worktree \
  --server 'npm run dev -- --port 5173' --port 5173 \
  --ready-url http://127.0.0.1:5173/health \
  --log-dir /absolute/evidence \
  -- python path/to/existing-verification.py
```

Repeat `--server`, `--port`, and `--ready-url` for multiple servers. Use actual project commands; the example does not install a package or create a verification program. Omit all URLs only when a TCP check is sufficient for launching the subsequent application-level check. Readiness URLs must be local HTTP endpoints on the corresponding port and return 2xx. The helper rejects already-listening ports; health endpoints and scenario assertions must still identify the correct application/build.

The helper creates a unique evidence directory with server logs, `verification.log`, and `result.json`. It bounds startup and verification duration, passes through the verification exit code, and terminates owned POSIX process groups on success, failure, or interruption. It does not undo database changes or stop resources a daemon moved outside its process group; use project teardown for those. Never use it to drive production. Lifecycle success proves only what the verification command asserts.

[Sources, revisions, and adaptation](SOURCES.md).
