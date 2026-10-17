#!/usr/bin/env python3
"""Jev review + cap + emit for harvested candidates.
  python3 scripts/harvest_jev.py jev     -> /workspace/jev/harvest_out.json
  python3 scripts/harvest_jev.py emit N  -> appends up to N entries to src/data/tools.json (cap 10 per category-year)"""
import json, re, sys, os, subprocess, datetime
sys.path.insert(0, os.path.dirname(__file__)); from jev import ask, choice, cost
D='/workspace/jev/harvest'; OUT='/workspace/jev/harvest_out.json'; P='src/data/tools.json'
TODAY=datetime.date.today().isoformat()
CATDEF={'single-cell':'Single-cell analysis tools and single-cell foundation models','spatial':'Spatial transcriptomics/proteomics analysis',
'protein':'Protein structure prediction, protein design, protein language models, antibodies','genomics':'DNA sequence models, regulatory genomics, variant effect prediction',
'drug-discovery':'Small molecules, docking, cheminformatics, molecular generation, MD for drug discovery','agents':'LLM agents and copilots for biology research',
'cloud-labs':'Cloud labs and wet-lab services','imaging':'Microscopy, bioimage analysis, pathology and medical imaging models',
'datasets':'Datasets, atlases and benchmarks','sequencing':'Read processing, basecalling, alignment, assembly and variant calling',
'proteomics':'Mass-spec proteomics and metabolomics','crispr':'CRISPR guide design, editing outcome analysis, gene editing tools',
'rna':'RNA structure, RNA design, RNA language models','microbiome':'Metagenomics, microbiome profiling, binning',
'clinical':'Clinical and biomedical LLMs / medical AI models','platforms':'R&D and bioinformatics platforms, workflow systems'}
BAR=("Toolome lists only influential, verified AI/ML tools for biology (see INCLUSION.md). AI/ML REQUIRED: the core method must use machine learning (deep learning, neural nets, foundation models, LLMs, trained classifiers) or be an ML dataset/benchmark; classical bioinformatics (aligners like samtools/STAR, quantifiers like kallisto, workflow engines like Nextflow, search like MMseqs2, statistical methods like Scanorama/PHATE) must be rejected. Include only if clearly influential: notable lab/company, "
 "strong peer-reviewed venue (Nature/Science/Cell family, Bioinformatics, NAR, Genome Biology, top ML venue), or meaningful adoption "
 "(roughly hundreds+ GitHub stars), and it is an actual usable tool/model/dataset (not a paper list, tutorial, course, personal script, or awesome list). "
 "Reject abandoned toy projects, generic non-biology software, and wrappers.")
def nrm(s): return re.sub(r'[^a-z0-9]','',(s or '').lower())
def clean(t): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>|!\[[^\]]*\]\([^)]*\)|\[!\[.*?\]\(.*?\)\]\(.*?\)|https?://\S+','',t or '')).strip()
def cands():
    E=json.load(open(f'{D}/enriched.json')); Pp=json.load(open(f'{D}/papers.json'))
    for k,c in E.items():
        if k not in Pp: continue
        c['paper']=Pp[k]; yield k,c
def jev():
    R=json.load(open(OUT)) if os.path.exists(OUT) else {}
    todo=[(k,c) for k,c in cands() if k not in R]
    for i in range(0,len(todo),8):
        part=todo[i:i+8]; qs={}
        for j,(k,c) in enumerate(part):
            p=c['paper'] or {}
            ctx=(f"Repo: {c['nameWithOwner']} (owner type {c['owner']['__typename']}); GitHub description: {c.get('description')}; stars: {c['stargazerCount']}; "
                 f"created {c['createdAt'][:10]}; license {(c.get('licenseInfo') or {}).get('spdxId')}; "
                 f"verified paper: {(p.get('title'),p.get('venue'),p.get('year')) if p else 'none found'}; listed in: {list(zip(c['sources'],c['sections']))}; "
                 f"README excerpt: {clean(c['readme'])[:1200]}")
            qs[f'i{j}']=choice(f"{BAR}\nCandidate:\n{ctx}\nShould Toolome include it?",{'include':'influential, verified, usable biology tool','reject':'below bar or not a tool'})
            qs[f'a{j}']=choice(f"Does this tool's CORE method use machine learning (deep learning, neural nets, foundation models, LLMs, trained classifiers), or is it an ML dataset/benchmark? Classical aligners, quantifiers, workflow engines, statistical methods = no.\n{ctx}",{'ai':'core method is AI/ML','not':'not AI/ML'})
            qs[f'c{j}']=choice(f"Primary Toolome category for this candidate:\n{ctx}",{**CATDEF,'none':'Fits no category'})
        try: r=ask({'bar':BAR},qs)
        except Exception as e: print('ERR',e,file=sys.stderr); continue
        a=r['answers']
        for j,(k,c) in enumerate(part):
            R[k]={'ai':a[f'a{j}']['choice'],'include':a[f'i{j}']['choice'] if a[f'a{j}']['choice']=='ai' else 'reject','p_include':a[f'i{j}']['probabilities'].get('include',0),'category':a[f'c{j}']['choice'],
                  'p_category':a[f'c{j}']['probabilities'],'stars':c['stargazerCount']}
        json.dump(R,open(OUT,'w'),indent=1); print(i,len(R),round(cost(),4),file=sys.stderr)
    print({'reviewed':len(R),'approved':sum(1 for v in R.values() if v['include']=='include' and v['category']!='none'),'cost':cost()})
