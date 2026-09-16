# Derived requirements from local agent interactions

This document is a privacy-safe synthesis of recurring intervention patterns
observed in local agent-development work. It is not a transcript and contains
no private prompts, machine paths, credentials, or raw command output.

AWG should support at least these intervention classes:

- **status and dependency clarification:** which task or prerequisite actually
  blocks progress, and whether another ready task can proceed;
- **scope correction:** work only on the named task, repository, platform, or
  capability, and do not broaden authorization from a nearby task;
- **decision correction:** revise an earlier plan when a user identifies the
  intended behavior or acceptable trade-off;
- **authorization:** explicitly permit a bounded system change, runner action,
  or implementation direction, with scope and expiry;
- **validation policy:** decide whether a failure needs explanation, repeated
  runs, a fast gate, a full gate, or a documented limitation;
- **worker recovery:** distinguish nominal assignment from live progress and
  decide whether to recover, reassign, or stop a worker;
- **publication and release:** distinguish source change, reviewed commit,
  green CI, merged PR, public release, and usable shipped behavior;
- **privacy/security boundary:** choose whether evidence can be public and what
  must be redacted or kept local.

These requirements motivate explicit trigger types, task/revision binding,
authority scope, downstream impact, and durable reusable guidance.
