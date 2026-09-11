#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from verification.m27.ddm_cosmological_energy_transfer import AI,OB,OR,OL,ODM,X,A,exact_solver,p95sym

PREREG='protocol/W04_M27_N1_REFERENCE_CONDITIONING_AUDIT_PREREGISTRATION_v0.1.md'

def direct_comoving(g0:float):
    def rhs(x,z):
        a=math.exp(x); t,R,D=map(float,z)
        R=max(R,0.0); D=max(D,0.0)
        H=math.sqrt(OR*a**-4+OB*a**-3+OL+R*a**-3+D*a**-4)
        return [1.0/H,-(g0/H)*R,a*(g0/H)*R]
    sol=solve_ivp(rhs,(X[0],X[-1]),[0.0,ODM,0.0],t_eval=X,method='DOP853',rtol=1e-10,atol=1e-12)
    if not sol.success: raise RuntimeError(sol.message)
    t,R,D=sol.y
    rp=R*A**-3; rr=D*A**-4
    H=np.sqrt(OR*A**-4+OB*A**-3+OL+rp+rr)
    return {'t':t,'R':R,'D':D,'rp':rp,'rr':rr,'H':H}

def run(g0:float,out:Path):
    try:
        e=exact_solver(1.0,1.0,g0,1)
        c=direct_comoving(g0)
        mask=(e['rr']+c['rr'])>1e-20*max(float(np.max(e['rr'])),float(np.max(c['rr'])),1.0)
        res={'H_p95':p95sym(e['H'],c['H']),'parent_p95':p95sym(e['rp'],c['rp']),'daughter_p95':p95sym(e['rr'],c['rr'],mask)}
        passed=all(v is not None and v<=1e-7 for v in res.values())
        r={'schema':'KMDSB.M27.N1ReferenceConditioningAudit.v1','preregistration':PREREG,'Gamma0_over_Hstar':g0,'formulation':'comoving_R=a^3rho_parent,D=a^4rho_dr','reference_residuals':res,'support_points_daughter':int(np.count_nonzero(mask)),'final_comoving_parent':float(c['R'][-1]),'final_comoving_daughter':float(c['D'][-1]),'classification':'M27_N1_COMOVING_REFERENCE_PASS' if passed else 'M27_N1_COMOVING_REFERENCE_NOT_ESTABLISHED','K1_promoted':False,'K4_promoted':False,'physical_falsification':False}
    except Exception as exc:
        r={'schema':'KMDSB.M27.N1ReferenceConditioningAudit.v1','preregistration':PREREG,'Gamma0_over_Hstar':g0,'classification':'M27_N1_COMOVING_REFERENCE_NUMERICAL_BLOCKED','error':repr(exc),'K1_promoted':False,'K4_promoted':False,'physical_falsification':False}
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('g0',type=float); ap.add_argument('out',type=Path); a=ap.parse_args(); run(a.g0,a.out)
