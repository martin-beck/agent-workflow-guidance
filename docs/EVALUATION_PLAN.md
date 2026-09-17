# Offline human-guidance evaluation plan

This first evaluation is synthetic and offline. It tests whether AWG’s packet
and gate design improves decision quality without hiding oracle effort or
downstream cost. It is not a deployment-safety or causal-effect claim.

## Hypotheses

1. Ranked alternatives plus expected-regret context reduce incorrect decisions
   on materially ambiguous tasks compared with autonomous action alone.
2. Batching independent decisions reduces packet overhead without authorizing
   unanswered items or coupled decisions silently.
3. Reusable guidance reduces repeated oracle questions only when scope and
   freshness are explicitly revalidated.
4. A separate downstream-impact confidence dimension catches cases where local
   applicability and outcome confidence are high but dependent-task risk is
   material.

## Conditions and measures

The bounded scenario set is evaluated under autonomous, oracle-guided,
independent-batch, and reusable-guidance conditions. Every scenario records:

- decision quality: whether the selected action matches the synthetic gold
  disposition and respects the stated constraints;
- oracle effort: packet count and response-item count, reported separately from
  outcome quality;
- rework: corrective actions required after an incorrect or stale decision;
- dependent-task impact: number and severity of downstream changes attributable
  to the decision;
- calibration: absolute error for applicability, outcome, and downstream-impact
  confidence separately;
- inappropriate autonomy: an autonomous action taken where the scenario’s
  expected regret exceeds the declared intervention threshold.

Results must report per-condition distributions and limitations. Fewer oracle
interventions alone is never a success criterion.

## Reproducibility boundary

Scenarios are checked offline by `tools/check_evaluation_plan.py`. No provider,
network, private transcript, or model runtime is required. The checked-in
scenario file is a contract for study inputs, not empirical results.
