#!/usr/bin/env python3
"""Toolome data audit. Read-only by default.

  python3 scripts/audit.py                 # L1 local consistency rules (exit 1 on any ERROR)
  python3 scripts/audit.py --online        # + L2 GitHub checks via `gh api` (stars, archived, moved, 404, license, activity)
  python3 scripts/audit.py --online --fix-stars   # also write fresh specs.stars + specs.starsChecked (only these fields)
  python3 scripts/audit.py --online --fix-archived  # also set/clear `archived` + `archivedChecked` from GitHub's archived flag
  python3 scripts/audit.py --online --fix-moves   # also rewrite `github` for repos GitHub reports as renamed/moved
  python3 scripts/audit.py --links         # + link-liveness report (report only, never deletes)
  python3 scripts/audit.py --links --stamp-checked  # also set lastChecked=today for tools whose links all returned 2xx
Writes audit-report.json (gitignored). Exceptions live in scripts/audit_allow.json: {"RULE": {"slug": "reason"}}.
"""
import json, re, sys, datetime, subprocess, collections, os
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'src/data/tools.json')
SITE = open(os.path.join(ROOT, 'src/lib/site.js')).read()
ALLOW = json.load(open(os.path.join(ROOT, 'scripts/audit_allow.json'))) if os.path.exists(os.path.join(ROOT, 'scripts/audit_allow.json')) else {}
TODAY = datetime.date.today()
args = set(sys.argv[1:])
tools = json.load(open(DATA))
CATS = re.findall(r"'([a-z-]+)':\s*\['", SITE.split('export const CATS')[1].split('};')[0])
SPEC_FIELDS = {c: re.findall(r"\['(\w+)','", body) for c, body in re.findall(r"'([a-z-]+)':\[(\[.*?\])\]", SITE.split('export const SPEC_FIELDS')[1].split('};')[0])}
PAIRS = re.findall(r"\['([^']+)','([^']+)'\]", SITE.split('export const PAIRS')[1].split(';')[0])
BLURB = re.findall(r"'([^']+)':'", SITE.split('export const PAIR_BLURB')[1].split('};')[0])
PRICING = {'Open source', 'Open source (non-commercial)', 'Contact', 'Freemium', 'Free (research)', 'Paid', 'Research release'}
SPDX = {'MIT','Apache-2.0','BSD-3-Clause','BSD-2-Clause','BSD-3-Clause-Clear','GPL-3.0','GPL-2.0','LGPL-3.0','AGPL-3.0','MPL-2.0','CC0-1.0','CC-BY-4.0','CC-BY-NC-4.0','CC-BY-NC-SA-4.0','CC-BY-NC-ND-4.0','Commercial','Proprietary','PolyForm-Strict-1.0','Oxford Nanopore Public License 1.0','Custom','Mixed','NOASSERTION'}
SEV = {}  # rule -> severity
out = []
def add(sev, rule, slug, msg):
    SEV[rule] = sev
    if slug in ALLOW.get(rule, {}): sev = 'ALLOWED'
    out.append(dict(sev=sev, rule=rule, slug=slug, msg=msg))
E = lambda *a: add('ERROR', *a); W = lambda *a: add('WARN', *a); I = lambda *a: add('INFO', *a)
DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
GH = re.compile(r'^https://github\.com/[^/\s]+/[^/\s]+$')
def norm(s): return re.sub(r'\s+', ' ', (s or '').strip().lower().rstrip('/'))

