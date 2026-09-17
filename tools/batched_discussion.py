"""Provider-neutral batched point model."""
class BatchedDiscussion:
 def __init__(self, points):
  if len(points)<2: raise ValueError('at least two independent points required')
  ids=[p['id'] for p in points]
  if len(set(ids))!=len(ids): raise ValueError('duplicate point identity')
  self.points=tuple(points); self.responses={}
 def answer(self, point_id, response):
  if point_id not in {p['id'] for p in self.points}: raise KeyError(point_id)
  self.responses[point_id]=dict(response)
 def unanswered(self): return tuple(p['id'] for p in self.points if p['id'] not in self.responses)
