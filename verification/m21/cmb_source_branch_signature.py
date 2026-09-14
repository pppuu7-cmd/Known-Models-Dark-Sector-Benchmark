#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
import numpy as np

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_CONDITIONAL_CMB_SOURCE_BRANCH_SIGNATURE_v0.1.md'
LANES=['NDF_T1E5','NDF_T1E6','NDF_T1E7','RK_T1E5','RK_T1E6','RK_T1E7']; CASES=['ref','f2','f3','f4']; SOURCES=['t0','t1','t2','p']
BRANCH=[('NDF_T1E5','NDF_T1E6'),('NDF_T1E6','NDF_T1E7'),('RK_T1E5','RK_T1E6'),('NDF_T1E7','RK_T1E7')]
CONTROL=[('RK_T1E6','RK_T1E7'),('NDF_T1E5','RK_T1E5'),('NDF_T1E6','RK_T1E6')]
J_FLOOR=1e-12; J_THRESHOLD=3.0

def H(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()
def load_npz(p:Path):
 z=np.load(p); tau=np.asarray(z['tau_Mpc'],float); k=np.asarray(z['k_anchor_Mpc_inv'],float)
 if tau.ndim!=1 or tau.size<16 or np.any(~np.isfinite(tau)) or np.any(np.diff(tau)<=0): raise RuntimeError(f'invalid tau {p}')
 if k.shape!=(5,) or np.any(~np.isfinite(k)) or np.any(np.diff(k)<=0): raise RuntimeError(f'invalid k {p}')
 d={'tau':tau,'k':k}
 for s in SOURCES:
  a=np.asarray(z[s],float)
  if a.shape!=(5,tau.size) or np.any(~np.isfinite(a)): raise RuntimeError(f'invalid source {p}/{s}: {a.shape}')
  d[s]=a
 return d

def D(A,B,s,ki):
 ta,tb=A['tau'],B['tau']; lo=max(float(ta.min()),float(tb.min())); hi=min(float(ta.max()),float(tb.max())); m=(ta>=lo)&(ta<=hi); t=ta[m]; ya=A[s][ki,m]
 if t.size<16: raise RuntimeError(f'insufficient tau overlap {s}/{ki}: {t.size}')
 yb=np.interp(t,tb,B[s][ki])
 return float(np.linalg.norm(ya-yb)/max(float(np.linalg.norm(ya)),float(np.linalg.norm(yb)),1e-300)),int(t.size)
def main(root:Path,config:Path,parent_path:Path,out:Path):
 cfg=json.load(open(config)); parent=json.load(open(parent_path)); result={'schema':'KMDSB.W04.M21.DirectCMBSourceBranchSignature.v0.1','protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}','J_floor':J_FLOOR,'J_threshold':J_THRESHOLD,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 try:
  if parent.get('classification')!='M21_CMB_BRANCH_NOT_LOCALIZED_IN_NATIVE_PERTURBATION_STATES': raise RuntimeError(f'conditional parent not authorized: {parent.get("classification")}')
  metas={}; dirs={}
  for mp in root.rglob('lane_meta.json'):
   m=json.load(open(mp)); lane=m.get('lane')
   if lane in metas: raise RuntimeError(f'duplicate lane {lane}')
   metas[lane]=m; dirs[lane]=mp.parent
  if set(metas)!=set(LANES): raise RuntimeError(f'lane set mismatch {sorted(metas)}')
  csha=H(config); data={}
  for lane in LANES:
   m=metas[lane]
   if m.get('provider_head')!=PIN or not m.get('exact_head') or not m.get('all_four_cases_present') or m.get('config_sha256')!=csha or m.get('profile_manifest',{}).get('lane')!=lane: raise RuntimeError(f'lane integrity {lane}')
   smp=dirs[lane]/'source_out/lane_sources_meta.json'; sm=json.load(open(smp))
   if set(sm.get('cases',{}))!=set(CASES): raise RuntimeError(f'source case set {lane}')
   for c in CASES:
    p=dirs[lane]/f'source_out/{c}_cmb_sources.npz'; data[(lane,c)]=load_npz(p)
    if not np.allclose(data[(lane,c)]['k'],np.asarray(cfg['k_anchors_unrounded_Mpc_inv'],float),rtol=0,atol=1e-15): raise RuntimeError(f'k anchor drift {lane}/{c}')
  edges={}
  for A,B in BRANCH+CONTROL:
   cells=[]
   for ki in range(5):
    for s in SOURCES:
     ds={}; ns={}
     for c in CASES:
      ds[c],ns[c]=D(data[(A,c)],data[(B,c)],s,ki)
     J=float(ds['f3']/max(ds['ref'],ds['f2'],ds['f4'],J_FLOOR)); cells.append({'k_index':ki,'source':s,'J':J,'distances':ds,'n_overlap':ns,'localized':J>=J_THRESHOLD})
   cells.sort(key=lambda x:x['J'],reverse=True); name=f'{A}__{B}'
   edges[name]={'kind':'branch_change' if (A,B) in BRANCH else 'same_branch_control','Jmax':cells[0]['J'],'top_cell':cells[0],'localized_cell_count':sum(x['localized'] for x in cells),'cell_count':20,'edge_localized':any(x['localized'] for x in cells),'top10':cells[:10]}
  nb=sum(edges[f'{a}__{b}']['edge_localized'] for a,b in BRANCH); nc=sum(edges[f'{a}__{b}']['edge_localized'] for a,b in CONTROL)
  if nb==4 and nc==0: cls='M21_CMB_SOURCE_BRANCH_SIGNATURE_MATCHES_CMB_MAP_WITH_SCOPE'
  elif nb>=2: cls='M21_CMB_SOURCE_BRANCH_SIGNATURE_PARTIAL'
  else: cls='M21_CMB_BRANCH_NOT_LOCALIZED_IN_DIRECT_CMB_SOURCES'
  result.update({'classification':cls,'cross_lane_input_identity':True,'parent_classification':parent['classification'],'parent_artifact_identity':parent.get('artifact_id'),'branch_change_localized_count':int(nb),'same_branch_control_localized_count':int(nc),'edges':edges,'k_anchors_Mpc_inv':cfg['k_anchors_unrounded_Mpc_inv'],'tau_window_Mpc':[146.1893481575377,488.2339443484317]})
 except Exception as e:
  result.update({'classification':'M21_CMB_SOURCE_BRANCH_SIGNATURE_BLOCKED','error':repr(e),'cross_lane_input_identity':False,'parent_classification':parent.get('classification')})
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':result['classification'],'branch_change_localized_count':result.get('branch_change_localized_count'),'same_branch_control_localized_count':result.get('same_branch_control_localized_count'),'error':result.get('error')},indent=2,sort_keys=True))
 if result['classification'].endswith('BLOCKED'): raise SystemExit(1)
if __name__=='__main__':
 if len(sys.argv)!=5: raise SystemExit('usage: cmb_source_branch_signature.py LANES_ROOT CONFIG PARENT OUT')
 main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]))
