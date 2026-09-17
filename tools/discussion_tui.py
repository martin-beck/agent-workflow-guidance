"""Provider-neutral discussion TUI session model; rendering is adapter-owned."""
from dataclasses import dataclass

@dataclass(frozen=True)
class DiscussionPoint:
    point_id: str
    anchor: str
    phrase: str
    unresolved: bool = False

class DiscussionSession:
    def __init__(self, points, document="design"):
        if not points: raise ValueError("at least one discussion point is required")
        self.points = tuple(points); self.document = document; self.index = 0
    @property
    def active(self): return self.points[self.index]
    @property
    def highlight(self): return self.active.phrase
    @property
    def unresolved_ids(self): return tuple(p.point_id for p in self.points if p.unresolved)
    def move(self, delta): self.index = max(0, min(len(self.points)-1, self.index + delta)); return self.active
    def switch_document(self, document): self.document = document; return self.active.anchor
