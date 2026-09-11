#!/usr/bin/env python3
import json, math, pathlib, sys
import numpy as np

root=pathlib.Path(sys.argv[1])
provider_commit=sys.argv[2]
expected='d9a20bd0c7b7a6c8957410fd245ed06b30b915c1'

def load(path):
    rows=[]
    with open(path,encoding='utf-8',errors='replace') as f:
        for line in f:
            s=line.strip()
            if not s or s.startswith('#'): continue
            try: rows.append([float(x) for x in s.split()])
            except ValueError: continue
    a=np.asarray(rows,float)
    if a.ndim != 2 or a.shape[0] < 5 or a.shape[1] < 2: raise RuntimeError(f'bad table {path}: {a.shape}')
    if not np.isfinite(a).all(): raise RuntimeError(f'nonfinite table {path}')
    return a

def rel_l2(a,b):
    lo=max(a[:,0].min(),b[:,0].min()); hi=min(a[:,0].max(),b[:,0].max())
    x=a[(a[:,0]>=lo)&(a[:,0]<=hi),0]
    ya=a[(a[:,0]>=lo)&(a[:,0]<=hi),1]
    yb=np.interp(x,b[:,0],b[:,1])
    scale=np.maximum(np.maximum(np.abs(ya),np.abs(yb)),1e-30)
    return float(np.sqrt(np.mean(((ya-yb)/scale)**2)))

out={'schema':'m35_k0_class_lvdm_provider_v0.1','provider_commit':provider_commit,'expected_commit':expected,
     'arms':{},'physical_falsification':False,'scope':'pinned CLASS_LVDM preferred-frame/LV-gravity provider; K0 only; K1-K9 open; no complete Einstein-Aether SVT claim'}
try:
    ccl=load(root/'control_cl.dat'); acl=load(root/'active_cl.dat')
    cpk=load(root/'control_pk.dat'); apk=load(root/'active_pk.dat')
    out['arms']['weak_gravity_control']={'cl_rows':len(ccl),'pk_rows':len(cpk),'finite':True}
    out['arms']['aether_gravity_active']={'cl_rows':len(acl),'pk_rows':len(apk),'finite':True}
    tt=rel_l2(ccl,acl); pk=rel_l2(cpk,apk)
    out['response']={'tt_normalized_l2':tt,'pk_normalized_l2':pk,'threshold':1e-6}
    passed=(provider_commit==expected and max(tt,pk)>1e-6)
    out['classification']='M35_K0_PASS_WITH_SCOPE_PINNED_CLASS_LVDM_AETHER_GRAVITY' if passed else 'M35_K0_NOT_ESTABLISHED'
    out['K0_promoted']=passed
except Exception as e:
    out['classification']='M35_K0_BLOCKED_PROVIDER_EXECUTION'
    out['K0_promoted']=False
    out['error']=repr(e)
print(json.dumps(out,indent=2,sort_keys=True))
pathlib.Path('m35_k0_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
