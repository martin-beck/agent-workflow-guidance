# Batched discussion packet TUI

The batch model groups only independent discussion points. Each point retains
its own ranked proposals, implication helper, response identity, and partial
status. An unanswered point is never authorized by another point's response.
User-added proposals carry the same confidence, trade-off, dependency, and
formal-evidence fields and must be evaluated before selection.

The model is provider-neutral and keeps query batching separate from oracle
authority. Coupled points are excluded or explicitly related rather than
silently coupled.
