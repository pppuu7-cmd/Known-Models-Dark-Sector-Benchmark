#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np

PROTOCOL='protocol/W04_M21_L400_SOURCE_SUPPORT_TAIL_COUNTERFACTUAL_v0.1.md'
CASES=('ref','f2','f3','f4')
J_SHARED=2905
HIGH=3.0

def find_one(root:Path,name:str)->Path:
 xs=list(root.rglob(name))
 if len(xs)!=1: raise RuntimeError(f'expected one {name} under {root}, got {xs}')
 return xs[0]

def table(p:Path)->np.ndarray:
 rows=[]; malformed=0
 for raw in p.read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s or s.startswith('#'): continue
  parts=s.split()
  if len(parts)!=12:
   malformed+=1; continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in parts]
  except ValueError:
   malformed+=1; continue
  if not all(math.isfinite(x) for x in r):
   malformed+=1; continue
  rows.append(r)
 if malformed: raise RuntimeError(f'{p}: malformed rows={malformed}')
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<1 or a.shape[1]!=12: raise RuntimeError(f'invalid {p}: {a.shape}')
 return a

def blocks(p:Path):
 a=table(p); out={}
 for q in sorted(set(int(round(x)) for x in a[:,0])):
  b=a[np.isclose(a[:,0],q,rtol=0,atol=1e-12)]
  out[q]=b[np.argsort(b[:,2])]
 return out

def seqsum(xs):
 s=0.0
 for x in xs:s += float(x)
 return s

def rel(a,b):return abs(a-b)/max(abs(a),abs(b),1e-300)

