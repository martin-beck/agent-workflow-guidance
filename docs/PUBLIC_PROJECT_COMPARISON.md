# Public project comparison

The matrix in `examples/public-project-matrix.json` is an observation snapshot
taken 2026-09-17 from public repository metadata and checked-in source/docs.
Each row records an exact default-branch revision, SPDX license, maintenance
signal, persistence model, human-intervention boundary, and AWG delta.

The candidates are comparison subjects, not AWG dependencies or endorsements:

- LangGraph provides durable execution, checkpointed state, and human-in-the-
  loop state inspection/modification.
- AutoGen explicitly reports maintenance mode and points new users to
  Microsoft Agent Framework; its human-input middleware is a useful comparison
  for interaction modes, not AWG decision provenance.
- Microsoft Agent Framework documents user approvals and durable-agent
  extensions, but approval is not the same as AWG ranked alternatives and
  revision-bound oracle records.
- OpenHands exposes sandbox and conversation-resume surfaces. The inspected
  evidence does not establish AWG packet semantics or a formal oracle gate.
- SWE-agent provides software-agent, human-configuration, and trajectory/
  benchmark context. The inspected evidence does not establish AWG pause,
  bounded authority, or durable oracle-decision semantics.

The matrix is a dated evidence snapshot. Maintenance and capability claims
must be refreshed before using it for a new integration decision.
