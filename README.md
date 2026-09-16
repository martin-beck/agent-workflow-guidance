# Agent Workflow Guidance

Agent Workflow Guidance (AWG) defines how an autonomous engineering agent
recognises a decision that should be exposed to a human oracle, presents
ranked alternatives, records the oracle's decision, and reuses durable
guidance without hiding uncertainty or transferring authority implicitly.

The initial oracle is a human. The protocol is deliberately oracle-neutral so
that a later trusted service can implement the same interface without changing
the provenance model.

## Design goals

- ask for clarification when the task, constraints, or intended outcome is
  materially ambiguous;
- ask for a decision when multiple viable paths have different trade-offs;
- ask for guidance when a local decision may constrain dependent work;
- require alternatives, evidence, confidence, downside, blast radius, and
  reversibility before escalation;
- allow one batched packet to contain independent decisions while preserving
  one response per decision;
- let the oracle add an alternative, have the agent evaluate it, and let the
  oracle make the final selection;
- record a tamper-evident, privacy-safe decision that can be cited by future
  tasks as guidance;
- express every design/conceptual decision as a formally checkable
  specification and require an autonomous check before oracle selection;
- keep the human's authority explicit: a recommendation is not an approval,
  and an approval is not evidence that implementation succeeded.

## Non-goals

AWG is not a task scheduler, lease manager, dependency database, test runner,
or general policy engine. Agent Workflow Coordinator owns task lifecycle and
durable coordination. Agent Workflow Quality owns quality requirements,
profiles, adapters, and evidence contracts. AWG supplies the decision layer
between them.

## Status

This repository starts as a protocol and reference-contract project. Runtime
implementation, interactive clients, and integrations are intentionally
downstream of the schemas and governance model.

See [Architecture](docs/ARCHITECTURE.md), [Integration](docs/INTEGRATION.md),
the [decision protocol](docs/DECISION_PROTOCOL.md), and the [literature review]
(docs/LITERATURE.md).

## Privacy boundary

Public artifacts must not contain credentials, private prompts, raw transcripts,
machine-specific paths, host identifiers, or unbounded command output. Public
examples use synthetic project names and redacted evidence.

Licensed under MIT.
