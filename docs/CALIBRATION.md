# Separate confidence calibration

AWG records applicability, outcome, and downstream-impact confidence as three
different values. A confidence value is an agent report, not a probability,
until labels and calibration error support that interpretation.

The offline fixture set uses a simple mean absolute calibration error per
dimension:

`MAE_dimension = mean(abs(confidence_dimension - observed_label_dimension))`.

The dimensions are never averaged into one score. A downstream-impact
confidence below the declared escalation threshold is an escalation signal even
when applicability and outcome confidence are high. The fixture checker only
validates the measurement contract; it does not establish a production
threshold or deployment safety.
