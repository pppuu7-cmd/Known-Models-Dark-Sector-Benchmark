#!/usr/bin/env python3
import json, pathlib, sys
import numpy as np

root=pathlib.Path(sys.argv[1])
provider_commit=sys.argv[2]
expected='d9a20bd0c7b7a6c8957410fd245ed06b30b915c1'
labels=['s1','s01','s001','s0001']
scales=[1.0,0.1,0.01,0.001]

def load(path):
    rows=[]
    with open(path,encoding='utf-8',errors='replace') as f:
        for line in f:
            s=line.strip()
            if not s or s.startswith('#'): continue
            try: rows.append([float(x) for x in s.split()])
            except ValueError: continue
    a=np.asarray(rows,float)
    if a.ndim != 2 or a.shape[0] < 5 or a.shape[1] < 2:
        raise RuntimeError(f'bad table {path}: {a.shape}')
    if not np.isfinite(a).all():
        raise RuntimeError(f'nonfinite table {path}')
    return a

def rel_l2(a,b):
    lo=max(a[:,0].min(),b[:,0].min()); hi=min(a[:,0].max(),b[:,0].max())
    aa=a[(a[:,0]>=lo)&(a[:,0]<=hi)]
    x=aa[:,0]; ya=aa[:,1]; yb=np.interp(x,b[:,0],b[:,1])
    scale=np.maximum(np.maximum(np.abs(ya),np.abs(yb)),1e-30)
    return float(np.sqrt(np.mean(((ya-yb)/scale)**2)))

def monotone_slack(vals,slack=0.02):
    return all(vals[i+1] <= vals[i]*(1.0+slack) + 1e-15 for i in range(len(vals)-1))

out={
 'schema':'m35_k1_gr_limit_ladder_v0.1',
 'provider_commit':provider_commit,
 'expected_commit':expected,
 'scales':scales,
 'physical_falsification':False,
 'scope':'pinned CLASS_LVDM scalar cosmology weak-coupling continuity only; no complete Einstein-Aether SVT claim; K2-K9 open'
}
try:
    ccl=load(root/'control_cl.dat'); cpk=load(root/'control_pk.dat')
    tt=[]; pk=[]; arms={}
    for label,s in zip(labels,scales):
        cl=load(root/f'{label}_cl.dat'); p=load(root/f'{label}_pk.dat')
        t=rel_l2(ccl,cl); q=rel_l2(cpk,p)
        tt.append(t); pk.append(q)
        arms[label]={'scale':s,'tt_normalized_l2':t,'pk_normalized_l2':q,'cl_rows':len(cl),'pk_rows':len(p),'finite':True}
    mono_tt=monotone_slack(tt); mono_pk=monotone_slack(pk)
    contraction_tt=(tt[-1] <= 0.20*tt[0]) if tt[0] > 0 else False
    contraction_pk=(pk[-1] <= 0.20*pk[0]) if pk[0] > 0 else False
    passed=(provider_commit==expected and mono_tt and mono_pk and contraction_tt and contraction_pk)
    out.update({'arms':arms,'tt_sequence':tt,'pk_sequence':pk,'monotone_tt_2pct_slack':mono_tt,'monotone_pk_2pct_slack':mono_pk,
                'final_over_initial_tt':tt[-1]/tt[0] if tt[0] else None,'final_over_initial_pk':pk[-1]/pk[0] if pk[0] else None,
                'contraction_tt_le_0p2':contraction_tt,'contraction_pk_le_0p2':contraction_pk,'K1_promoted':passed})
    out['classification']='M35_K1_PASS_WITH_SCOPE_PINNED_CLASS_LVDM_GR_LIMIT' if passed else 'M35_K1_PARTIAL_GR_LIMIT_NOT_ESTABLISHED'
except Exception as e:
    out['classification']='M35_K1_BLOCKED_IMPLEMENTATION'
    out['K1_promoted']=False
    out['error']=repr(e)

text=json.dumps(out,indent=2,sort_keys=True)+'\n'
print(text,end='')
pathlib.Path('m35_k1_result.json').write_text(text)
