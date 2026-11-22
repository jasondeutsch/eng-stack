---
name: go-planning-evidence
description: Ground consequential Go design and review claims in the repository's module, toolchain, API contracts, and concurrency behavior. Use when planning or reviewing Go changes, not for unrelated architecture work.
license: MIT
---

# Go planning evidence

Inspect go.mod, applicable project rules, existing interfaces, tests, and lint configuration before proposing dependencies or API contracts. Distinguish the declared Go version from the installed toolchain. Use locally available tools; do not install a toolchain or dependency to resolve a planning question without authorization.

Verify consequential library claims with targeted source reads or `GOTOOLCHAIN=local go doc package.Symbol`. Check the project's selected dependency version rather than memory of a newer API. If documentation is unavailable locally, report the specific unverified claim and its consequence. Do not run broad module downloads as discovery.

For shared state, name ownership, synchronization boundaries, atomic operations, and cancellation/error behavior. Show a concrete competing-operation sequence when it affects the design. Verify that the proposed tests can observe the invariant, including repeated or race-enabled tests when relevant; listing a command is not evidence it passed.

Record only the verified fact, source/location or command, and design consequence. Keep speculative implementation code out of the plan unless exact interface detail is needed. Recheck facts affected by revisions, reuse still-valid evidence, and keep the generic architecture method unchanged for other languages.