LIC={'MIT','Apache-2.0','BSD-3-Clause','BSD-2-Clause','GPL-3.0','GPL-2.0','LGPL-3.0','AGPL-3.0','MPL-2.0','CC0-1.0','CC-BY-4.0','CC-BY-NC-4.0','CC-BY-NC-SA-4.0','CC-BY-NC-ND-4.0'}
def emit(N):
    T=json.load(open(P)); R=json.load(open(OUT)); C=dict(cands())
    have={nrm(t['name']) for t in T}|{t['slug'] for t in T}|{(t.get('github') or '').lower() for t in T}
    cnt={}
    for t in T:
        y=(t.get('firstReleased') or t.get('released') or '')[:4]
        if y: cnt[(t['category'],y)]=cnt.get((t['category'],y),0)+1
    ok=[(k,v) for k,v in R.items() if v['include']=='include' and v.get('ai','ai')=='ai' and v['category']!='none']
    ok.sort(key=lambda kv:(-kv[1]['p_include'],-(1 if (C[kv[0]]['paper'] or {}).get('venue') else 0),-kv[1]['stars']))
    stats={'approved':len(ok),'no_date':0,'bad_desc':0,'dup':0,'capped':0,'added':0,'queued':[]}
    allow=json.load(open('scripts/audit_allow.json')); new=[]
    for k,v in ok:
        c=C[k]; p=c['paper'] or {}; repo='https://github.com/'+c['nameWithOwner']; name=c['nameWithOwner'].split('/')[1]
        slug=re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',name.lower())).strip('-')
        if repo.lower() in have or nrm(name) in have or slug in have: stats['dup']+=1; continue
        rel=(c['releases']['nodes'] or [{}])[0].get('publishedAt')
        ds=[(p['date'],p['url'])] if p.get('date') else []
        if rel: ds.append((rel[:10],repo+'/releases/tag/'+c['releases']['nodes'][0]['tagName']))
        if not ds: stats['no_date']+=1; continue
        fr,src=min(ds)
        desc=clean(c.get('description') or '').rstrip('.')+'.'
        desc=re.sub(r'[^\x20-\x7E\u00B0-\u024F\u2013\u2014\u2018-\u201D\u00D7]','',desc).strip()
        if not (40<=len(desc)<=220) or re.search(r'(?<![-\w])free(?![-\w])',desc,re.I): stats['bad_desc']+=1; continue
        key=(v['category'],fr[:4])
        if cnt.get(key,0)>=10: stats['capped']+=1; continue
        if len(new)>=N: stats['queued'].append(k); continue
        cnt[key]=cnt.get(key,0)+1
        lic=(c.get('licenseInfo') or {}).get('spdxId')
        lic=lic if lic in LIC else ('NOASSERTION' if lic in (None,'NOASSERTION','OTHER') else lic)
        pr='Open source (non-commercial)' if '-NC' in lic else ('Research release' if lic=='NOASSERTION' else 'Open source')
        topics=json.loads(subprocess.run(['gh','api',f'repos/{c["nameWithOwner"]}/topics','--jq','.names'],capture_output=True,text=True).stdout or '[]')[:3]
        tags=[re.sub(r'[^a-z0-9-]','',x.lower()) for x in topics if x] or [v['category']]
        e={'slug':slug,'name':name,'category':v['category'],'url':c.get('homepageUrl') if (c.get('homepageUrl') or '').startswith('https://') and 'github.com' not in c.get('homepageUrl') else repo,
           'github':repo}
        if p.get('venue'): e['paper']=p['url']
        e.update(license=lic,pricing=pr,description=desc,tags=list(dict.fromkeys(tags)),added=TODAY,lastChecked=TODAY,firstReleased=fr,dateSource=src,
           notability=f"{c['stargazerCount']} GitHub stars; listed in {', '.join(c['sources'])}"+(f"; {p['venue']} {p.get('year')}" if p.get('venue') else ''),
           specs={'stars':c['stargazerCount'],'starsChecked':TODAY},specsChecked=TODAY,specsSources=[repo],harvested=True)
        if p.get('venue'): e['paperVenue']=p['venue']; e['paperYear']=p.get('year')
        if lic=='NOASSERTION': e['licenseNote']='no license detected by GitHub'
        allow.setdefault('D5',{})[slug]='Auto-harvested entry; category spec fields pending manual review (only verified stars set)'
        new.append(e); have|={slug,nrm(name),repo.lower()}
    stats['added']=len(new); stats['queued_n']=len(stats['queued'])
    T+=new; json.dump(T,open(P,'w'),indent=2,ensure_ascii=False); open(P,'a').write('\n')
    json.dump(allow,open('scripts/audit_allow.json','w'),indent=1,ensure_ascii=False)
    json.dump(stats,open(f'{D}/emit_stats.json','w'),indent=1); print({k:v for k,v in stats.items() if k!='queued'})
if __name__=='__main__':
    {'jev':jev,'emit':lambda:emit(int(sys.argv[2]) if len(sys.argv)>2 else 150)}[sys.argv[1]]()
