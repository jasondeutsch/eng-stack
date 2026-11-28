# Sources and adaptation

- [pstack verification generation](https://github.com/cursor/plugins/blob/b7b93c36be9bcc36a74db438e0fd385d660bc559/pstack/skills/create-verification-skill/SKILL.md) and [maintenance](https://github.com/cursor/plugins/blob/b7b93c36be9bcc36a74db438e0fd385d660bc559/pstack/skills/maintain-verification-skill/SKILL.md) — reviewed revision `b7b93c36be9bcc36a74db438e0fd385d660bc559`. Retained [MIT notice](LICENSE.MIT).
- [Anthropic webapp-testing server helper](https://github.com/anthropics/skills/blob/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/webapp-testing/scripts/with_server.py) — reviewed revision `e4bb5d960d87126ff3b3a8af1a104b7db67560ba`. Retained [Apache-2.0 license](LICENSE.Apache-2.0).

The method preserves real-interface verification, application readiness, resource isolation, evidence surviving cleanup, and distinction between harness drift and product defects. It replaces Cursor-specific paths and automatic agent/PR coordination with assignment-selected target-project skill authoring. Helpers and project facts remain local to their owner.

with-server.py is a rewritten adaptation of the lifecycle concept: occupied-port rejection, optional HTTP readiness, durable logs, bounded command duration, signal handling, and owned process-group cleanup replace the upstream TCP-only/pipe/shell-parent behavior. It requires POSIX and Python 3.10+; it does not provision dependencies or promise readiness from a successful socket connection.
