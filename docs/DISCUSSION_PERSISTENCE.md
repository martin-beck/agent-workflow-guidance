# Discussion persistence and future-point capture

The session journal is append-only, revision-bound, and atomically committed.
Safe exit preserves every proposal, evaluation, response, unresolved point,
and re-ask marker. Resume rejects stale revisions. Public state stores only
bounded summaries/digests; private raw text remains local.

Every request for future discussion is classified and mapped to an existing or
new AR, or explicitly rejected with a reason. It may never be silently dropped
or treated as an implementation instruction.
