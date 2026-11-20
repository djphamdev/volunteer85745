#!/usr/bin/env python3
"""
Quick status report for volunteer85745 daily cron.
"""
import json
from pathlib import Path

target_dir = Path('/home/donzzz/Documents/_obsidian_androidZzz/20-PROJECTS/volunteer85745/leads')
json_files = sorted(target_dir.glob('*-leads.json'), reverse=True)

if not json_files:
    print('  No vault leads found yet')
else:
    latest = json.loads(json_files[0].read_text())
    remote_count = sum(1 for e in latest if e.get('category') == 'remote')
    local_count = sum(1 for e in latest if e.get('category') == 'local')
    total = len(latest)
    hrs = [e.get('hours_per_week', 0) for e in latest]
    print(f'  Latest: {total} listings ({remote_count} remote, {local_count} local)')
    print(f'  Hours/wk: {min(hrs)} to {max(hrs)}, avg: {sum(hrs)/len(hrs):.1f}')
    over20 = sum(1 for h in hrs if h >= 20)
    print(f'  Roles >= 20 hrs/wk: {over20} (meets 80/mo alone)')
    print(f'  Date: {json_files[0].stem.replace("-leads", "")}')