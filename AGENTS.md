# Contributor instructions

Read `README.md`, `docs/ARCHITECTURE.md`, `docs/INTEGRATION.md`, and
`docs/DECISION_PROTOCOL.md` before changing contracts. Preserve the boundary:
Coordinator owns task lifecycle and AWQ owns quality policy and evidence.

Every schema or protocol change needs positive and negative fixtures, an
updated decision record or migration note, and a review of privacy,
provenance, authority, replay, and dependent-task effects. Do not claim that
an oracle decision proves implementation correctness.

Every design or conceptual decision must have a versioned specification with
invariants, acceptance predicates, and a declared formal checker. Run that
checker autonomously before presenting candidates to the oracle and again
before implementation if the bound revision, policy, or specification
changes. Missing, stale, failed, timed-out, or inconclusive checks are
fail-closed conditions.

Do not add runtime network access, floating versions, credentials, private
paths, raw prompts, raw transcripts, or unbounded evidence. Commands in future
adapters must be argument arrays with finite deadlines and content-minimized
results. Commits must include a matching DCO `Signed-off-by` trailer and be
published through reviewed pull requests.

Use the separate state repository with Agent Workflow Coordinator for task
claims, dependencies, revisions, and durable progress. Use Agent Workflow
Quality for offline contract and privacy checks. Generated state and quality
artifacts are not hand-edited.
