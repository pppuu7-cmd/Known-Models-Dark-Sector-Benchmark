#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from verification.m27.ddm_cosmological_energy_transfer import exact_solver
from verification.m27.perturbation_source_conditioning_audit import solve_norm,support_index

PREREG='protocol/W04_M27_PERTURBATION_SOURCE_DEEP_TOLERANCE_RECOVERY_PREREGISTRATION_v0.1.md'
KS=(0.1,1.0,10.0)
RTOLS=(1e-11,3e-12,1e-12)

def ampmax(a,b):
    a=np.asarray(a); b=np.asarray(b); den=max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300)
    return float(np.max(np.abs(a-b))/den)

def run(g,out):
    try:
        e=exact_solver(1.0,1.0,g,1)
        i0=support_index(e['D'],e['D'],1e-4)
        pairs={}; finite=True; allpass=True
        for k in KS:
            sol=[]
            for rtol in RTOLS:
                d,t=solve_norm(e,k,rtol,i0); sol.append((d,t)); finite &= bool(np.all(np.isfinite(d)) and np.all(np.isfinite(t)))
            a={'dhat_amp_norm_max':ampmax(sol[0][0],sol[1][0]),'that_amp_norm_max':ampmax(sol[0][1],sol[1][1])}
            b={'dhat_amp_norm_max':ampmax(sol[1][0],sol[2][0]),'that_amp_norm_max':ampmax(sol[1][1],sol[2][1])}
            ok=all(v<=1e-6 for v in a.values()) and all(v<=1e-6 for v in b.values())
            allpass &= ok
            pairs[str(k)]={'pair_1e11_vs_3e12':a,'pair_3e12_vs_1e12':b,'pass':bool(ok)}
        ok=bool(finite and allpass)
        r={'schema':'KMDSB.M27.PerturbationSourceDeepToleranceRecovery.v1','preregistration':PREREG,'Gamma0_over_Hstar':float(g),'support_fraction':1e-4,'k_over_Hstar':list(KS),'rtols':list(RTOLS),'pairs':pairs,'finite':bool(finite),'classification':'M27_PERTURBATION_SOURCE_DEEP_TOLERANCE_GAMMA_PASS' if ok else 'M27_PERTURBATION_SOURCE_DEEP_TOLERANCE_GAMMA_NOT_ESTABLISHED','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
    except Exception as exc:
        r={'schema':'KMDSB.M27.PerturbationSourceDeepToleranceRecovery.v1','preregistration':PREREG,'Gamma0_over_Hstar':float(g),'classification':'M27_PERTURBATION_SOURCE_DEEP_TOLERANCE_NUMERICAL_BLOCKED','error':repr(exc),'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('g',type=float); ap.add_argument('out',type=Path); a=ap.parse_args(); run(a.g,a.out)
