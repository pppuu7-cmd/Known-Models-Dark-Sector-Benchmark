#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from verification.m27.ddm_cosmological_energy_transfer import exact_solver,spec,A,ODM
from verification.m27.perturbation_source_conditioning_audit import solve_norm,support_index,forcing_hat

PREREG='protocol/W04_M27_PERTURBATION_SOURCE_NORMALIZED_PRODUCTION_RECOVERY_PREREGISTRATION_v0.1.md'
AUTH='waves/wave_04_dark_matter/M27_PERTURBATION_SOURCE_DEEP_TOLERANCE_RECOVERY_SUMMARY.json'
KS=(0.1,1.0,10.0)

def ampmax(a,b):
    a=np.asarray(a); b=np.asarray(b); den=max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300)
    return float(np.max(np.abs(a-b))/den)

def norm_l2(a,b):
    a=np.asarray(a); b=np.asarray(b); den=max(float(np.linalg.norm(a)),float(np.linalg.norm(b)),1e-300)
    return float(np.linalg.norm(a-b)/den)

def run(delta,y,g,out):
    try:
        auth=json.loads((ROOT/AUTH).read_text())
        authorized=bool(auth.get('normalized_27way_recovery_authorized')) and auth.get('production_rtol_if_authorized')==1e-11 and auth.get('support_fraction_if_authorized')==1e-4
        if not authorized: raise RuntimeError('canonical deep-tolerance authorization absent or mismatched')
        e=exact_solver(delta,y,g,64); i0=support_index(e['D'],e['D'],1e-4)
        _,w,G=spec(delta,y,g,64)
        t=e['t']; surv=np.exp(np.clip(-np.outer(t,G),-745,0)); rhoi=ODM*A[:,None]**-3*(surv*w[None,:])
        x0=float(np.log(A[i0])); h,_=forcing_hat(np.log(A),x0); dp=-0.5*h
        lhs=np.sum(rhoi*G[None,:]*dp[:,None],axis=1); rhs=e['src']*dp
        sid=ampmax(lhs[i0:],rhs[i0:]); source_pass=bool(sid<=1e-12)
        stability={}; finite=True; stable=True; prod={}
        for k in KS:
            d11,t11=solve_norm(e,k,1e-11,i0); d12,t12=solve_norm(e,k,1e-12,i0)
            rd=ampmax(d11,d12); rt=ampmax(t11,t12); ok=rd<=1e-6 and rt<=1e-6
            stability[str(k)]={'dhat_amp_norm_max':rd,'that_amp_norm_max':rt,'pass':bool(ok)}; stable &= ok
            finite &= bool(np.all(np.isfinite(d11)) and np.all(np.isfinite(t11)) and np.all(np.isfinite(d12)) and np.all(np.isfinite(t12)))
            prod[k]=(d11,t11)
        geff=float(np.dot(e['w'],e['G'])); c=exact_solver(delta,y,geff,1); ic=support_index(e['D'],c['D'],1e-4)
        comparator={}
        for k in KS:
            de,te=solve_norm(e,k,1e-11,ic); dc,tc=solve_norm(c,k,1e-11,ic)
            comparator[str(k)]={'dhat_normalized_L2':norm_l2(de,dc),'that_normalized_L2':norm_l2(te,tc)}
        gates={'deep_n1_authorization':authorized,'component_source_identity':source_pass,'ensemble_solver_stability':bool(stable),'finite':bool(finite)}
        ok=all(gates.values())
        r={'schema':'KMDSB.M27.PerturbationSourceNormalizedProductionRecovery.v1','preregistration':PREREG,'authorization_file':AUTH,'authorization_run_id':34557946030,'original_raw_source_run_id':34557311114,'delta':float(delta),'y':float(y),'Gamma0_over_Hstar':float(g),'N':64,'support_fraction':1e-4,'production_rtol':1e-11,'verification_rtol':1e-12,'k_over_Hstar':list(KS),'source_identity_amp_norm_max':sid,'solver_stability':stability,'moment_matched_single_comparator':comparator,'gates':gates,'classification':'M27_DDM_PERTURBATION_SOURCE_CLOSURE_PASS_WITH_NORMALIZED_FLUID_SCOPE' if ok else 'M27_DDM_PERTURBATION_SOURCE_NORMALIZED_PRODUCTION_NOT_ESTABLISHED','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,'full_hierarchy_gate':'OPEN'}
    except Exception as exc:
        r={'schema':'KMDSB.M27.PerturbationSourceNormalizedProductionRecovery.v1','preregistration':PREREG,'delta':float(delta),'y':float(y),'Gamma0_over_Hstar':float(g),'classification':'M27_DDM_PERTURBATION_SOURCE_NORMALIZED_PRODUCTION_BLOCKED','error':repr(exc),'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,'full_hierarchy_gate':'OPEN'}
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('delta',type=float); ap.add_argument('y',type=float); ap.add_argument('g',type=float); ap.add_argument('out',type=Path); a=ap.parse_args(); run(a.delta,a.y,a.g,a.out)
