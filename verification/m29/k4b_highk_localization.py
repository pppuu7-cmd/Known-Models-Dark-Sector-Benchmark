#!/usr/bin/env python3
import json, math
from pathlib import Path

OMEGAS=['15','1e4']
PROFILES=['baseline_permille','grid_ref','evolution_ref','pk_core_ref','full_ref']


def rows(path):
    out=[]
    if path is None or not path.exists(): return out
    for line in path.read_text(errors='ignore').splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        try: v=[float(x) for x in s.split()]
        except ValueError: continue
        if len(v)>=2 and all(math.isfinite(x) for x in v[:2]): out.append((v[0],v[1]))
    out.sort()
    return out


def find_pk(base):
    xs=sorted((base/'output').glob('*_pk.dat'))
    return xs[0] if xs else None


def interp(pts,x):
    if not pts or x<pts[0][0] or x>pts[-1][0]: return None
    lo,hi=0,len(pts)-1
    while hi-lo>1:
        m=(lo+hi)//2
        if pts[m][0]<=x: lo=m
        else: hi=m
    if pts[lo][0]==x: return pts[lo][1]
    x0,y0=pts[lo]; x1,y1=pts[hi]
    if x1==x0: return y0
    return y0+(y1-y0)*(x-x0)/(x1-x0)


def q(vals,p):
    if not vals: return None
    a=sorted(vals); u=(len(a)-1)*p; i=int(math.floor(u)); j=int(math.ceil(u))
    if i==j:return a[i]
    return a[i]+(a[j]-a[i])*(u-i)


def compare(a,b):
    es=[]
    for x,y in a:
        z=interp(b,x)
        if z is None: continue
        e=2*abs(y-z)/(abs(y)+abs(z)+1e-300)
        es.append((e,x))
    if not es: return {'n':0,'max':None,'rms':None,'median':None,'p95':None,'p99':None,'max_k':None}
    vals=[e for e,_ in es]; em,xm=max(es)
    return {'n':len(vals),'max':em,'rms':math.sqrt(sum(e*e for e in vals)/len(vals)),
            'median':q(vals,.5),'p95':q(vals,.95),'p99':q(vals,.99),'max_k':xm}

out={'schema':'m29_k4b_highk_localization_v0.1','provider_commit':'0009f51d89e6465c79e570b496c66fc90058fa77',
     'parent_classification':'M29_K4_NOT_ESTABLISHED_NUMERICAL_ROBUSTNESS','K4_promoted':False,
     'physical_falsification':False,'metrics':{},'reductions':{},'exit_codes':{},'checks':{}}
all_exit=True; all_finite=True
for om in OMEGAS:
    data={}; out['metrics'][om]={}
    for pr in PROFILES:
        base=Path('m29k4b')/om/pr
        ep=base/'exit_code.txt'; rc=int(ep.read_text().strip()) if ep.exists() else None
        out['exit_codes'][f'{om}:{pr}']=rc; all_exit &= (rc==0)
        pts=rows(find_pk(base)); data[pr]=pts; all_finite &= len(pts)>0
        out['metrics'][om][pr]={'native_n':len(pts),'k_min':pts[0][0] if pts else None,'k_max':pts[-1][0] if pts else None}
    ref=data['full_ref']
    for pr in PROFILES[:-1]: out['metrics'][om][pr]['vs_full_ref']=compare(data[pr],ref)
    e0=out['metrics'][om]['baseline_permille']['vs_full_ref']['max']
    out['reductions'][om]={}
    for pr in ('grid_ref','evolution_ref','pk_core_ref'):
        ep=out['metrics'][om][pr]['vs_full_ref']['max']
        out['reductions'][om][pr]=None if e0 in (None,0) or ep is None else 1-ep/e0

suff={pr: all(out['reductions'][om].get(pr) is not None and out['reductions'][om][pr]>=0.80 for om in OMEGAS)
      for pr in ('grid_ref','evolution_ref','pk_core_ref')}
out['checks']['all_exit_zero']=all_exit; out['checks']['finite_outputs']=all_finite
out['checks']['sufficient_both_omegas']=suff
if not all_exit or not all_finite:
    cls='M29_K4B_DIAGNOSTIC_EXECUTION_OR_FINITE_OUTPUT_BLOCK'
elif suff['grid_ref'] and not suff['evolution_ref']:
    cls='M29_K4B_GRID_DOMINATED'
elif suff['evolution_ref'] and not suff['grid_ref']:
    cls='M29_K4B_EVOLUTION_DOMINATED'
elif suff['grid_ref'] and suff['evolution_ref']:
    cls='M29_K4B_BOTH_INDIVIDUALLY_SUFFICIENT'
elif (not suff['grid_ref']) and (not suff['evolution_ref']) and suff['pk_core_ref']:
    cls='M29_K4B_COMBINED_GRID_EVOLUTION'
else:
    cls='M29_K4B_UNRESOLVED_REF_PROFILE_DEPENDENCE'
out['classification']=cls
out['scope']='diagnostic attribution of parent K4 P(k) max discrepancy only; no K4 promotion, no K3 resolution, no physical falsification'
Path('waves/wave_05_modified_gravity').mkdir(parents=True,exist_ok=True)
p=Path('waves/wave_05_modified_gravity/M29_K4B_HIGHK_LOCALIZATION_RESULT.json')
p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
