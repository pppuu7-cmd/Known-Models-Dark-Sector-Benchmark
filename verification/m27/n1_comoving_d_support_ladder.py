#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from verification.m27.ddm_cosmological_energy_transfer import A,exact_solver,p95sym
from verification.m27.n1_reference_conditioning_audit import direct_comoving

PREREG='protocol/W04_M27_N1_COMOVING_D_SUPPORT_LADDER_PREREGISTRATION_v0.1.md'
LEVELS=[('D12',1e-12),('D10',1e-10),('D08',1e-8),('D06',1e-6),('D04',1e-4),('D02',1e-2)]

def qstats(a,b,m):
    d=2*np.abs(a[m]-b[m])/(np.abs(a[m])+np.abs(b[m])+1e-300); idx=np.where(m)[0]
    return {'n':int(d.size),'a_min':float(A[idx[0]]) if d.size else None,'p50':float(np.percentile(d,50)) if d.size else None,'p95':float(np.percentile(d,95)) if d.size else None,'p99':float(np.percentile(d,99)) if d.size else None,'max':float(np.max(d)) if d.size else None}

def run(g0,out):
    try:
        e=exact_solver(1.0,1.0,g0,1); c=direct_comoving(g0); de=e['D']; dc=c['D']; dm=max(float(np.max(de)),float(np.max(dc)),1e-300)
        slices={name:qstats(de,dc,(de+dc)>fac*dm) for name,fac in LEVELS}
        r={'schema':'KMDSB.M27.N1ComovingDSupportLadder.v1','preregistration':PREREG,'Gamma0_over_Hstar':g0,'slices':slices,'D_amplitude_normalized_max_abs':float(np.max(np.abs(de-dc))/dm),'H_p95':p95sym(e['H'],c['H']),'parent_p95':p95sym(e['rp'],c['rp']),'classification':'M27_N1_COMOVING_D_SUPPORT_LADDER_MEASURED','K1_promoted':False,'K4_promoted':False,'physical_falsification':False}
    except Exception as exc:
        r={'schema':'KMDSB.M27.N1ComovingDSupportLadder.v1','preregistration':PREREG,'Gamma0_over_Hstar':g0,'classification':'M27_N1_COMOVING_D_SUPPORT_NUMERICAL_BLOCKED','error':repr(exc),'K1_promoted':False,'K4_promoted':False,'physical_falsification':False}
    Path(out).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('g0',type=float); p.add_argument('out',type=Path); a=p.parse_args(); run(a.g0,a.out)
