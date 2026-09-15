#!/usr/bin/env python3
from __future__ import annotations
import json,math,pathlib,sys
PROTOCOL='protocol/W04_M21_CONDITIONAL_LATE_SOURCE_APPROXIMATION_OFF_ACCURACY_REFERENCE_v0.1.md'
PARENTS={'M21_LATE_SOURCE_THRESHOLD_MECHANISM_GENERALIZES_WITH_BOUNDARY_CROSSINGS_WITH_SCOPE','M21_LATE_SOURCE_THRESHOLD_MECHANISM_GENERALIZES_STRUCTURALLY_WITH_SCOPE'}
PROVIDERS=('P0','P1');COSMOS=('base','h95','h105','ob95','ob105','odm95','odm105')
def one(root,pat):
 x=list(pathlib.Path(root).rglob(pat))
 if len(x)!=1:raise RuntimeError((pat,x))
 return x[0]
def diag(p):
 d={}
 for z in pathlib.Path(p).read_text(errors='replace').splitlines():
  x=[float(v.replace('D','E').replace('d','e')) for v in z.split()]
  if len(x)!=15 or not all(math.isfinite(v) for v in x):raise RuntimeError(f'bad row {p}')
  k=(int(round(x[2])),int(round(x[0])));d[k]=x
 return d
def cl_ee400(root,segment,c):
 xs=[p for p in pathlib.Path(root).rglob(f'{c}*_cl.dat') if segment in p.parts]
 if len(xs)!=1:raise RuntimeError((segment,c,xs))
 for raw in xs[0].read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s or s.startswith('#'):continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except:continue
  if len(r)>=3 and int(round(r[0]))==400:return r[2]
 raise RuntimeError(f'no EE l400 {xs[0]}')
def rel(a,b):return abs(a-b)/max(abs(a),abs(b),1e-300)
def main(offroot,parentroot,parentagg,out):
 pa=json.load(open(parentagg));
 if pa.get('classification') not in PARENTS:raise RuntimeError('unauthorized parent')
 offroot=pathlib.Path(offroot);parentroot=pathlib.Path(parentroot)
 off={};par={}
 for d in offroot.iterdir():
  if not d.is_dir():continue
  ms=list(d.rglob('case_meta.json'))
  if len(ms)==1:
   m=json.load(open(ms[0]));k=(m.get('provider_label'),m.get('cosmology_id'))
   if k[0] in PROVIDERS and k[1] in COSMOS:off[k]=(d,m)
 for d in parentroot.iterdir():
  if not d.is_dir():continue
  ms=list(d.rglob('case_meta.json'))
  if len(ms)==1:
   m=json.load(open(ms[0]));k=(m.get('provider_label'),m.get('cosmology_id'))
   if k[0] in PROVIDERS and k[1] in COSMOS:par[k]=(d,m)
 need={(p,c) for p in PROVIDERS for c in COSMOS}
 if set(off)!=need or set(par)!=need:raise RuntimeError(f'missing off={need-set(off)} parent={need-set(par)}')
 authority=True;all_pass=True;cells={}
 for key in sorted(need):
  p,c=key;od,om=off[key];pd,pm=par[key];authority &= om.get('authority_clean') is True and pm.get('authority_clean') is True
  O=diag(one(od,'off.dat'));N=diag(one(pd,'native.dat'));I=diag(one(pd,'cf.dat'))
  keys=set(O);shape=keys==set(N)==set(I)
  if not shape:raise RuntimeError(f'key mismatch {key}')
  arvals={r[3] for r in N.values()}
  if len(arvals)!=1:raise RuntimeError(f'ar mismatch {key}')
  ar=next(iter(arvals)); affected=ar<1.0
  l399_native=0.;l399_ident=0.;l400_native=0.;l400_ident=0.;l401_native=0.;l401_ident=0.;ep399=True
  for k in keys:
   l=k[0];o=O[k];n=N[k];i=I[k]
   rn=rel(n[13],o[13]);ri=rel(i[13],o[13])
   if l==399:
    l399_native=max(l399_native,rn);l399_ident=max(l399_ident,ri);ep399 &= int(round(n[10]))==int(round(i[10]))==int(round(o[10]))
   elif l==400:l400_native=max(l400_native,rn);l400_ident=max(l400_ident,ri)
   elif l==401:l401_native=max(l401_native,rn);l401_ident=max(l401_ident,ri)
  eeN=cl_ee400(pd,'native_output',c);eeI=cl_ee400(pd,'cf_output',c);eeO=cl_ee400(od,'off_output',c);eN=rel(eeN,eeO);eI=rel(eeI,eeO)
  locality=ep399 and l399_native<=1e-10 and l399_ident<=1e-10
  if affected:
   identity_matches=l400_ident<=1e-10
   not_worse=l400_ident<=l400_native+1e-14 and eI<=eN+1e-14
   cellpass=locality and identity_matches and not_worse
  else:
   identity_matches=max(l400_native,l400_ident)<=1e-10
   not_worse=eI<=1e-10 and eN<=1e-10
   cellpass=locality and identity_matches and not_worse
  all_pass &= cellpass
  cells[f'{p}/{c}']={'angular_rescaling':ar,'affected_native_branch':affected,'l399_native_vs_off_max_rel':l399_native,'l399_identity_vs_off_max_rel':l399_ident,'l400_native_vs_off_max_rel':l400_native,'l400_identity_vs_off_max_rel':l400_ident,'l401_native_vs_off_max_rel_descriptive':l401_native,'l401_identity_vs_off_max_rel_descriptive':l401_ident,'l400_EE_native_vs_off_rel':eN,'l400_EE_identity_vs_off_rel':eI,'l399_locality_clean':locality,'identity_matches_off':identity_matches,'identity_not_worse_than_native':not_worse,'cell_pass':cellpass}
 if not authority:cls='M21_LATE_SOURCE_APPROXIMATION_OFF_ACCURACY_REFERENCE_BLOCKED';rc=1
 elif all_pass:cls='M21_LATE_SOURCE_FLAT_IDENTITY_MATCHES_APPROXIMATION_OFF_REFERENCE_WITH_SCOPE';rc=0
 else:cls='M21_LATE_SOURCE_FLAT_IDENTITY_ACCURACY_ADVANTAGE_NOT_ESTABLISHED_WITH_SCOPE';rc=0
 o={'schema':'KMDSB.W04.M21.ApproximationOffAccuracyReference.v0.1','protocol':PROTOCOL,'parent_classification':pa.get('classification'),'classification':cls,'authority_clean':authority,'all_cells_pass':all_pass,'cells':cells,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,'class_defect_claimed':False,'production_fix_claimed':False}
 pathlib.Path(out).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n');print(json.dumps(o,indent=2,sort_keys=True));return rc
if __name__=='__main__':
 if len(sys.argv)!=5:raise SystemExit('usage: analyzer OFF_COMPONENTS PARENT_COMPONENTS PARENT_AGG OUT')
 raise SystemExit(main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]))
