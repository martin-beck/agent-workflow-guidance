# Architecture

AWG has five conceptual records:

1. **Decision trigger** — why the agent stopped, including uncertainty,
   impact, reversibility, deadline, and the task/revision context.
2. **Candidate set** — the highest-probability applicable solutions, each with
   rationale, evidence references, confidence, expected task outcome, costs,
   downstream restrictions, and rollback.
3. **Oracle packet** — a bounded, human-readable and machine-readable request
   containing one or more independent decisions.
4. **Oracle response** — clarification, selection, rejection, or an additional
   proposal. An additional proposal is not accepted directly: the agent must
   evaluate it using the same candidate schema before final selection.
5. **Decision record** — the final authority-bearing result, scope, conditions,
   expiry, reusable guidance, and links to implementation evidence.

Every AWG decision has a sixth required artifact: a **formal specification**.
For design and conceptual decisions this is a hard gate, including the
decision to create or restructure the first AR queue of a new project. The
specification states the objective, assumptions, state/transition model,
invariants, acceptance predicates, and the autonomous checker that evaluates
them. An oracle must not select a design candidate whose specification has not
passed its declared checks.

The record is append-only from the protocol's perspective. Corrections are
new records that supersede an earlier decision; they never rewrite history.
The decision digest binds the canonical request, candidates, response, and
context references. Secrets and private source material stay outside public
records and are represented by typed redactions or content digests.

## Decision gate

An agent may proceed without an oracle only when the applicable candidate is
above the configured confidence threshold, the expected outcome is adequate,
the impact is within policy, the decision is reversible enough for its risk,
and no task or quality contract requires explicit human authority. Otherwise
the agent must stop at the gate or continue only with explicitly safe,
non-committing preparation.

Confidence is not a probability of truth. AWG records the agent's calibrated
estimate and the basis for it; policy may require an oracle regardless of a
high score for irreversible, security-sensitive, privacy-sensitive, or
project-direction decisions.

## Context flow

Coordinator contributes stable task ID, revision, dependency state, owner,
branch/worktree identity, and durable event references. AWQ contributes
applicable requirements, policy, exception state, evidence classifications,
and quality-gate results. AWG contributes the decision and guidance records.

No project may infer an approval merely because a task is claimed, a quality
check is green, or an agent has a high confidence score.

Formal checking does not prove arbitrary implementation correctness. It proves
only the declared model and predicates within the declared method and scope.
The decision record must preserve that boundary and keep implementation,
quality, and runtime evidence separate.
