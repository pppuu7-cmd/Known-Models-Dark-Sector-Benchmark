#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from verification.m27.ddm_cosmological_energy_transfer import exact_solver,direct_single,spec,A,X,ODM

PREREG='protocol/W04_M27_DDM_PERTURBATION_SOURCE_CLOSURE_PREREGISTRATION_v0.1.md'
KS=(0.1,1.0,10.0)
AMPS=(1e-5,2e-5)
D04=1e-4

def forcing(x,x0,amp):
    u=(x-x0)/(0.0-x0)
    h=amp*(np.sin(2*np.pi*u)+0.35*np.sin(5*np.pi*u))
    dh=amp*(2*np.pi*np.cos(2*np.pi*u)+0.35*5*np.pi*np.cos(5*np.pi*u))/(0.0-x0)
    return h,dh

def support_index(Da,Db):
    s=np.asarray(Da)+np.asarray(Db); thr=D04*max(float(s[-1]),1e-300)
    w=np.flatnonzero(s>thr)
    if w.size==0: raise RuntimeError('D04 support empty')
    return int(w[0])

def interp(x,arr): return float(np.interp(x,X,arr))

def fluid_response(bg,k,amp,i0):
    x0=float(X[i0]); h0,_=forcing(x0,x0,amp); dp0=-0.5*h0
    def rhs(x,z):
        a=math.exp(x); H=interp(x,bg['H']); rr=max(interp(x,bg['rr']),1e-300); Q=interp(x,bg['src'])
        h,dh=forcing(x,x0,amp); dp=-0.5*h; dd=float(z[0]); th=float(z[1]); C=Q/(H*rr)
        return [-(4.0/3.0)*th/(a*H)-(2.0/3.0)*dh+C*(dp-dd), (k*k/(4*a*H))*dd-C*th]
    xs=X[i0:]
    sol=solve_ivp(rhs,(float(xs[0]),float(xs[-1])),[dp0,0.0],t_eval=xs,method='DOP853',rtol=1e-10,atol=1e-12)
    if not sol.success: raise RuntimeError(sol.message)
    return xs,sol.y[0],sol.y[1]

def direct_bg(g0):
    d=direct_single(g0); d['src']=g0*np.maximum(d['rp'],0.0); d['D']=np.maximum(d['rr'],0.0)*A**4; return d

def amp_norm_max(a,b):
    a=np.asarray(a); b=np.asarray(b); den=max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300)
    return float(np.max(np.abs(a-b))/den)

def norm_l2(a,b):
    a=np.asarray(a); b=np.asarray(b); den=max(float(np.linalg.norm(a)),float(np.linalg.norm(b)),1e-300)
    return float(np.linalg.norm(a-b)/den)

def common_interp(xa,ya,xb,yb):
    x0=max(float(xa[0]),float(xb[0])); x=np.linspace(x0,0.0,2501)
    return x,np.interp(x,xa,ya),np.interp(x,xb,yb)

def run(delta,y,g0,out):
    try:
        e=exact_solver(delta,y,g0,64); e1=exact_solver(delta,y,g0,1); d1=direct_bg(g0)
        # Component source perturbation identity on ensemble D04 support.
        iens=support_index(e['D'],e['D'])
        _,w,G=spec(delta,y,g0,64)
        t=e['t']; surv=np.exp(np.clip(-np.outer(t,G),-745,0)); rhoi=ODM*A[:,None]**-3*(surv*w[None,:])
        x0=float(X[iens]); h,_=forcing(X,x0,AMPS[0]); dp=-0.5*h
        lhs=np.sum(rhoi*G[None,:]*dp[:,None],axis=1); rhs=e['src']*dp
        sid=amp_norm_max(lhs[iens:],rhs[iens:]); source_pass=bool(sid<=1e-12)
        # N=1 formulation vs independently integrated direct single-DCDM background.
        iref=support_index(e1['D'],d1['D'])
        n1={}; n1pass=True
        for k in KS:
            xa,da,ta=fluid_response(e1,k,AMPS[0],iref); xb,db,tb=fluid_response(d1,k,AMPS[0],iref)
            _,da_i,db_i=common_interp(xa,da,xb,db); _,ta_i,tb_i=common_interp(xa,ta,xb,tb)
            rd=amp_norm_max(da_i,db_i); rt=amp_norm_max(ta_i,tb_i)
            n1[str(k)]={'delta_dr_amp_norm_max':rd,'theta_amp_norm_max':rt}
            n1pass &= (rd<=1e-5 and rt<=1e-5)
        # Linearity of the actual ensemble response.
        linear={}; linpass=True; finite=True
        ensemble_resp={}
        for k in KS:
            x1,dlo,tlo=fluid_response(e,k,AMPS[0],iens); x2,dhi,thi=fluid_response(e,k,AMPS[1],iens)
            rd=amp_norm_max(dhi,2*dlo); rt=amp_norm_max(thi,2*tlo)
            linear[str(k)]={'delta_dr_amp_norm_max':rd,'theta_amp_norm_max':rt}; linpass &= (rd<=1e-7 and rt<=1e-7)
            finite &= bool(np.all(np.isfinite(dlo)) and np.all(np.isfinite(tlo)) and np.all(np.isfinite(dhi)) and np.all(np.isfinite(thi)))
            ensemble_resp[k]=(x1,dlo,tlo)
        # Moment-matched single-lifetime response geometry, descriptive only.
        geff=float(np.dot(e['w'],e['G'])); c=exact_solver(delta,y,geff,1); ic=support_index(e['D'],c['D'])
        comparator={}
        for k in KS:
            xe,de,te=fluid_response(e,k,AMPS[0],ic); xc,dc,tc=fluid_response(c,k,AMPS[0],ic)
            _,dei,dci=common_interp(xe,de,xc,dc); _,tei,tci=common_interp(xe,te,xc,tc)
            comparator[str(k)]={'delta_dr_normalized_L2':norm_l2(dei,dci),'theta_normalized_L2':norm_l2(tei,tci)}
        gates={'component_source_identity':source_pass,'n1_reference':bool(n1pass),'linearity':bool(linpass),'finite':bool(finite)}
        ok=all(gates.values())
        r={'schema':'KMDSB.M27.DDMPerturbationSourceClosure.v1','preregistration':PREREG,'delta':float(delta),'y':float(y),'Gamma0_over_Hstar':float(g0),'N':64,'k_over_Hstar':list(KS),'source_identity_amp_norm_max':sid,'n1_reference':n1,'linearity':linear,'moment_matched_single_comparator':comparator,'gates':gates,'classification':'M27_DDM_PERTURBATION_SOURCE_CLOSURE_PASS_WITH_FLUID_SCOPE' if ok else 'M27_DDM_PERTURBATION_SOURCE_CLOSURE_NOT_ESTABLISHED','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,'full_hierarchy_gate':'OPEN'}
    except Exception as exc:
        r={'schema':'KMDSB.M27.DDMPerturbationSourceClosure.v1','preregistration':PREREG,'delta':float(delta),'y':float(y),'Gamma0_over_Hstar':float(g0),'classification':'M27_DDM_PERTURBATION_SOURCE_CLOSURE_NUMERICAL_BLOCKED','error':repr(exc),'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,'full_hierarchy_gate':'OPEN'}
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('delta',type=float); ap.add_argument('y',type=float); ap.add_argument('g0',type=float); ap.add_argument('out',type=Path); a=ap.parse_args(); run(a.delta,a.y,a.g0,a.out)
