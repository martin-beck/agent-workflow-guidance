# Quality integration

Agent Workflow Quality is enforced by the pinned AWQ workflow in
`.github/workflows/awq.yml`, which mirrors the pinned source workflow. The checked-in profile and lock select the
offline requirements for core, documentation, GitHub Actions, privacy,
Python, schemas, shell, and supply-chain checks.

AWQ remains the owner of the shared quality policy; this repository must not
copy or silently fork its requirement registry. Changes to this integration
are specification-first and must pass both the AWG formal checker and AWQ.
