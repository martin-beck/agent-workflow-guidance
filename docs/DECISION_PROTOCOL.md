# Decision protocol

The first version is intentionally transport-neutral. JSON Schema files define
the public shape; a future CLI or UI may carry these records over files,
Coordinator events, or another reviewed adapter.

## Mandatory specification gate

Every AWG request carries a machine-readable specification. A request whose
decision class is `design` or `conceptual` cannot be sent to the oracle until
the specification passes its autonomous checks. The same rule applies when a
new project is bootstrapped: the initial AR-task topology is a conceptual
decision and must have a specification before the first AR is opened.

The specification must include:

- objective and scope;
- explicit assumptions and unknowns;
- state variables and permitted transitions;
- invariants that must hold in every represented state;
- acceptance predicates for the intended outcome;
- formalization method, model reference, checker command, and bounded scope;
- expected checker result and a content digest of the checked artifact.

The autonomous checker runs before oracle presentation and again before
implementation begins if task revision, repository head, policy lock, or
specification digest changes. A failed, missing, stale, or inconclusive check
causes a fail-closed stop; it may not be overridden by an oracle approval.

The checker records compact evidence, not hidden model reasoning or private
transcripts. See [Formal specifications](FORMAL_SPECIFICATION.md) and
`schema/specification.schema.json`.

## Required reasoning fields

Each candidate must state:

- the proposed action and the assumptions it relies on;
- evidence references and important evidence gaps;
- confidence that it applies to the actual task;
- confidence that it solves the underlying issue;
- expected follow-on restrictions, migrations, or dependent-task changes;
- impact, reversibility, rollback, cost, and time;
- why the alternatives rank below it.

The agent must not use a single opaque “confidence” field to hide these
different uncertainties.

## Oracle interaction

The oracle can request clarification, ask the agent to gather evidence, select
one candidate, reject all candidates, or supply an additional candidate. The
agent evaluates an additional candidate exactly like the original candidates.
The oracle has final decision authority within the declared scope, but cannot
make the record claim evidence that does not exist.

## Reuse

A final decision may emit reusable guidance. Guidance is not a global rule by
default: it has a scope predicate, origin decision, applicability conditions,
counterexamples, owner, review date, and optional expiry. A future agent may
use it to avoid asking a duplicate question only after checking those fields
against the current task and policy.

See `schema/decision-request.schema.json` and
`schema/decision-record.schema.json` for the decision contract, and
`schema/specification.schema.json` plus
`schema/formal-check-result.schema.json` for the formal gate.
