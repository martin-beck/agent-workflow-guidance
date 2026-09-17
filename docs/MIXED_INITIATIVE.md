# Mixed-initiative feedback semantics

AWG treats oracle interaction as a durable feedback loop. A correction creates
a new packet revision and explicitly supersedes the recommendation it changes.
Confirmation records the exact revision approved; it never approves an older
revision. Pause and resume preserve packet identity, revision, and a bounded
context identity. A pause is not implementation authorization.

`tools/check_mixed_initiative.py` validates synthetic event packets offline.
The checker covers correction supersession, stale confirmation rejection, and
context-preserving resume. It does not claim a transport, UI, or runtime agent
implementation.
