#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from pathlib import Path
import sys

import numpy as np

PIN = "e17d3664dac677b604fd4ff02fb2af105a6937fa"
PREREG = "protocol/W04_M20_SIDM_K1_NONLINEAR_REFERENCE_PREREGISTRATION_v0.1.md"
SIGMAS = [10.0, 3.0, 1.0, 0.3, 0.1]
W = 24.33
OUT_NAMES = [
    'ma200','z_acc','rsCDM_acc','rhosCDM_acc','rmaxCDM_acc','VmaxCDM_acc',
    'rsSIDM_acc','rhosSIDM_acc','rcSIDM_acc','rmaxSIDM_acc','VmaxSIDM_acc',
    'm_z0','rsCDM_z0','rhosCDM_z0','rmaxCDM_z0','VmaxCDM_z0','rsSIDM_z0',
    'rhosSIDM_z0','rcSIDM_z0','rmaxSIDM_z0','VmaxSIDM_z0','ctCDM_z0',
    'tt_ratio','weightCDM','weightSIDM','surviveCDM','surviveSIDM'
]
STRUCT = {
    'Vmax_z0': ('VmaxSIDM_z0','VmaxCDM_z0'),
    'rmax_z0': ('rmaxSIDM_z0','rmaxCDM_z0'),
    'rs_z0': ('rsSIDM_z0','rsCDM_z0'),
    'rhos_z0': ('rhosSIDM_z0','rhosCDM_z0'),
}
CATALOG_ARGS = dict(M0=1.e12, redshift=0., M0_at_redshift=True,
                    dz=0.2, N_herm=3, zmax=4., logmamin=9, N_ma=30)


def run_case(mod, sigma):
    sh = mod.subhalo_properties(sigma0_m=float(sigma), w=W)
    raw = sh.subhalo_properties_calc(**CATALOG_ARGS)
    if len(raw) != len(OUT_NAMES):
        raise RuntimeError(f'output length={len(raw)}')
    return {k: np.asarray(v) for k,v in zip(OUT_NAMES, raw)}


def sym_stats(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    if a.shape != b.shape: raise RuntimeError(f'shape mismatch {a.shape} {b.shape}')
    if not (np.all(np.isfinite(a)) and np.all(np.isfinite(b))):
        raise RuntimeError('nonfinite structural block')
    scale=max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300)
    floor=1e-14*scale
    r=2*(a-b)/(np.abs(a)+np.abs(b)+floor)
    q=np.abs(r).ravel()
    return {'median_abs':float(np.median(q)),'rms':float(np.sqrt(np.mean(r*r))),
            'p95_abs':float(np.percentile(q,95)),'max_abs':float(np.max(q)),
            'n':int(q.size),'floor':floor}


def pos_stats(x):
    x=np.asarray(x,float)
    if not np.all(np.isfinite(x)): raise RuntimeError('nonfinite positive block')
    q=np.abs(x).ravel()
    return {'median':float(np.median(q)),'rms':float(np.sqrt(np.mean(q*q))),
            'p95':float(np.percentile(q,95)),'max':float(np.max(q)),'n':int(q.size)}


def slope(vals):
    v=np.asarray(vals[-3:],float); s=np.asarray(SIGMAS[-3:],float)
    if np.any(v<=0): return {'valid':False,'p':None}
    p,b=np.polyfit(np.log(s),np.log(v),1)
    return {'valid':True,'p':float(p),'logA':float(b)}


def judge(vals):
    vals=[float(v) for v in vals]
    monotonic=all(vals[i+1] <= vals[i]*1.02 for i in range(len(vals)-1))
    decreased=vals[-1] < vals[0]
    fit=slope(vals)
    exp_ok=bool(fit['valid'] and fit['p'] is not None and fit['p']>0.5)
    return {'p95_sequence':vals,'monotonic_with_2pct_slack':monotonic,
            'smallest_lower_than_largest':decreased,'fit_smallest3':fit,
            'pass':bool(monotonic and decreased and exp_ok)}


