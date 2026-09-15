#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
P='protocol/W04_M21_L400_NATIVE_GRID_TOPOLOGY_DIAGNOSTIC_v0.1.md'; CASES=('ref','f2','f3','f4')
def one(r,n):
 x=list(r.rglob(n));
 if len(x)!=1: raise RuntimeError(f'expected one {n}, got {x}')
 return x[0]
def tab(p):
 rows=[]
 for s in p.read_text(errors='replace').splitlines():
  s=s.strip()
  if not s or s.startswith('#'): continue
  try:a=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except: continue
  if len(a)==12 and all(math.isfinite(x) for x in a): rows.append(a)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[1]!=12: raise RuntimeError('bad table')
 return a
def blocks(p):
 a=tab(p); return {q:a[np.isclose(a[:,0],q,rtol=0,atol=1e-12)][np.argsort(a[np.isclose(a[:,0],q,rtol=0,atol=1e-12)][:,2])] for q in sorted(set(int(round(x)) for x in a[:,0]))}
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),1e-300)
def main(root,parentp,outp):
 parent=json.loads(parentp.read_text()); pc=parent.get('classification','')
 base={'schema':'KMDSB.W04.M21.NativeGridTopology.v0.1','protocol':P,'parent_classification':pc,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 if pc!='M21_L400_ACCUMULATION_WINDOW_LOCALIZATION_BLOCKED':
  base['classification']='M21_L400_NATIVE_GRID_TOPOLOGY_NOT_AUTHORIZED'; outp.write_text(json.dumps(base,indent=2,sort_keys=True)+'\n'); return 0
 B={c:blocks(one(root,f'conv_{c}.dat')) for c in CASES}; M={c:json.loads(one(root,f'{c}_case_meta.json').read_text()) for c in CASES}
 checks={f'{c}_authority_clean':M[c].get('authority_clean') is True for c in CASES}; qsets=[set(B[c]) for c in CASES]; checks['same_q_set']=all(s==qsets[0] for s in qsets[1:]); qs=sorted(set.intersection(*qsets)); checks['q_nonempty']=bool(qs)
 per={}; excl=0; endpoint=True
 for q in qs:
  z={}; ok=True
  for c in CASES:
   a=B[c][q]; n=len(a); idx=a[:,2].astype(int); u=a[:,3]; du=np.diff(u); mono=bool(np.all(du>0) or np.all(du<0)); stored=int(round(a[0,10])); good=n>=20 and np.array_equal(idx,np.arange(n)) and mono and stored==n-1
   ok &= good; ad=np.abs(du)
   z[c]={'N':n,'dN_vs_ref':None,'u_min':float(u.min()),'u_max':float(u.max()),'median_abs_du':float(np.median(ad)),'min_abs_du':float(ad.min()),'max_abs_du':float(ad.max()),'integrity':good}
  nr=z['ref']['N']
  for c in CASES: z[c]['dN_vs_ref']=z[c]['N']-nr; z[c]['N_ratio_vs_ref']=z[c]['N']/nr
  ex=z['f3']['dN_vs_ref']>0 and z['f3']['dN_vs_ref']>max(z['f2']['dN_vs_ref'],z['f4']['dN_vs_ref']); excl+=int(ex); z['f3_exclusive_expansion']=ex
  for c in ('f2','f3','f4'):
   if rel(z[c]['u_min'],z['ref']['u_min'])>1e-8 or rel(z[c]['u_max'],z['ref']['u_max'])>1e-8: endpoint=False
  checks[f'q{q}_integrity']=ok; per[str(q)]=z
 frac=excl/len(qs) if qs else 0.0; clean=all(checks.values())
 if not clean: cls='M21_L400_NATIVE_GRID_TOPOLOGY_BLOCKED'
 elif frac>=0.9 and endpoint: cls='M21_L400_F3_NATIVE_GRID_DENSIFICATION_WITH_SCOPE'
 elif frac>=0.9: cls='M21_L400_F3_NATIVE_GRID_SUPPORT_AND_DENSITY_CHANGE_WITH_SCOPE'
 else: cls='M21_L400_NATIVE_GRID_CHANGE_NOT_F3_EXCLUSIVE_WITH_SCOPE'
 base.update({'classification':cls,'checks':checks,'q_count':len(qs),'f3_exclusive_expansion_fraction':frac,'endpoint_clean':endpoint,'per_q':per}); outp.write_text(json.dumps(base,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'fraction':frac,'endpoint_clean':endpoint},indent=2)); return 1 if cls.endswith('_BLOCKED') else 0
if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: script COMPONENTS BLOCKED_RESULT OUT')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])))