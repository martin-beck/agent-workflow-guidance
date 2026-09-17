# Optional LangGraph pause/resume mapping

This is a dependency-free conceptual mapping, pinned to the LangGraph revision
in the public comparison matrix. It does not import LangGraph or claim runtime
compatibility.

| LangGraph-style concept | AWG record | Required boundary |
| --- | --- | --- |
| checkpoint/thread identity | execution and packet identity | resume must use the same identity |
| interrupt payload | decision request | interruption creates a request, not authorization |
| human response | oracle decision record | response binds to packet revision |
| resume input | implementation continuation | stale checkpoint or decision is rejected |

The mapping preserves synthetic context only; raw transcripts, credentials,
provider calls, and framework serialization are outside this study. A tested
adapter is a separate future AR.
