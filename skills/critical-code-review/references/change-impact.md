# Change impact beyond the diff

Identify the one or few facts that make a consequential change safe. Trace their actual protections before accepting the author's explanation: pinned library behavior, asynchronous ordering/teardown, serialized data, database columns, wire formats, feature flags, cross-language consumers, and downstream callers that symbol search misses.

For each material risk, distinguish a source citation, an execution-path argument, an executed reproduction/check, and observed application behavior. Prefer the cheapest evidence that resolves the uncertainty. Use existing checks or authorized scratch scripts; a read-only review must not quietly add files to the submitted source or mutate a running shared application. If execution is unavailable, mark the safety assumption unproven rather than claiming a defect without a trigger.

Report the triggering case, affected contract, evidence, consequence, and correction or check needed. Record risks investigated and cleared where that prevents repeated work. Do not turn every hypothetical consumer into a blocker, treat caller count as calibrated risk, or run a multi-model review automatically. Respect the agreed scope and review role.
