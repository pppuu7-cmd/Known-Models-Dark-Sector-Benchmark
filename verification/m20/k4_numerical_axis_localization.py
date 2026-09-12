#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np

PIN='e17d3664dac677b604fd4ff02fb2af105a6937fa'
PREREG='protocol/W04_M20_K4_NUMERICAL_AXIS_LOCALIZATION_PREREGISTRATION_v0.1.md'
W=24.33
SIGMAS=[0.0,1.0,0.1,0.01]
OUT=['ma200','z_acc','rsCDM_acc','rhosCDM_acc','rmaxCDM_acc','VmaxCDM_acc','rsSIDM_acc','rhosSIDM_acc','rcSIDM_acc','rmaxSIDM_acc','VmaxSIDM_acc','m_z0','rsCDM_z0','rhosCDM_z0','rmaxCDM_z0','VmaxCDM_z0','rsSIDM_z0','rhosSIDM_z0','rcSIDM_z0','rmaxSIDM_z0','VmaxSIDM_z0','ctCDM_z0','tt_ratio','weightCDM','weightSIDM','surviveCDM','surviveSIDM']
STRUCT={'Vmax_z0':('VmaxSIDM_z0','VmaxCDM_z0'),'rmax_z0':('rmaxSIDM_z0','rmaxCDM_z0'),'rs_z0':('rsSIDM_z0','rsCDM_z0'),'rhos_z0':('rhosSIDM_z0','rhosCDM_z0')}
BASE={'M0':1.e12,'redshift':0.,'M0_at_redshift':True,'dz':0.2,'N_herm':3,'zmax':4.,'logmamin':9,'N_ma':30}
PROFILES={'hermite5':{'dz':0.2,'N_herm':5},'dz01':{'dz':0.1,'N_herm':3}}

def run(mod,s,args):
    r=mod.subhalo_properties(sigma0_m=float(s),w=W).subhalo_properties_calc(**args)
    if len(r)!=len(OUT): raise RuntimeError(f'output contract {len(r)} != {len(OUT)}')
    return {k:np.asarray(v) for k,v in zip(OUT,r)}

def sym(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    if a.shape!=b.shape or not(np.all(np.isfinite(a)) and np.all(np.isfinite(b))): raise RuntimeError('finite/shape contract')
    floor=1e-14*max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300)
    q=np.abs(2*(a-b)/(np.abs(a)+np.abs(b)+floor)).ravel()
    return float(np.percentile(q,95)),float(np.max(q))

def profile(mod,args):
    ref=run(mod,0.0,args)
    mask=np.isfinite(ref['weightCDM'].astype(float))&(ref['weightCDM'].astype(float)>0)
    if not np.any(mask): raise RuntimeError('empty reference support')
    exact_max=0.0
    for _,(sidm,cdm) in STRUCT.items():
        _,mx=sym(ref[sidm][mask],ref[cdm][mask]); exact_max=max(exact_max,mx)
    core0=np.abs(ref['rcSIDM_z0'][mask].astype(float))/np.maximum(np.abs(ref['rsCDM_z0'][mask].astype(float)),1e-300)
    if not np.all(np.isfinite(core0)): raise RuntimeError('core zero nonfinite')
    exact_max=max(exact_max,float(np.max(core0)))
    responses={}
    for s in SIGMAS[1:]:
        c=run(mod,s,args)
        for k in OUT:
            if np.asarray(c[k]).shape!=np.asarray(ref[k]).shape: raise RuntimeError(f'{s} shape {k}')
        cell={}
        for name,(sidm,cdm) in STRUCT.items(): cell[name]=sym(c[sidm][mask],ref[cdm][mask])[0]
        core=np.abs(c['rcSIDM_z0'][mask].astype(float))/np.maximum(np.abs(ref['rsCDM_z0'][mask].astype(float)),1e-300)
        if not np.all(np.isfinite(core)): raise RuntimeError('core nonfinite')
        cell['core_ratio']=float(np.percentile(core,95))
        responses[str(s)]=cell
    return {'args':args,'support_n':int(mask.sum()),'exact_zero_identity_max':exact_max,'exact_zero_identity_pass':bool(exact_max<=1e-10),'responses':responses}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('provider',type=Path); ap.add_argument('lane',choices=sorted(PROFILES)); ap.add_argument('out',type=Path); a=ap.parse_args()
    sys.path.insert(0,str(a.provider.resolve())); import sashimi_si
    out={'schema':'KMDSB.M20.K4NumericalAxisLocalization.v1','model_id':'M20','family_id':'F20','provider':'shinichiroando/sashimi-si','provider_commit':PIN,'preregistration':PREREG,'lane':a.lane,'K4_promoted':False,'physical_falsification':False,'scientific_fail':False,'diagnostic_only':True}
    try:
        base=profile(sashimi_si,dict(BASE))
        var_args=dict(BASE); var_args.update(PROFILES[a.lane]); var=profile(sashimi_si,var_args)
        ds=[]; cells=[]
        for s in map(str,SIGMAS[1:]):
            for k in list(STRUCT)+['core_ratio']:
                x=float(base['responses'][s][k]); y=float(var['responses'][s][k]); d=float(2*abs(y-x)/(abs(y)+abs(x)+1e-30)); ds.append(d); cells.append({'sigma0_m':float(s),'observable':k,'baseline':x,'diagnostic':y,'symmetric_relative_discrepancy':d})
        mx=float(max(ds)); med=float(np.median(ds))
        integrity=bool(base['exact_zero_identity_pass'] and var['exact_zero_identity_pass'])
        if not integrity: cls='M20_K4_AXIS_EXECUTION_OR_INTEGRITY_BLOCKED'
        elif mx<=0.10: cls='M20_K4_AXIS_LOW_SENSITIVITY_DIAGNOSTIC'
        elif mx<=0.30: cls='M20_K4_AXIS_MODERATE_SENSITIVITY_DIAGNOSTIC'
        else: cls='M20_K4_AXIS_STRONG_SENSITIVITY_DIAGNOSTIC'
        out.update({'baseline':base,'diagnostic_profile':var,'response_comparison_cells':cells,'max_symmetric_relative_discrepancy':mx,'median_symmetric_relative_discrepancy':med,'classification':cls})
    except Exception as e:
        out.update({'classification':'M20_K4_AXIS_EXECUTION_OR_INTEGRITY_BLOCKED','error':repr(e)})
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__': main()
