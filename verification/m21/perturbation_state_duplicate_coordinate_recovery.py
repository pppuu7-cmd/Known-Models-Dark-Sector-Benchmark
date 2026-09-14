#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
import perturbation_state_branch_signature as base

PROTOCOL='protocol/W04_M21_PERTURBATION_STATE_DUPLICATE_COORDINATE_RECOVERY_v0.1.md'

def collapse_exact(A:np.ndarray, ia:int, policy:str)->np.ndarray:
    x=A[:,ia]
    if np.any(~np.isfinite(x)) or np.any(x<=0):
        raise RuntimeError('nonfinite/nonpositive a coordinate')
    chosen={}
    if policy=='FIRST':
        for i,v in enumerate(x): chosen.setdefault(float(v),i)
    elif policy=='LAST':
        for i,v in enumerate(x): chosen[float(v)]=i
    else: raise RuntimeError('unknown duplicate policy')
    idx=np.array(sorted(chosen.values()),dtype=int)
    return A[idx]

def make_prepare(policy:str):
    def prepare_pair(pA:Path,pB:Path,variables:list[str]):
        tA,A=base.parse_table(pA); tB,B=base.parse_table(pB)
        for q in ['a']+variables:
            if q not in tA or q not in tB: raise RuntimeError(f'missing {q} in pair {pA} / {pB}')
        iaA=tA.index('a'); iaB=tB.index('a')
        A=collapse_exact(A,iaA,policy); B=collapse_exact(B,iaB,policy)
        ordA=np.argsort(A[:,iaA]); ordB=np.argsort(B[:,iaB]); A=A[ordA]; B=B[ordB]
        xa=A[:,iaA]; xb=B[:,iaB]
        if np.unique(xa).size!=xa.size or np.unique(xb).size!=xb.size: raise RuntimeError('duplicate collapse failed')
        ma=(xa>=base.A_LO)&(xa<=base.A_HI); mb=(xb>=base.A_LO)&(xb<=base.A_HI)
        xa=xa[ma]; xb=xb[mb]; AA=A[ma]; BB=B[mb]
        if xa.size<16 or xb.size<16: raise RuntimeError(f'insufficient window samples {pA}/{pB}: {xa.size}/{xb.size}')
        lo=max(float(xa.min()),float(xb.min())); hi=min(float(xa.max()),float(xb.max())); keep=(xa>=lo)&(xa<=hi)
        x=xa[keep]; AA=AA[keep]
        if x.size<16: raise RuntimeError(f'insufficient overlap {pA}/{pB}: {x.size}')
        lx=np.log(x); lxb=np.log(xb); out={}
        for v in variables:
            ya=AA[:,tA.index(v)]; yb=np.interp(lx,lxb,BB[:,tB.index(v)])
            d=float(np.linalg.norm(ya-yb)/max(float(np.linalg.norm(ya)),float(np.linalg.norm(yb)),1e-300))
            out[v]={'D':d,'n':int(x.size)}
        return out
    return prepare_pair

def run_view(root:Path,cfg:Path,policy:str,out:Path):
    base.prepare_pair=make_prepare(policy)
    try: base.main(root,cfg,out)
    except SystemExit: pass
    return json.loads(out.read_text())

def edge_map(d):
    return {k:bool(v.get('edge_localized')) for k,v in d.get('edges',{}).items()}

def main(root:Path,cfg:Path,out:Path):
    first=run_view(root,cfg,'FIRST',Path('FIRST_RESULT.json'))
    last=run_view(root,cfg,'LAST',Path('LAST_RESULT.json'))
    usable=(not str(first.get('classification','')).endswith('BLOCKED') and
            not str(last.get('classification','')).endswith('BLOCKED') and
            first.get('classification')==last.get('classification') and
            edge_map(first)==edge_map(last) and
            first.get('cross_lane_input_identity') is True and last.get('cross_lane_input_identity') is True)
    result={
      'schema':'KMDSB.W04.M21.PerturbationStateDuplicateCoordinateRecovery.v0.1',
      'protocol':PROTOCOL,
      'parent_run_id':34895647832,
      'parent_blocked_artifact_id':10369361506,
      'recovery_classification':'M21_PERTURBATION_STATE_DUPLICATE_RECOVERY_ROBUST' if usable else 'M21_PERTURBATION_STATE_DUPLICATE_RECOVERY_AMBIGUOUS_BLOCKED',
      'inherited_classification':first.get('classification') if usable else None,
      'edge_map_identical':edge_map(first)==edge_map(last),
      'first':first,'last':last,
      'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False
    }
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'recovery_classification':result['recovery_classification'],'inherited_classification':result['inherited_classification'],'edge_map_identical':result['edge_map_identical']},indent=2))
    if not usable: raise SystemExit(1)

if __name__=='__main__':
    if len(sys.argv)!=4: raise SystemExit('usage: recovery.py LANES_ROOT CONFIG OUT')
    main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
