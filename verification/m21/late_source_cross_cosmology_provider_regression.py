#!/usr/bin/env python3
from __future__ import annotations
import json,math,pathlib,struct,sys
PINS={'P0':'e85808324f51fc694d12e3ed7439552a3c3f9540','P1':'64bbab707faf4de4779a9e04edd180fef18d98fa'}
COSMOS=('base','h95','h105','ob95','ob105','odm95','odm105'); LS=(399,400,401)
PROTOCOL='protocol/W04_M21_LATE_SOURCE_CROSS_COSMOLOGY_PROVIDER_REGRESSION_v0.1.md'
def ulp(x):
 if x<=0:raise ValueError(x)
 return int(struct.unpack('>Q',struct.pack('>d',x))[0])-int(struct.unpack('>Q',struct.pack('>d',1.0))[0])
def one(root,pat):
 x=list(pathlib.Path(root).rglob(pat))
 if len(x)!=1:raise RuntimeError((pat,x))
 return x[0]
def diag(p):
 d={}
 for z in pathlib.Path(p).read_text(errors='replace').splitlines():
  x=[float(v.replace('D','E').replace('d','e')) for v in z.split()]
  if len(x)!=15 or not all(math.isfinite(v) for v in x):raise RuntimeError(f'bad row {p}')
  k=(int(round(x[2])),int(round(x[0])))
  if k in d:raise RuntimeError(f'duplicate {k}')
  d[k]=x
 return d
def cell_check(d,m):
 N=diag(one(d,'native.dat')); C=diag(one(d,'cf.dat')); keys=set(N)
 if keys!=set(C):return False,{'reason':'key_mismatch'}
 arvals={r[3] for r in N.values()}
 if len(arvals)!=1:return False,{'reason':'ar_not_constant'}
 ar=next(iter(arvals)); pred400=(ar<1.0); max_neighbor=0.0; relation=True; qn={l:0 for l in LS}
 for key in sorted(keys):
  l,q=key;n=N[key];c=C[key];qn[l]+=1
  npred=bool(round(n[7]));cpred=bool(round(c[7]));nactual=bool(round(n[8]));cactual=bool(round(c[8]))
  expn={399:False,400:pred400,401:True}[l];expc={399:False,400:False,401:True}[l]
  relation &= npred==expn and nactual==npred and cpred==expc and cactual==cpred
  if l in (399,401):
   relation &= int(round(n[10]))==int(round(c[10]))
   rel=abs(n[13]-c[13])/max(abs(n[13]),abs(c[13]),1e-300);max_neighbor=max(max_neighbor,rel);relation &= rel<=1e-10
  else:
   changed=int(round(n[10]))!=int(round(c[10]));relation &= changed==pred400
   if pred400: relation &= int(round(c[10]))==int(round(c[9]))
 qshape=all(qn[l]>=20 for l in LS)
 return bool(m.get('authority_clean') is True and qshape and relation),{'angular_rescaling':ar,'signed_ulp_from_1':ulp(ar),'below_one':ar<1.0,'equal_one':ar==1.0,'above_one':ar>1.0,'q_counts':qn,'max_neighbor_transfer_relative_difference':max_neighbor,'structural_rule_pass':relation,'authority_clean':m.get('authority_clean') is True}
def main(root,out):
 root=pathlib.Path(root); entries={}
 for d in root.iterdir():
  if not d.is_dir():continue
  ms=list(d.rglob('case_meta.json'))
  if len(ms)!=1:continue
  m=json.load(open(ms[0]));k=(m.get('provider_label'),m.get('cosmology_id'))
  if k[0] in PINS and k[1] in COSMOS:entries[k]=(d,m)
 need={(p,c) for p in PINS for c in COSMOS}
 if set(entries)!=need:raise RuntimeError(f'missing {need-set(entries)}')
 cases={}; provider={}; all_authority=True; all_struct=True
 for p in PINS:
  cells={};nlo=neq=nhi=0;ppass=True
  for c in COSMOS:
   d,m=entries[(p,c)]
   if m.get('provider_pin')!=PINS[p]:raise RuntimeError(f'pin mismatch {p}/{c}')
   ok,info=cell_check(d,m);cells[c]=info;ppass &= ok;all_authority &= info.get('authority_clean',False);all_struct &= info.get('structural_rule_pass',False)
   nlo+=int(info.get('below_one',False));neq+=int(info.get('equal_one',False));nhi+=int(info.get('above_one',False))
  provider[p]={'provider_pin':PINS[p],'cells':cells,'count_below_one':nlo,'count_equal_one':neq,'count_above_one':nhi,'sign_diversity':nlo>=1 and (neq+nhi)>=1,'all_cells_pass':ppass}
 version_struct=[provider[p]['all_cells_pass'] for p in PINS]
 if all(version_struct):
  if all(provider[p]['sign_diversity'] for p in PINS):cls='M21_LATE_SOURCE_THRESHOLD_MECHANISM_GENERALIZES_WITH_BOUNDARY_CROSSINGS_WITH_SCOPE'
  else:cls='M21_LATE_SOURCE_THRESHOLD_MECHANISM_GENERALIZES_STRUCTURALLY_WITH_SCOPE'
  rc=0
 elif all_authority and version_struct[0]!=version_struct[1]:
  cls='M21_LATE_SOURCE_THRESHOLD_PROVIDER_VERSION_DIVERGENCE_WITH_SCOPE';rc=0
 else:
  cls='M21_LATE_SOURCE_CROSS_COSMOLOGY_PROVIDER_REGRESSION_BLOCKED';rc=1
 o={'schema':'KMDSB.W04.M21.CrossCosmologyProviderRegression.v0.1','protocol':PROTOCOL,'classification':cls,'providers':provider,'all_authority_clean':all_authority,'all_structural_rules_pass':all_struct,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,'class_defect_claimed':False,'production_fix_claimed':False}
 pathlib.Path(out).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n');print(json.dumps(o,indent=2,sort_keys=True));return rc
if __name__=='__main__':
 if len(sys.argv)!=3:raise SystemExit('usage: analyzer COMPONENTS OUT')
 raise SystemExit(main(sys.argv[1],sys.argv[2]))
