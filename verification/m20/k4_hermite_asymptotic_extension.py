#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
from k4_numerical_axis_localization import BASE, profile, STRUCT, SIGMAS
PIN='e17d3664dac677b604fd4ff02fb2af105a6937fa'
PREREG='protocol/W04_M20_K4_HERMITE_ASYMPTOTIC_EXTENSION_PREREGISTRATION_v0.1.md'
ORDERS=[13,17,21]; OBS=list(STRUCT)+['core_ratio']
def cmp(a,b):
 ds=[];cells=[]
 for s in map(str,SIGMAS[1:]):
  for k in OBS:
   x=float(a['responses'][s][k]);y=float(b['responses'][s][k]);d=float(2*abs(y-x)/(abs(y)+abs(x)+1e-30));ds.append(d);cells.append({'sigma0_m':float(s),'observable':k,'a':x,'b':y,'D':d})
 return {'max':float(max(ds)),'median':float(np.median(ds)),'cells':cells}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('provider',type=Path);ap.add_argument('out',type=Path);a=ap.parse_args();sys.path.insert(0,str(a.provider.resolve()));import sashimi_si
 out={'schema':'KMDSB.M20.K4HermiteAsymptotic.v1','model_id':'M20','family_id':'F20','provider_commit':PIN,'preregistration':PREREG,'orders':ORDERS,'diagnostic_only':True,'K4_promoted':False,'physical_falsification':False,'scientific_fail':False}
 try:
  ps={}
  for n in ORDERS:
   args=dict(BASE);args['N_herm']=n;ps[str(n)]=profile(sashimi_si,args)
  integ=all(p['exact_zero_identity_pass'] for p in ps.values());d1317=cmp(ps['13'],ps['17']);d1721=cmp(ps['17'],ps['21'])
  if not integ:cls='M20_K4_HERMITE_ASYMPTOTIC_BLOCKED'
  elif d1721['max']<=0.10 and d1721['max']<d1317['max']:cls='M20_K4_HERMITE_ASYMPTOTIC_CONVERGENCE_CANDIDATE_DIAGNOSTIC'
  elif d1721['max']<d1317['max']:cls='M20_K4_HERMITE_ASYMPTOTIC_IMPROVING_NOT_CONVERGED_DIAGNOSTIC'
  else:cls='M20_K4_HERMITE_ASYMPTOTIC_STALL_OR_NONCONVERGENCE_DIAGNOSTIC'
  out.update({'profiles':ps,'D_13to17':d1317,'D_17to21':d1721,'classification':cls})
 except Exception as e:out.update({'classification':'M20_K4_HERMITE_ASYMPTOTIC_BLOCKED','error':repr(e)})
 a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out.get(k) for k in ['classification','D_13to17','D_17to21']},indent=2,sort_keys=True))
if __name__=='__main__':main()
