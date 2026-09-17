# Human-in-the-loop assistance transfer boundary

Human-in-the-loop reinforcement-learning literature is useful vocabulary, but
its action-level feedback must not be imported as AWG semantics. This bounded
translation keeps four concepts distinct:

- action correction can inform an option but cannot silently rewrite an AWG
  decision record;
- delayed outcomes can update later evaluation but are not immediate approval;
- intervention timing can identify a gate, while the gate still requires a
  ranked decision packet; and
- confidence is an applicability estimate, not reward or task success.

Each term has a transfer disposition and a counterexample. The accompanying
checker rejects missing boundaries and claims no behavioral equivalence.
