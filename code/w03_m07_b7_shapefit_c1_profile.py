#!/usr/bin/env python3
"""Profile the M07 local q direction against C1 smooth-w in frozen ShapeFit space."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import numpy as np

USE=("LRG1","LRG2","LRG3","ELG2","QSO")
COV_SCALE=1e-4
COV={
"LRG1":[[541.309833,48.425593,-4.652853,-37.707751],[48.425593,97.249820,-34.923265,-14.418597],[-4.652853,-34.923265,41.295470,15.405508],[-37.707751,-14.418597,15.405508,48.918910]],
"LRG2":[[762.457717,39.781004,-1.896006,-62.812849],[39.781004,36.344098,-17.341350,-8.333900],[-1.896006,-17.341350,28.119682,8.865225],[-62.812849,-8.333900,8.865225,47.624520]],
"LRG3":[[847.499793,26.038900,3.257324,-37.016091],[26.038900,16.251088,-10.044074,-3.698790],[3.257324,-10.044074,22.370314,6.467510],[-37.016091,-3.698790,6.467510,34.883220]],
"ELG2":[[2342.506886,26.159601,13.521001,-95.336060],[26.159601,10.309303,-6.654663,-5.183903],[13.521001,-6.654663,13.997473,9.109619],[-95.336060,-5.183903,9.109619,43.575710]],
"QSO":[[3013.788566,-2.205101,36.332110,-98.167826],[-2.205101,5.845806,-6.747133,-1.913326],[36.332110,-6.747133,19.785658,5.357546],[-98.167826,-1.913326,5.357546,26.266260]],
}

def cov3(n):
    a=np.asarray(COV[n],float)*COV_SCALE
    return a[np.ix_([1,2,3],[1,2,3])]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--m07',required=True); ap.add_argument('--m01',required=True); ap.add_argument('--json',required=True); args=ap.parse_args()
    m07=json.loads(Path(args.m07).read_text()); m01=json.loads(Path(args.m01).read_text())
    dq={k:np.asarray(v,float) for k,v in m07['local_derivative_per_bin_at_lambda_0p025'].items()}
    de={}
    for k,v in m01['per_bin_local_derivative_at_1e-4'].items():
        de[k]=np.asarray([v['dAP_depsilon'],v['dgrowth_depsilon'],0.0],float)
    Fqq=Fee=Fqe=0.0; per={}
    for n in USE:
        C=cov3(n)
        fq=float(dq[n]@np.linalg.solve(C,dq[n])); fe=float(de[n]@np.linalg.solve(C,de[n])); fqe=float(dq[n]@np.linalg.solve(C,de[n]))
        Fqq+=fq; Fee+=fe; Fqe+=fqe; per[n]={'Fqq':fq,'Fee':fe,'Fqe':fqe}
    cos=Fqe/math.sqrt(Fqq*Fee); angle=math.degrees(math.acos(min(1,max(-1,abs(cos)))))
    Fprof=Fqq-Fqe*Fqe/Fee
    sigma_un=1/math.sqrt(Fqq); sigma_prof=1/math.sqrt(Fprof)
    out={
      'schema':'KMDSB.W03.M07.B7.ShapeFitC1Profile.v0.1',
      'scope':'same corrected DESI DR1 ShapeFit AP+growth+shape covariance as M01/M07 B5; local optimistic unmarginalized except profiling C1 epsilon amplitude',
      'Fqq':Fqq,'Fee':Fee,'Fqe':Fqe,
      'whitened_cosine_q_vs_epsilon':cos,
      'whitened_acute_angle_deg':angle,
      'profiled_Fq_given_C1_epsilon':Fprof,
      'sigma_q_unprofiled':sigma_un,
      'sigma_q_profiled_over_C1':sigma_prof,
      'sigma_degradation_factor':sigma_prof/sigma_un,
      'best_fit_C1_epsilon_per_unit_q':Fqe/Fee,
      'whitened_orthogonal_residual_fraction':math.sqrt(Fprof/Fqq),
      'largest_tested_q':0.09,
      'largest_tested_q_profiled_significance_sigma':0.09/sigma_prof,
      'per_bin':per,
      'classification':'NONIDENTIFIABLE_AFTER_C1_PROFILING_IN_FROZEN_SHAPEFIT_CONTROL',
      'interpretation':{
        'supported':'M07 and C1 are not collinear after ShapeFit whitening, but the absolute M07 information is extremely small and becomes weaker after profiling the nearest C1 amplitude.',
        'not_supported':['observational mechanism discrimination','physical falsification of M07 or C1','full DESI likelihood conclusion','universal statement for all quintessence potentials']
      }
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
