#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from verification.m25.m25_k1_precision_floor_diagnostic import analyze as base_analyze

PREREG='protocol/W04_M25_NCDM_FLUID_APPROXIMATION_DIAGNOSTIC_PREREGISTRATION_v0.1.md'

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('root',type=Path); ap.add_argument('model',choices=['m0','m1']); ap.add_argument('status',type=Path); ap.add_argument('out',type=Path); a=ap.parse_args()
    tmp=a.out.with_suffix('.base.json')
    base_analyze(a.root,a.model,'pk_ref',a.status,tmp)
    r=json.loads(tmp.read_text()); tmp.unlink(missing_ok=True)
    blocks=r.get('blocks',{})
    targets=['Pk','CMB_TT','CMB_EE','CMB_TE']
    recovered=[k for k in targets if blocks.get(k,{}).get('tail_scaling_recovered')]
    base_cls=r.get('classification','')
    if base_cls=='M25_PRECISION_FLOOR_DIAGNOSTIC_PROVIDER_BLOCKED': cls='M25_NCDM_FLUID_APPROXIMATION_PROVIDER_BLOCKED'
    elif len(recovered)==len(targets) and blocks.get('H',{}).get('tail_scaling_recovered'): cls='M25_NCDM_FLUID_APPROXIMATION_LOCALIZED'
    elif recovered: cls='M25_NCDM_FLUID_APPROXIMATION_PARTIALLY_LOCALIZED'
    else: cls='M25_NCDM_FLUID_APPROXIMATION_INSENSITIVE'
    r.update({'schema':'KMDSB.M25.NCDMFluidApproximationDiagnostic.v1','preregistration':PREREG,'ncdm_fluid_approximation':3,'ncdmfa_mode':'none','source_matched_tolerance':1e-6,'recovered_perturbation_blocks':recovered,'classification':cls,'K1_promoted':False,'K4_promoted':False,'physical_falsification':False})
    a.out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
