# Remote SSH transport contracts

The UI owns runtime discovery and tunnelling; Guidance owns the public
decision-layer contracts that describe those facts. `remote-endpoint-candidates`
contains only redacted, revision-bound candidates and observed host-key
fingerprints. `remote-ssh-enrollment` records explicit consent, a device
public key, a pinned host key, and a loopback workflow-service forwarding scope.

Private keys, reusable credentials, SSH config contents, private paths, and raw
agent prompts are forbidden. Candidate discovery is advisory until the phone
probes the endpoint. Enrollment is one-time, expiring, revocable, and must fail
closed on host-key mismatch or forwarding-scope changes.
