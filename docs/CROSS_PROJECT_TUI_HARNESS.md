# Cross-project TUI harness

The AWG-owned harness consumes only the versioned public Coordinator AR-0029
and AWQ AR-0065 contracts. It uses deterministic offline traces to exercise
agent/user entry, batching, two-pane synchronization, proposal evaluation,
safe exit, resume/re-ask, future-request mapping, and hostile fail-closed
cases. It does not import Coordinator or AWQ implementation internals.
