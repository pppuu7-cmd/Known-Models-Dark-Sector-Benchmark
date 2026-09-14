#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_v0.1.md'
CASES=('ref','f2','f3','f4')
KMIN=0.03030247505892471
KMAX=0.04401375054733766
HIGH=3.0

def table(p:Path,ncol:int)->np.ndarray:
 rows=[]
 for raw in p.read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s or s.startswith('#'): continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError: continue
  if len(r)==ncol and all(math.isfinite(x) for x in r): rows.append(r)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<1 or a.shape[1]!=ncol: raise RuntimeError(f'invalid {p}: {a.shape}')
 return a

def find_one(root:Path,name:str)->Path:
 xs=list(root.rglob(name))
 if len(xs)!=1: raise RuntimeError(f'expected one {name} under {root}, got {xs}')
 return xs[0]

def load_blocks(p:Path):
 a=table(p,12); out={}
 for qv in sorted(set(int(round(x)) for x in a[:,0])):
  b=a[np.isclose(a[:,0],qv,rtol=0,atol=1e-12)]
  b=b[np.argsort(b[:,2])]
  out[qv]=b
 return out

def parent_delta(parent:Path,c:str):
 a=table(parent/f'diag_{c}.dat',9)
 a=a[np.isclose(a[:,0],400,rtol=0,atol=1e-12)]
 return {int(round(r[2])):(float(r[4]),float(r[5])) for r in a}

def rel(a,b): return abs(a-b)/max(abs(a),abs(b),1e-300)
def profile_D(x,ref): return float(np.linalg.norm(x-ref)/max(float(np.linalg.norm(ref)),1e-300))

