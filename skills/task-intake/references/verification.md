# Type-specific verification

The admitted task supplies scope and acceptance criteria. Use this table when specifying, implementing, or reviewing it; unknown evidence is an investigation need, not permission to claim success.

| Type | Evidence to plan and evaluate |
| --- | --- |
| `bug-fix` | Demonstrate the reported symptom before the repair when feasible, and its correction afterward. Cover related regression risks. Explain when the original failure cannot be reproduced. |
| `feature` | Exercise acceptance scenarios through the relevant public interface, including material failure cases and compatibility obligations. |
| `refactor` | Show that relevant observable behavior is preserved across the structural change; verify the intended structural improvement separately. |
| `performance` | Compare a baseline and changed revision under declared workload and measurement conditions. Check correctness, repeatability, resource use, and regressions. Report uncertainty rather than treating one noisy number as proof. |
| `investigation` | Answer the question with traceable evidence; distinguish observations from hypotheses and state limitations. Deliver a report without implementation changes. |

Choose checks proportional to the task. Existing evidence can be reused when its source revision, conditions, and covered behavior remain applicable. A later type/scope conflict must be reported for reassessment; agents cannot change routes or skip approval gates.
