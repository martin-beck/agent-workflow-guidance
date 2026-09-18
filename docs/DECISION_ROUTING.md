# Mandatory decision routing

User authority is a protocol event, not a conversational convenience. When a
decision is important, the agent must create an AWG decision request and route
it through the Coordinator's AR--TUI bridge. Asking the user to choose in the
Codex, OpenCode, or other host-agent interface is not a valid substitute.

An important decision is any user-requested choice, request for more detail or
proposal review, agent uncertainty, policy-required approval, design or
conceptual choice, or choice with high/critical impact, difficult or
irreversible rollback, project-direction, security, privacy, public-API,
data-model, migration, or dependency consequences. The agent must classify the
decision before implementation; confidence does not waive this rule.

The routing record is `schema/agent-decision-routing.schema.json`. It binds the
human trigger and request reference to `channel: workflow-tui` and explicitly
forbids a direct host-interface question. The TUI handoff may be shown in the
host interface, but it contains only session status and how to attach; it must
not ask for, accept, or imply the authoritative choice there.

Agents should finish safe, independent ARs first, then batch independent
requests. Every item remains independently revision-bound and unanswered items
never receive implicit approval. If the trigger, request, or TUI session is
missing or stale, the Coordinator must fail closed and leave the AR waiting.
