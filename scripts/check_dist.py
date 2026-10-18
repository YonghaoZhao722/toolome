#!/usr/bin/env python3
"""L3 post-build checks on dist/. Run after `astro build`. Exit 1 on any failure."""
import json, os, re, sys, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(ROOT, 'dist')
tools = json.load(open(os.path.join(ROOT, 'src/data/tools.json')))
site = open(os.path.join(ROOT, 'src/lib/site.js')).read()
CATS = re.findall(r"'([a-z-]+)':\s*\['", site.split('export const CATS')[1].split('};')[0])
PAIRS = re.findall(r"\['([^']+)','([^']+)'\]", site.split('export const PAIRS')[1].split(';')[0])
errs = []
def err(rule, where, msg): errs.append(f'{rule} {where}: {msg}')
lic_text = lambda t: t['license'] if not t.get('licenseNote') else (t['licenseNote'] if t['license'] in ('Custom','Mixed','NOASSERTION') else f"{t['license']} ({t['licenseNote']})")
rd = lambda p: open(os.path.join(D, p), encoding='utf-8').read()
# H1 + H5: tool pages
for t in tools:
    p = f"tools/{t['slug']}/index.html"
    if not os.path.exists(os.path.join(D, p)): err('H2', p, 'missing tool page'); continue
    h = rd(p)
    m = re.search(r'<th scope="row"[^>]*>GitHub stars</th>\s*<td[^>]*>(.*?)</td>', h, re.S)
    if t.get('github'):
        if not m or '—' in m.group(1): err('H1', t['slug'], 'has GitHub but stars cell missing or "—"')
    elif m: err('H1', t['slug'], 'stars row shown without GitHub')
    if bool(t.get('archived')) != bool(re.search(r'<h1[^>]*>(?:(?!</h1>).)*class="arch"', h, re.S)): err('H8', t['slug'], 'Archived badge does not match data')
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: ld = json.loads(j)
        except Exception as e: err('H5', t['slug'], f'JSON-LD parse: {e}'); continue
        if ld.get('@type') == 'SoftwareApplication':
            if ld.get('license') != lic_text(t): err('H5', t['slug'], 'JSON-LD license mismatch')
            if ld.get('codeRepository') != t.get('github'): err('H5', t['slug'], 'JSON-LD codeRepository mismatch')
# H2: counts
tdirs = [x for x in os.listdir(os.path.join(D, 'tools')) if os.path.exists(os.path.join(D, 'tools', x, 'index.html'))]
redir = [x for x in tdirs if 'http-equiv="refresh"' in rd(f'tools/{x}/index.html')]
slugs = {t['slug'] for t in tools}
for x in redir:
    m = re.search(r'url=/tools/([^/"]+)/', rd(f'tools/{x}/index.html'))
    if not m or m.group(1) not in slugs: err('H9', x, 'redirect page target missing')
    if x in slugs: err('H9', x, 'redirect page shadows a live slug')
n_pages = len(tdirs) - len(redir)
if n_pages != len(tools): err('H2', 'tools/', f'{n_pages} pages vs {len(tools)} tools')
for c in CATS:
    h = rd(f'category/{c}/index.html'); n = h.count('class="card"'); want = sum(t['category'] == c or c in (t.get('alsoIn') or []) for t in tools)
    if n != want: err('H2', c, f'{n} cards vs {want} tools')
idx = rd('index.html')
m = re.search(r'<span class="num">(\d+)</span>', idx)
if not m or int(m.group(1)) != len(tools): err('H2', 'index', f'home count {m and m.group(1)} vs {len(tools)}')
if idx.count('class="card"') < len(tools): err('H2', 'index', 'home shows fewer cards than tools')
# H3: internal links + junk strings
files = []
for dp, _, fs in os.walk(D):
    for f in fs:
        if f.endswith(('.html', '.txt', '.xml')): files.append(os.path.join(dp, f))
for f in files:
    s = open(f, encoding='utf-8').read(); rel = os.path.relpath(f, D)
    body = re.sub(r'<script\b.*?</script>', '', s, flags=re.S)
    for bad in ('undefined', 'NaN', '[object Object]', '>null<'):
        if re.search(r'(?<![\w-])' + re.escape(bad) + r'(?![\w-])', re.sub(r'<[^>]+>', ' ', body) if bad != '>null<' else body): err('H3', rel, f'contains {bad!r}')
    if f.endswith('.html'):
        for href in re.findall(r'(?:href|src)="([^"]+)"', s):
            href = html.unescape(href).split('#')[0].split('?')[0]
            if not href.startswith('/') or href.startswith('//'): continue
            tgt = os.path.join(D, href.lstrip('/'))
            if not (os.path.isfile(tgt) or os.path.isfile(os.path.join(tgt, 'index.html'))): err('H3', rel, f'broken internal link {href}')
# H4: sitemap + llms
sm = set(re.findall(r'<loc>https?://[^/]+(/[^<]*)</loc>', rd('sitemap.xml')))
want = {'/', '/submit/', '/compare/', '/licenses/'} | {f'/category/{c}/' for c in CATS} | {f"/tools/{t['slug']}/" for t in tools} | {f'/compare/{a}-vs-{b}/' for a, b in PAIRS}
for x in want - sm: err('H4', 'sitemap', f'missing {x}')
for x in sm - want: err('H4', 'sitemap', f'extra {x}')
for f in ('llms.txt', 'llms-full.txt'):
    n = len(set(re.findall(r'/tools/([^/)]+)/', rd(f))))
    if n != len(tools): err('H4', f, f'{n} tools vs {len(tools)}')
for e in errs: print('ERROR', e)
print(f'check_dist: {len(errs)} error(s) over {len(files)} files, {len(tools)} tools')
sys.exit(1 if errs else 0)
