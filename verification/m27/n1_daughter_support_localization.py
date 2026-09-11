#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from verification.m27.ddm_cosmological_energy_transfer import A,exact_solver
from verification.m27.n1_reference_conditioning_audit import direct_comoving

PREREG='protocol/W04_M27_N1_DAUGHTER_SUPPORT_LOCALIZATION_PREREGISTRATION_v0.1.md'

def stats(a,b,mask):
    d=2*np.abs(a[mask]-b[mask])/(np.abs(a[mask])+np.abs(b[mask])+1e-300)
    idx=np.where(mask)[0]
    return {'n':int(d.size),'a_min':float(A[idx[0]]) if d.size else None,'p50':float(np.percentile(d,50)) if d.size else None,'p95':float(np.percentile(d,95)) if d.size else None,'p99':float(np.percentile(d,99)) if d.size else None,'max':float(np.max(d)) if d.size else None}

def run(g0:float,out:Path):
    try:
        e=exact_solver(1.0,1.0,g0,1); c=direct_comoving(g0)
        r1=e['rr']; r2=c['rr']; mx=max(float(np.max(r1)),float(np.max(r2)),1e-300)
        masks={
          'S20':(r1+r2)>1e-20*max(mx,1.0),
          'S16':(r1+r2)>1e-16*mx,
          'S12':(r1+r2)>1e-12*mx,
          'S08':(r1+r2)>1e-8*mx,
        }
        slices={k:stats(r1,r2,m) for k,m in masks.items()}
        rho_abs=float(np.max(np.abs(r1-r2))/mx)
        D1=e['D']; D2=c['D']; dmx=max(float(np.max(np.abs(D1))),float(np.max(np.abs(D2))),1e-300)
        D_abs=float(np.max(np.abs(D1-D2))/dmx)
        if slices['S20']['p95']>1e-7 and slices['S12']['p95']<=1e-7 and slices['S08']['p95']<=1e-7 and rho_abs<=1e-8:
            cls='M27_N1_DAUGHTER_EARLY_NULL_RELATIVE_METRIC_LOCALIZED'
        else:
            cls='M27_N1_DAUGHTER_PERSISTENT_DISCREPANCY' if (slices['S12']['p95']>1e-7 or slices['S08']['p95']>1e-7) else 'M27_N1_DAUGHTER_SUPPORT_DIAGNOSTIC_INCONCLUSIVE'
        r={'schema':'KMDSB.M27.N1DaughterSupportLocalization.v1','preregistration':PREREG,'Gamma0_over_Hstar':g0,'slices':slices,'rho_dr_amplitude_normalized_max_abs':rho_abs,'D_amplitude_normalized_max_abs':D_abs,'classification':cls,'K1_promoted':False,'K4_promoted':False,'physical_falsification':False}
    except Exception as exc:
        r={'schema':'KMDSB.M27.N1DaughterSupportLocalization.v1','preregistration':PREREG,'Gamma0_over_Hstar':g0,'classification':'M27_N1_DAUGHTER_SUPPORT_NUMERICAL_BLOCKED','error':repr(exc),'K1_promoted':False,'K4_promoted':False,'physical_falsification':False}
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('g0',type=float); ap.add_argument('out',type=Path); a=ap.parse_args(); run(a.g0,a.out)
