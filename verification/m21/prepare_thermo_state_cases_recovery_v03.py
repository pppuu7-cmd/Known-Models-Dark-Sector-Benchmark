#!/usr/bin/env python3
from __future__ import annotations
import hashlib,importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
GEN=HERE/'mixed_cold_warm_k1_reference.py'
CASES=('ref','f2','f3','f4')
PROTOCOL='protocol/W04_M21_THERMO_STATE_EXPLICIT_NONE_KEY_RECOVERY_v0.1.md'
REMOVE=('output = tCl,pCl,mPk','non linear = none')
ADD='write_thermodynamics = yes'
def loadmod():
 s=importlib.util.spec_from_file_location('m21_k1_gen',GEN); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def H(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main(out:Path):
 out.mkdir(parents=True,exist_ok=True); base=out/'_full'; loadmod().prepare(base)
 manifest={'schema':'KMDSB.W04.M21.ThermoStateCasesRecovery.v0.3','protocol':PROTOCOL,'parent_protocol':'protocol/W04_M21_THERMODYNAMICS_STATE_BRANCH_SIGNATURE_v0.1.md','generator':str(GEN),'removed_lines':list(REMOVE),'added_line':ADD,'cases':{}}
 for c in CASES:
  src=base/f'{c}.ini'; lines=src.read_text().splitlines(); positions={x:[i for i,v in enumerate(lines) if v==x] for x in REMOVE}
  if any(len(positions[x])!=1 for x in REMOVE): raise RuntimeError(f'expected exactly one frozen downstream line in {c}: {positions}')
  if any(v.strip().startswith('write_thermodynamics') or v.strip().startswith('write thermodynamics') for v in lines): raise RuntimeError(f'source already sets thermodynamics output: {c}')
  retained=[v for v in lines if v not in REMOVE]; dst_lines=retained+[ADD]; dst=out/f'{c}.ini'; dst.write_text('\n'.join(dst_lines)+'\n')
  if [v for v in dst_lines if v!=ADD] != retained: raise RuntimeError(f'retained-line drift: {c}')
  # Explicit guard: state-only file must not contain either nonlinear key spelling.
  for v in dst_lines:
   key=v.split('=',1)[0].strip() if '=' in v else ''
   if key in {'non linear','non_linear'}: raise RuntimeError(f'nonlinear key survived recovery in {c}: {v}')
  manifest['cases'][c]={'source_sha256':H(src),'state_sha256':H(dst),'source_line_count':len(lines),'state_line_count':len(dst_lines),'removed_line_indices_zero_based':{x:positions[x][0] for x in REMOVE},'all_retained_lines_order_preserved':True,'physical_lines_preserved':True,'nonlinear_key_absent':True}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
 for p in base.iterdir(): p.unlink()
 base.rmdir(); print(json.dumps(manifest,indent=2,sort_keys=True))
if __name__=='__main__':
 if len(sys.argv)!=2: raise SystemExit('usage: prepare_thermo_state_cases_recovery_v03.py OUTDIR')
 main(Path(sys.argv[1]))
