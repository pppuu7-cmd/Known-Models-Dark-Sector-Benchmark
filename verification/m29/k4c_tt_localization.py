#!/usr/bin/env python3
import json, math
from pathlib import Path

PROFILES=['base_grid','thermo_ref','projection_ref','thermo_projection_ref','full_core_ref','full_ref']

def rows(path):
    out=[]
    if path is None or not path.exists(): return out
    for line in path.read_text(errors='ignore').splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        try: v=[float(x) for x in s.split()]
        except ValueError: continue
        if len(v)>=2 and all(math.isfinite(x) for x in v[:2]): out.append((v[0],v[1]))
    out.sort(); return out

def find_cl(base):
    xs=sorted((base/'output').glob('*_cl.dat'))
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

def quant(vals,p):
    a=sorted(vals)
    if not a:return None
    u=(len(a)-1)*p; i=int(math.floor(u)); j=int(math.ceil(u))
    if i==j:return a[i]
    return a[i]+(a[j]-a[i])*(u-i)

def compare(a,b):
    es=[]
    for x,y in a:
        z=interp(b,x)
        if z is None: continue
        es.append((2*abs(y-z)/(abs(y)+abs(z)+1e-300),x))
    if not es:return {'n':0,'max':None,'rms':None,'median':None,'p95':None,'p99':None,'max_ell':None}
    vals=[e for e,_ in es]; em,xm=max(es)
    return {'n':len(vals),'max':em,'rms':math.sqrt(sum(e*e for e in vals)/len(vals)),
            'median':quant(vals,.5),'p95':quant(vals,.95),'p99':quant(vals,.99),'max_ell':xm}

out={'schema':'m29_k4c_tt_localization_v0.1','provider_commit':'0009f51d89e6465c79e570b496c66fc90058fa77',
     'omega_BD':15,'K4_promoted':False,'physical_falsification':False,'metrics':{},'reductions':{},'exit_codes':{},'checks':{}}
data={}; all_exit=True; all_finite=True
for pr in PROFILES:
    base=Path('m29k4c')/pr
    ep=base/'exit_code.txt'; rc=int(ep.read_text().strip()) if ep.exists() else None
    out['exit_codes'][pr]=rc; all_exit &= (rc==0)
    pts=rows(find_cl(base)); data[pr]=pts; all_finite &= len(pts)>0
ref=data['full_ref']
for pr in PROFILES[:-1]: out['metrics'][pr]=compare(data[pr],ref)
e0=out['metrics']['base_grid']['max']
for pr in ('thermo_ref','projection_ref','thermo_projection_ref','full_core_ref'):
    ep=out['metrics'][pr]['max']
    out['reductions'][pr]=None if e0 in (None,0) or ep is None else 1-ep/e0
suff={pr:(out['reductions'][pr] is not None and out['reductions'][pr]>=0.80) for pr in out['reductions']}
out['checks']['all_exit_zero']=all_exit; out['checks']['finite_outputs']=all_finite; out['checks']['sufficient_80pct']=suff
if not all_exit or not all_finite:
    cls='M29_K4C_DIAGNOSTIC_EXECUTION_OR_FINITE_OUTPUT_BLOCK'
elif suff['thermo_ref'] and not suff['projection_ref']:
    cls='M29_K4C_THERMO_DOMINATED'
elif suff['projection_ref'] and not suff['thermo_ref']:
    cls='M29_K4C_PROJECTION_DOMINATED'
elif suff['thermo_ref'] and suff['projection_ref']:
    cls='M29_K4C_BOTH_INDIVIDUALLY_SUFFICIENT'
elif suff['thermo_projection_ref']:
    cls='M29_K4C_COMBINED_THERMO_PROJECTION'
elif suff['full_core_ref']:
    cls='M29_K4C_FULL_CORE_REQUIRED'
else:
    cls='M29_K4C_UNRESOLVED_REF_PROFILE_DEPENDENCE'
out['classification']=cls
out['scope']='omega_BD=15 TT precision attribution only; no K4 promotion, no K3 resolution, no physical falsification'
Path('waves/wave_05_modified_gravity').mkdir(parents=True,exist_ok=True)
p=Path('waves/wave_05_modified_gravity/M29_K4C_TT_LOCALIZATION_RESULT.json')
p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
