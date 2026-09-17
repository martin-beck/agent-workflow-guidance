# Canonical oracle interaction lifecycle

AWG interaction is a four-gate lifecycle. The gates are mandatory for a
project decision that uses oracle guidance; they are not optional UI steps and
cannot be inferred from a claim, an approval, or a green quality check.

| Gate | Required purpose | Continue condition |
| --- | --- | --- |
| `intake` | Record the request, task identity, scope, work plan, and design boundary. | The user-facing scope and initial plan are explicit. |
| `discussion` | Present bounded context, alternatives, implications, uncertainty, and user questions. | Interaction occurred and the user disposition is explicit. |
| `specification-review` | Review the versioned formal specification and autonomous result before relying on the design. | The exact specification and passing check are cited. |
| `reconciliation` | Apply the discussion outcome to the plan, design, specification, and dependent AR references. | Before/after artifacts and contradictions are reconciled. |

Each gate carries the Coordinator task ID and exact task revision. It also
contains versioned, digest-bound references for both the before and after
work plan and design document, plus the applicable specification and formal
check. A gate records interaction evidence as a bounded digest or typed public
reference; private prompts and transcripts remain outside public state.

Every gate must state `continue` or `unresolved`. `continue` allows the next
gate only when all other requirements pass. `unresolved` is durable evidence
that the lifecycle is not complete and requires reopening or further
discussion. A lifecycle with an unresolved contradiction can never be marked
complete.

Coordinator owns task revisions, claims, dependencies, and lifecycle
transitions. AWG owns this interaction contract and the authority-bearing
decision record. AWQ checks the record shape, privacy boundary, and evidence
classes. None of these records proves implementation correctness.

The offline state checker and synthetic positive/hostile fixtures live in the
companion state repository at `tools/check_oracle_lifecycle.py` and
`integration/oracle-lifecycle-*.json`.

## Consumer mapping

Coordinator AR-0022 consumes the gate ordering and revision binding when it
records a task event. AWQ AR-0058 consumes the required evidence classes and
fail-closed predicates. Later discussion UI ARs may add transport fields but
must preserve the four gate types, artifact references, explicit disposition,
and contradiction rule.
