#!/usr/bin/env python3
import argparse,json
def main():
 p=argparse.ArgumentParser();p.add_argument('fixture');a=p.parse_args();v=json.load(open(a.fixture))
 points=v.get('points',[])
 if not points or any(not x.get('anchor') or ('unresolved' in x and x['unresolved'] and not x.get('highlighted')) for x in points): raise SystemExit('AWG-TUI-FAIL: anchor/highlight invariant')
 print('AWG-TUI-PASS: '+a.fixture)
if __name__=='__main__':main()
