#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from collections import OrderedDict
from pathlib import Path
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_PERTURBATION_STATE_BRANCH_SIGNATURE_v0.1.md'
LANES={
'NDF_T1E5':('ndf15','1','1e-5'),'NDF_T1E6':('ndf15','1','1e-6'),'NDF_T1E7':('ndf15','1','1e-7'),
'RK_T1E5':('rk','0','1e-5'),'RK_T1E6':('rk','0','1e-6'),'RK_T1E7':('rk','0','1e-7')}
def H(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def parse(p):
 out=[]
 for raw in Path(p).read_text(errors='replace').splitlines():
  s=raw.split('#',1)[0].strip()
  if not s: continue
  if '=' not in s: raise RuntimeError(f'unparsed {p}: {raw!r}')
  k,v=(x.strip() for x in s.split('=',1)); out.append((k,v))
 return out
def main(lane,clp,ncdm,out,manifest):
 if lane not in LANES: raise RuntimeError(f'unknown lane {lane}')
 semantic,serialized,tol=LANES[lane]; vals=OrderedDict(); origin={}; conflicts=[]
 def apply(src,items):
  for k,v in items:
   if k in vals: conflicts.append({'key':k,'previous_value':vals[k],'previous_source':origin[k],'final_value':v,'final_source':src})
   vals[k]=v; origin[k]=src
 apply('cl_permille.pre',parse(clp)); apply('m21_ncdm_tight.pre',parse(ncdm)); apply('frozen_common_control',[('evolver','0')]); apply(lane,[('thermo_evolver',serialized),('tol_thermo_integration',tol)])
 if conflicts: raise RuntimeError(f'unexpected lane-profile override(s): {conflicts}')
 lines=['# M21 perturbation-state branch-signature numerical profile',f'# protocol: {PROTOCOL}',f'# lane: {lane}',f'# semantic_solver: {semantic}']+[f'{k} = {v}' for k,v in vals.items()]
 Path(out).write_text('\n'.join(lines)+'\n'); r=parse(out); ks=[k for k,_ in r]; d=dict(r)
 if len(ks)!=len(set(ks)): raise RuntimeError('duplicate serialized keys')
 if d.get('evolver')!='0' or d.get('thermo_evolver')!=serialized or d.get('tol_thermo_integration')!=tol: raise RuntimeError('lane serialization mismatch')
 m={'schema':'KMDSB.W04.M21.PerturbationStateLaneProfile.v0.1','protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}','lane':lane,'thermo_evolver':semantic,'thermo_evolver_serialized':serialized,'tol_thermo_integration':tol,'generic_evolver':'0','cl_permille_sha256':H(clp),'ncdm_tight_sha256':H(ncdm),'output_sha256':H(out),'duplicate_free_serialization':True,'conflicts':conflicts}
 Path(manifest).write_text(json.dumps(m,indent=2,sort_keys=True)+'\n'); print(json.dumps(m,indent=2,sort_keys=True))
if __name__=='__main__':
 if len(sys.argv)!=6: raise SystemExit('usage: build_perturbation_state_lane_profile.py LANE CL_PERMILLE NCDM_TIGHT OUT MANIFEST')
 main(*sys.argv[1:])
