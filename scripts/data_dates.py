#!/usr/bin/env python3
"""Write src/data/lastmod.json: slug -> date (YYYY-MM-DD, America/Denver) of the last git commit
that changed that tool's data in src/data/tools.json. Check-stamp fields are ignored so a link check
alone does not count as a content change. Uncommitted edits count as today."""
import json, subprocess, datetime, os
from zoneinfo import ZoneInfo
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
F = 'src/data/tools.json'
VOL = {'lastChecked', 'specsChecked', 'licenseChecked', 'archivedChecked', 'starsChecked', 'stars'}
key = lambda t: json.dumps({k: v for k, v in t.items() if k not in VOL}, sort_keys=True)
tz = ZoneInfo('America/Denver')
log = subprocess.run(['git', 'log', '--reverse', '--format=%H %ct', '--', F], capture_output=True, text=True, check=True).stdout.split('\n')
seen, out = {}, {}
def scan(tools, day):
    for t in tools:
        k = key(t)
        if seen.get(t['slug']) != k: seen[t['slug']] = k; out[t['slug']] = day
for line in filter(None, log):
    h, ct = line.split()
    try: tools = json.loads(subprocess.run(['git', 'show', f'{h}:{F}'], capture_output=True, text=True, check=True).stdout)
    except Exception: continue
    scan(tools, datetime.datetime.fromtimestamp(int(ct), tz).date().isoformat())
cur = json.load(open(F))
scan(cur, datetime.datetime.now(tz).date().isoformat())
res = {t['slug']: out[t['slug']] for t in cur}
json.dump(res, open('src/data/lastmod.json', 'w'), indent=0, sort_keys=True)
print(f'lastmod.json: {len(res)} tools, latest {max(res.values())}')
