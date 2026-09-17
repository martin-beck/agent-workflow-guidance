# Planner, executor, and reviewer separation

AWG keeps five evidence roles distinct: a planner recommendation, the oracle
decision, implementation output, quality evidence, and independent review.
Approval selects intent; it does not verify that implementation followed that
intent. A plausible recommendation can therefore end in a failed quality
check, which blocks independent review until corrected.

The synthetic contract binds each record to its predecessor and rejects a
review that is based only on approval or that bypasses quality evidence.
