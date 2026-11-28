---
name: ci-diagnostics
description: Inspect GitHub PR checks and GitHub Actions logs, distinguish failed from pending or unavailable checks, and produce a scoped diagnosis with source evidence. Use when a PR's CI is failing or its check status is unclear.
license: Apache-2.0
---

# Diagnose CI

Use authenticated `gh` and Python 3.10+ from the assigned repository/worktree. Do not install tools, change credentials, rerun workflows, push changes, or widen permissions merely to obtain a green result. Missing access is a diagnostic limitation.

```sh
python /path/to/ci-diagnostics/scripts/inspect-pr-checks.py --help
python /path/to/ci-diagnostics/scripts/inspect-pr-checks.py \
  --repo /absolute/task-worktree --pr 123 --json
```

The helper reads PR metadata and all reported checks, then fetches bounded output excerpts for failed GitHub Actions checks. External providers are reported by URL only. It records the PR head and run metadata when available; a different run SHA may represent a merge revision, so inspect provenance before attributing the failure to current source.

| Exit | Meaning |
| --- | --- |
| 0 | A nonempty reported check set is entirely successful. |
| 1 | At least one reported check failed; diagnostics may still have gaps. |
| 2 | No checks, pending/skipped/unknown checks without a failure, unavailable access/data, or a diagnostic error. |

JSON includes every check's state and available failure diagnostics. Skipped/neutral checks are explicit, not treated as failures or proof of completion. A successful snapshot does not prove required checks are all present, branch protection is satisfied, or the task is accepted. Do not poll indefinitely; report a pending state and let the workflow/human decide when to check again.

Read relevant configuration, changed source, and actual failure excerpts. Distinguish an application assertion failure from dependency, runner, configuration, permission, provider, or flaky-test failures. A log excerpt is a lead, not a root cause. Use the existing debugging method for further diagnosis; do not label a failure flaky just because a retry passes.

Return the PR/head, failing job and run URL, evidence, supported cause or hypothesis, smallest proposed repair, verification method, and missing evidence. Review/redact log excerpts before writing them into task documents or sharing them. Route repairs through existing task authorization; record actual results in the assigned progress/result artifact. Recheck the relevant new run after an authorized repair.

[Source revision and modifications](SOURCES.md); retained [Apache license](LICENSE).
