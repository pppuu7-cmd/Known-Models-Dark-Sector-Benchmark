#!/usr/bin/env python3
from __future__ import annotations
import json,math,pathlib,sys
import numpy as np

PROTOCOL='protocol/W04_M21_L400_CONDITIONAL_FLAT_IDENTITY_PREDICATE_COUNTERFACTUAL_v0.1.md'
PARENT_REQUIRED='M21_L400_LATE_SOURCE_PREDICATE_ULP_SPLIT_LOCALIZED_WITH_SCOPE'
CASES=('ref','f2','f3','f4')
LANES=('native','flat_identity_predicate')
EXPECTED_Q=set(range(261,334))

def numeric(p:pathlib.Path):
 rows=[]
 for raw in p.read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s or s.startswith('#'): continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError: continue
  if r and all(math.isfinite(x) for x in r): rows.append(r)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<3: raise RuntimeError(f'bad numeric table {p}: {a.shape}')
 return a

def l2(a,b):
 if a.shape!=b.shape:return float('inf')
 return float(np.linalg.norm(a-b)/max(float(np.linalg.norm(a)),float(np.linalg.norm(b)),1e-300))

def load_diag(p:pathlib.Path):
 out={}
 for raw in p.read_text(errors='replace').splitlines():
  x=raw.split()
  if len(x)!=17: raise RuntimeError(f'bad diagnostic row in {p}: {raw[:100]}')
  r=[float(v.replace('D','E').replace('d','e')) for v in x]
  if not all(math.isfinite(v) for v in r): raise RuntimeError(f'nonfinite row in {p}')
  q=int(round(r[0]));
  if q in out: raise RuntimeError(f'duplicate q={q} in {p}')
  out[q]=r
 return out

def find_one(root:pathlib.Path,pattern:str):
 xs=list(root.rglob(pattern))
 if len(xs)!=1: raise RuntimeError(f'{pattern}: expected one under {root}, got {xs}')
 return xs[0]

