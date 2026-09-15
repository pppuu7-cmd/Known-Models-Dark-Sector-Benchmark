#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
P='protocol/W04_M21_L400_SUPPORT_DOMAIN_DECOMPOSITION_v0.1.md'; CASES=('ref','f2','f3','f4')
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
def main(root,topop,outp):
 topo=json.loads(topop.read_text()); pc=topo.get('classification','')
 base={'schema':'KMDSB.W04.M21.SupportDomainDecomposition.v0.1','protocol':P,'parent_classification':pc,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 if pc!='M21_L400_F3_NATIVE_GRID_SUPPORT_AND_DENSITY_CHANGE_WITH_SCOPE':
  base['classification']='M21_L400_SUPPORT_DOMAIN_DECOMPOSITION_NOT_AUTHORIZED'; outp.write_text(json.dumps(base,indent=2,sort_keys=True)+'\n'); return 0
 B={c:blocks(one(root,f'conv_{c}.dat')) for c in CASES}; M={c:json.loads(one(root,f'{c}_case_meta.json').read_text()) for c in CASES}
 checks={f'{c}_authority_clean':M[c].get('authority_clean') is True for c in CASES}; qsets=[set(B[c]) for c in CASES]; checks['same_q_set']=all(s==qsets[0] for s in qsets[1:]); qs=sorted(set.intersection(*qsets)); checks['q_nonempty']=bool(qs)
 per={}; delta=[]; dcf=[]; xext=[]; f3non=0; neighbor_out=0; maxrecon=0.
 for q in qs:
  arr={c:B[c][q] for c in CASES}; good=True; T={}
  for c in CASES:
   a=arr[c]; n=len(a); idx=a[:,2].astype(int); u=a[:,3]; du=np.diff(u); stored=int(round(a[0,10])); mono=bool(np.all(du>0) or np.all(du<0)); recon=float(a[:,7].sum()+a[0,9]); tf=float(a[0,8]); rr=abs(recon-tf)/max(abs(recon),abs(tf),1e-300); maxrecon=max(maxrecon,rr); g=n>=20 and np.array_equal(idx,np.arange(n)) and mono and stored==n-1 and rr<=1e-10; good &= g; T[c]=recon
  lo=float(arr['ref'][:,3].min()); hi=float(arr['ref'][:,3].max()); masks={c:(arr[c][:,3]<lo)|(arr[c][:,3]>hi) for c in CASES}; xe=float(arr['f3'][masks['f3'],7].sum()); d=T['f3']-T['ref']; dc=T['f3']-xe-T['ref']; f3non+=int(masks['f3'].any()); neighbor_out+=int(masks['f2'].any() or masks['f4'].any()); delta.append(d); dcf.append(dc); xext.append(xe); checks[f'q{q}_integrity']=good; per[str(q)]={'ref_support':[lo,hi],'extended_rows':{c:int(masks[c].sum()) for c in CASES},'X_ext_f3':xe,'Delta':d,'Delta_cf':dc,'T':T}
 clean=all(checks.values()); nd=float(np.linalg.norm(delta)); ncf=float(np.linalg.norm(dcf)); nx=float(np.linalg.norm(xext)); rcf=ncf/max(nd,1e-300); rext=nx/max(nd,1e-300); frac=f3non/len(qs) if qs else 0.; neigh=neighbor_out/len(qs) if qs else 0.
 if not clean: cls='M21_L400_SUPPORT_DOMAIN_DECOMPOSITION_BLOCKED'
 elif frac>=.9 and rcf<=.5: cls='M21_L400_F3_EXTENDED_SUPPORT_AMPLITUDE_SUFFICIENT_WITH_SCOPE'
 elif frac>=.9: cls='M21_L400_F3_EXTENDED_SUPPORT_AMPLITUDE_INSUFFICIENT_WITH_SCOPE'
 else: cls='M21_L400_F3_EXTENDED_SUPPORT_NOT_SYSTEMATIC_WITH_SCOPE'
 base.update({'classification':cls,'checks':checks,'q_count':len(qs),'f3_extended_support_fraction':frac,'neighbor_outside_ref_fraction':neigh,'R_cf':rcf,'R_ext':rext,'norm_Delta':nd,'norm_Delta_cf':ncf,'norm_X_ext':nx,'max_reconstruction_relative_error':maxrecon,'per_q':per}); outp.write_text(json.dumps(base,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'R_cf':rcf,'R_ext':rext,'f3_fraction':frac},indent=2)); return 1 if cls.endswith('_BLOCKED') else 0
if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: script COMPONENTS TOPOLOGY_RESULT OUT')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])))
