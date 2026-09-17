# Initial project planning and design review

Before an implementation AR proceeds, the project must expose the decomposed
work plan, dependency graph, AR manifest, and concise design document for an
explicit user disposition. Each artifact has version and digest references on
both sides of the review and is bound to the exact Coordinator task revision.

The disposition is `approve`, `reject`, or `changes-requested`; only
`approve` makes the review implementation-ready. A claim, formal pass, or
quality pass cannot substitute for this interaction. Private discussion stays
outside public state and is represented by bounded typed evidence.

The offline checker is in the companion state repository at
`tools/check_planning_review.py`. Coordinator remains authoritative for task
state; AWG owns the review contract; AWQ validates evidence shape. Approval
does not assert implementation correctness.
