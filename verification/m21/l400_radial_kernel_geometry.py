#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np

PROTOCOL='protocol/W04_M21_L400_RADIAL_KERNEL_GEOMETRY_v0.1.md'
CASES=('ref','f2','f3','f4')
HIGH=3.0

def find_one(root:Path,name:str)->Path:
 xs=list(root.rglob(name))
 if len(xs)!=1: raise RuntimeError(f'expected one {name} under {root}, got {xs}')
 return xs[0]

def table(p:Path)->np.ndarray:
 rows=[]
 for raw in p.read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s or s.startswith('#'): continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError: continue
  if len(r)==12 and all(math.isfinite(x) for x in r): rows.append(r)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<1 or a.shape[1]!=12: raise RuntimeError(f'invalid {p}: {a.shape}')
 return a

def blocks(p:Path):
 a=table(p); out={}
 for q in sorted(set(int(round(x)) for x in a[:,0])):
  b=a[np.isclose(a[:,0],q,rtol=0,atol=1e-12)]
  b=b[np.argsort(b[:,2])]
  out[q]=b
 return out

def D(y,yr):
 return float(np.linalg.norm(y-yr)/max(float(np.linalg.norm(yr)),1e-300))

def main(components:Path,parent_result:Path,outp:Path)->int:
 parent=json.loads(parent_result.read_text())
 pcl=parent.get('classification','')
 authorized=pcl in {
  'M21_L400_TRANSFER_SPIKE_RADIAL_KERNEL_LOCALIZED_WITH_SCOPE',
  'M21_L400_TRANSFER_SPIKE_SOURCE_AND_RADIAL_MIXED_WITH_SCOPE',
 }
 if not authorized:
  obj={'schema':'KMDSB.W04.M21.L400RadialKernelGeometry.v0.1','protocol':PROTOCOL,
       'parent_classification':pcl,'classification':'M21_L400_RADIAL_GEOMETRY_NOT_AUTHORIZED',
       'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
  outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); return 0
 B={c:blocks(find_one(components,f'conv_{c}.dat')) for c in CASES}
 metas={c:json.loads(find_one(components,f'{c}_case_meta.json').read_text()) for c in CASES}
 checks={f'{c}_authority_clean':metas[c].get('authority_clean') is True for c in CASES}
 qsets=[set(B[c]) for c in CASES]; checks['same_q_set']=all(s==qsets[0] for s in qsets[1:])
 qs=sorted(set.intersection(*qsets)) if qsets else []
 weights={int(q):float(v['W_parent']) for q,v in parent.get('per_q',{}).items() if 'W_parent' in v}
 checks['parent_weights_cover_q']=set(qs).issubset(weights)
 parent_Eu=float(parent.get('profile_summary',{}).get('R',{}).get('E',float('nan')))
 distances={c:{} for c in ('f2','f3','f4')}; perq={}; max_krel=0.; min_support_fraction=1.
 if not all(checks.values()):
  cls='M21_L400_RADIAL_GEOMETRY_AUDIT_BLOCKED'
 else:
  for q in qs:
   arr={c:B[c][q] for c in CASES}; k={c:float(arr[c][0,1]) for c in CASES}; kr={c:abs(k[c]-k['ref'])/max(abs(k['ref']),1e-300) for c in ('f2','f3','f4')}; max_krel=max(max_krel,max(kr.values()))
   curves={}
   for c in CASES:
    x=k[c]*arr[c][:,3]; r=arr[c][:,5]; order=np.argsort(x); curves[c]=(x[order],r[order])
   lo=max(curves[c][0].min() for c in CASES); hi=min(curves[c][0].max() for c in CASES)
   xr,rr=curves['ref']; mask=(xr>=lo)&(xr<=hi); xg=xr[mask]; rg=rr[mask]
   if len(xg)<20: raise RuntimeError(f'q={q}: insufficient common x nodes {len(xg)}')
   frac=len(xg)/max(len(xr),1); min_support_fraction=min(min_support_fraction,frac)
   dq={}
   for c in ('f2','f3','f4'):
    xc,rc=curves[c]; rcg=np.interp(xg,xc,rc); dq[c]=D(rcg,rg); distances[c][q]=dq[c]
   perq[str(q)]={'k_ref':k['ref'],'k_relative':kr,'common_x_min':float(lo),'common_x_max':float(hi),'n_common_x':int(len(xg)),'reference_x_fraction':float(frac),'D_R_x':dq,'W_parent':weights[q]}
  den=sum(weights[q] for q in qs)
  if den<=0: raise RuntimeError('non-positive parent weight')
  A={c:math.sqrt(sum(weights[q]*distances[c][q]**2 for q in qs)/den) for c in ('f2','f3','f4')}
  Ex=A['f3']/max(A['f2'],A['f4'],1e-300)
  if not math.isfinite(parent_Eu) or max_krel>1e-6: cls='M21_L400_RADIAL_GEOMETRY_AUDIT_BLOCKED'
  elif parent_Eu>HIGH and Ex<=HIGH: cls='M21_L400_RADIAL_COORDINATE_GEOMETRY_LOCALIZED_WITH_SCOPE'
  elif Ex>HIGH: cls='M21_L400_RADIAL_INTERPOLATOR_OR_ENDPOINT_STATE_LOCALIZED_WITH_SCOPE'
  else: cls='M21_L400_RADIAL_PARENT_SIGNAL_NOT_REPRODUCED_WITH_SCOPE'
 obj={'schema':'KMDSB.W04.M21.L400RadialKernelGeometry.v0.1','protocol':PROTOCOL,'parent_classification':pcl,'classification':cls,'parent_common_u_E_R':parent_Eu,'common_x':{'A_R':A if 'A' in locals() else None,'E_R':Ex if 'Ex' in locals() else None,'max_same_q_k_relative_difference':max_krel,'min_reference_x_support_fraction':min_support_fraction},'checks':checks,'per_q':perq,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'parent_Eu':parent_Eu,'common_x_E_R':obj['common_x']['E_R'],'max_krel':max_krel},indent=2,sort_keys=True)); return 1 if cls.endswith('_BLOCKED') else 0

if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: l400_radial_kernel_geometry.py COMPONENTS_DIR PARENT_RESULT.json OUT.json')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])))
