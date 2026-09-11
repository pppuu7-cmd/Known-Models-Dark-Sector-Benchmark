#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from verification.m27.ddm_cosmological_energy_transfer import exact_solver,direct_single,A,X

PREREG='protocol/W04_M27_PERTURBATION_SOURCE_CONDITIONING_RECOVERY_PREREGISTRATION_v0.1.md'
KS=(0.1,1.0,10.0)
SUPPORTS=(1e-4,3e-4,1e-3,3e-3,1e-2)
RTOLS=(1e-9,1e-10,1e-11)

def direct_bg(g):
    d=direct_single(g); d['D']=np.maximum(d['rr'],0)*A**4; d['src']=g*np.maximum(d['rp'],0); return d

def support_index(Da,Db,f=1e-4):
    s=np.asarray(Da)+np.asarray(Db); w=np.flatnonzero(s>f*max(float(s[-1]),1e-300))
    if not w.size: raise RuntimeError(f'empty support {f}')
    return int(w[0])

def forcing_hat(x,x0):
    u=(x-x0)/(0.0-x0)
    h=np.sin(2*np.pi*u)+0.35*np.sin(5*np.pi*u)
    dh=(2*np.pi*np.cos(2*np.pi*u)+0.35*5*np.pi*np.cos(5*np.pi*u))/(0.0-x0)
    return h,dh

def interp(x,arr): return float(np.interp(x,X,arr))

def solve_norm(bg,k,rtol,i0):
    x0=float(X[i0]); h0,_=forcing_hat(x0,x0); dp0=-0.5*h0
    def rhs(x,z):
        a=math.exp(x); H=interp(x,bg['H']); rr=max(interp(x,bg['rr']),1e-300); Q=interp(x,bg['src'])
        h,dh=forcing_hat(x,x0); dp=-0.5*h; dd=float(z[0]); th=float(z[1]); C=Q/(H*rr)
        return [-(4/3)*th/(a*H)-(2/3)*dh+C*(dp-dd),(k*k/(4*a*H))*dd-C*th]
    xs=X[i0:]
    sol=solve_ivp(rhs,(float(xs[0]),0.0),[dp0,0.0],t_eval=xs,method='DOP853',rtol=rtol,atol=rtol*1e-3)
    if not sol.success: raise RuntimeError(sol.message)
    return sol.y[0],sol.y[1]

def ampmax(a,b,mask):
    a=np.asarray(a)[mask]; b=np.asarray(b)[mask]
    den=max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300)
    return float(np.max(np.abs(a-b))/den)

def run(g,out):
    try:
        e=exact_solver(1.0,1.0,g,1); d=direct_bg(g); i0=support_index(e['D'],d['D'],1e-4)
        Dsum=e['D']+d['D']; Dmax=max(float(Dsum[-1]),1e-300)
        base={}; fine={}; coarse={}; finite=True
        sols={}
        for k in KS:
            sols[(k,'e9')]=solve_norm(e,k,1e-9,i0)
            sols[(k,'e10')]=solve_norm(e,k,1e-10,i0)
            sols[(k,'e11')]=solve_norm(e,k,1e-11,i0)
            sols[(k,'d10')]=solve_norm(d,k,1e-10,i0)
            for pair in sols.values(): finite &= bool(np.all(np.isfinite(pair[0])) and np.all(np.isfinite(pair[1])))
        for f in SUPPORTS:
            m=(Dsum[i0:] > f*Dmax)
            key=f'{f:.0e}'
            base[key]={}; fine[key]={}; coarse[key]={}
            for k in KS:
                de,te=sols[(k,'e10')]; dd,td=sols[(k,'d10')]
                base[key][str(k)]={'dhat_amp_norm_max':ampmax(de,dd,m),'that_amp_norm_max':ampmax(te,td,m)}
                d10,t10=sols[(k,'e10')]; d11,t11=sols[(k,'e11')]
                fine[key][str(k)]={'dhat_amp_norm_max':ampmax(d10,d11,m),'that_amp_norm_max':ampmax(t10,t11,m)}
                d9,t9=sols[(k,'e9')]
                coarse[key][str(k)]={'dhat_amp_norm_max':ampmax(d9,d10,m),'that_amp_norm_max':ampmax(t9,t10,m)}
        support_pass={key:all(v['dhat_amp_norm_max']<=1e-5 and v['that_amp_norm_max']<=1e-5 for v in vals.values()) for key,vals in base.items()}
        r={'schema':'KMDSB.M27.PerturbationSourceConditioningAudit.v1','preregistration':PREREG,'Gamma0_over_Hstar':float(g),'k_over_Hstar':list(KS),'supports':list(SUPPORTS),'n1_reference_by_support':base,'n1_support_pass':support_pass,'solver_fine_pair_by_support':fine,'solver_coarse_pair_by_support':coarse,'finite':bool(finite),'classification':'M27_PERTURBATION_SOURCE_CONDITIONING_GAMMA_MEASURED','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
    except Exception as exc:
        r={'schema':'KMDSB.M27.PerturbationSourceConditioningAudit.v1','preregistration':PREREG,'Gamma0_over_Hstar':float(g),'classification':'M27_PERTURBATION_SOURCE_CONDITIONING_NUMERICAL_BLOCKED','error':repr(exc),'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('g',type=float); ap.add_argument('out',type=Path); a=ap.parse_args(); run(a.g,a.out)
