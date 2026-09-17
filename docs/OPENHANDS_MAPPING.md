# OpenHands decision-gate mapping

This is a dependency-free conceptual mapping against the exact OpenHands
revision recorded in `examples/openhands-mapping.json`. It does not import
OpenHands or claim adapter compatibility.

| OpenHands surface | AWG surface | Required invariant |
| --- | --- | --- |
| planning/tool action | candidate solution and ranked options | uncertainty and downstream impact are recorded before execution |
| sandboxed tool execution | bounded authority disposition | sandbox scope does not authorize a consequential external change |
| review or approval pause | oracle decision request | a pause creates a revision-bound packet, not implicit approval |
| conversation resume | continuation with decision context | resume rejects stale task, packet, or decision revisions |

The mapping preserves only synthetic identifiers and decision metadata. Raw
transcripts, credentials, provider calls, and a tested runtime adapter are
outside this study.