def main(provider:Path,out:Path):
    sys.path.insert(0,str(provider.resolve()))
    import sashimi_si

    ref=run_case(sashimi_si,0.0)
    mask=np.isfinite(ref['weightCDM'].astype(float)) & (ref['weightCDM'].astype(float)>0)
    if not mask.any(): raise RuntimeError('no positive exact-zero CDM reference support')

    exact={}
    max_identity=0.0
    for block,(sidm,cdm) in STRUCT.items():
        st=sym_stats(ref[sidm][mask],ref[cdm][mask])
        exact[block]=st
        max_identity=max(max_identity,st['max_abs'])
    core0=np.abs(ref['rcSIDM_z0'][mask].astype(float))/np.maximum(np.abs(ref['rsCDM_z0'][mask].astype(float)),1e-300)
    exact['core_ratio']=pos_stats(core0)
    exact_ok=bool(max_identity <= 1e-10 and exact['core_ratio']['max']<=1e-10)

    cases=[]
    block_points={k:[] for k in list(STRUCT)+['core_ratio']}
    pop=[]
    for sigma in SIGMAS:
        c=run_case(sashimi_si,sigma)
        for k in OUT_NAMES:
            if np.asarray(c[k]).shape != np.asarray(ref[k]).shape:
                raise RuntimeError(f'{sigma}: shape mismatch {k}')
        csum={'sigma0_m':sigma,'continuous':{}}
        for block,(sidm,cdm_ref) in STRUCT.items():
            st=sym_stats(c[sidm][mask],ref[cdm_ref][mask])
            csum['continuous'][block]=st
            block_points[block].append(st['p95_abs'])
        cr=np.abs(c['rcSIDM_z0'][mask].astype(float))/np.maximum(np.abs(ref['rsCDM_z0'][mask].astype(float)),1e-300)
        cs=pos_stats(cr)
        csum['continuous']['core_ratio']=cs
        block_points['core_ratio'].append(cs['p95'])

        wst=sym_stats(c['weightSIDM'][mask].astype(float),ref['weightCDM'][mask].astype(float))
        surv=np.asarray(c['surviveSIDM'][mask]).astype(bool)
        surv0=np.asarray(ref['surviveCDM'][mask]).astype(bool)
        pd={'sigma0_m':sigma,'weight':wst,'survival_mismatch_fraction':float(np.mean(surv!=surv0))}
        pop.append(pd)
        cases.append(csum)

    blocks={}
    allpass=exact_ok
    for block,vals in block_points.items():
        q=judge(vals); q['points']=[{'sigma0_m':SIGMAS[i],'p95_response':float(vals[i])} for i in range(len(SIGMAS))]
        blocks[block]=q; allpass=allpass and q['pass']

    result={
        'schema':'KMDSB.M20.SIDM.K1NonlinearReference.v1',
        'provider':'shinichiroando/sashimi-si','pin':PIN,'preregistration':PREREG,
        'w_km_s':W,'sigma0_m_cm2_g':SIGMAS,'catalog_args':CATALOG_ARGS,
        'reference_support_n':int(mask.sum()),'exact_zero':exact,'exact_zero_identity_pass':exact_ok,
        'blocks':blocks,'cases':cases,'population_diagnostics':pop,
        'failing_blocks':[k for k,v in blocks.items() if not v['pass']],
        'K1_reference_limit':'PASS_WITH_SCOPE_NONLINEAR_HALO_CDM_LIMIT' if allpass else 'NOT_PROMOTED',
        'K2_physical_geometry':'ONE_SIDED_SIGMA_GE_0_NO_SIGN_QUOTIENT',
        'K4_promoted':False,'physical_falsification':False,
        'classification':'M20_K1_NONLINEAR_REFERENCE_LIMIT_PASS_WITH_SCOPE' if allpass else 'M20_K1_NONLINEAR_REFERENCE_LIMIT_NOT_ESTABLISHED'
    }
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: sidm_k1_nonlinear_reference.py PROVIDER OUT')
    main(Path(sys.argv[1]),Path(sys.argv[2]))
