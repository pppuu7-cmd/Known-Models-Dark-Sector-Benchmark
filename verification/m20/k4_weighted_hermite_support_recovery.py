#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np

PIN='e17d3664dac677b604fd4ff02fb2af105a6937fa'
PREREG='protocol/W04_M20_K4_WEIGHTED_HERMITE_SUPPORT_RECOVERY_PREREGISTRATION_v0.1.md'
W=24.33
ORDERS=[13,17,21]
SIGMAS=[0.0,1.0,0.1,0.01]
OUT=['ma200','z_acc','rsCDM_acc','rhosCDM_acc','rmaxCDM_acc','VmaxCDM_acc','rsSIDM_acc','rhosSIDM_acc','rcSIDM_acc','rmaxSIDM_acc','VmaxSIDM_acc','m_z0','rsCDM_z0','rhosCDM_z0','rmaxCDM_z0','VmaxCDM_z0','rsSIDM_z0','rhosSIDM_z0','rcSIDM_z0','rmaxSIDM_z0','VmaxSIDM_z0','ctCDM_z0','tt_ratio','weightCDM','weightSIDM','surviveCDM','surviveSIDM']
STRUCT={'Vmax_z0':('VmaxSIDM_z0','VmaxCDM_z0'),'rmax_z0':('rmaxSIDM_z0','rmaxCDM_z0'),'rs_z0':('rsSIDM_z0','rsCDM_z0'),'rhos_z0':('rhosSIDM_z0','rhosCDM_z0')}
BASE={'M0':1.e12,'redshift':0.,'M0_at_redshift':True,'dz':0.2,'zmax':4.,'logmamin':9,'N_ma':30}

def run(mod,s,n):
    args=dict(BASE); args['N_herm']=n
    r=mod.subhalo_properties(sigma0_m=float(s),w=W).subhalo_properties_calc(**args)
    if len(r)!=len(OUT): raise RuntimeError(f'output contract {len(r)} != {len(OUT)}')
    return {k:np.asarray(v) for k,v in zip(OUT,r)}

def abs_sym(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    if a.shape!=b.shape or not(np.all(np.isfinite(a)) and np.all(np.isfinite(b))): raise RuntimeError('finite/shape contract')
    floor=1e-14*max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300)
    return np.abs(2*(a-b)/(np.abs(a)+np.abs(b)+floor)).ravel()

def wq(x,w,q=0.95):
    x=np.asarray(x,float).ravel(); w=np.asarray(w,float).ravel()
    m=np.isfinite(x)&np.isfinite(w)&(w>0)
    x=x[m]; w=w[m]
    if x.size==0 or not np.isfinite(w.sum()) or w.sum()<=0: raise RuntimeError('empty/nonfinite weighted support')
    ii=np.argsort(x); x=x[ii]; w=w[ii]; c=np.cumsum(w)/np.sum(w)
    return float(np.interp(q,c,x))

def profile(mod,n):
    ref=run(mod,0.0,n)
    rw=np.asarray(ref['weightCDM'],float).ravel()
    mask=np.isfinite(rw)&(rw>0)
    if not np.any(mask): raise RuntimeError('empty reference support')
    w=rw[mask]
    exact_max=0.0
    for sidm,cdm in STRUCT.values(): exact_max=max(exact_max,float(np.max(abs_sym(np.asarray(ref[sidm])[mask],np.asarray(ref[cdm])[mask]))))
    core0=np.abs(np.asarray(ref['rcSIDM_z0'],float)[mask])/np.maximum(np.abs(np.asarray(ref['rsCDM_z0'],float)[mask]),1e-300)
    if not np.all(np.isfinite(core0)): raise RuntimeError('core zero nonfinite')
    exact_max=max(exact_max,float(np.max(core0)))
    responses={}
    for s in SIGMAS[1:]:
        c=run(mod,s,n)
        for k in OUT:
            if np.asarray(c[k]).shape!=np.asarray(ref[k]).shape: raise RuntimeError(f'{n}/{s} shape {k}')
        cell={}
        for name,(sidm,cdm) in STRUCT.items():
            q=abs_sym(np.asarray(c[sidm])[mask],np.asarray(ref[cdm])[mask])
            cell[name]={'weighted_p95':wq(q,w),'unweighted_p95':float(np.percentile(q,95))}
        core=np.abs(np.asarray(c['rcSIDM_z0'],float)[mask])/np.maximum(np.abs(np.asarray(ref['rsCDM_z0'],float)[mask]),1e-300)
        if not np.all(np.isfinite(core)): raise RuntimeError('core nonfinite')
        cell['core_ratio']={'weighted_p95':wq(core,w),'unweighted_p95':float(np.percentile(core,95))}
        responses[str(s)]=cell
    return {'N_herm':n,'support_n':int(mask.sum()),'reference_weight_sum':float(np.sum(w)),'exact_zero_identity_max':exact_max,'exact_zero_identity_pass':bool(exact_max<=1e-10),'responses':responses}

def disc(a,b): return float(2*abs(a-b)/(abs(a)+abs(b)+1e-30))

def compare(pa,pb,stat):
    cells=[]
    for s in map(str,SIGMAS[1:]):
        for k in list(STRUCT)+['core_ratio']:
            a=float(pa['responses'][s][k][stat]); b=float(pb['responses'][s][k][stat]); d=disc(a,b)
            cells.append({'sigma0_m':float(s),'observable':k,'a':a,'b':b,'D':d})
    ds=[c['D'] for c in cells]
    return {'max':float(max(ds)),'median':float(np.median(ds)),'cells':cells}

def main(provider,outp):
    sys.path.insert(0,str(provider.resolve())); import sashimi_si
    out={'schema':'KMDSB.M20.K4WeightedHermiteSupportRecovery.v1','model_id':'M20','family_id':'F20','provider':'shinichiroando/sashimi-si','provider_commit':PIN,'preregistration':PREREG,'orders':ORDERS,'K4_promoted':False,'scientific_fail':False,'physical_falsification':False,'diagnostic_only':True}
    try:
        p={str(n):profile(sashimi_si,n) for n in ORDERS}; out['profiles']=p
        if not all(v['exact_zero_identity_pass'] for v in p.values()): raise RuntimeError('exact-zero identity failed')
        w13=compare(p['13'],p['17'],'weighted_p95'); w17=compare(p['17'],p['21'],'weighted_p95')
        u13=compare(p['13'],p['17'],'unweighted_p95'); u17=compare(p['17'],p['21'],'unweighted_p95')
        out['weighted_D_13to17']=w13; out['weighted_D_17to21']=w17
        out['unweighted_control_D_13to17']=u13; out['unweighted_control_D_17to21']=u17
        if w17['max']<=0.10 and w17['max']<=1.05*w13['max']:
            cls='M20_K4_WEIGHTED_HERMITE_CONVERGENCE_RECOVERED_DIAGNOSTIC'
        elif w17['max']<=0.5*u17['max']:
            cls='M20_K4_WEIGHTING_REDUCES_SENSITIVITY_NOT_CONVERGED_DIAGNOSTIC'
        else:
            cls='M20_K4_WEIGHTED_HERMITE_NONCONVERGENCE_PERSISTS_DIAGNOSTIC'
        out['classification']=cls
    except Exception as e:
        out['classification']='M20_K4_WEIGHTED_HERMITE_EXECUTION_OR_INTEGRITY_BLOCKED'; out['error']=repr(e)
    outp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__': main(Path(sys.argv[1]),Path(sys.argv[2]))
