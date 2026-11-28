---
name: performance-measurement
description: Design, run, or assess performance comparisons using declared workloads, correctness checks, comparable environments, repeated measurements, and explicit uncertainty. Use for measured regressions, optimization claims, or benchmark-based choices.
license: MIT
---

# Measure performance

State the proposed claim before measuring: operation, workload, metric/unit, baseline, candidate, and target or decision. Inspect the measurement command to establish what it times, counts, and excludes. Unknown measurements remain unknown; do not infer a baseline from code.

## Make the comparison meaningful

- Use equivalent data, build modes, runtime versions, concurrency, caching policy, and relevant tuning. Record source revisions, commands, machine/environment, and competing load. If the sides are not comparable, describe what was actually compared.
- Confirm work occurs inside the timed region and its results are consumed. Count failures, rejected requests, timeouts, retries, and completed work. Verify output correctness: fast errors, cached no-ops, and missing work are not performance wins.
- Use an untimed profiling run when needed to identify the limiting resource or hot path. Profiling overhead does not belong in reported timings. Check the claim against physical limits and the fraction of total time the changed part occupies.
- Warm up when appropriate, alternate baseline and candidate, and repeat enough to expose variation. Five runs per side is a starting point for a decision, not a statistical guarantee. Report run count, median and spread; use the project's established statistical method for a close comparison. A single ballpark run must be labelled as such and cannot decide a close winner.
- Include the relevant end-to-end user path when claiming user benefit. Report microbenchmarks as a component of that path, not a substitute for it. Declare resource, correctness, or compatibility tradeoffs.

Prefer existing project benchmarks and profilers. Use the host's actual tools: macOS does not supply Linux-specific `nproc`, `pidstat`, or `perf` by default. Missing tools or access are limitations, not permission to install software or change shared services. Bound optimization by the assigned objective and budget; this skill does not authorize an autonomous hill-climbing loop.

## Report

Give a verdict: faster, slower, no measurable difference, or inconclusive. Include baseline/candidate source state, workload, environment, exact commands, measurements with units, run count/spread, completed-work/error counts, output correctness, and the limiter when established. Link raw run evidence from the assigned progress/result artifact; separate expected targets from observed results. If variation or confounding prevents a conclusion, say what additional measurement would discriminate it.

Keep the primary outcome concise. Do not bury a failed correctness check behind a favorable latency number.

[Source and adaptation](SOURCES.md); retained [MIT notice](LICENSE).
