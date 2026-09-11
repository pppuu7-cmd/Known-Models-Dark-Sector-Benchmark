#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

PREREG='protocol/W04_M27_DDM_COSMOLOGICAL_ENERGY_TRANSFER_PREREGISTRATION_v0.1.md'
AI=1e-5; OB=0.05; OR=9e-5; OL=0.69; ODM=0.26; N=64; DM=0.25
X=np.linspace(math.log(AI),0.0,4001); A=np.exp(X)

def spec(delta,y,g0,ncomp=N):
    n=np.arange(ncomp,dtype=float); m=1+DM*np.power(n,delta); w=np.power(m,-y); w/=w.sum(); G=g0*np.power(m,y); return m,w,G

def exact_solver(delta,y,g0,ncomp=N):
    _,w,G=spec(delta,y,g0,ncomp)
    def rhs(x,z):
        a=math.exp(x); t=max(float(z[0]),0.0); D=max(float(z[1]),0.0)
        surv=np.exp(np.clip(-G*t,-745,0)); rp=ODM*a**-3*float(np.dot(w,surv)); rr=D*a**-4
        H=math.sqrt(OR*a**-4+OB*a**-3+OL+rp+rr)
        src=ODM*a**-3*float(np.dot(w*G,surv))
        return [1/H,a**4*src/H]
    sol=solve_ivp(rhs,(X[0],X[-1]),[0.0,0.0],t_eval=X,method='DOP853',rtol=1e-10,atol=1e-12)
    if not sol.success: raise RuntimeError(sol.message)
    t=sol.y[0]; D=sol.y[1]; surv=np.exp(np.clip(-np.outer(t,G),-745,0)); rp=ODM*A**-3*(surv@w); rr=D*A**-4
    H=np.sqrt(OR*A**-4+OB*A**-3+OL+rp+rr); src=ODM*A**-3*(surv@(w*G)); integrand=A**4*src/H
    return {'t':t,'D':D,'rp':rp,'rr':rr,'H':H,'src':src,'integrand':integrand,'w':w,'G':G}

def direct_single(g0):
    rp0=ODM*AI**-3
    def rhs(x,z):
        a=math.exp(x); t,rp,rr=map(float,z); rp=max(rp,0.0); rr=max(rr,0.0)
        H=math.sqrt(OR*a**-4+OB*a**-3+OL+rp+rr)
        return [1/H,-3*rp-(g0/H)*rp,-4*rr+(g0/H)*rp]
    sol=solve_ivp(rhs,(X[0],X[-1]),[0.0,rp0,0.0],t_eval=X,method='DOP853',rtol=1e-10,atol=1e-12)
    if not sol.success: raise RuntimeError(sol.message)
    t,rp,rr=sol.y; H=np.sqrt(OR*A**-4+OB*A**-3+OL+np.maximum(rp,0)+np.maximum(rr,0)); return {'t':t,'rp':rp,'rr':rr,'H':H}

def p95sym(a,b,mask=None):
    a=np.asarray(a); b=np.asarray(b); m=np.isfinite(a)&np.isfinite(b)
    if mask is not None: m &= mask
    d=2*np.abs(a[m]-b[m])/(np.abs(a[m])+np.abs(b[m])+1e-300)
    return float(np.percentile(d,95)) if d.size else None

def run(delta,y,g0,out):
    try:
        e=exact_solver(delta,y,g0,N); e1=exact_solver(delta,y,g0,1); d1=direct_single(g0)
        drm=(e1['rr']+d1['rr'])>1e-20*max(float(np.max(e1['rr'])),float(np.max(d1['rr'])),1.0)
        reference={'H_p95':p95sym(e1['H'],d1['H']),'parent_p95':p95sym(e1['rp'],d1['rp']),'daughter_p95':p95sym(e1['rr'],d1['rr'],drm)}
        refpass=all(v is not None and v<=1e-7 for v in reference.values())
        finite=all(np.all(np.isfinite(e[k])) for k in ['t','D','rp','rr','H','src'])
        positive=bool(np.all(e['H']>0) and np.all(e['rp']>=0) and np.all(e['rr']>=-1e-12))
        comp=A**3*e['rp']; parentmono=bool(np.all(np.diff(comp)<=1e-10*np.maximum(comp[:-1],1.0)))
        dmono=bool(np.all(np.diff(e['D'])>=-1e-10*np.maximum(np.abs(e['D'][:-1]),1.0)))
        daughter=bool(abs(float(e['D'][0]))<=1e-14 and e['D'][-1]>0)
        q=float(np.trapezoid(e['integrand'],X)); cons=abs(q-e['D'][-1])/max(abs(e['D'][-1]),1e-300); conspass=cons<=1e-4
        geff=float(np.dot(e['w'],e['G'])); c=exact_solver(delta,y,geff,1)
        drm2=(e['rr']+c['rr'])>1e-12*max(float(np.max(e['rr'])),float(np.max(c['rr'])),1.0)
        comparator={'Gamma_eff_initial':geff,'H_p95_symmetric':p95sym(e['H'],c['H']),'parent_p95_symmetric':p95sym(e['rp'],c['rp']),'daughter_p95_symmetric':p95sym(e['rr'],c['rr'],drm2)}
        gates={'n1_reference':refpass,'finite':finite,'positive':positive,'parent_comoving_nonincreasing':parentmono,'daughter_comoving_nondecreasing':dmono,'daughter_created':daughter,'source_integral_conservation':conspass}
        ok=all(gates.values())
        r={'schema':'KMDSB.M27.DDMCosmologicalEnergyTransfer.v1','preregistration':PREREG,'delta':delta,'y':y,'gamma':-y,'Gamma0_over_Hstar':g0,'N':N,'reference_residuals':reference,'source_integral_relative_residual':cons,'final':{'t_Hstar':float(e['t'][-1]),'parent_density':float(e['rp'][-1]),'daughter_radiation_density':float(e['rr'][-1]),'H_over_Hstar':float(e['H'][-1])},'moment_matched_single_comparator':comparator,'gates':gates,'classification':'M27_DDM_COSMOLOGICAL_ENERGY_TRANSFER_PASS_WITH_SCOPE' if ok else 'M27_DDM_COSMOLOGICAL_ENERGY_TRANSFER_NOT_ESTABLISHED','K1_promoted':False,'K4_promoted':False,'physical_falsification':False}
    except Exception as exc:
        r={'schema':'KMDSB.M27.DDMCosmologicalEnergyTransfer.v1','preregistration':PREREG,'delta':delta,'y':y,'Gamma0_over_Hstar':g0,'classification':'M27_DDM_COSMOLOGICAL_ENERGY_TRANSFER_NUMERICAL_BLOCKED','error':repr(exc),'K1_promoted':False,'K4_promoted':False,'physical_falsification':False}
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('delta',type=float); ap.add_argument('y',type=float); ap.add_argument('g0',type=float); ap.add_argument('out',type=Path); a=ap.parse_args(); run(a.delta,a.y,a.g0,a.out)
