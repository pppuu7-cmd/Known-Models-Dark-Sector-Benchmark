#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
from k4_numerical_axis_localization import BASE, profile, STRUCT, SIGMAS

PIN='e17d3664dac677b604fd4ff02fb2af105a6937fa'
PREREG='protocol/W04_M20_K4_HERMITE_CONVERGENCE_PREREGISTRATION_v0.1.md'
ORDERS=[5,7,9]
OBS=list(STRUCT)+['core_ratio']

def compare(a,b):
    cells=[]; ds=[]
    for s in map(str,SIGMAS[1:]):
        for k in OBS:
            x=float(a['responses'][s][k]); y=float(b['responses'][s][k])
            d=float(2*abs(y-x)/(abs(y)+abs(x)+1e-30)); ds.append(d)
            cells.append({'sigma0_m':float(s),'observable':k,'a':x,'b':y,'D':d})
    return {'max':float(max(ds)),'median':float(np.median(ds)),'cells':cells}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('provider',type=Path); ap.add_argument('out',type=Path); a=ap.parse_args()
    sys.path.insert(0,str(a.provider.resolve())); import sashimi_si
    out={'schema':'KMDSB.M20.K4HermiteConvergence.v1','model_id':'M20','family_id':'F20','provider_commit':PIN,'preregistration':PREREG,'orders':ORDERS,'diagnostic_only':True,'K4_promoted':False,'physical_falsification':False,'scientific_fail':False}
    try:
        ps={}
        for n in ORDERS:
            args=dict(BASE); args['N_herm']=n; ps[str(n)]=profile(sashimi_si,args)
        integrity=all(p['exact_zero_identity_pass'] for p in ps.values())
        d57=compare(ps['5'],ps['7']); d79=compare(ps['7'],ps['9'])
        if not integrity: cls='M20_K4_HERMITE_CONVERGENCE_BLOCKED'
        elif d79['max']<=0.10 and d79['max']<d57['max']: cls='M20_K4_HERMITE_CONVERGENCE_CANDIDATE_DIAGNOSTIC'
        elif d79['max']<d57['max']: cls='M20_K4_HERMITE_IMPROVING_NOT_CONVERGED_DIAGNOSTIC'
        else: cls='M20_K4_HERMITE_NONCONVERGENCE_PERSISTS_DIAGNOSTIC'
        out.update({'profiles':ps,'D_5to7':d57,'D_7to9':d79,'classification':cls})
    except Exception as e:
        out.update({'classification':'M20_K4_HERMITE_CONVERGENCE_BLOCKED','error':repr(e)})
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:out.get(k) for k in ['classification','D_5to7','D_7to9','K4_promoted','physical_falsification']},indent=2,sort_keys=True))

if __name__=='__main__': main()
