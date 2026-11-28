---
name: evidence-based-debugging
description: Investigate failed checks, runtime errors, and contradictory behavior with minimized reproductions, discriminating experiments, and preserved evidence; distinguish product defects from environment or tooling failures.
license: MIT
---

# Evidence-based debugging

Capture the failing command or action, working directory, relevant versions, exit status, and useful error output. Preserve the original evidence before changing configuration. Keep credentials out of task records; refer to private diagnostics when output is sensitive.

State what the evidence establishes and what remains a hypothesis. Trace the failure to its owning layer: application, agent, tool, provider, permissions, network, or host configuration. A failed check is not automatically a product defect, and a successful retry does not establish a root cause.

Choose the smallest observation or reproduction that distinguishes plausible causes. Change one relevant factor at a time and explain why it should affect the failure. Use the project's existing diagnostic tools; do not install packages, change global configuration, disable certificate validation, or widen permissions merely to make the failure disappear.

Prefer a rerunnable check that exercises the reported symptom and can fail for that defect, not merely a command that exits successfully. Start from existing checks or real API/CLI/UI behavior. Capture the original failure, then reduce inputs, configuration, and steps one factor at a time while retaining it. Pin relevant clocks, randomness, fixtures, or environment state when practical. For intermittent failures, record attempts and failure frequency instead of claiming determinism.

Choose the technique that discriminates the current hypotheses: replay a redacted trace, compare old/new behavior on the same input, use an invariant/property where the behavior has that shape, or run bisection when known good/bad revisions and an automated verdict exist. Do not bisect a dirty/shared checkout; use a separately authorized workspace. If reproduction or safe instrumentation is unavailable, state that gap and the evidence/access needed. Do not turn difficulty reproducing into permission to mutate a live system.

Verify the relevant behavior after a fix. Record the original failure, supported cause, change, verification, and remaining uncertainty. Reviewers return repair requests to the implementation owner unless explicitly assigned the repair.

Stop when the same failure repeats without new evidence or a different justified approach. Report the blocker and the specific information or decision needed instead of consuming more retries. Preserve partial work so another session can continue.

[Adaptation source and retained notice](SOURCES.md).
