# Formal specification gate

AWG treats a design/conceptual decision as an engineering artifact, not just
conversation. The agent must turn the decision into a specification before it
asks the oracle to choose.

## Required lifecycle

1. Classify the request. `design` and `conceptual` are mandatory formal-gate
   classes; `operational` requests still carry a bounded specification.
2. Write a versioned specification with assumptions, state, transitions,
   invariants, acceptance predicates, and a formalization/checker plan.
3. Run the checker autonomously, offline where possible, using an exact model
   and finite resource/deadline bounds.
4. Bind the formal-check result to the exact specification digest, identity,
   version, method, and a passing status. A stale or differently bound result
   is not evidence.
5. Stop on failure, timeout, stale digest, missing evidence, or an inconclusive
   result. The oracle can choose among checked candidates but cannot waive a
   failed formal gate.
6. Include the passed check result and specification digest in the oracle
   packet and final decision record.
7. Recheck when the task revision, repository head, quality lock, model,
   assumptions, or specification changes.

## Formalization levels

The method must match the claim:

- `json-schema`: structural contract only;
- `state-machine`: finite transition and invariant model;
- `tlaplus`: temporal safety/liveness model with declared bounds;
- `smtlib`: satisfiability/constraint proof with declared solver and limits;
- `alloy`: bounded relational model with declared scope.

Calling a JSON parser a formal proof is prohibited. A structural pass can be
one property of a stronger state/model check, but its limitation must remain
visible.

## AR bootstrap rule

Creating the first AR topology is itself a conceptual decision. The project
must first create a bootstrap specification for the queue policy, dependency
graph, authority boundaries, and initial acceptance criteria. The bootstrap
specification is checked before AR-0001 or any successor is promoted to active
work. Existing AWG ARs are migrated under the same rule by the follow-up ARs
in the companion state repository.

See `specifications/bootstrap-queue.json` for the initial AWG artifact and
`specifications/bootstrap-queue.check.json` for its recorded autonomous check.

## Self-hosting rule

After the initial formal gates are complete, AWG applies this workflow to its
own evolution. AWG design changes, schema changes, formal-checker changes,
Coordinator/AWQ integrations, and release-policy changes require their own
specification, autonomous check, oracle decision where applicable, and
independent implementation/quality evidence.

The bootstrap specification and checker form the finite initial seed. Changes
to that seed or to the self-hosting rule require a successor specification;
this recursion boundary prevents an unbounded bootstrap loop while preserving
formal governance of the governance mechanism itself. See AR-0028 in the
companion coordination repository.
