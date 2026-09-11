#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from verification.m27.ddm_cosmological_energy_transfer import exact_solver,direct_single,A,X,AI,OR
from verification.m27.perturbation_source_conditioning_audit import support_index,forcing_hat

PREREG='protocol/W04_M27_DDM_DR_HIERARCHY_CONVERGENCE_PREREGISTRATION_v0.1.md'
KS=(0.1,1.0,10.0)
LMAXS=(8,17,32)
RTOL=1e-11
ATOL=1e-14


def direct_bg(g):
    d=direct_single(g)
    d['D']=np.maximum(d['rr'],0.0)*A**4
    d['src']=g*np.maximum(d['rp'],0.0)
    return d


def tau_array(bg):
    H=np.asarray(bg['H'],dtype=float)
    integ=1.0/(A*H)
    tau=np.empty_like(A)
    tau[0]=AI/math.sqrt(OR)
    dx=np.diff(X)
    tau[1:]=tau[0]+np.cumsum(0.5*(integ[1:]+integ[:-1])*dx)
    return tau


def interp(x,arr):
    return float(np.interp(x,X,arr))


def hierarchy(bg,k,L,i0):
    tau=tau_array(bg)
    x0=float(X[i0])
    xs=X[i0:]
    D=np.asarray(bg['D'],dtype=float)
    src=np.asarray(bg['src'],dtype=float)
    Hs=np.asarray(bg['H'],dtype=float)

    def rhs(x,F):
        a=math.exp(x)
        H=interp(x,Hs)
        f=max(interp(x,D),1e-300)
        Q=interp(x,src)
        t=max(interp(x,tau),1e-300)
        h,dh=forcing_hat(x,x0)
        dp=-0.5*h
        c=k/(a*H)
        dDdx=a**4*Q/H
        d=np.zeros_like(F)
        d[0]=-c*F[1]-(2.0/3.0)*dh*f+dDdx*dp
        d[1]=c*(F[0]-2.0*F[2])/3.0
        d[2]=c*(2.0*F[1]/5.0-3.0*F[3]/5.0)
        for l in range(3,L):
            d[l]=c*(l*F[l-1]-(l+1.0)*F[l+1])/(2.0*l+1.0)
        d[L]=c*F[L-1]-(L+1.0)/(a*H*t)*F[L]
        return d

    sol=solve_ivp(rhs,(float(xs[0]),float(xs[-1])),np.zeros(L+1),t_eval=xs,method='DOP853',rtol=RTOL,atol=ATOL)
    if not sol.success:
        raise RuntimeError(sol.message)
    Farr=sol.y
    f=np.maximum(D[i0:],1e-300)
    delta=Farr[0]/f
    theta=0.75*k*Farr[1]/f
    shear=0.5*Farr[2]/f
    return {'x':xs,'delta':delta,'theta':theta,'shear':shear,'finite':bool(np.all(np.isfinite(Farr)))}


def ampmax(a,b):
    a=np.asarray(a,dtype=float); b=np.asarray(b,dtype=float)
    den=max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300)
    return float(np.max(np.abs(a-b))/den)


def compare(a,b):
    return {q:ampmax(a[q],b[q]) for q in ('delta','theta','shear')}


def ensemble(delta,y,g,out):
    try:
        bg=exact_solver(delta,y,g,64)
        i0=support_index(bg['D'],bg['D'],1e-4)
        res={}; finite=True; passfine=True
        for k in KS:
            sols={L:hierarchy(bg,k,L,i0) for L in LMAXS}
            finite &= all(s['finite'] for s in sols.values())
            coarse=compare(sols[8],sols[17])
            fine=compare(sols[17],sols[32])
            ok=all(v<=1e-4 for v in fine.values())
            passfine &= ok
            res[str(k)]={'L8_vs_L17':coarse,'L17_vs_L32':fine,'fine_pass':bool(ok)}
        ok=bool(finite and passfine)
        r={'schema':'KMDSB.M27.DDMDRHierarchyConvergence.v1','preregistration':PREREG,'mode':'ensemble','delta':float(delta),'y':float(y),'Gamma0_over_Hstar':float(g),'N':64,'lmax_values':list(LMAXS),'k_over_Hstar':list(KS),'support_fraction':1e-4,'rtol':RTOL,'atol':ATOL,'comparisons':res,'finite':bool(finite),'classification':'M27_DDM_DR_HIERARCHY_CONVERGENCE_PASS_WITH_PRESCRIBED_METRIC_SCOPE' if ok else 'M27_DDM_DR_HIERARCHY_CONVERGENCE_NOT_ESTABLISHED','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,'self_consistent_metric_gate':'OPEN'}
    except Exception as exc:
        r={'schema':'KMDSB.M27.DDMDRHierarchyConvergence.v1','preregistration':PREREG,'mode':'ensemble','delta':float(delta),'y':float(y),'Gamma0_over_Hstar':float(g),'classification':'M27_DDM_DR_HIERARCHY_NUMERICAL_BLOCKED','error':repr(exc),'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,'self_consistent_metric_gate':'OPEN'}
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')


def control(g,out):
    try:
        e=exact_solver(1.0,1.0,g,1)
        d=direct_bg(g)
        i0=support_index(e['D'],d['D'],1e-4)
        res={}; finite=True; passed=True
        for k in KS:
            a=hierarchy(e,k,17,i0); b=hierarchy(d,k,17,i0)
            finite &= a['finite'] and b['finite']
            rr=compare(a,b)
            ok=all(v<=1e-4 for v in rr.values())
            passed &= ok
            res[str(k)]={'N1_exact_vs_direct':rr,'pass':bool(ok)}
        ok=bool(finite and passed)
        r={'schema':'KMDSB.M27.DDMDRHierarchyN1Control.v1','preregistration':PREREG,'mode':'control','Gamma0_over_Hstar':float(g),'l_max_dr':17,'k_over_Hstar':list(KS),'support_fraction':1e-4,'rtol':RTOL,'atol':ATOL,'comparisons':res,'finite':bool(finite),'classification':'M27_DDM_DR_HIERARCHY_N1_CONTROL_PASS_WITH_SCOPE' if ok else 'M27_DDM_DR_HIERARCHY_N1_CONTROL_NOT_ESTABLISHED','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
    except Exception as exc:
        r={'schema':'KMDSB.M27.DDMDRHierarchyN1Control.v1','preregistration':PREREG,'mode':'control','Gamma0_over_Hstar':float(g),'classification':'M27_DDM_DR_HIERARCHY_N1_CONTROL_NUMERICAL_BLOCKED','error':repr(exc),'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    sp=ap.add_subparsers(dest='mode',required=True)
    a=sp.add_parser('ensemble'); a.add_argument('delta',type=float); a.add_argument('y',type=float); a.add_argument('g',type=float); a.add_argument('out',type=Path)
    c=sp.add_parser('control'); c.add_argument('g',type=float); c.add_argument('out',type=Path)
    q=ap.parse_args()
    ensemble(q.delta,q.y,q.g,q.out) if q.mode=='ensemble' else control(q.g,q.out)
