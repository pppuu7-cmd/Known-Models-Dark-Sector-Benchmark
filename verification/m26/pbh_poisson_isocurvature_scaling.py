#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import numpy as np

OMEGA_DM=0.12
RHO_DM=2.77536627e11*OMEGA_DM
FRACS=np.array([1.0,0.3,0.1,0.03,0.01,0.003,0.001],dtype=float)
PREREG='protocol/W04_M26_PBH_POISSON_ISOCURVATURE_SCALING_PREREGISTRATION_v0.1.md'


def run(mass:float,out:Path):
    vals=FRACS*mass/RHO_DM
    slope=float(np.polyfit(np.log(FRACS),np.log(vals),1)[0])
    ratio=vals/FRACS
    spread=float((ratio.max()-ratio.min())/ratio.mean())
    null=0.0*mass/RHO_DM
    ok=(null==0.0 and np.all(vals>0) and abs(slope-1.0)<=1e-12 and spread<=1e-12)
    r={
      'schema':'KMDSB.M26.PBHPoissonIsocurvatureScaling.v1',
      'preregistration':PREREG,'mass_Msun':mass,'omega_dm':OMEGA_DM,'rho_dm_Msun_Mpc3':RHO_DM,
      'fractions':FRACS.tolist(),'P_shot_total_Mpc3':vals.tolist(),'exact_null':null,
      'fraction_loglog_slope':slope,'P_over_f_relative_spread':spread,
      'classification':'M26_PBH_POISSON_K1_ANALYTIC_PASS_WITH_SCOPE' if ok else 'M26_PBH_POISSON_K1_ANALYTIC_NOT_ESTABLISHED',
      'K1_promoted':False,'K4_promoted':False,'physical_falsification':False,
    }
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('mass',type=float); ap.add_argument('out',type=Path); a=ap.parse_args(); run(a.mass,a.out)