def main(comp_root:pathlib.Path,parent_json:pathlib.Path,out:pathlib.Path):
 parent=json.load(open(parent_json))
 if parent.get('classification')!=PARENT_REQUIRED:
  raise RuntimeError(f'parent classification not authorized: {parent.get("classification")}')
 entries={}
 for d in comp_root.iterdir():
  if not d.is_dir(): continue
  metas=list(d.rglob('case_meta.json'))
  if len(metas)!=1: continue
  m=json.load(open(metas[0])); key=(m.get('case'),m.get('lane'))
  if key[0] not in CASES or key[1] not in LANES: continue
  if key in entries: raise RuntimeError(f'duplicate component {key}')
  entries[key]=(d,m)
 if set(entries)!={(c,l) for c in CASES for l in LANES}:
  raise RuntimeError(f'missing components: {set((c,l) for c in CASES for l in LANES)-set(entries)}')
 authority=all(m.get('authority_clean') is True for _,m in entries.values())
 diags={}; cls={}
 for key,(d,m) in entries.items():
  c,lane=key
  diags[key]=load_diag(find_one(d,f'flat_identity_{c}_{lane}.dat'))
  cls[key]=numeric(find_one(d,f'{c}_*_cl.dat'))
 qsets={key:set(v) for key,v in diags.items()}
 q_integrity=all(qs==EXPECTED_Q for qs in qsets.values())
 max_k_rel=0.0
 for q in sorted(EXPECTED_Q):
  vals=[diags[key][q][1] for key in sorted(diags)]
  den=max(max(abs(x) for x in vals),1e-300)
  max_k_rel=max(max_k_rel,(max(vals)-min(vals))/den)
 geometry_ok=max_k_rel<=1e-6
 threshold_ok=all(all(r[5]==400.0 for r in D.values()) for D in diags.values())
 native_expected={c:(c!='f3') for c in CASES}
 native_pattern=True; native_endpoint=True
 for c in CASES:
  for r in diags[(c,'native')].values():
   pred=bool(round(r[7])); actual=bool(round(r[8])); bessel=int(round(r[10])); final=int(round(r[11]))
   native_pattern &= pred==native_expected[c] and actual==pred
   native_endpoint &= ((final<bessel) if native_expected[c] else (final==bessel))
 branch_normalized=True; endpoint_normalized=True; cf_effective_identity=True
 for c in CASES:
  for r in diags[(c,'flat_identity_predicate')].values():
   pred=bool(round(r[7])); actual=bool(round(r[8])); bessel=int(round(r[10])); final=int(round(r[11]))
   branch_normalized &= (not pred) and (not actual)
   endpoint_normalized &= final==bessel
   cf_effective_identity &= r[4]==1.0 and int(round(r[16]))==1
 f3_cmb_l2=l2(cls[('f3','native')],cls[('f3','flat_identity_predicate')])
 f3_transfer_rel=0.0; f3_endpoint_same=True
 for q in sorted(EXPECTED_Q):
  a=diags[('f3','native')][q]; b=diags[('f3','flat_identity_predicate')][q]
  f3_endpoint_same &= int(round(a[11]))==int(round(b[11]))
  den=max(abs(a[15]),abs(b[15]),1e-300); f3_transfer_rel=max(f3_transfer_rel,abs(a[15]-b[15])/den)
 f3_null=f3_cmb_l2<=1e-12 and f3_transfer_rel<=1e-10 and f3_endpoint_same
 changed_only_expected=True
 for c in CASES:
  for q in sorted(EXPECTED_Q):
   na=diags[(c,'native')][q]; cf=diags[(c,'flat_identity_predicate')][q]
   changed=int(round(na[11]))!=int(round(cf[11]))
   if c=='f3' and changed: changed_only_expected=False
 authority_all=all([authority,q_integrity,geometry_ok,threshold_ok,native_pattern,native_endpoint,cf_effective_identity,changed_only_expected])
 if not authority_all:
  classification='M21_L400_FLAT_IDENTITY_COUNTERFACTUAL_BLOCKED'; rc=1
 elif not branch_normalized:
  classification='M21_L400_FLAT_IDENTITY_PREDICATE_NOT_CAUSAL_WITH_SCOPE'; rc=0
 elif not endpoint_normalized:
  classification='M21_L400_FLAT_IDENTITY_PREDICATE_ENDPOINT_MISMATCH_BLOCKED'; rc=1
 elif not f3_null:
  classification='M21_L400_FLAT_IDENTITY_COUNTERFACTUAL_NONLOCAL_BLOCKED'; rc=1
 else:
  classification='M21_L400_FLAT_IDENTITY_PREDICATE_BRANCH_CAUSAL_WITH_SCOPE'; rc=0
 obj={
  'schema':'KMDSB.W04.M21.FlatIdentityPredicateCounterfactual.v0.1','protocol':PROTOCOL,
  'parent_classification':parent.get('classification'),'classification':classification,
  'authority_clean':authority,'q_integrity':q_integrity,'q_count':len(EXPECTED_Q),'max_same_q_k_relative_difference':max_k_rel,'geometry_ok':geometry_ok,
  'runtime_threshold_exact_400':threshold_ok,'native_predicate_pattern_reproduced':native_pattern,'native_endpoint_pattern_reproduced':native_endpoint,
  'branch_normalized':branch_normalized,'endpoint_normalized':endpoint_normalized,'counterfactual_effective_identity':cf_effective_identity,
  'f3_full_cmb_native_vs_counterfactual_l2':f3_cmb_l2,'f3_transfer_max_relative_difference':f3_transfer_rel,'f3_endpoint_same':f3_endpoint_same,'f3_null':f3_null,
  'changed_only_expected_cases':changed_only_expected,
  'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 out.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps(obj,indent=2,sort_keys=True)); return rc

if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: l400_flat_identity_predicate_counterfactual.py COMPONENTS PARENT_RESULT OUT')
 raise SystemExit(main(pathlib.Path(sys.argv[1]),pathlib.Path(sys.argv[2]),pathlib.Path(sys.argv[3])))
