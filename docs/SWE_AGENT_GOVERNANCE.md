# SWE-agent benchmark and governance boundary

SWE-agent task success is an outcome measure, not evidence that an oracle
intervention was safe or that autonomy is ready. This synthetic contract keeps
the measures separate:

- `task_score` records task outcome;
- `intervention_cost` records pauses, latency, and oracle effort;
- `rework_count` records work invalidated by the decision;
- `dependent_impact` records effects on later tasks;
- `decision_quality` records applicability and downstream-risk assessment; and
- `governance_status` records the independent review result.

The checker fails closed when governance evidence is absent or when a
successful task is paired with unsafe intervention or dependent-task evidence.
The records contain no provider calls, credentials, or production-safety claim.
