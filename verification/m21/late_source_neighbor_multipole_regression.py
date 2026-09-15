#!/usr/bin/env python3
from __future__ import annotations
import json,math,pathlib,sys
CASES=('ref','f2','f3','f4'); LANES=('native','flat_identity_predicate'); LS=(399,400,401); Q=set(range(261,334))
PARENT='M21_L400_FLAT_IDENTITY_PREDICATE_BRANCH_CAUSAL_WITH_SCOPE'
PROTOCOL='protocol/W04_M21_CONDITIONAL_LATE_SOURCE_NEIGHBOR_MULTIPOLE_REGRESSION_v0.1.md'
def one(root,pat):
 x=list(pathlib.Path(root).rglob(pat))
 if len(x)!=1:raise RuntimeError((pat,x))
 return x[0]
def diag(p):
 d={}
 for z in pathlib.Path(p).read_text(errors='replace').splitlines():
  x=[float(v.replace('D','E').replace('d','e')) for v in z.split()]
  if len(x)!=15 or not all(math.isfinite(v) for v in x):raise RuntimeError('bad row')
  k=(int(round(x[2])),int(round(x[0])))
  if k in d:raise RuntimeError('duplicate')
  d[k]=x
 return d
def main(root,parent,out):
 p=json.load(open(parent));
 if p.get('classification')!=PARENT:raise RuntimeError('unauthorized parent')
 entries={}
 for d in pathlib.Path(root).iterdir():
  if not d.is_dir():continue
  ms=list(d.rglob('case_meta.json'))
  if len(ms)!=1:continue
  m=json.load(open(ms[0]));k=(m.get('case'),m.get('lane'))
  if k[0] in CASES and k[1] in LANES: entries[k]=(d,m)
 need={(c,l) for c in CASES for l in LANES}
 if set(entries)!=need:raise RuntimeError(f'missing {need-set(entries)}')
 authority=all(m.get('authority_clean') is True for _,m in entries.values()); D={k:diag(one(d,f'neighbor_{k[0]}_{k[1]}.dat')) for k,(d,m) in entries.items()}
 shape=all(set(x)=={(l,q) for l in LS for q in Q} for x in D.values())
 exp_native={399:{c:False for c in CASES},400:{c:c!='f3' for c in CASES},401:{c:True for c in CASES}}
 pattern=True; endpoint_control=True; transfer_control=True; l400_expected=True; max_k_rel=0.0; max_neighbor_transfer_rel=0.0
 for l in LS:
  for q in Q:
   ks=[D[(c,ln)][(l,q)][1] for c in CASES for ln in LANES]; den=max(max(map(abs,ks)),1e-300);max_k_rel=max(max_k_rel,(max(ks)-min(ks))/den)
   for c in CASES:
    n=D[(c,'native')][(l,q)]; cf=D[(c,'flat_identity_predicate')][(l,q)]
    npred=bool(round(n[7])); cpred=bool(round(cf[7])); pattern &= npred==exp_native[l][c]
    pattern &= cpred==({399:False,400:False,401:True}[l])
    if l in (399,401):
     endpoint_control &= int(round(n[10]))==int(round(cf[10]))
     rel=abs(n[13]-cf[13])/max(abs(n[13]),abs(cf[13]),1e-300);max_neighbor_transfer_rel=max(max_neighbor_transfer_rel,rel);transfer_control &= rel<=1e-10
    else:
     changed=int(round(n[10]))!=int(round(cf[10])); l400_expected &= (changed==(c!='f3'))
 geometry=max_k_rel<=1e-6
 if authority and shape and geometry and pattern and endpoint_control and transfer_control and l400_expected:cls='M21_LATE_SOURCE_ULP_SENSITIVITY_THRESHOLD_LOCALIZED_WITH_SCOPE';rc=0
 elif authority and shape and geometry and pattern and (not endpoint_control or not transfer_control):cls='M21_LATE_SOURCE_COUNTERFACTUAL_NEIGHBOR_NONLOCAL_BLOCKED';rc=1
 else:cls='M21_LATE_SOURCE_NEIGHBOR_MULTIPOLE_REGRESSION_BLOCKED';rc=1
 o={'schema':'KMDSB.W04.M21.NeighborMultipoleRegression.v0.1','protocol':PROTOCOL,'parent_classification':p.get('classification'),'classification':cls,'authority_clean':authority,'shape_clean':shape,'geometry_clean':geometry,'max_same_q_k_relative_difference':max_k_rel,'predicate_pattern_exact':pattern,'neighbor_endpoints_invariant':endpoint_control,'neighbor_transfer_null':transfer_control,'max_neighbor_transfer_relative_difference':max_neighbor_transfer_rel,'l400_expected_changes_only':l400_expected,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 pathlib.Path(out).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n');print(json.dumps(o,indent=2,sort_keys=True));return rc
if __name__=='__main__':
 if len(sys.argv)!=4:raise SystemExit('usage: analyzer COMPONENTS PARENT OUT')
 raise SystemExit(main(sys.argv[1],sys.argv[2],sys.argv[3]))
