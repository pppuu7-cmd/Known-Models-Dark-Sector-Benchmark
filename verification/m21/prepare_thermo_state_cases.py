#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
import importlib.util
HERE=Path(__file__).resolve().parent
GEN=HERE/'mixed_cold_warm_k1_reference.py'
CASES=('ref','f2','f3','f4')
PROTOCOL='protocol/W04_M21_THERMODYNAMICS_STATE_BRANCH_SIGNATURE_v0.1.md'
def loadmod():
 s=importlib.util.spec_from_file_location('m21_k1_gen',GEN); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def H(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main(out:Path):
 out.mkdir(parents=True,exist_ok=True); base=out/'_full'; mod=loadmod(); mod.prepare(base)
 manifest={'schema':'KMDSB.W04.M21.ThermoStateCases.v0.1','protocol':PROTOCOL,'generator':str(GEN),'cases':{},'only_removed_line':'output = tCl,pCl,mPk','only_added_line':'write_thermodynamics = yes'}
 for c in CASES:
  src=base/f'{c}.ini'; lines=src.read_text().splitlines(); removed=[x for x in lines if x.strip().startswith('output =')]
  if removed!=['output = tCl,pCl,mPk']: raise RuntimeError(f'unexpected output line for {c}: {removed}')
  if any(x.strip().startswith('write_thermodynamics') or x.strip().startswith('write thermodynamics') for x in lines): raise RuntimeError('source already sets thermodynamics output')
  dst_lines=[x for x in lines if x!='output = tCl,pCl,mPk']+['write_thermodynamics = yes']
  dst=out/f'{c}.ini'; dst.write_text('\n'.join(dst_lines)+'\n')
  # Verify exact transformation at text-line level: one removal, one addition, no other change.
  reconstructed=[x for x in dst_lines if x!='write_thermodynamics = yes']
  expected=[x for x in lines if x!='output = tCl,pCl,mPk']
  if reconstructed!=expected: raise RuntimeError(f'physical-line drift for {c}')
  manifest['cases'][c]={'source_sha256':H(src),'state_sha256':H(dst),'source_line_count':len(lines),'state_line_count':len(dst_lines),'physical_lines_preserved':True}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
 # Remove unused full-case staging only after hashes are frozen.
 for p in base.iterdir(): p.unlink()
 base.rmdir()
 print(json.dumps(manifest,indent=2,sort_keys=True))
if __name__=='__main__':
 if len(sys.argv)!=2: raise SystemExit('usage: prepare_thermo_state_cases.py OUTDIR')
 main(Path(sys.argv[1]))
