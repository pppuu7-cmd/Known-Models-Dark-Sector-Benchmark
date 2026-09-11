#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from verification.m25.m25_k1_precision_floor_diagnostic import analyze as base_analyze

PREREG='protocol/W04_M25_SOURCE_MATCHED_TOLERANCE_LADDER_PREREGISTRATION_v0.1.md'
TOLS={'t1e6':1e-6,'t3e7':3e-7,'t1e7':1e-7}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('root',type=Path); ap.add_argument('model',choices=['m0','m1']); ap.add_argument('profile',choices=sorted(TOLS)); ap.add_argument('status',type=Path); ap.add_argument('out',type=Path); a=ap.parse_args()
    tmp=a.out.with_suffix('.base.json')
    base_analyze(a.root,a.model,'pk_ref',a.status,tmp)
    r=json.loads(tmp.read_text()); tmp.unlink(missing_ok=True)
    r['schema']='KMDSB.M25.SourceMatchedToleranceLadder.v1'; r['preregistration']=PREREG
    r['tolerance_profile']=a.profile; r['tol_ncdm_bg']=TOLS[a.profile]; r['tol_ncdm']=TOLS[a.profile]
    r['source_matched']=(a.profile=='t1e6'); r['K1_promoted']=False; r['K4_promoted']=False; r['physical_falsification']=False
    a.out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
