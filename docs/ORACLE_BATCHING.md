# Oracle packet batching

AWG may present one decision, independent decisions, or explicitly coupled
decisions in one oracle packet. The packet persists each item identity and its
relation. A response authorizes only the declared item set; independent items
never inherit a response, and unanswered items remain unresolved.

The synthetic checker covers single-item, partial independent-batch, and
coupled-batch cases. It rejects silent cross-item authorization and does not
claim a workload or latency improvement.
