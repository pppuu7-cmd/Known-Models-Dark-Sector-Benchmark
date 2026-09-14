#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, math, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
GEN=HERE/'mixed_cold_warm_k1_reference.py'
PROTOCOL='protocol/W04_M21_PERTURBATION_STATE_BRANCH_SIGNATURE_v0.1.md'
CASES=('ref','f2','f3','f4')
L_EXPECT=[100,400,800,1200,2000]

def H(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def loadmod():
 s=importlib.util.spec_from_file_location('m21_k1_source_gate',GEN); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def main(config:Path,out:Path):
 cfg=json.load(open(config))
 if cfg.get('capability_classification')!='M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_PASS_WITH_SCOPE': raise RuntimeError('capability authority absent')
 if cfg.get('l_anchors')!=L_EXPECT: raise RuntimeError('l anchor drift')
 ku=cfg.get('k_anchors_unrounded_Mpc_inv'); ks=cfg.get('k_anchors_12sig_Mpc_inv')
 if not isinstance(ku,list) or not isinstance(ks,list) or len(ku)!=5 or len(ks)!=5: raise RuntimeError('invalid k anchor vectors')
 D=float(cfg['D_star_Mpc'])
 for ell,u,s in zip(L_EXPECT,ku,ks):
  if not math.isfinite(float(u)) or abs(float(u)-ell/D)>max(1e-15,abs(ell/D)*2e-13): raise RuntimeError('unrounded geometry formula mismatch')
  if abs(float(s)-float(f'{float(u):.12g}'))>max(1e-15,abs(float(u))*2e-12): raise RuntimeError('serialized k mismatch')
 if not all(float(ks[i])<float(ks[i+1]) for i in range(4)): raise RuntimeError('k anchors not increasing')
 out.mkdir(parents=True,exist_ok=True); full=out/'_full'; loadmod().prepare(full)
 kvals=','.join(f'{float(x):.12g}' for x in ks)
 manifest={'schema':'KMDSB.W04.M21.PerturbationStateCases.v0.1','protocol':PROTOCOL,'capability_config_sha256':H(config),'k_output_values_serialized':kvals,'cases':{}}
 for c in CASES:
  src=full/f'{c}.ini'; lines=src.read_text().splitlines(); keys=[v.split('=',1)[0].strip() for v in lines if '=' in v]
  if 'k_output_values' in keys: raise RuntimeError(f'{c} already sets k_output_values')
  dst_lines=lines+[f'k_output_values = {kvals}']; dst=out/f'{c}.ini'; dst.write_text('\n'.join(dst_lines)+'\n')
  if dst_lines[:-1]!=lines: raise RuntimeError(f'physical line drift {c}')
  manifest['cases'][c]={'source_sha256':H(src),'output_sha256':H(dst),'physical_lines_preserved':True,'added_line':dst_lines[-1]}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
 for p in full.iterdir(): p.unlink()
 full.rmdir(); print(json.dumps(manifest,indent=2,sort_keys=True))

if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: prepare_perturbation_state_cases.py CONFIG OUTDIR')
 main(Path(sys.argv[1]),Path(sys.argv[2]))
