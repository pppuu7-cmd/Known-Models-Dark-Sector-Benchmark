#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
PIN='e17d3664dac677b604fd4ff02fb2af105a6937fa'
PREREG='protocol/W04_M20_K4_WEIGHTED_GRID_AXES_PREREGISTRATION_v0.1.md'
W=24.33; SIGMAS=[0.0,1.0,0.1,0.01]
OUT=['ma200','z_acc','rsCDM_acc','rhosCDM_acc','rmaxCDM_acc','VmaxCDM_acc','rsSIDM_acc','rhosSIDM_acc','rcSIDM_acc','rmaxSIDM_acc','VmaxSIDM_acc','m_z0','rsCDM_z0','rhosCDM_z0','rmaxCDM_z0','VmaxCDM_z0','rsSIDM_z0','rhosSIDM_z0','rcSIDM_z0','rmaxSIDM_z0','VmaxSIDM_z0','ctCDM_z0','tt_ratio','weightCDM','weightSIDM','surviveCDM','surviveSIDM']
STRUCT={'Vmax_z0':('VmaxSIDM_z0','VmaxCDM_z0'),'rmax_z0':('rmaxSIDM_z0','rmaxCDM_z0'),'rs_z0':('rsSIDM_z0','rsCDM_z0'),'rhos_z0':('rhosSIDM_z0','rhosCDM_z0')}
BASE={'M0':1.e12,'redshift':0.,'M0_at_redshift':True,'zmax':4.,'logmamin':9,'N_herm':25}
AXES={
 'mass': [('N_ma30',{'N_ma':30,'dz':0.2}),('N_ma60',{'N_ma':60,'dz':0.2}),('N_ma120',{'N_ma':120,'dz':0.2})],
 'redshift': [('dz02',{'N_ma':30,'dz':0.2}),('dz01',{'N_ma':30,'dz':0.1}),('dz005',{'N_ma':30,'dz':0.05})],
}
def run(mod,s,args):
 r=mod.subhalo_properties(sigma0_m=float(s),w=W).subhalo_properties_calc(**args)
 if len(r)!=len(OUT):raise RuntimeError('output contract')
 return {k:np.asarray(v) for k,v in zip(OUT,r)}
def asym(a,b):
 a=np.asarray(a,float);b=np.asarray(b,float)
 if a.shape!=b.shape or not(np.all(np.isfinite(a)) and np.all(np.isfinite(b))):raise RuntimeError('finite/shape response')
 floor=1e-14*max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300)
 return np.abs(2*(a-b)/(np.abs(a)+np.abs(b)+floor)).ravel()
def wq(x,w,q=.95):
 x=np.asarray(x,float).ravel();w=np.asarray(w,float).ravel();m=np.isfinite(x)&np.isfinite(w)&(w>0);x=x[m];w=w[m]
 if x.size==0 or not np.isfinite(w.sum()) or w.sum()<=0:raise RuntimeError('bad weights')
 i=np.argsort(x);x=x[i];w=w[i];return float(np.interp(q,np.cumsum(w)/np.sum(w),x))
def profile(mod,args):
 ref=run(mod,0,args);rw=np.asarray(ref['weightCDM'],float).ravel();mask=np.isfinite(rw)&(rw>0);w=rw[mask]
 if not np.any(mask):raise RuntimeError('empty support')
 ident=0.0
 for s,c in STRUCT.values():ident=max(ident,float(np.max(asym(np.asarray(ref[s])[mask],np.asarray(ref[c])[mask]))))
 core0=np.abs(np.asarray(ref['rcSIDM_z0'],float)[mask])/np.maximum(np.abs(np.asarray(ref['rsCDM_z0'],float)[mask]),1e-300);ident=max(ident,float(np.max(core0)))
 resp={}
 for sig in SIGMAS[1:]:
  cur=run(mod,sig,args)
  for k in OUT:
   if np.asarray(cur[k]).shape!=np.asarray(ref[k]).shape:raise RuntimeError(f'shape {sig}/{k}')
  cell={}
  for name,(s,c) in STRUCT.items():cell[name]=wq(asym(np.asarray(cur[s])[mask],np.asarray(ref[c])[mask]),w)
  core=np.abs(np.asarray(cur['rcSIDM_z0'],float)[mask])/np.maximum(np.abs(np.asarray(ref['rsCDM_z0'],float)[mask]),1e-300);cell['core_ratio']=wq(core,w);resp[str(sig)]=cell
 return {'args':args,'support_n':int(mask.sum()),'reference_weight_sum':float(w.sum()),'exact_zero_identity_max':ident,'exact_zero_identity_pass':bool(ident<=1e-10),'responses':resp}
def d(a,b):return float(2*abs(a-b)/(abs(a)+abs(b)+1e-30))
def cmp(a,b):
 cells=[]
 for s in map(str,SIGMAS[1:]):
  for k in list(STRUCT)+['core_ratio']:
   x=float(a['responses'][s][k]);y=float(b['responses'][s][k]);cells.append({'sigma0_m':float(s),'observable':k,'a':x,'b':y,'D':d(x,y)})
 ds=[x['D'] for x in cells];return {'max':float(max(ds)),'median':float(np.median(ds)),'cells':cells}
def main(provider,axis,outp):
 sys.path.insert(0,str(provider.resolve()));import sashimi_si
 out={'schema':'KMDSB.M20.K4WeightedGridAxis.v1','model_id':'M20','family_id':'F20','axis':axis,'provider_commit':PIN,'preregistration':PREREG,'K4_promoted':False,'scientific_fail':False,'physical_falsification':False,'diagnostic_only':True}
 try:
  specs=AXES[axis];p={}
  for tag,ov in specs:
   a=dict(BASE);a.update(ov);p[tag]=profile(sashimi_si,a)
  out['profiles']=p;tags=[x[0] for x in specs]
  if not all(p[t]['exact_zero_identity_pass'] for t in tags):raise RuntimeError('zero identity')
  c1=cmp(p[tags[0]],p[tags[1]]);c2=cmp(p[tags[1]],p[tags[2]]);out['step1']=c1;out['step2']=c2
  pre='M20_K4_'+axis.upper()
  if c1['max']<=.10 and c2['max']<=.10 and c2['max']<=1.05*c1['max']:cls=pre+'_WEIGHTED_GRID_CONVERGENCE_CANDIDATE_DIAGNOSTIC'
  elif c1['max']<=.10 and c2['max']<=.10:cls=pre+'_WEIGHTED_GRID_LOW_AMPLITUDE_NONMONOTONE_DIAGNOSTIC'
  elif c2['max']<c1['max']:cls=pre+'_WEIGHTED_GRID_IMPROVING_NOT_CONVERGED_DIAGNOSTIC'
  else:cls=pre+'_WEIGHTED_GRID_NONCONVERGENCE_PERSISTS_DIAGNOSTIC'
  out['classification']=cls
 except Exception as e:out['classification']='M20_K4_'+axis.upper()+'_WEIGHTED_GRID_EXECUTION_OR_INTEGRITY_BLOCKED';out['error']=repr(e)
 outp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('provider',type=Path);ap.add_argument('axis',choices=sorted(AXES));ap.add_argument('out',type=Path);a=ap.parse_args();main(a.provider,a.axis,a.out)
