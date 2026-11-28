# Source and modifications

Adapted from OpenAI's [gh-fix-ci skill](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci/SKILL.md) and [inspect_pr_checks.py](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci/scripts/inspect_pr_checks.py) at reviewed revision `49f948faa9258a0c61caceaf225e179651397431`. Retained [Apache-2.0 license](LICENSE).

inspect-pr-checks.py retains check/log inspection and CLI field fallback. Local modifications distinguish successful, failed, pending, skipped, and unknown checks; accept valid check JSON despite gh's nonzero check-status exits; produce structured incomplete/error output; bound subprocess duration; include PR-head provenance; and scope run-log retrieval to Actions URLs from the selected repository/host. Repairs remain assigned work; the skill does not own approvals, CI reruns, pushes, or acceptance.
