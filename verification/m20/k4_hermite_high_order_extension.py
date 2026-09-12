#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
from k4_numerical_axis_localization import BASE, profile, STRUCT, SIGMAS

PIN='e17d3664dac677b604fd4ff02fb2af105a6937fa'
PREREG='protocol/W04_M20_K4_HERMITE_HIGHER_ORDER_EXTENSION_PREREGISTRATION_v0.1.md'
ORDERS=[9,11,13]
OBS=list(STRUCT)+['core_ratio']

def compare(a,b):
    ds=[]; cells=[]
    for s in map(str,SIGMAS[1:]):
        for k in OBS:
            x=float(a['responses'][s][k]); y=float(b['responses'][s][k])
            d=float(2*abs(y-x)/(abs(y)+abs(x)+1e-30)); ds.append(d)
            cells.append({'sigma0_m':float(s),'observable':k,'a':x,'b':y,'D':d})
    return {'max':float(max(ds)),'median':float(np.median(ds)),'cells':cells}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('provider',type=Path); ap.add_argument('out',type=Path); a=ap.parse_args()
    sys.path.insert(0,str(a.provider.resolve())); import sashimi_si
    out={'schema':'KMDSB.M20.K4HermiteHighOrderExtension.v1','model_id':'M20','family_id':'F20','provider_commit':PIN,'preregistration':PREREG,'orders':ORDERS,'diagnostic_only':True,'K4_promoted':False,'physical_falsification':False,'scientific_fail':False}
    try:
        ps={}
        for n in ORDERS:
            args=dict(BASE); args['N_herm']=n; ps[str(n)]=profile(sashimi_si,args)
        integrity=all(p['exact_zero_identity_pass'] for p in ps.values())
        d911=compare(ps['9'],ps['11']); d1113=compare(ps['11'],ps['13'])
        if not integrity: cls='M20_K4_HERMITE_HIGH_ORDER_BLOCKED'
        elif d1113['max']<=0.10 and d1113['max']<d911['max']: cls='M20_K4_HERMITE_HIGH_ORDER_CONVERGENCE_CANDIDATE_DIAGNOSTIC'
        elif d1113['max']<d911['max']: cls='M20_K4_HERMITE_HIGH_ORDER_IMPROVING_NOT_CONVERGED_DIAGNOSTIC'
        else: cls='M20_K4_HERMITE_HIGH_ORDER_NONCONVERGENCE_PERSISTS_DIAGNOSTIC'
        out.update({'profiles':ps,'D_9to11':d911,'D_11to13':d1113,'classification':cls})
    except Exception as e:
        out.update({'classification':'M20_K4_HERMITE_HIGH_ORDER_BLOCKED','error':repr(e)})
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:out.get(k) for k in ['classification','D_9to11','D_11to13','K4_promoted','physical_falsification']},indent=2,sort_keys=True))

if __name__=='__main__': main()
