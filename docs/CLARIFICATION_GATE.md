# Clarification and expected-regret gate

AWG asks for clarification when the expected cost of acting under unresolved
ambiguity exceeds the bounded cost of asking, or when a material ambiguity is
explicitly unresolved. The first rule is deterministic:

`expected_regret = ambiguity × downstream_impact × harm_if_wrong`.

Clarification is required when `material_ambiguity` is true and the ambiguity
is unresolved, or when expected regret is greater than `intervention_cost`.
Confidence is reported as context; high confidence does not suppress a
material unresolved ambiguity. A clarification request is not authorization to
implement.

The gate asks the smallest useful question, represented by a bounded question
scope and at least two plausible alternatives. `tools/check_clarification_gate.py`
checks synthetic cases offline, including high-confidence ambiguity and low-
regret action cases. The thresholds are study parameters, not deployment-safe
values; they require later empirical calibration.

The conceptual inputs are Ros et al. (EACL 2024), on clarification as a
targeted uncertainty-reduction interaction, and *Act or Clarify?*, on trading
the cost of intervention against the regret of acting. AWG adds durable task
identity, dependent-task impact, ranked alternatives, and explicit oracle
authority boundaries.
