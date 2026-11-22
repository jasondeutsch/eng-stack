# Task readiness

Consumes `task` (original execution input) and `typed_task` (intake's named `task` output). The MCP entrypoint requires both. Before calling the provider, it validates the [task contract](../../skills/task-intake/SKILL.md), preserves the original brief/document metadata, and checks captured-document digests. Invalid tasks fail visibly; they never become admission decisions.

The provider assesses `type_match`, `readiness`, and `missing_target` using the original request, captured document contents, and typed task. Its answers are fallible evidence. Template completeness does not imply readiness; discoverable root causes, code locations, and baselines are not required at submission.

## Admission policy

With `overrides.admission: {minimum_probability: 0.85}`, code admits only when the selected type is confirmed, intake has not marked classification uncertain, and readiness chooses `accept` with accept probability at least the threshold. This initial threshold is not a calibrated reliability guarantee.

| Type | Admitted | Human review required |
| --- | --- | --- |
| Bug fix, feature, refactor, performance | `admitted` | `review_required` |
| Investigation | `investigation_admitted` | `investigation_review_required` |

[factory.yaml](../../factory.yaml) owns the routes. Human admission overrides this gate within the selected route; it does not change type or authorize implementation for an investigation. Reject and resubmit when the type/scope must change. The operator's reason remains in accepted history. `admission: null` is advisory and returns `completed`; it needs a workflow configured for that outcome.

Completion returns `data.request` and `data.response` unchanged for downstream bindings. Provider errors, missing credentials, malformed responses, digest changes, or exceeded limits fail the attempt rather than producing an admission outcome.

## Runtime

- `config.json`: provider, model, endpoint, credential variable, limits, optional admission policy. Package overrides select effective settings.
- `questions.json`: type fidelity, readiness, missing target rubric.
- `evaluate.mjs`: contract/digest validation, bounded request, response validation, deterministic admission mapping.
- `run.mjs` and `start.sh`: MCP assignment entrypoint.
- `legacy.mjs`: legacy file/environment compatibility and saved-evaluation replay. Legacy callers may omit typed_task for advisory use; governed factory executions supply it.

OpenRouter Decisions and `typesafe/jev-1.14` are configured defaults. The timeout defaults to 20 seconds and is capped at 120 seconds. Request and response each have a 24,000-byte maximum, including rubric and duplicated source in the typed task; oversized inputs fail without truncation. No hidden provider retry. Structured usage is reported when available; missing usage is unknown. Credentials and provider bodies are not printed to stdout. Agents and scripts run with host-user permissions.

Legacy replay validates saved requests against current inputs/settings before resubmission. MCP completion supports unchanged result retries; it does not automatically repeat an uncertain provider call. Factory pins package/configuration identity; do not edit a bundle during an active execution.
