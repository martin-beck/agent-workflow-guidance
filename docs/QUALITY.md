# AWQ quality enforcement

Agent Workflow Quality is a required gate for AWG changes. The repository
checks in `quality/awq.json` and `quality/awq.lock.json`; the lock selects the
profiles and requirement identifiers, while the workflow executes the pinned
AWQ source.

The [AWQ reusable workflow source](https://github.com/martin-beck/agent-workflow-quality/blob/fcf8df6ab7ac8d5be63400727bcf2b02fff74804/.github/workflows/awq-reusable.yml)
is mirrored by `.github/workflows/awq.yml` at the same full immutable source
SHA, with an explicit consumer-side timeout. It runs on every pull request,
every push to `main`, and manual dispatch. It executes `doctor` and the PR
tier offline against the consumer tree. The repository workflow does not
claim that a green AWQ result proves formal correctness, oracle alignment, or
runtime behavior.

Changes to AWQ profiles, locks, workflow references, or quality policy are
themselves governed changes: they require an AWG specification, autonomous
formal check, review, and the resulting AWQ checks. A changed lock must not be
treated as an approval to weaken requirements.

The exact self-hosting enforcement decision is recorded in
`specifications/awq-enforcement.json` and its check result. The current local
baseline passes AWQ 0.6.0 profiles `core`, `docs`, `github-actions`, `privacy`,
`python`, `schemas`, `shell`, and `supply-chain`.
