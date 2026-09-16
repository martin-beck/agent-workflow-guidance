# Literature and related systems

This is an initial review, not a claim of exhaustive coverage. The project
uses concepts from clarification dialogue, delegation, uncertainty-aware
control, human-agent teaming, and accountable workflow design.

## Concepts to adopt

- **Clarification as uncertainty reduction:** Ask the smallest question that
  resolves a consequential ambiguity; do not ask the user to re-plan the whole
  task. See [Ros et al., EACL 2024](https://aclanthology.org/2024.eacl-long.16/).
- **Expected-regret gating:** The value of asking depends on uncertainty and
  the cost of acting incorrectly. This supports a threshold based on expected
  regret, impact, and intervention cost rather than confidence alone. See
  [Act or Clarify?](https://repositories.cdlib.org/uc/item/5kb446j5).
- **Uncertainty-aware assistance:** An autonomous system can request help when
  its confidence in eventual success is low. See
  [Decision Making for Human-in-the-loop Robotic Agents](https://arxiv.org/abs/2303.06710).
- **Mixed initiative and feedback:** Human interaction is a feedback loop, not
  a one-time approval button; the system should support correction and
  confirmation. See the review of
  [feedback in conversational agents](https://doi.org/10.3389/fcomp.2022.744574).
- **Delegation and control:** Delegation changes perceived control and risk;
  users need enough context to make an informed decision. See
  [Rise of the machines: Delegating decisions to autonomous AI](https://doi.org/10.1016/j.chb.2022.107308).

## Related engineering patterns

- Oracle-guided or human-in-the-loop reinforcement learning treats a human as
  an external source of guidance, but often focuses on action-level feedback.
  AWG extends the idea to software-engineering decisions, provenance, and
  dependent-task consequences.
- Approval workflows in agent platforms provide useful checkpoint concepts,
  but AWG requires ranked alternatives, an explicit additional-option path,
  bounded authority, and durable decision reuse.
- Planner/executor/reviewer systems motivate separating a recommendation from
  verification. AWG keeps oracle intent, implementation, and quality evidence
  as distinct records.

## Public project candidates

These are comparison and adapter candidates, not dependencies or endorsements:

- [LangGraph](https://github.com/langchain-ai/langgraph) exposes durable
  interrupt/resume human-in-the-loop control with checkpointed state. Compare
  its runtime pause semantics with AWG's ranked alternatives, oracle-added
  candidate, bounded authority, and append-only decision record.
- [AutoGen](https://github.com/microsoft/autogen) demonstrates human feedback
  in multi-agent teams, but its repository currently describes AutoGen as
  maintenance mode and points new users to [Microsoft Agent
  Framework](https://github.com/microsoft/agent-framework). Evaluate both as a
  migration/comparison pair rather than pinning AutoGen.
- [OpenHands](https://github.com/All-Hands-AI/OpenHands) and its software-agent
  SDK are relevant hosts for software-development decision gates. Study where
  AWG packets can sit between planning, tool execution, review, and resumption.
- [SWE-agent](https://github.com/SWE-agent/SWE-agent) provides a software
  engineering agent and benchmark context. Use it to test whether AWG's
  intervention points improve task outcomes without confusing benchmark scores
  with human-governance evidence.

Each candidate must be evaluated offline or in a sandbox first. The project
must record exact revision, license, protocol fit, privacy boundary, and what
was not tested before claiming integration.

## Research questions

1. How should confidence be calibrated across applicability, outcome, and
   downstream impact rather than collapsed into one score?
2. What packet size and batching strategy minimize oracle workload without
   creating hidden coupling between decisions?
3. When does reusable guidance become stale or over-generalized?
4. How can the system detect a human rubber stamp or an agent framing that
   omits the most important alternative?
5. Which intervention evidence best predicts whether a future task can safely
   proceed without another oracle interaction?

The coordination state tracks each concept, project candidate, and research
question as a separate AR so that findings can be accepted, rejected, or
superseded independently.
