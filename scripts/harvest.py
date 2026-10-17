#!/usr/bin/env python3
"""Harvest candidate tools from curated awesome lists, dedupe, enrich (GitHub GraphQL, Crossref/arXiv).
Stages (cached in /workspace/jev/harvest/): links -> enrich -> papers. Jev + emit are in harvest_jev.py.
Usage: python3 scripts/harvest.py [links|enrich|papers|all]"""
import json, re, sys, subprocess, base64, os, time, urllib.request, urllib.parse
D = '/workspace/jev/harvest'; os.makedirs(D, exist_ok=True)
SOURCES = ['seandavi/awesome-single-cell','danielecook/Awesome-Bioinformatics','Peldom/papers_for_protein_design_using_DL',
 'OmicsML/awesome-foundation-model-single-cell-papers','davidliwei/awesome-CRISPR','apeterswu/Awesome-Bio-Foundation-Models',
 'FreedomIntelligence/Awesome-AI4Med','aristoteleo/awesome-bioagent-papers','wrab12/awesome-spatial-transcriptomics',
 'crazyhottommy/awesome-long-reads','AspirinCode/awesome-AI4MolConformation-MD']
TOOLS = json.load(open('src/data/tools.json'))
def gh(*a): return subprocess.run(['gh','api',*a],capture_output=True,text=True).stdout
def nrm(s): return re.sub(r'[^a-z0-9]','',(s or '').lower())
def http(u):
    r=urllib.request.Request(u,headers={'User-Agent':'toolome/1.0 (mailto:toolome.bio@gmail.com)'}); return urllib.request.urlopen(r,timeout=30).read()

def links():
    have_repo={t['github'].lower().rstrip('/') for t in TOOLS if t.get('github')}
    have_name={nrm(x) for t in TOOLS for x in [t['name'],t['slug']]+re.split(r'[/(),&]',t['name']) if len(nrm(x))>2}
    C={}
    for src in SOURCES:
        md=base64.b64decode(json.loads(gh(f'repos/{src}/readme'))['content']).decode('utf8','ignore'); sec=''
        for line in md.splitlines():
            if line.startswith('#'): sec=line.strip('# ').strip(); continue
            for m in re.finditer(r'github\.com/([\w.-]+)/([\w.-]+)',line):
                o,r=m.group(1),re.sub(r'\.git$','',m.group(2)).rstrip('.')
                if o.lower() in ('sponsors','topics','orgs','features','apps') or r.lower() in ('issues','pulls','wiki'): continue
                full=f'{o}/{r}'; k=full.lower()
                if k==src.lower(): continue
                c=C.setdefault(k,{'repo':full,'sources':[],'lines':[],'sections':[]})
                if src not in c['sources']: c['sources'].append(src); c['lines'].append(re.sub(r'\s+',' ',line)[:300]); c['sections'].append(sec)
    st={'harvested':len(C)}
    out={}
    for k,c in C.items():
        if 'https://github.com/'+k in have_repo or nrm(c['repo'].split('/')[1]) in have_name: continue
        out[k]=c
    st['after_dedupe']=len(out); json.dump(out,open(f'{D}/links.json','w'),indent=1); print(st)

Q='''query{%s}'''
F='''r%d: repository(owner:%s,name:%s){nameWithOwner url description homepageUrl stargazerCount createdAt isArchived isFork
 licenseInfo{spdxId} owner{login __typename} releases(first:1,orderBy:{field:CREATED_AT,direction:ASC}){nodes{publishedAt tagName}}
 readme:object(expression:"HEAD:README.md"){... on Blob{text}}}'''
def enrich():
    L=json.load(open(f'{D}/links.json')); keys=list(L); E={}
    for i in range(0,len(keys),40):
        part=keys[i:i+40]
        q=Q%' '.join(F%(j,json.dumps(L[k]['repo'].split('/')[0]),json.dumps(L[k]['repo'].split('/')[1])) for j,k in enumerate(part))
        res=json.loads(subprocess.run(['gh','api','graphql','-f','query='+q],capture_output=True,text=True).stdout or '{}').get('data') or {}
        for j,k in enumerate(part):
            r=res.get(f'r{j}')
            if not r: continue
            rd=(r.pop('readme') or {}).get('text') or ''
            r['readme']=rd[:6000]; E[k]={**L[k],**r}
        print(i,len(E),file=sys.stderr)
    json.dump(E,open(f'{D}/enriched.json','w'),indent=1); print({'enriched':len(E)})

