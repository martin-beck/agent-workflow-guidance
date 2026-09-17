# Post-discussion reconciliation and reopen loop

After a discussion, AWG records a deterministic impact analysis and preserves
versioned before/after references for the work plan, design document,
specification set, dependency graph, and affected AR records. Each change
identifies its scope, impact, provenance, and affected ARs.

Contradictory, incomplete, stale, or scope-changing guidance cannot be marked
reconciled silently. The checker requires a targeted `reopen` or
`discussion-required` disposition, names the affected ARs, and requires a new
discussion before reconciliation can continue. Prior versions remain cited;
private prompts and transcripts remain outside public state.

Coordinator owns task revisions and AR transitions. AWG owns reconciliation
semantics and provenance. AWQ validates public evidence shape. Reconciliation
does not prove implementation correctness.