def main(components:Path,parent_result:Path,outp:Path)->int:
 parent=json.loads(parent_result.read_text())
 B={c:blocks(find_one(components,f'conv_{c}.dat')) for c in CASES}
 metas={c:json.loads(find_one(components,f'{c}_case_meta.json').read_text()) for c in CASES}
 checks={f'{c}_authority_clean':metas[c].get('authority_clean') is True for c in CASES}
 qsets=[set(B[c]) for c in CASES]
 checks['same_q_set']=all(s==qsets[0] for s in qsets[1:])
 qs=sorted(set.intersection(*qsets)) if qsets else []
 checks['q_count_73']=len(qs)==73
 checks['neighbor_shared_endpoint']=all(all(int(round(B[c][q][-1,2]))==J_SHARED for q in qs) for c in ('ref','f2','f4'))
 checks['f3_extends_beyond_shared']=all(int(round(B['f3'][q][-1,2]))>J_SHARED for q in qs)
 weights={int(q):float(v['W_parent']) for q,v in parent.get('per_q',{}).items() if 'W_parent' in v}
 checks['parent_weights_cover_q']=set(qs).issubset(weights)
 checks['positive_parent_weight']=sum(weights.get(q,0.0) for q in qs)>0
 if not all(checks.values()):
  obj={'schema':'KMDSB.W04.M21.L400SourceSupportTailCounterfactual.v0.1','protocol':PROTOCOL,'classification':'M21_L400_SOURCE_SUPPORT_TAIL_COUNTERFACTUAL_BLOCKED','checks':checks,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
  outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); return 1
 responses={c:{} for c in ('f2','f4','f3_full','f3_shared')}; tails={}; perq={}; max_recon=0.; max_tail_identity=0.; max_krel=0.
 for q in qs:
  arr={c:B[c][q] for c in CASES}
  for c in CASES:
   idx=arr[c][:,2].astype(int)
   if len(arr[c])<20 or not np.array_equal(idx,np.arange(len(arr[c]))): raise RuntimeError(f'{c} q={q}: tau integrity')
   native=float(arr[c][0,8]); calc=seqsum(arr[c][:,7])+float(arr[c][0,9]); rr=rel(calc,native); max_recon=max(max_recon,rr)
   if rr>1e-10: raise RuntimeError(f'{c} q={q}: native reconstruction {rr}')
  kref=float(arr['ref'][0,1])
  for c in ('f2','f3','f4'):
   kr=rel(float(arr[c][0,1]),kref); max_krel=max(max_krel,kr)
   if kr>1e-6: raise RuntimeError(f'{c} q={q}: k geometry {kr}')
  tref=float(arr['ref'][0,8]); tf2=float(arr['f2'][0,8]); tf4=float(arr['f4'][0,8]); tfull=float(arr['f3'][0,8])
  f3=arr['f3']; mask=f3[:,2].astype(int)<=J_SHARED
  if int(mask.sum())!=J_SHARED+1: raise RuntimeError(f'f3 q={q}: shared prefix size {mask.sum()}')
  tshared=seqsum(f3[mask,7])
  tail_direct=seqsum(f3[~mask,7])+float(f3[0,9])
  tail_diff=tfull-tshared
  tr=rel(tail_direct,tail_diff); max_tail_identity=max(max_tail_identity,tr)
  if tr>1e-10: raise RuntimeError(f'f3 q={q}: tail identity {tr}')
  responses['f2'][q]=tf2-tref; responses['f4'][q]=tf4-tref; responses['f3_full'][q]=tfull-tref; responses['f3_shared'][q]=tshared-tref; tails[q]=tail_diff
  tailrows=f3[~mask]
  tail_budget=seqsum(abs(x) for x in tailrows[:,7])+abs(float(f3[0,9]))
  perq[str(q)]={'W_parent':weights[q],'k_ref':kref,'index_tau_max':int(round(f3[-1,10])),'T_ref':tref,'T_f2':tf2,'T_f4':tf4,'T_f3_full':tfull,'T_f3_shared':tshared,'T_tail':tail_diff,'tail_identity_relative_error':tr,'tail_rows':int((~mask).sum()),'tail_u_min':float(tailrows[:,3].min()),'tail_u_max':float(tailrows[:,3].max()),'source_at_shared_endpoint':float(f3[J_SHARED,4]),'source_at_native_last':float(f3[-1,4]),'tail_absolute_contribution_budget':tail_budget,'native_edge_correction':float(f3[0,9])}
 den=sum(weights[q] for q in qs)
 def amp(d): return math.sqrt(sum(weights[q]*d[q]*d[q] for q in qs)/den)
 A={k:amp(v) for k,v in responses.items()}; A_tail=amp(tails)
 neighbor=max(A['f2'],A['f4'],1e-300); E_full=A['f3_full']/neighbor; E_shared=A['f3_shared']/neighbor
 if E_full<=HIGH: cls='M21_L400_SOURCE_SUPPORT_PARENT_SPECIFICITY_INCONSISTENT_BLOCKED'; rc=1
 elif E_shared<=HIGH: cls='M21_L400_F3_SPECIFICITY_LOCALIZED_TO_EXTENDED_SOURCE_SUPPORT_WITH_SCOPE'; rc=0
 else: cls='M21_L400_F3_SPECIFICITY_PERSISTS_ON_SHARED_SOURCE_SUPPORT_WITH_SCOPE'; rc=0
 obj={'schema':'KMDSB.W04.M21.L400SourceSupportTailCounterfactual.v0.1','protocol':PROTOCOL,'parent_classification':parent.get('classification'),'classification':cls,'checks':checks,'shared_endpoint_index_tau':J_SHARED,'response_amplitudes':A,'A_tail':A_tail,'E_full':E_full,'E_shared':E_shared,'tail_fraction_of_f3_response_amplitude':A_tail/max(A['f3_full'],1e-300),'max_native_reconstruction_relative_error':max_recon,'max_tail_identity_relative_error':max_tail_identity,'max_same_q_k_relative_difference':max_krel,'per_q':perq,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'A':A,'A_tail':A_tail,'E_full':E_full,'E_shared':E_shared,'tail_fraction':obj['tail_fraction_of_f3_response_amplitude']},indent=2,sort_keys=True)); return rc

if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: l400_source_support_tail_counterfactual.py COMPONENTS_DIR PARENT_RESULT.json OUT.json')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])))
