#!/usr/bin/env python3
import argparse,json
def fail(m): raise SystemExit('AWG-BATCH-FAIL: '+m)
def check(v):
 points=v.get('points',[])
 if len(points)<2: fail('at least two points required')
 ids=set()
 for p in points:
  if p.get('id') in ids or not p.get('id'): fail('duplicate point identity')
  ids.add(p['id'])
  if len(p.get('proposals',[]))<2 or not p.get('implications'): fail('proposals and implication helper required')
  r=p.get('response',{})
  if r.get('added_proposal') is not None and not r['added_proposal'].get('evaluated'): fail('added proposal not evaluated')
  if r.get('authorized') and r.get('point_id')!=p['id']: fail('cross-point authorization')
 if v.get('queries')!=1: fail('independent points must be batched')
 print('AWG-BATCH-PASS: '+str(v.get('session_id')))
def main():
 p=argparse.ArgumentParser();p.add_argument('fixture');a=p.parse_args();check(json.load(open(a.fixture)))
if __name__=='__main__':main()
