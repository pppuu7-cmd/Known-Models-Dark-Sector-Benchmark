#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np

PIN='e17d3664dac677b604fd4ff02fb2af105a6937fa'
PREREG='protocol/W04_M20_K2_SIGMA_W_LOCAL_GEOMETRY_PREREGISTRATION_v0.1.md'
BASE_SIGMA=0.1; BASE_W=24.33; HS=[0.10,0.05]
OUT=['ma200','z_acc','rsCDM_acc','rhosCDM_acc','rmaxCDM_acc','VmaxCDM_acc','rsSIDM_acc','rhosSIDM_acc','rcSIDM_acc','rmaxSIDM_acc','VmaxSIDM_acc','m_z0','rsCDM_z0','rhosCDM_z0','rmaxCDM_z0','VmaxCDM_z0','rsSIDM_z0','rhosSIDM_z0','rcSIDM_z0','rmaxSIDM_z0','VmaxSIDM_z0','ctCDM_z0','tt_ratio','weightCDM','weightSIDM','surviveCDM','surviveSIDM']
STRUCT={'Vmax_z0':('VmaxSIDM_z0','VmaxCDM_z0'),'rmax_z0':('rmaxSIDM_z0','rmaxCDM_z0'),'rs_z0':('rsSIDM_z0','rsCDM_z0'),'rhos_z0':('rhosSIDM_z0','rhosCDM_z0')}
ARGS={'M0':1.e12,'redshift':0.,'M0_at_redshift':True,'zmax':4.,'logmamin':9,'N_herm':25,'N_ma':120,'dz':0.05}
NAMES=list(STRUCT)+['core_ratio']

def run(mod,sigma,w):
 r=mod.subhalo_properties(sigma0_m=float(sigma),w=float(w)).subhalo_properties_calc(**ARGS)
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
def response(cur,ref,mask,w):
 cell={}
 for name,(s,c) in STRUCT.items():cell[name]=wq(asym(np.asarray(cur[s])[mask],np.asarray(ref[c])[mask]),w)
 core=np.abs(np.asarray(cur['rcSIDM_z0'],float)[mask])/np.maximum(np.abs(np.asarray(ref['rsCDM_z0'],float)[mask]),1e-300)
 cell['core_ratio']=wq(core,w)
 v=np.asarray([cell[k] for k in NAMES],float)
 if not np.all(np.isfinite(v)) or np.any(v<=0):raise RuntimeError(f'nonpositive response {v}')
 return cell,v
def cosine(a,b):
 na=float(np.linalg.norm(a));nb=float(np.linalg.norm(b))
 return float(np.dot(a,b)/(na*nb)) if na>0 and nb>0 else float('nan')
def deriv(vp,vm,h):return (np.log(vp)-np.log(vm))/(2*h)
def conv(dc,df):
 nc=float(np.linalg.norm(dc));nf=float(np.linalg.norm(df));co=cosine(dc,df);mis=abs(nc-nf)/max(nf,1e-300)
 return {'coarse':dc.tolist(),'fine':df.tolist(),'coarse_norm':nc,'fine_norm':nf,'signed_cosine':co,'relative_norm_mismatch':float(mis),'pass':bool(np.isfinite(co) and co>=.995 and mis<=.10 and nc>1e-6 and nf>1e-6)}
def main(provider,outp):
 sys.path.insert(0,str(provider.resolve()));import sashimi_si
 out={'schema':'KMDSB.M20.K2SigmaWLocalGeometry.v1','model_id':'M20','family_id':'F20','provider_commit':PIN,'preregistration':PREREG,'base_sigma0_m':BASE_SIGMA,'base_w_km_s':BASE_W,'steps_log':HS,'response_names':NAMES,'numerics':ARGS,'K2_promoted':False,'K5_promoted':False,'scientific_fail':False,'physical_falsification':False,'diagnostic_only':True}
 try:
  ref=run(sashimi_si,0.0,BASE_W);rw=np.asarray(ref['weightCDM'],float).ravel();mask=np.isfinite(rw)&(rw>0);w=rw[mask]
  if not np.any(mask):raise RuntimeError('empty CDM weight support')
  out['reference_support_n']=int(mask.sum());out['reference_weight_sum']=float(w.sum())
  vec={};cells={}
  for h in HS:
   tag=str(h)
   for par,sgn in [('sigma_plus',1),('sigma_minus',-1),('w_plus',1),('w_minus',-1)]:
    if par.startswith('sigma'):
     s=BASE_SIGMA*math.exp(sgn*h);wv=BASE_W
    else:
     s=BASE_SIGMA;wv=BASE_W*math.exp(sgn*h)
    cur=run(sashimi_si,s,wv)
    for k in OUT:
     if np.asarray(cur[k]).shape!=np.asarray(ref[k]).shape:raise RuntimeError(f'shape {tag}/{par}/{k}')
    c,v=response(cur,ref,mask,w);cells[f'{tag}:{par}']={'sigma0_m':s,'w':wv,'responses':c};vec[(tag,par)]=v
  out['points']=cells
  derivs={}
  for p in ['sigma','w']:
   dc=deriv(vec[('0.1',p+'_plus')],vec[('0.1',p+'_minus')],0.10)
   df=deriv(vec[('0.05',p+'_plus')],vec[('0.05',p+'_minus')],0.05)
   derivs[p]=conv(dc,df)
  out['tangent_convergence']=derivs
  a=np.asarray(derivs['sigma']['fine'],float);b=np.asarray(derivs['w']['fine'],float)
  c=max(-1.,min(1.,cosine(a,b)));angle=float(np.degrees(np.arccos(c)))
  A=np.column_stack([a/np.linalg.norm(a),b/np.linalg.norm(b)]);sv=np.linalg.svd(A,compute_uv=False);ratio=float(sv[-1]/sv[0])
  indep=bool(angle>=10.0 and ratio>=0.08)
  out['fine_local_independence']={'signed_cosine':c,'principal_angle_deg':angle,'normalized_column_singular_values':sv.tolist(),'s2_over_s1':ratio,'pass':indep}
  if derivs['sigma']['pass'] and derivs['w']['pass']:
   cls='M20_K2_FINITE_BASE_LOCAL_RANK2_SIGMA_W_DIAGNOSTIC' if indep else 'M20_K2_FINITE_BASE_SIGMA_W_LOCAL_DEGENERACY_DIAGNOSTIC'
  else:cls='M20_K2_FINITE_BASE_SIGMA_W_TANGENT_NOT_CONVERGED_DIAGNOSTIC'
  out['classification']=cls
 except Exception as e:
  out['classification']='M20_K2_FINITE_BASE_SIGMA_W_EXECUTION_OR_INTEGRITY_BLOCKED';out['error']=repr(e)
 outp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]))
