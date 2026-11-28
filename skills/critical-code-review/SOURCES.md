# Sources and adaptation

Reviewed 2026-10-18.

Selected review principles are adapted from [Superpowers' code reviewer prompt](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/code-reviewer.md), by Jesse Vincent and contributors. The upstream [MIT notice](https://github.com/obra/superpowers/blob/main/LICENSE) is retained in [LICENSE](LICENSE).

The adaptation keeps plan alignment, direct source inspection, unchanged submitted work, concrete findings, calibrated severity, and an explicit verdict. It replaces Git range assumptions with the available task baseline, preserves assignment scope and the caller's decision authority, and adds a bounded evidence-based challenge and finding-resolution method. It does not install Superpowers or adopt its full development workflow.

Additional primary guidance consulted: Google's [what to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) and [standard of code review](https://google.github.io/eng-practices/review/reviewer/standard.html). These are external references; their text and templates are not bundled.

This is a local adaptation. The source link tracks upstream main, not a pinned Git revision; no automatic update mechanism or dependency is added.

Change-impact guidance adapts [pstack blast-radius](https://github.com/cursor/plugins/blob/b7b93c36be9bcc36a74db438e0fd385d660bc559/pstack/skills/blast-radius/SKILL.md) at reviewed revision `b7b93c36be9bcc36a74db438e0fd385d660bc559`; its [MIT notice](LICENSE.pstack) is retained separately. The adaptation keeps evidence-backed indirect-contract analysis and omits automatic arena dispatch, output rewriting dependencies, and reviewer-owned source edits.
