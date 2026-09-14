#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
CASES=('ref','f0','f1','f2','f3','f4')
def main(primary,shadow,selection,out):
 p=json.loads((primary/'lane_meta.json').read_text()); s=json.loads((shadow/'lane_meta.json').read_text()); sel=json.loads(selection.read_text())
 reasons=[]; solver=sel.get('thermo_evolver')
 if sel.get('authorized') is not True: reasons.append('selection_not_authorized')
 for role,m in [('primary',p),('shadow',s)]:
  if m.get('role')!=role: reasons.append(f'{role}_role_mismatch')
  if m.get('provider_head')!=PIN or m.get('exact_head') is not True: reasons.append(f'{role}_provider_pin')
  if m.get('all_cases_rc0') is not True: reasons.append(f'{role}_case_execution')
  if m.get('thermo_evolver')!=solver: reasons.append(f'{role}_solver')
  if m.get('duplicate_free_serialization') is not True: reasons.append(f'{role}_serialization')
 expected={'primary':{'tol_thermo_integration':'1e-7','l_logstep':'1.005','l_linstep':'10'},'shadow':{'tol_thermo_integration':'1e-6','l_logstep':'1.0075','l_linstep':'12'}}
 for role,m in [('primary',p),('shadow',s)]:
  for k,v in expected[role].items():
   if str(m.get(k))!=v: reasons.append(f'{role}_{k}')
 for c in CASES:
  if p.get('ini_sha256',{}).get(c) is None or p.get('ini_sha256',{}).get(c)!=s.get('ini_sha256',{}).get(c): reasons.append(f'ini_identity_{c}')
 for k in ('cl_permille_sha256','ncdm_tight_sha256'):
  if p.get(k) is None or p.get(k)!=s.get(k): reasons.append(k+'_identity')
 result={'schema':'KMDSB.W04.M21.K1V2ExecutionIdentity.v0.1','provider':f'lesgourg/class_public@{PIN}','selection_authorized':sel.get('authorized') is True,'thermo_evolver':solver,'physical_input_identity':not any(x.startswith('ini_identity_') for x in reasons),'baseline_precision_identity':not any(x.endswith('_identity') and not x.startswith('ini_identity_') for x in reasons),'all_cases_rc0':p.get('all_cases_rc0') is True and s.get('all_cases_rc0') is True,'reasons':reasons,'pass':len(reasons)==0}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps(result,indent=2,sort_keys=True))
 if reasons: raise SystemExit(1)
if __name__=='__main__':
 if len(sys.argv)!=5: raise SystemExit('usage: validate_k1v2_execution_identity.py PRIMARY_DIR SHADOW_DIR SELECTION.json OUT.json')
 main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]))
