import json,re,urllib.request,time,sys
P='src/data/tools.json';T=json.load(open(P))
def get(u):
    r=urllib.request.Request(u,headers={'User-Agent':'toolome/1.0 (mailto:toolome.bio@gmail.com)'})
    return json.load(urllib.request.urlopen(r,timeout=30))
def doi_of(u):
    m=re.search(r'(10\.\d{4,9}/[^\s?#]+)',u)
    if m: return re.sub(r'(\.full|\.abstract|\.full-text|v\d+)$','',m.group(1).rstrip('/'))
    m=re.search(r'nature\.com/articles/([^/?#]+)',u)
    if m: return '10.1038/'+m.group(1)
    m=re.search(r'genomebiology\.biomedcentral\.com/articles/(10\.[^?#]+)',u)
    return None
st={'filled':0,'preprint':0,'omit':[]}
for t in T:
    u=t.get('paper')
    if not u: continue
    v=y=None
    try:
        m=re.search(r'arxiv\.org/(?:abs|pdf)/(\d{4})\.',u)
        if m: v='arXiv preprint'; y=2000+int(m.group(1)[:2])
        else:
            d=doi_of(u)
            if d and d.startswith('10.48550/'):
                v='arXiv preprint';y=2000+int(re.search(r'arXiv\.(\d\d)',d,re.I).group(1))
            elif d:
                if re.search(r'biorxiv\.org',u): d=re.sub(r'v\d+$','',d)
                m_=get('https://api.crossref.org/works/'+d)['message']
                yr=(m_.get('published-print') or m_.get('published-online') or m_.get('issued') or {}).get('date-parts',[[None]])[0][0]
                if m_.get('type')=='posted-content':
                    inst=(m_.get('institution') or [{}])[0].get('name') or m_.get('publisher','')
                    nm='bioRxiv' if 'bioRxiv' in inst or 'biorxiv' in u else ('medRxiv' if 'medRxiv' in inst else ('ChemRxiv' if 'ChemRxiv' in inst or 'chemrxiv' in inst.lower() else ('Research Square' if 'Research Square' in inst else None)))
                    v=nm+' preprint' if nm else None
                else:
                    ct=m_.get('container-title') or []
                    v=ct[0] if ct else None
                    if not v and m_.get('type')=='proceedings-article': v=(m_.get('event') or {}).get('name')
                y=yr
                time.sleep(0.2)
    except Exception as e: print('ERR',t['slug'],u,e,file=sys.stderr)
    if v:
        v=v.replace('&amp;','&').strip()
        t['paperVenue']=v
        if y: t['paperYear']=int(y)
        st['preprint' if 'preprint' in v else 'filled']+=1
    else:
        t.pop('paperVenue',None);t.pop('paperYear',None);st['omit'].append((t['slug'],u))
json.dump(T,open(P,'w'),indent=2,ensure_ascii=False);open(P,'a').write('\n')
print(st)
for t in T[:0]:pass
