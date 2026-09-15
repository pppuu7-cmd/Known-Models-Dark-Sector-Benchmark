#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
PROTOCOL='protocol/W04_M21_L400_ACCUMULATION_WINDOW_LOCALIZATION_v0.1.md'
CASES=('ref','f2','f3','f4')

def one(root,n):
 x=list(root.rglob(n))
 if len(x)!=1: raise RuntimeError(f'expected one {n}, got {x}')
 return x[0]
def tab(p):
 r=[]
 for s in p.read_text(errors='replace').splitlines():
  s=s.strip()
  if not s or s.startswith('#'): continue
  try:a=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except: continue
  if len(a)==12 and all(math.isfinite(x) for x in a): r.append(a)
 a=np.asarray(r,float)
 if a.ndim!=2 or a.shape[1]!=12: raise RuntimeError('bad table')
 return a
def blocks(p):
 a=tab(p); return {q:a[np.isclose(a[:,0],q,rtol=0,atol=1e-12)][np.argsort(a[np.isclose(a[:,0],q,rtol=0,atol=1e-12)][:,2])] for q in sorted(set(int(round(x)) for x in a[:,0]))}
def main(root,edgep,outp):
 edge=json.loads(edgep.read_text()); pc=edge.get('classification','')
 if pc!='M21_L400_EDGE_SPECIFICITY_ABSOLUTELY_INSUFFICIENT_WITH_SCOPE':
  o={'schema':'KMDSB.W04.M21.AccumulationWindowLocalization.v0.1','protocol':PROTOCOL,'parent_classification':pc,'classification':'M21_L400_ACCUMULATION_WINDOW_LOCALIZATION_NOT_AUTHORIZED','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}; outp.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n'); return 0
 B={c:blocks(one(root,f'conv_{c}.dat')) for c in CASES}; M={c:json.loads(one(root,f'{c}_case_meta.json').read_text()) for c in CASES}
 checks={f'{c}_authority_clean':M[c].get('authority_clean') is True for c in CASES}; qs=sorted(set.intersection(*(set(B[c]) for c in CASES))); checks['same_q_set']=all(set(B[c])==set(B['ref']) for c in CASES); checks['q_nonempty']=bool(qs)
 Wbins=np.zeros(10); sumT=0.; maxclose=0.; detail={}
 if all(checks.values()):
  for q in qs:
   A={c:B[c][q] for c in CASES}; n=len(A['ref']); ok=n>=20 and all(len(A[c])==n and np.array_equal(A[c][:,2].astype(int),np.arange(n)) for c in CASES); checks[f'q{q}_tau_integrity']=ok
   if not ok: continue
   w=np.abs(A['ref'][:,7]); sw=float(w.sum()); checks[f'q{q}_positive_abs_budget']=sw>0
   if sw<=0: continue
   cum=np.cumsum(w)/sw; bid=np.minimum((cum*10).astype(int),9)
   # ensure first samples are assigned by cumulative endpoint; deterministic native-index partition
   S={c:np.array([A[c][bid==b,7].sum() for b in range(10)]) for c in CASES}
   d={c:S[c]-S['ref'] for c in ('f2','f3','f4')}
   T={c:float(A[c][0,8]) for c in CASES}; td={c:T[c]-T['ref'] for c in ('f2','f3','f4')}
   wt=max(td['f3']**2-max(td['f2']**2,td['f4']**2),0.0); sumT+=wt
   wb=[]
   for b in range(10):
    x=max(float(d['f3'][b]**2-max(d['f2'][b]**2,d['f4'][b]**2)),0.0); Wbins[b]+=x; wb.append(x)
   clos={c:abs(float(d[c].sum())-(td[c]-(float(A[c][0,9])-float(A['ref'][0,9]))))/max(abs(td[c]),1e-300) for c in ('f2','f3','f4')}; maxclose=max(maxclose,max(clos.values()))
   detail[str(q)]={'W_total':wt,'W_bins':wb,'closure_relative_error':clos,'bin_counts':[int((bid==b).sum()) for b in range(10)]}
 checks['signed_closure_clean']=maxclose<=1e-10
 if not all(checks.values()) or sumT<=0:
  cls='M21_L400_ACCUMULATION_WINDOW_LOCALIZATION_BLOCKED'; F=[None]*10; fm=None; bm=None
 else:
  F=(Wbins/sumT).tolist(); fm=max(F); bm=F.index(fm); cls='M21_L400_ACCUMULATION_WINDOW_CONCENTRATED_WITH_SCOPE' if fm>=0.5 else 'M21_L400_ACCUMULATION_WINDOW_DISTRIBUTED_WITH_SCOPE'
 o={'schema':'KMDSB.W04.M21.AccumulationWindowLocalization.v0.1','protocol':PROTOCOL,'parent_classification':pc,'classification':cls,'checks':checks,'q_count':len(qs),'sum_W_total':sumT,'F_bins':F,'Fmax':fm,'bmax':bm,'max_signed_closure_relative_error':maxclose,'per_q':detail,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}; outp.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'Fmax':fm,'bmax':bm},indent=2)); return 1 if cls.endswith('_BLOCKED') else 0
if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: script COMPONENTS EDGE_RESULT OUT')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])))