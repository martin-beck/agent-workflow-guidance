# End-to-end oracle workflow example

AR-0039's trace is synthetic and offline. It records public-safe intake,
planning review, scoped discussion, formal specification review,
post-discussion reconciliation, implementation, quality evidence, and final
handoff in that order. Each event binds to one trace revision and identifies
its evidence class. Planning and specification review cannot be skipped, and
unresolved guidance blocks handoff.

The companion state checker rejects skipped-gate and unresolved-guidance
traces. It does not claim provider integration, user intent, or implementation
correctness; those remain separate evidence obligations.
