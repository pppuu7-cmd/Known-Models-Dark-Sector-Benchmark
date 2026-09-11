#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from verification.m27.ddm_dr_hierarchy_convergence import exact_solver,support_index,hierarchy,compare,KS,RTOL,ATOL

PREREG='protocol/W04_M27_DDM_DR_HIGH_L_REFINEMENT_PREREGISTRATION_v0.1.md'
LMAXS=(17,32,64)


def run(delta:float,y:float,g:float,out:Path):
    try:
        bg=exact_solver(delta,y,g,64)
        i0=support_index(bg['D'],bg['D'],1e-4)
        res={}; finite=True; passed=True
        for k in KS:
            sols={L:hierarchy(bg,k,L,i0) for L in LMAXS}
            finite &= all(s['finite'] for s in sols.values())
            parent=compare(sols[17],sols[32])
            refine=compare(sols[32],sols[64])
            ok=all(v<=1e-4 for v in refine.values())
            passed &= ok
            res[str(k)]={'L17_vs_L32':parent,'L32_vs_L64':refine,'refinement_pass':bool(ok)}
        ok=bool(finite and passed)
        cls='M27_DDM_DR_HIGH_L_HIERARCHY_CONVERGENCE_PASS_WITH_PRESCRIBED_METRIC_SCOPE' if ok else 'M27_DDM_DR_HIGH_L_HIERARCHY_CONVERGENCE_NOT_ESTABLISHED'
        r={'schema':'KMDSB.M27.DDMDRHighLRefinement.v1','preregistration':PREREG,'mode':'ensemble','delta':delta,'y':y,'Gamma0_over_Hstar':g,'N':64,'lmax_values':list(LMAXS),'k_over_Hstar':list(KS),'support_fraction':1e-4,'rtol':RTOL,'atol':ATOL,'comparisons':res,'finite':bool(finite),'classification':cls,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,'parent_L17_failure_preserved':True}
    except Exception as exc:
        r={'schema':'KMDSB.M27.DDMDRHighLRefinement.v1','preregistration':PREREG,'mode':'ensemble','delta':delta,'y':y,'Gamma0_over_Hstar':g,'classification':'M27_DDM_DR_HIGH_L_HIERARCHY_NUMERICAL_BLOCKED','error':repr(exc),'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,'parent_L17_failure_preserved':True}
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    if len(sys.argv)!=5: raise SystemExit('usage: script delta y g out.json')
    run(float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),Path(sys.argv[4]))
