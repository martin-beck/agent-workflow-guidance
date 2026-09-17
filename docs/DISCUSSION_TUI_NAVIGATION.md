# Reusable discussion TUI navigation

The AWG TUI model exposes a left document pane and a right discussion-point
pane. Selecting a point updates the left document, anchor, and highlighted
phrase while preserving the point selection across document switches.
Unresolved points remain visibly highlighted. This dependency-light model is
provider-neutral; rendering adapters may be added later without changing
decision semantics.
