#!/usr/bin/env python3
import argparse,json
def fail(m): raise SystemExit('AWG-PERSISTENCE-FAIL: '+m)
def check(v):
 if not v.get('journal_id') or not isinstance(v.get('revision'),int): fail('journal identity/revision required')
 if v.get('status') not in {'saved','re-ask','resumed'}: fail('invalid journal status')
 if not v.get('points') or any(not p.get('id') or 'proposals' not in p or 'response' not in p for p in v['points']): fail('lossless point record required')
 for request in v.get('future_requests',[]):
  if request.get('classification') not in {'existing-ar','new-ar','rejected'} or not request.get('reason'): fail('future request mapping incomplete')
  if request['classification']!='rejected' and not request.get('ar_ref'): fail('future request AR mapping missing')
 if v.get('resume_revision') is not None and v['resume_revision']!=v['revision']: fail('stale resume')
 print('AWG-PERSISTENCE-PASS: '+v['journal_id'])
def main():
 p=argparse.ArgumentParser();p.add_argument('fixture');a=p.parse_args();check(json.load(open(a.fixture)))
if __name__=='__main__':main()