def main(components:Path,parent:Path,outp:Path)->int:
 metas={}; blocks={}; checks={}
 for c in CASES:
  m=json.loads(find_one(components,f'{c}_case_meta.json').read_text())
  metas[c]=m; blocks[c]=load_blocks(find_one(components,f'conv_{c}.dat'))
  checks[f'{c}_authority_clean']=m.get('authority_clean') is True
  checks[f'{c}_null_clean']=m.get('null_cl_l2_le_1e12') is True
 checks['provider_identity']=all(m.get('provider_head')==PIN for m in metas.values())
 qsets=[set(blocks[c]) for c in CASES]
 checks['same_q_index_set']=all(s==qsets[0] for s in qsets[1:])
 qset=sorted(set.intersection(*qsets)) if qsets else []
 checks['support_q_nonempty']=len(qset)>0
 integrity={}; max_recon=0.; kgeom_max=0.; profiles={x:{c:{} for c in ('f2','f3','f4')} for x in ('S','R','P','C')}
 valid_q=[]
 if all(checks.values()):
  for q in qset:
   ok=True; im={}
   for c in CASES:
    b=blocks[c][q]; idx=b[:,2].astype(int); im[c]={'rows':int(len(b)),'k':float(b[0,1])}
    if len(b)<20 or not np.array_equal(idx,np.arange(len(b))) or int(round(b[0,10]))!=len(b)-1: ok=False
    recon=float(np.sum(b[:,7])+b[0,9]); tf=float(b[0,8]); rr=rel(recon,tf); im[c]['reconstruction_relative_error']=rr; max_recon=max(max_recon,rr)
    if rr>1e-10: ok=False
   kref=im['ref']['k']
   for c in ('f2','f3','f4'):
    kg=rel(im[c]['k'],kref); kgeom_max=max(kgeom_max,kg)
    if kg>1e-6: ok=False
   im['valid']=ok; integrity[str(q)]=im
   if ok: valid_q.append(q)
 checks['all_blocks_reconstruct_and_geometry_clean']=len(valid_q)==len(qset) and len(valid_q)>0
 if not all(checks.values()):
  obj={'schema':'KMDSB.W04.M21.L400TransferConvolutionDecomposition.v0.1','protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}','classification':'M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_BLOCKED','checks':checks,'max_reconstruction_relative_error':max_recon,'max_cross_case_k_relative_difference':kgeom_max,'integrity':integrity,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
  outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':obj['classification'],'checks':checks},indent=2,sort_keys=True)); return 1
 # Parent frozen excess W by q-index.
 pd={c:parent_delta(parent,c) for c in CASES}; W={}
 for q in valid_q:
  if any(q not in pd[c] for c in CASES): raise RuntimeError(f'parent diagnostic missing q={q}')
  r={c:pd[c][q][1]-pd['ref'][q][1] for c in ('f2','f3','f4')}
  W[q]=max(r['f3']**2-max(r['f2']**2,r['f4']**2),0.0)
 checks['positive_parent_weight']=sum(W.values())>0
 perq={}
 for q in valid_q:
  arr={c:blocks[c][q] for c in CASES}; lo=max(float(x[:,3].min()) for x in arr.values()); hi=min(float(x[:,3].max()) for x in arr.values())
  ur=arr['ref'][:,3]; mask=(ur>=lo)&(ur<=hi); ug=ur[mask]
  # reference rows were sorted by index_tau, while u decreases; sort common grid ascending for interpolation/norm invariance.
  ug=np.sort(ug)
  if ug.size<20: raise RuntimeError(f'common u too short q={q}: {ug.size}')
  vals={}
  for c,b in arr.items():
   order=np.argsort(b[:,3]); u=b[order,3]
   vals[c]={
    'S':np.interp(ug,u,b[order,4]),
    'R':np.interp(ug,u,b[order,5]),
    'P':np.interp(ug,u,b[order,4]*b[order,5]),
    'C':np.interp(ug,u,b[order,7]),
   }
  e={}
  for X in ('S','R','P','C'):
   d={c:profile_D(vals[c][X],vals['ref'][X]) for c in ('f2','f3','f4')}
   for c in d: profiles[X][c][q]=d[c]
   e[X]=d['f3']/max(d['f2'],d['f4'],1e-300)
  perq[str(q)]={'k_ref':float(arr['ref'][0,1]),'n_common_u':int(ug.size),'W_parent':W[q],'E':e}
 weight=sum(W.values()); A={}; E={}; summary={}
 for X in ('S','R','P','C'):
  A[X]={c:math.sqrt(sum(W[q]*profiles[X][c][q]**2 for q in valid_q)/weight) for c in ('f2','f3','f4')}
  E[X]=A[X]['f3']/max(A[X]['f2'],A[X]['f4'],1e-300)
  es=[perq[str(q)]['E'][X] for q in valid_q]
  summary[X]={'A':A[X],'E':E[X],'high':E[X]>HIGH,'per_q_E_median_report_only':float(np.median(es)),'per_q_E_max_report_only':float(np.max(es))}
 if E['S']>HIGH and E['R']<=HIGH: cls='M21_L400_TRANSFER_SPIKE_SOURCE_PROFILE_LOCALIZED_WITH_SCOPE'
 elif E['R']>HIGH and E['S']<=HIGH: cls='M21_L400_TRANSFER_SPIKE_RADIAL_KERNEL_LOCALIZED_WITH_SCOPE'
 elif E['S']>HIGH and E['R']>HIGH: cls='M21_L400_TRANSFER_SPIKE_SOURCE_AND_RADIAL_MIXED_WITH_SCOPE'
 elif E['S']<=HIGH and E['R']<=HIGH and E['P']>HIGH: cls='M21_L400_TRANSFER_SPIKE_SOURCE_RADIAL_INTERACTION_WITH_SCOPE'
 else: cls='M21_L400_TRANSFER_SPIKE_CONVOLUTION_ACCUMULATION_WITH_SCOPE'
 obj={'schema':'KMDSB.W04.M21.L400TransferConvolutionDecomposition.v0.1','protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}','parent_transfer_localization_run_id':34905311127,'parent_k_support_run_id':34905488316,'classification':cls,'checks':checks,'support':{'k_min':KMIN,'k_max':KMAX,'q_count':len(valid_q),'parent_weight_sum':weight},'max_reconstruction_relative_error':max_recon,'max_cross_case_k_relative_difference':kgeom_max,'profile_summary':summary,'per_q':perq,'integrity':integrity,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'classification':cls,'q_count':len(valid_q),'E':E,'max_reconstruction_relative_error':max_recon,'max_k_rel':kgeom_max},indent=2,sort_keys=True)); return 0
if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: l400_transfer_convolution_decomposition.py COMPONENTS_DIR PARENT_DIAG_A_DIR OUT.json')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])))