def l1():
    seen = collections.defaultdict(lambda: collections.defaultdict(list))
    for t in tools:
        s, sp = t['slug'], t.get('specs') or {}
        gh = t.get('github')
        # D: dependencies
        if gh and not (isinstance(sp.get('stars'), int) and sp['stars'] > 0): E('D1', s, 'github set but specs.stars missing')
        if 'stars' in sp and not gh: E('D2', s, 'specs.stars without github')
        if 'stars' in sp and not sp.get('starsChecked'): W('D1b', s, 'specs.stars without specs.starsChecked')
        if t.get('released') and not t.get('source'): E('D3', s, 'released without source')
        if t.get('firstReleased') and not t.get('dateSource'): E('D3', s, 'firstReleased without dateSource')
        if sp and not (t.get('specsSources') and t.get('specsChecked')): E('D4', s, 'specs without specsSources/specsChecked')
        fields = SPEC_FIELDS.get(t['category'], [])
        if sp and fields and sum(1 for f in fields if sp.get(f)) * 2 < len(fields): W('D5', s, f"fewer than half of {fields} filled")
        if t['pricing'].startswith('Open source') and not gh: W('D6', s, 'Open source pricing but no github')
        if not sp: W('D7', s, 'no specs')
        if t.get('paper') and not t.get('paperVenue'): W('D9', s, 'paper URL without paperVenue')
        if not (t.get('released') or t.get('firstReleased')): W('D8', s, 'no date')
        if 'specsSource' in t: W('D9', s, 'redundant singular specsSource')
        if t.get('archived') and not gh: E('A1', s, 'archived without github')
        if t.get('archived') and not t.get('archivedChecked'): E('A1', s, 'archived without archivedChecked')
        if 'archived' in t and t['archived'] is not True: E('A1', s, 'archived must be true or absent')
        # C: contradictions
        lic, pr = (t['license'] + (' (' + t['licenseNote'] + ')' if t.get('licenseNote') else '')), t['pricing']
        if pr == 'Open source' and re.search(r'commercial|proprietary', lic, re.I) and not re.search(r'non-commercial|incl\. commercial', lic, re.I): W('C1', s, f'Open source vs license {lic!r}')
        if pr in ('Paid', 'Contact') and re.match(r'(MIT|Apache|BSD|GPL)', lic): W('C1', s, f'{pr} vs license {lic!r}')
        if re.search(r'\bNC\b|non-commercial|academic', lic, re.I) and pr == 'Open source': E('C2', s, f'non-commercial license {lic!r} but pricing "Open source"')
        m = re.search(r'\(([^)]+)\)', str(sp.get('weights', '')))
        if m:
            wl = m.group(1)
            if re.search(r'non-commercial|academic|\bNC\b', wl, re.I) and not re.search(r'non-commercial|academic|NC|research', lic, re.I): W('C3', s, f'weights ({wl}) vs license {lic!r}')
            elif re.match(r'(MIT|Apache|BSD|GPL|CC-|CC0)', wl) and wl.split()[0].split('-')[0] not in lic: W('C3', s, f'weights ({wl}) vs license {lic!r}')
        if t.get('released') and t.get('firstReleased') and t['released'] != t['firstReleased']: W('C4', s, 'released != firstReleased')
        um = re.match(r'^https://github\.com/([^/]+/[^/#?]+)', t.get('url', ''))
        if um and norm(gh) != norm('https://github.com/' + um.group(1)): E('C5', s, 'url is a GitHub repo but github differs/missing')
        # F: formats
        if gh and not GH.match(gh): E('F1', s, f'bad github url {gh}')
        for k in ('released', 'firstReleased', 'added', 'lastChecked', 'specsChecked'):
            v = t.get(k) or (sp.get('starsChecked') if k == 'specsChecked' else None)
            if t.get(k):
                v = t[k]
                if not DATE.match(v) or not ('1990-01-01' <= v <= TODAY.isoformat()): E('F2', s, f'{k}={v}')
        if sp.get('starsChecked') and not DATE.match(sp['starsChecked']): E('F2', s, 'bad starsChecked')
        if t['category'] not in CATS: E('F3', s, f"category {t['category']}")
        ai = t.get('alsoIn')
        if ai is not None:
            if not isinstance(ai, list) or not ai: E('F7', s, f'alsoIn must be a non-empty list: {ai!r}')
            else:
                for c in ai:
                    if c not in CATS: E('F7', s, f'alsoIn unknown category {c!r}')
                if t['category'] in ai: E('F7', s, 'alsoIn repeats primary category')
                if len(set(ai)) != len(ai): E('F7', s, f'alsoIn duplicates {ai}')
        if pr not in PRICING: E('F3', s, f'pricing {pr!r}')
        if t['license'] not in SPDX: I('F4', s, f'non-SPDX license {lic!r}')
        tg = t.get('tags') or []
        if not tg or any((not x) or x != x.lower() for x in tg) or len(set(tg)) != len(tg): W('F5', s, f'tags {tg}')
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', s): I('F6', s, 'slug style (rename deferred: needs redirects)')
        d = t.get('description', '')
        if not (40 <= len(d) <= 220): W('F7', s, f'description length {len(d)}')
        if norm(d) == norm(t['name']): W('F7', s, 'description equals name')
        if re.search(r'(?<![-\w])free(?![-\w])', d, re.I): W('F8', s, 'description says "free" (house rule: say "no signup")')
        for k in ('github', 'url', 'paper'):
            if t.get(k): seen[k][norm(t[k])].append(s)
        seen['name'][norm(t['name'])].append(s); seen['slug'][s].append(s)
    for k, rule, f in (('github', 'U1', W), ('url', 'U2', W), ('paper', 'U2', W), ('name', 'U3', E), ('slug', 'U3', E)):
        for v, ss in seen[k].items():
            if len(ss) > 1:
                for x in ss: f(rule, x, f'duplicate {k} {v} shared with {[y for y in ss if y != x]}')
    by = {t['slug']: t for t in tools}
    for a, b in PAIRS:
        if a not in by or b not in by: E('U4', f'{a}-vs-{b}', 'PAIRS references missing slug')
        elif by[a]['category'] != by[b]['category']: E('U4', f'{a}-vs-{b}', 'PAIRS across categories')
    pk = {f'{a}-{b}' for a, b in PAIRS}
    for k in pk ^ set(BLURB): W('U5', k, 'PAIR_BLURB/PAIRS mismatch')

def gh_repo(full):
    r = subprocess.run(['gh', 'api', f'repos/{full}'], capture_output=True, text=True)
    if r.returncode: return full, None, r.stderr.strip()[:120]
    return full, json.loads(r.stdout), ''

