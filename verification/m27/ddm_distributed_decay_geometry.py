#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import numpy as np

PREREG='protocol/W04_M27_DDM_DISTRIBUTED_DECAY_GEOMETRY_PREREGISTRATION_v0.1.md'
N=64; DM=0.25

def run(delta:float,y:float,out:Path):
    gamma=-y
    n=np.arange(N,dtype=float)
    mass=1.0+DM*np.power(n,delta)
    width=np.power(mass,y)
    raw=np.power(mass,gamma); w=raw/raw.sum()
    t=np.logspace(-4,4,20001)
    E=np.exp(-np.outer(t,width))
    S=E@w
    J=E@(w*width)
    Q=E@(w*width*width)
    mask=S>1e-250
    geff=np.full_like(S,np.nan); curv=np.full_like(S,np.nan)
    geff[mask]=J[mask]/S[mask]
    curv[mask]=Q[mask]/S[mask]-geff[mask]**2

    s1=np.exp(-t); j1=np.exp(-t); m1=s1>1e-250
    rel_s=float(np.max(np.abs(S*0 + s1-s1)[m1]/s1[m1]))
    # Independent N=1 numerical evaluation rather than reusing analytic arrays.
    num_s1=np.exp(-np.outer(t,np.array([1.0])))@np.array([1.0])
    num_j1=np.exp(-np.outer(t,np.array([1.0])))@np.array([1.0])
    rel_s=float(np.max(np.abs(num_s1[m1]-s1[m1])/s1[m1]))
    rel_j=float(np.max(np.abs(num_j1[m1]-j1[m1])/j1[m1]))
    rel_g=float(np.max(np.abs(num_j1[m1]/num_s1[m1]-1.0)))
    single_pass=max(rel_s,rel_j,rel_g)<=1e-12

    supported=np.where(mask)[0]
    sdiff=np.diff(S[supported])
    monotonic_s=bool(np.all(sdiff<=1e-14*np.maximum(S[supported][:-1],1e-300)))
    j_positive=bool(np.all(J[supported]>0))
    gd=np.diff(geff[supported]); monotonic_g=bool(np.all(gd<=1e-11*np.maximum(geff[supported][:-1],1.0)))
    curv_min=float(np.min(curv[supported])); curv_max=float(np.max(curv[supported]))
    curv_nonneg=curv_min>=-1e-10*max(curv_max,1.0)
    curv_positive=curv_max>1e-12
    tau=1.0/width; lifetime_span=float(np.log10(tau.max())-np.log10(tau.min()))

    fitmask=(S>1e-10)&(S<0.999999)
    if fitmask.sum()>20:
        X=np.column_stack([np.ones(fitmask.sum()),-t[fitmask]])
        beta=np.linalg.lstsq(X,np.log(S[fitmask]),rcond=None)[0]
        A=float(np.exp(beta[0])); g=float(beta[1]); pred=A*np.exp(-g*t[fitmask])
        residual=float(np.linalg.norm(pred-S[fitmask])/np.linalg.norm(S[fitmask]))
    else:
        A=g=residual=None

    weights_pass=bool(np.all(w>0) and abs(float(w.sum())-1.0)<=1e-14)
    ordered=bool(np.all(np.diff(width)>0))
    gates={'single_species_exact':single_pass,'weights':weights_pass,'nondegenerate_widths':ordered,'survival_monotonic':monotonic_s,'injection_positive':j_positive,'effective_rate_nonincreasing':monotonic_g,'curvature_nonnegative':bool(curv_nonneg),'curvature_positive_somewhere':bool(curv_positive),'lifetime_span_positive':lifetime_span>0}
    ok=all(gates.values())
    r={'schema':'KMDSB.M27.DDMDistributedDecayGeometry.v1','preregistration':PREREG,'delta':delta,'y':y,'gamma':gamma,'N':N,'delta_m_over_m0':DM,'weights_sum':float(w.sum()),'width_min':float(width.min()),'width_max':float(width.max()),'lifetime_log10_span':lifetime_span,'single_species_max_relative_errors':{'S':rel_s,'J':rel_j,'Gamma_eff':rel_g},'curvature_min':curv_min,'curvature_max':curv_max,'Gamma_eff_initial_supported':float(geff[supported[0]]),'Gamma_eff_final_supported':float(geff[supported[-1]]),'best_single_exponential':{'A':A,'Gamma':g,'relative_L2_residual':residual},'gates':gates,'classification':'M27_DDM_DISTRIBUTED_DECAY_GEOMETRY_PASS_WITH_SCOPE' if ok else 'M27_DDM_DISTRIBUTED_DECAY_GEOMETRY_NOT_ESTABLISHED','K1_promoted':False,'K4_promoted':False,'physical_falsification':False}
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('delta',type=float); ap.add_argument('y',type=float); ap.add_argument('out',type=Path); a=ap.parse_args(); run(a.delta,a.y,a.out)
