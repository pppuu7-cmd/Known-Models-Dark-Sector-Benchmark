#!/usr/bin/env python3
import json, math
from pathlib import Path

OMEGAS=['15','1e4']
PROFILES=['coarse_localized','production_core','super_ref']
KINDS=['background','tt','pk']

def rows(path):
    out=[]
    if path is None or not path.exists(): return out
    for line in path.read_text(errors='ignore').splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        try: v=[float(x) for x in s.split()]
        except ValueError: continue
        if v and all(math.isfinite(x) for x in v): out.append(v)
    return out

def find_file(base,suffix):
    xs=sorted((base/'output').glob(f'*{suffix}'))
    return xs[0] if xs else None

def series(base,kind):
    if kind=='background': p=find_file(base,'_background.dat'); xi,yi=0,3
    elif kind=='tt': p=find_file(base,'_cl.dat'); xi,yi=0,1
    else: p=find_file(base,'_pk.dat'); xi,yi=0,1
    rr=rows(p); pts=[]
    for r in rr:
        if len(r)>max(xi,yi): pts.append((r[xi],r[yi]))
    pts.sort(key=lambda z:z[0]); return pts

def interp(pts,x):
    if not pts or x<pts[0][0] or x>pts[-1][0]: return None
    lo,hi=0,len(pts)-1
    while hi-lo>1:
        m=(lo+hi)//2
        if pts[m][0]<=x: lo=m
        else: hi=m
    if pts[lo][0]==x:return pts[lo][1]
    x0,y0=pts[lo]; x1,y1=pts[hi]
    if x1==x0:return y0
    return y0+(y1-y0)*(x-x0)/(x1-x0)

def compare(a,b):
    es=[]
    for x,y in a:
        z=interp(b,x)
        if z is None: continue
        es.append(2*abs(y-z)/(abs(y)+abs(z)+1e-300))
    if not es:return {'n':0,'max':None,'rms':None}
    return {'n':len(es),'max':max(es),'rms':math.sqrt(sum(e*e for e in es)/len(es))}

out={'schema':'m29_k4d_final_acceptance_v0.1',
     'provider_commit':'0009f51d89e6465c79e570b496c66fc90058fa77',
     'parent_k4':'M29_K4_NOT_ESTABLISHED_NUMERICAL_ROBUSTNESS',
     'parent_k4b':'M29_K4B_GRID_DOMINATED',
     'parent_k4c':'M29_K4C_FULL_CORE_REQUIRED',
     'K3_status':'BLOCKED_PROVIDER_GAUGE_IMPLEMENTATION',
     'metrics':{},'checks':{},'exit_codes':{},'K4_promoted':False,'physical_falsification':False}
all_exit=True; all_finite=True; all_pass=True
for om in OMEGAS:
    data={}; out['metrics'][om]={}
    for pr in PROFILES:
        base=Path('m29k4d')/om/pr
        ep=base/'exit_code.txt'
        try: rc=int(ep.read_text().strip())
        except Exception: rc=None
        out['exit_codes'][f'{om}:{pr}']=rc; all_exit &= (rc==0)
        data[pr]={}
        for kind in KINDS:
            pts=series(base,kind); data[pr][kind]=pts; all_finite &= len(pts)>0
    for pr in ('coarse_localized','production_core'):
        out['metrics'][om][pr]={kind:compare(data[pr][kind],data['super_ref'][kind]) for kind in KINDS}
    p=out['metrics'][om]['production_core']; c=out['metrics'][om]['coarse_localized']
    chk={}
    chk['production_thresholds']={
      'tt': p['tt']['max'] is not None and p['tt']['max']<=5e-3 and p['tt']['rms']<=1e-3,
      'pk': p['pk']['max'] is not None and p['pk']['max']<=1e-3 and p['pk']['rms']<=5e-4,
      'background': p['background']['max'] is not None and p['background']['max']<=1e-4 and p['background']['rms']<=5e-5}
    chk['coarse_to_production_nonincrease_20pct']={
      k:(p[k]['rms'] is not None and c[k]['rms'] is not None and p[k]['rms']<=1.2*c[k]['rms']) for k in KINDS}
    chk['pass']=all(chk['production_thresholds'].values()) and all(chk['coarse_to_production_nonincrease_20pct'].values())
    out['checks'][om]=chk; all_pass &= chk['pass']
out['checks']['all_exit_zero']=all_exit; out['checks']['finite_outputs']=all_finite
passed=all_exit and all_finite and all_pass
out['K4_promoted']=passed
if passed:
    out['classification']='M29_K4D_PASS_WITH_SCOPE_NUMERICAL_ROBUSTNESS'
elif not all_exit or not all_finite:
    out['classification']='M29_K4D_BLOCKED_IMPLEMENTATION_OR_NUMERICAL_EXECUTION'
else:
    out['classification']='M29_K4D_NOT_ESTABLISHED_NUMERICAL_ROBUSTNESS'
out['scope']='final synchronous-provider numerical acceptance against prospectively tightened super-reference; original K4 thresholds preserved; does not resolve K3 or promote K5-K9'
Path('waves/wave_05_modified_gravity').mkdir(parents=True,exist_ok=True)
p=Path('waves/wave_05_modified_gravity/M29_K4D_FINAL_ACCEPTANCE_RESULT.json')
p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
