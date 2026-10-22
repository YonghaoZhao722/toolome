#!/usr/bin/env python3
"""Guard: homepage 'Recently released' must list every tool whose release date
(released || firstReleased) falls in the 14-day window, and recent entries need valid dates."""
import json, re, sys, datetime as dt
from zoneinfo import ZoneInfo
tools = json.load(open('src/data/tools.json'))
h = open('dist/index.html').read()
m = re.search(r'<section id="recent"[^>]*data-window-from="([\d-]+)"[^>]*data-window-to="([\d-]+)"[^>]*>(.*?)</section>', h, re.S)
today = dt.datetime.now(ZoneInfo('America/Denver')).date()
lo = (today - dt.timedelta(days=14)).isoformat(); hi = today.isoformat()
err = []
seed = min(t.get('added','9999') for t in tools)  # initial bulk import; legacy tools may lack dates
def ok(s):
    try: dt.date.fromisoformat(s); return True
    except Exception: return False
for t in tools:
    for k in ('released', 'firstReleased'):
        if t.get(k) and not ok(t[k]): err.append(f"{t['slug']}: invalid {k} {t[k]!r}")
    if t.get('added', '') > seed and t.get('added', '') >= lo and not (t.get('released') or t.get('firstReleased')):
        err.append(f"{t['slug']}: added {t['added']} but has no released/firstReleased date")
exp = sorted([t for t in tools if lo <= (t.get('released') or t.get('firstReleased') or '') <= hi], key=lambda t: t.get('released') or t['firstReleased'], reverse=True)
body = m.group(3) if m else ''
if exp and not m: err.append('Recently released section missing from dist/index.html')
for t in exp:
    if f'/tools/{t["slug"]}/' not in body: err.append(f"{t['slug']} ({t.get('released') or t['firstReleased']}) missing from Recently released")
if m:
    order = re.findall(r'/tools/([^/"]+)/', body); order = list(dict.fromkeys(order))
    if order[:len(exp)] != [t['slug'] for t in exp][:len(order)] and set(order) >= {t['slug'] for t in exp}:
        pass
print(f"check_recent: {len(exp)} expected in window {lo}..{hi}, {len(err)} error(s)")
for e in err: print('  ' + e)
sys.exit(1 if err else 0)
