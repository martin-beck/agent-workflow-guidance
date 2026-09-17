#!/usr/bin/env python3
import argparse,json
ORDER=('entry','packet','formal-review','user-response','persistence','coordinator-event','quality','reconciliation')
def fail(m): raise SystemExit('AWG-TUI-INTEGRATION-FAIL: '+m)
def check(v):
 if v.get('entry_point') not in {'agent','user'} or v.get('status')!='reconciled': fail('invalid entry/status')
 events=v.get('events',[]); rev=v.get('task_revision')
 if [e.get('stage') for e in events]!=list(ORDER): fail('bypass or incomplete sequence')
 if not isinstance(rev,int) or any(e.get('task_revision')!=rev for e in events): fail('stale event revision')
 if not v.get('formal_check') or not v.get('awq_check') or not v.get('user_authority'): fail('required evidence missing')
 print('AWG-TUI-INTEGRATION-PASS: '+v['entry_point'])
def main():
 p=argparse.ArgumentParser(); p.add_argument('fixture'); a=p.parse_args(); check(json.load(open(a.fixture)))
if __name__=='__main__': main()
