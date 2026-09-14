#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
PROTOCOL='protocol/W04_M21_CONDITIONAL_K1_V2_NUMERICAL_REFERENCE_PREREGISTRATION_v0.1.md'
THERMO_MAP={
 'M21_THERMO_NDF15_SPECIFIC_SENSITIVITY_SUPPORTED':'rk',
 'M21_THERMO_SOLVER_INDEPENDENT_TIGHT_LIMIT_SUPPORTED_WITH_SCOPE':'ndf15',
}
TAIL_REQUIRED='M21_G2B_L_SAMPLING_TAIL_CONTRACTION_SUPPORTED_WITH_SCOPE'
def main(thermo_path,tail_path,out):
 t=json.loads(thermo_path.read_text()); l=json.loads(tail_path.read_text())
 tc=t.get('classification'); lc=l.get('classification'); solver=THERMO_MAP.get(tc)
 t_identity=t.get('cross_lane_input_identity') is True
 l_identity=l.get('cross_lane_input_identity') is True
 authorized=solver is not None and lc==TAIL_REQUIRED and t_identity and l_identity
 result={
  'schema':'KMDSB.W04.M21.K1V2NumericalReferenceSelection.v0.1',
  'protocol':PROTOCOL,
  'thermo_parent_classification':tc,
  'tail_parent_classification':lc,
  'thermo_parent_identity':t_identity,
  'tail_parent_identity':l_identity,
  'authorized':authorized,
  'thermo_evolver':solver if authorized else None,
  'thermo_evolver_serialized':({'rk':'0','ndf15':'1'}.get(solver) if authorized else None),
  'primary':({'tol_thermo_integration':'1e-7','l_logstep':'1.005','l_linstep':'10'} if authorized else None),
  'shadow':({'tol_thermo_integration':'1e-6','l_logstep':'1.0075','l_linstep':'12'} if authorized else None),
  'classification':('M21_K1_V2_NUMERICAL_REFERENCE_AUTHORIZED' if authorized else 'M21_K1_V2_NOT_AUTHORIZED_NUMERICAL_REFERENCE_OPEN'),
  'K1_promoted':False,
  'physical_falsification':False,
 }
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: select_k1v2_numerical_reference.py THERMO.json TAIL.json OUT.json')
 main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
