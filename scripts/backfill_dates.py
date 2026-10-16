import json,re,subprocess,urllib.request
from concurrent.futures import ThreadPoolExecutor
d=json.load(open('src/data/tools.json'))
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'toolome/1.0 (mailto:yonghao+toolome@mail.grokbot.com)'}),timeout=25).read().decode()
def repo(t):
    m=re.match(r'https://github.com/([^/]+/[^/#?]+)',t.get('github') or '')
    if not m: return None
    r=subprocess.run(['gh','api','repos/'+m[1].removesuffix('.git'),'--jq','.created_at+" "+.html_url'],capture_output=True,text=True).stdout.split()
    return (r[0][:10],r[1]) if r else None
def paper(t):
    p=t.get('paper') or ''
    try:
        m=re.search(r'arxiv.org/(?:abs|pdf)/(\d{4}\.\d{4,5})',p)
        if m:
            x=get(f'http://export.arxiv.org/api/query?id_list={m[1]}'); dt=re.search(r'<published>(\d{4}-\d\d-\d\d)',x)
            return (dt[1],f'https://arxiv.org/abs/{m[1]}v1') if dt else None
        m=re.search(r'biorxiv.org/content/(10\.1101/[\d.]+)',p)
        if m:
            x=json.loads(get(f'https://api.biorxiv.org/details/biorxiv/{m[1]}'))['collection']
            return (min(c['date'] for c in x),'https://doi.org/'+m[1]) if x else None
        m=re.search(r'(10\.\d{4,9}/[^\s?#]+)',p)
        if not m and 'nature.com/articles/' in p: m=[None,'10.1038/'+p.rsplit('/',1)[1]]
        if m:
            doi=m[1].rstrip('/'); doi=re.sub(r'/(full|abstract|pdf)$','',doi)
            x=json.loads(get('https://api.crossref.org/works/'+doi))['message']
            for k in ('published-online','published-print','issued'):
                if k in x and x[k]['date-parts'][0] and len(x[k]['date-parts'][0])==3:
                    y,mo,da=x[k]['date-parts'][0]; return (f'{y:04d}-{mo:02d}-{da:02d}','https://doi.org/'+doi)
    except Exception as e: return None
def go(t):
    if t.get('released'): return t,None
    c=[x for x in (repo(t),paper(t)) if x]
    return t,(min(c) if c else None)
with ThreadPoolExecutor(8) as ex:
    for t,r in ex.map(go,d):
        if r: t['firstReleased'],t['dateSource']=r
json.dump(d,open('src/data/tools.json','w'),indent=1)
print('dated',sum(1 for t in d if t.get('released') or t.get('firstReleased')),'undated',[t['slug'] for t in d if not(t.get('released') or t.get('firstReleased'))])
