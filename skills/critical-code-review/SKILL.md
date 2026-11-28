---
name: critical-code-review
description: Challenge implementation and verification claims through source tracing, concrete counterexamples, focused questions, and calibrated findings without editing the submitted work.
license: MIT
---

# Critical code review

Build an independent view from the brief, applicable spec and plan, actual source, and tests before relying on the author's explanation. Review relevant callers and boundaries, not just edited lines. Establish what changed without requiring Git or a clean branch.

For a material claim, identify the evidence and try to construct a realistic counterexample. Ask precise questions: which invariant prevents the failure, what happens after partial success, or which assertion demonstrates the required result? Trace existing protections before reporting a defect. The goal is better software, not an argument or a quota of findings.

For changes whose safety depends on indirect behavior, read [change-impact guidance](references/change-impact.md): trace external contracts and verify consequential safety assumptions beyond direct callers. This is additional scrutiny within the assigned review, not authorization to edit source or run an arena.

Use [the review method](references/review-method.md) for investigation, useful challenge questions, evidence grading, and report structure. Resolve links from this skill's source directory. Use the configured language skills for language-specific behavior and verification quality.

Keep the submitted application source and tests unchanged. Report needed repairs and design or scope disagreements through the assigned handoff. Recheck responses against the actual finding and preserve stable IDs across rounds. Stop when material concerns are resolved; do not manufacture more work.

Report a clear readiness recommendation, unresolved defects or questions, evidence, and limitations. A clean review is valid; it is not a guarantee that no defects exist. See [sources](SOURCES.md) and the retained [MIT notice](LICENSE).

On the first pass establish independent coverage of the changed behavior and relevant boundaries. In later rounds, inspect the actual source delta and tests, recheck open finding IDs and affected invariants, and expand coverage when a repair changes scope. Record which revision or publication was reviewed and what evidence remains valid. Before readiness, cross-check the current implementation against acceptance criteria; do not rerun identical broad checks without a new reason. Send a consolidated review rather than a stream of tentative findings.
