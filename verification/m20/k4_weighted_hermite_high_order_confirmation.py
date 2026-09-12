#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np

PIN='e17d3664dac677b604fd4ff02fb2af105a6937fa'
PREREG='protocol/W04_M20_K4_WEIGHTED_HERMITE_HIGH_ORDER_CONFIRMATION_PREREGISTRATION_v0.1.md'
W=24.33; ORDERS=[21,25,29]; SIGMAS=[0.0,1.0,0.1,0.01]
OUT=['ma200','z_acc','rsCDM_acc','rhosCDM_acc','rmaxCDM_acc','VmaxCDM_acc','rsSIDM_acc','rhosSIDM_acc','rcSIDM_acc','rmaxSIDM_acc','VmaxSIDM_acc','m_z0','rsCDM_z0','rhosCDM_z0','rmaxCDM_z0','VmaxCDM_z0','rsSIDM_z0','rhosSIDM_z0','rcSIDM_z0','rmaxSIDM_z0','VmaxSIDM_z0','ctCDM_z0','tt_ratio','weightCDM','weightSIDM','surviveCDM','surviveSIDM']
STRUCT={'Vmax_z0':('VmaxSIDM_z0','VmaxCDM_z0'),'rmax_z0':('rmaxSIDM_z0','rmaxCDM_z0'),'rs_z0':('rsSIDM_z0','rsCDM_z0'),'rhos_z0':('rhosSIDM_z0','rhosCDM_z0')}
BASE={'M0':1.e12,'redshift':0.,'M0_at_redshift':True,'dz':0.2,'zmax':4.,'logmamin':9,'N_ma':30}

def run(mod,s,n):
 a=dict(BASE);a['N_herm']=n;r=mod.subhalo_properties(sigma0_m=float(s),w=W).subhalo_properties_calc(**a)
 if len(r)!=len(OUT):raise RuntimeError('output contract')
 return {k:np.asarray(v) for k,v in zip(OUT,r)}
def asym(a,b):
 a=np.asarray(a,float);b=np.asarray(b,float);floor=1e-14*max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300)
 q=np.abs(2*(a-b)/(np.abs(a)+np.abs(b)+floor)).ravel()
 if not np.all(np.isfinite(q)):raise RuntimeError('nonfinite response')
 return q
def wq(x,w,q=.95):
 x=np.asarray(x,float).ravel();w=np.asarray(w,float).ravel();m=np.isfinite(x)&np.isfinite(w)&(w>0);x=x[m];w=w[m]
 if x.size==0 or w.sum()<=0:raise RuntimeError('bad weight support')
 i=np.argsort(x);x=x[i];w=w[i];return float(np.interp(q,np.cumsum(w)/np.sum(w),x))
def profile(mod,n):
 ref=run(mod,0,n);rw=np.asarray(ref['weightCDM'],float).ravel();mask=np.isfinite(rw)&(rw>0);w=rw[mask]
 if not np.any(mask):raise RuntimeError('empty support')
 ident=0.0
 for s,c in STRUCT.values():ident=max(ident,float(np.max(asym(np.asarray(ref[s])[mask],np.asarray(ref[c])[mask]))))
 core0=np.abs(np.asarray(ref['rcSIDM_z0'],float)[mask])/np.maximum(np.abs(np.asarray(ref['rsCDM_z0'],float)[mask]),1e-300);ident=max(ident,float(np.max(core0)))
 resp={}
 for sig in SIGMAS[1:]:
  cur=run(mod,sig,n)
  for k in OUT:
   if np.asarray(cur[k]).shape!=np.asarray(ref[k]).shape:raise RuntimeError(f'shape {n}/{sig}/{k}')
  cell={}
  for name,(s,c) in STRUCT.items():cell[name]=wq(asym(np.asarray(cur[s])[mask],np.asarray(ref[c])[mask]),w)
  core=np.abs(np.asarray(cur['rcSIDM_z0'],float)[mask])/np.maximum(np.abs(np.asarray(ref['rsCDM_z0'],float)[mask]),1e-300);cell['core_ratio']=wq(core,w);resp[str(sig)]=cell
 return {'support_n':int(mask.sum()),'reference_weight_sum':float(w.sum()),'exact_zero_identity_max':ident,'exact_zero_identity_pass':bool(ident<=1e-10),'responses':resp}
def d(a,b):return float(2*abs(a-b)/(abs(a)+abs(b)+1e-30))
def cmp(a,b):
 cells=[]
 for s in map(str,SIGMAS[1:]):
  for k in list(STRUCT)+['core_ratio']:
   x=float(a['responses'][s][k]);y=float(b['responses'][s][k]);cells.append({'sigma0_m':float(s),'observable':k,'a':x,'b':y,'D':d(x,y)})
 ds=[c['D'] for c in cells];return {'max':float(max(ds)),'median':float(np.median(ds)),'cells':cells}
def main(provider,outp):
 sys.path.insert(0,str(provider.resolve()));import sashimi_si
 out={'schema':'KMDSB.M20.K4WeightedHermiteHighOrderConfirmation.v1','model_id':'M20','family_id':'F20','provider_commit':PIN,'preregistration':PREREG,'orders':ORDERS,'K4_promoted':False,'scientific_fail':False,'physical_falsification':False,'diagnostic_only':True}
 try:
  p={str(n):profile(sashimi_si,n) for n in ORDERS};out['profiles']=p
  if not all(v['exact_zero_identity_pass'] for v in p.values()):raise RuntimeError('zero identity')
  a=cmp(p['21'],p['25']);b=cmp(p['25'],p['29']);out['weighted_D_21to25']=a;out['weighted_D_25to29']=b
  if a['max']<=.10 and b['max']<=.10 and b['max']<=1.05*a['max']:cls='M20_K4_WEIGHTED_HIGH_ORDER_CONFIRMATION_PASS_DIAGNOSTIC'
  elif a['max']<=.10 and b['max']<=.10:cls='M20_K4_WEIGHTED_HIGH_ORDER_LOW_AMPLITUDE_NONMONOTONE_DIAGNOSTIC'
  else:cls='M20_K4_WEIGHTED_HIGH_ORDER_NONCONVERGENCE_PERSISTS_DIAGNOSTIC'
  out['classification']=cls
 except Exception as e:out['classification']='M20_K4_WEIGHTED_HIGH_ORDER_EXECUTION_OR_INTEGRITY_BLOCKED';out['error']=repr(e)
 outp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]))