PAT=re.compile(r'(https?://(?:arxiv\.org/(?:abs|pdf)/\d{4}\.\d{4,5}|(?:www\.)?biorxiv\.org/content/10\.\d+/[\d.]+|doi\.org/10\.\d{4,9}/[^\s)\]>"]+|www\.nature\.com/articles/[\w.-]+|academic\.oup\.com/[^\s)\]>"]+/(?:doi/)?10\.\d+/[^\s)\]>"]+))')
def doi_of(u):
    m=re.search(r'(10\.\d{4,9}/[^\s?#]+)',u)
    if m: return re.sub(r'(\.full|\.abstract|\.full-text|v\d+)$','',m.group(1).rstrip('/.'))
    m=re.search(r'nature\.com/articles/([^/?#]+)',u)
    return '10.1038/'+m.group(1) if m else None
def resolve(u):
    """returns dict(title,venue,year,date) from arXiv/Crossref, or None"""
    m=re.search(r'arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})',u)
    if m:
        x=http('https://export.arxiv.org/api/query?id_list='+m.group(1)).decode()
        t=re.findall(r'<title>([^<]+)',x); p=re.findall(r'<published>([^<]+)',x)
        if len(t)<2 or not p: return None
        return dict(url='https://arxiv.org/abs/'+m.group(1),title=re.sub(r'\s+',' ',t[1]),venue='arXiv preprint',year=int(p[0][:4]),date=p[0][:10])
    d=doi_of(u)
    if not d: return None
    if d.startswith('10.48550/'):
        return resolve('https://arxiv.org/abs/'+d.split('arXiv.')[-1])
    m_=json.loads(http('https://api.crossref.org/works/'+urllib.parse.quote(d)))['message']
    dp=lambda k:(m_.get(k) or {}).get('date-parts',[[None]])[0]
    yr=(dp('published-print') or dp('published-online') or dp('issued'))[0]
    if m_.get('type')=='posted-content':
        inst=(m_.get('institution') or [{}])[0].get('name') or m_.get('publisher','')
        nm='bioRxiv' if 'bioRxiv' in inst or 'biorxiv' in u else ('medRxiv' if 'medRxiv' in inst else ('ChemRxiv' if 'chemrxiv' in inst.lower() else ('Research Square' if 'Research Square' in inst else None)))
        v=nm+' preprint' if nm else None
    else:
        ct=m_.get('container-title') or []; v=ct[0] if ct else None
    dates=[x for x in (dp('posted'),dp('published-online'),dp('published-print'),dp('issued')) if x and x[0] and len(x)==3]
    date='%04d-%02d-%02d'%tuple(min(dates)) if dates else None
    return dict(url='https://doi.org/'+d,title=(m_.get('title') or [''])[0],venue=(v or '').replace('&amp;','&').strip() or None,year=yr,date=date)
def papers():
    E=json.load(open(f'{D}/enriched.json')); P=json.load(open(f'{D}/papers.json')) if os.path.exists(f'{D}/papers.json') else {}
    for k,c in E.items():
        if k in P or c['stargazerCount']<int(os.environ.get('MINSTARS','50')) or c['isArchived'] or c['isFork']: continue
        name=nrm(c['nameWithOwner'].split('/')[1]); got=None
        for u in list(dict.fromkeys(PAT.findall(c['readme'])))[:6]:
            try: r=resolve(u)
            except Exception as e: r=None
            time.sleep(0.15)
            nm=re.escape(c['nameWithOwner'].split('/')[1].lower())
            if r and r.get('title') and len(name)>=3 and re.search(r'(?<![a-z0-9])'+nm+r'(?![a-z0-9]|-?\d)',r['title'].lower()): got=r; break
        P[k]=got
    json.dump(P,open(f'{D}/papers.json','w'),indent=1); print({'papers_checked':len(P),'verified':sum(1 for v in P.values() if v)})
if __name__=='__main__':
    s=sys.argv[1] if len(sys.argv)>1 else 'all'
    for f in ([links,enrich,papers] if s=='all' else [globals()[s]]): f()
