import json,subprocess,sys,datetime
sys.path.insert(0,'scripts'); from candidates import T
from concurrent.futures import ThreadPoolExecutor
def ok(u):
    if not u: return True
    r=subprocess.run(["curl","-sL","-o","/dev/null","-w","%{http_code}","-m","25","-A","Mozilla/5.0 (X11; Linux x86_64) Chrome/124",u],capture_output=True,text=True).stdout
    return r.startswith(("2","3")) or r in("403","405","429"), r
def chk(t):
    if not t[2]: return t,False,"empty"
    a=ok(t[2]); g=ok("https://github.com/"+t[3]) if t[3] else (True,"")
    return t,a[0] and g[0],f"{a[1]} {g[1]}"
out=[];today=datetime.date.today().isoformat()
with ThreadPoolExecutor(16) as ex:
  for t,good,info in ex.map(chk,T):
    if not good: print("DROP",t[0],info); continue
    if info.split()[0] in("403","405","429"): print("WARN",t[0],info)
    n,c,u,gh,pa,li,pr,de,tg=t
    out.append(dict(slug=''.join(ch if ch.isalnum() else '-' for ch in n.lower()).strip('-').replace('--','-'),name=n,category=c,url=u,github=("https://github.com/"+gh) if gh else None,paper=pa or None,license=li,pricing=pr,description=de,tags=tg.split(','),added="2026-10-15",lastChecked=today))
json.dump(out,open('src/data/tools.json','w'),indent=1); print(len(out))