def l2():
    fix_stars, fix_moves, fix_arch, changed = '--fix-stars' in args, '--fix-moves' in args, '--fix-archived' in args, False
    repos = {t['github'].split('github.com/')[1]: t for t in tools if t.get('github') and GH.match(t['github'])}
    users = collections.defaultdict(list)
    for t in tools:
        if t.get('github') and GH.match(t['github']): users[t['github'].split('github.com/')[1].lower()].append(t)
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(gh_repo, {k for k in repos}))
    for full, d, err in res:
        for t in users[full.lower()]:
            s, sp = t['slug'], t.setdefault('specs', {})
            if d is None: E('G2', s, f'repo {full} not reachable: {err}'); continue
            arch = bool(d.get('archived'))
            if arch != bool(t.get('archived')):
                W('G2', s, f"repo {full} archived={arch} but data says {bool(t.get('archived'))}")
            elif arch: I('G2', s, f'repo {full} archived (badge shown)')
            if fix_arch:
                if arch: t['archived'] = True; t['archivedChecked'] = TODAY.isoformat()
                else: t.pop('archived', None); t.pop('archivedChecked', None)
                changed = True
            if d['full_name'].lower() != full.lower():
                W('G2', s, f"repo moved {full} -> {d['full_name']}")
                if fix_moves: t['github'] = d['html_url']; changed = True
            n = d['stargazers_count']; old = sp.get('stars')
            if old is None or abs(n - old) > max(500, 0.2 * old) or not sp.get('starsChecked'):
                I('G1', s, f'stars {old} -> {n}')
            if fix_stars and n > 0:
                sp['stars'] = n; sp['starsChecked'] = TODAY.isoformat(); changed = True
                if not t.get('specsSources'): t['specsSources'] = [t['github'] + '#readme']
                if not t.get('specsChecked'): t['specsChecked'] = TODAY.isoformat()
            g = (d.get('license') or {}).get('spdx_id')
            if g and g != 'NOASSERTION' and g not in t['license'] and not (g == 'GPL-3.0' and 'GPL' in t['license']):
                I('G3', s, f'GitHub license {g} vs ours {t["license"]!r} (report only)')
            p = d.get('pushed_at', '')[:10]
            if p and (TODAY - datetime.date.fromisoformat(p)).days > 730: W('G4', s, f'no push since {p}')
            if not sp: del t['specs']
    return changed

def links():
    def chk(u):
        r = subprocess.run(['curl', '-sL', '-o', '/dev/null', '-w', '%{http_code}', '-m', '25', '-A', 'Mozilla/5.0 (X11; Linux x86_64) Chrome/124', u], capture_output=True, text=True).stdout
        return u, r
    urls = collections.defaultdict(list)
    for t in tools:
        for k in ('url', 'paper', 'source', 'dateSource'):
            if t.get(k): urls[t[k]].append(t['slug'])
        for x in t.get('specsSources') or []: urls[x].append(t['slug'])
    for t in tools:
        if t.get('github'): urls[t['github']].append(t['slug'])
    bad = set()
    with ThreadPoolExecutor(16) as ex:
        for u, c in ex.map(chk, list(urls)):
            if not c.startswith('2'):
                bad.update(urls[u])
                for s in set(urls[u]): (I if c in ('403', '429', '302', '405') or 'doi.org/10.1101' in u else W)('G5', s, f'{c} {u}')
    return bad

def stamp(bad):
    # lastChecked = today only for tools whose every link returned 2xx in this run; others keep their last real date
    n = 0
    for t in tools:
        if t['slug'] not in bad and t.get('lastChecked') != TODAY.isoformat(): t['lastChecked'] = TODAY.isoformat(); n += 1
    json.dump(tools, open(DATA, 'w'), indent=2, ensure_ascii=False); open(DATA, 'a').write('\n')
    print(f'lastChecked stamped {TODAY} on {n} tools; {len(bad)} tools had a non-2xx link and kept their previous date')

l1()
if '--online' in args and l2():
    json.dump(tools, open(DATA, 'w'), indent=2, ensure_ascii=False); open(DATA, 'a').write('\n'); print('wrote', DATA)
if '--links' in args:
    _bad = links()
    if '--stamp-checked' in args: stamp(_bad)
json.dump(out, open(os.path.join(ROOT, 'audit-report.json'), 'w'), indent=1)
cnt = collections.Counter((o['sev'], o['rule']) for o in out)
for o in out:
    if o['sev'] in ('ERROR',) or ('-v' in args and o['sev'] != 'ALLOWED'): print(f"{o['sev']:5} {o['rule']:4} {o['slug']}: {o['msg']}")
print('summary:', ', '.join(f'{r}:{s}={n}' for (s, r), n in sorted(cnt.items(), key=lambda x: (x[0][1], x[0][0]))))
nerr = sum(n for (s, r), n in cnt.items() if s == 'ERROR')
print(f'{nerr} ERROR, {sum(n for (s,r),n in cnt.items() if s=="WARN")} WARN')
sys.exit(1 if nerr else 0)
