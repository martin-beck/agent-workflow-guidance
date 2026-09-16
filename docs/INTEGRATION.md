# Integration with Coordinator and Quality

## Ownership matrix

| Concern | Coordinator | AWG | AWQ |
| --- | --- | --- | --- |
| task identity, claim, lease, revision | authoritative | references | observes |
| dependency readiness and ownership | authoritative | considers downstream effects | observes policy impact |
| ambiguity, alternatives, confidence | observes | authoritative | may require a gate |
| human clarification or choice | records event reference | authoritative decision record | checks required approval |
| quality requirements and exceptions | observes | cites | authoritative |
| command execution and evidence | bounded wrapper and result | cites | classifies/contracts |
| implementation correctness | project-specific | never asserts from approval | never replaces domain tests |

## Suggested lifecycle

1. A Coordinator task reaches a decision boundary.
2. The agent snapshots task identity and current repository context through the
   Coordinator boundary.
3. The agent loads applicable AWQ requirements and policy. A policy-required
   approval is a mandatory gate even when the agent is confident.
4. AWG creates one or more decision items, ranks alternatives, and records
   confidence, impact, reversibility, and dependent-task consequences.
5. Independent items may be batched into one oracle packet. Each item retains
   its own status and response.
6. The human answers, rejects all candidates, asks for more evidence, or adds
   a proposal. Added proposals are evaluated before the human selects the
   final option.
7. AWG appends the final decision and reusable guidance. The Coordinator
   records the task event and revision-bound reference; AWQ validates the
   record shape and required evidence class.
8. The agent implements only within the decision scope and records separate
   execution and verification evidence.

## Overlap and failure modes

- **Duplicate authority:** a task note must not be treated as the decision
  record. Store an immutable AWG ID and digest in Coordinator state.
- **Stale decision:** a decision bound to an old task revision, branch, policy
  lock, or repository head must be revalidated or reopened.
- **Rubber-stamping:** the packet must expose alternatives, uncertainty,
  evidence limits, and rejection affordances; “approve” alone is insufficient.
- **Guidance drift:** reusable guidance has scope, provenance, confidence,
  applicability conditions, and expiry/review requirements.
- **Batch coupling:** one unanswered item must not silently authorize another;
  each item has an independent disposition.
- **Quality laundering:** an oracle choice is not a test result, and a green
  quality check is not user intent.
- **Privacy leakage:** packet generation must redact private context before a
  public projection and retain only bounded, typed evidence references.
