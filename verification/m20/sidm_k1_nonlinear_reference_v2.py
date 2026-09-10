#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np

PIN='e17d3664dac677b604fd4ff02fb2af105a6937fa'
PREREG='protocol/W04_M20_SIDM_K1_NONLINEAR_REFERENCE_V2_PREREGISTRATION_v0.1.md'
SIGMAS=[10.0,3.0,1.0,0.3,0.1,0.03,0.01,0.003]
W=24.33
OUT=['ma200','z_acc','rsCDM_acc','rhosCDM_acc','rmaxCDM_acc','VmaxCDM_acc','rsSIDM_acc','rhosSIDM_acc','rcSIDM_acc','rmaxSIDM_acc','VmaxSIDM_acc','m_z0','rsCDM_z0','rhosCDM_z0','rmaxCDM_z0','VmaxCDM_z0','rsSIDM_z0','rhosSIDM_z0','rcSIDM_z0','rmaxSIDM_z0','VmaxSIDM_z0','ctCDM_z0','tt_ratio','weightCDM','weightSIDM','surviveCDM','surviveSIDM']
STRUCT={'Vmax_z0':('VmaxSIDM_z0','VmaxCDM_z0'),'rmax_z0':('rmaxSIDM_z0','rmaxCDM_z0'),'rs_z0':('rsSIDM_z0','rsCDM_z0'),'rhos_z0':('rhosSIDM_z0','rhosCDM_z0')}
ARGS=dict(M0=1.e12,redshift=0.,M0_at_redshift=True,dz=0.2,N_herm=3,zmax=4.,logmamin=9,N_ma=30)

def run(mod,s):
 r=mod.subhalo_properties(sigma0_m=float(s),w=W).subhalo_properties_calc(**ARGS)
 if len(r)!=len(OUT): raise RuntimeError('output contract')
 return {k:np.asarray(v) for k,v in zip(OUT,r)}

def sym(a,b):
 a=np.asarray(a,float);b=np.asarray(b,float)
 if a.shape!=b.shape or not(np.all(np.isfinite(a)) and np.all(np.isfinite(b))): raise RuntimeError('structural finite/shape contract')
 floor=1e-14*max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300)
 r=2*(a-b)/(np.abs(a)+np.abs(b)+floor); q=np.abs(r).ravel()
 return {'median_abs':float(np.median(q)),'rms':float(np.sqrt(np.mean(r*r))),'p95_abs':float(np.percentile(q,95)),'max_abs':float(np.max(q)),'n':int(q.size)}

def pos(a):
 q=np.abs(np.asarray(a,float)).ravel()
 if not np.all(np.isfinite(q)): raise RuntimeError('core finite contract')
 return {'median':float(np.median(q)),'rms':float(np.sqrt(np.mean(q*q))),'p95':float(np.percentile(q,95)),'max':float(np.max(q)),'n':int(q.size)}

def judge(vals,core=False):
 vals=np.asarray(vals,float); tail=vals[-4:]; sig=np.asarray(SIGMAS[-4:],float)
 p=None if np.any(tail<=0) else float(np.polyfit(np.log(sig),np.log(tail),1)[0])
 mono=bool(np.all(vals[1:]<=vals[:-1]*1.02)); dec=bool(vals[-1]<vals[0]); exp=bool(p is not None and p>0)
 advance=bool(vals[-1] <= 0.25*vals[SIGMAS.index(1.0)])
 core_ok=(not core) or bool(p is not None and 0.25<=p<=0.75)
 return {'p95_sequence':vals.tolist(),'fit_smallest4':{'p':p,'valid':p is not None},'monotonic_with_2pct_slack':mono,'smallest_lower_than_largest':dec,'smallest_le_quarter_of_sigma1':advance,'core_source_asymptote_consistent':core_ok if core else None,'pass':bool(mono and dec and exp and advance and core_ok)}

def main(provider,out):
 sys.path.insert(0,str(provider.resolve())); import sashimi_si
 ref=run(sashimi_si,0.0); mask=np.isfinite(ref['weightCDM'].astype(float))&(ref['weightCDM'].astype(float)>0)
 exact={}; ident=0.
 for k,(s,c) in STRUCT.items(): exact[k]=sym(ref[s][mask],ref[c][mask]); ident=max(ident,exact[k]['max_abs'])
 cr0=np.abs(ref['rcSIDM_z0'][mask].astype(float))/np.maximum(np.abs(ref['rsCDM_z0'][mask].astype(float)),1e-300); exact['core_ratio']=pos(cr0)
 exact_ok=bool(ident<=1e-10 and exact['core_ratio']['max']<=1e-10)
 seq={k:[] for k in list(STRUCT)+['core_ratio']}; pop=[]
 for sigma in SIGMAS:
  c=run(sashimi_si,sigma)
  for k in OUT:
   if np.asarray(c[k]).shape!=np.asarray(ref[k]).shape: raise RuntimeError(f'{sigma} shape {k}')
  for k,(s,rc) in STRUCT.items(): seq[k].append(sym(c[s][mask],ref[rc][mask])['p95_abs'])
  core=np.abs(c['rcSIDM_z0'][mask].astype(float))/np.maximum(np.abs(ref['rsCDM_z0'][mask].astype(float)),1e-300); seq['core_ratio'].append(pos(core)['p95'])
  ws=sym(c['weightSIDM'][mask].astype(float),ref['weightCDM'][mask].astype(float)); sm=float(np.mean(np.asarray(c['surviveSIDM'][mask]).astype(bool)!=np.asarray(ref['surviveCDM'][mask]).astype(bool)))
  pop.append({'sigma0_m':sigma,'weight':ws,'survival_mismatch_fraction':sm})
 blocks={k:judge(v,k=='core_ratio') for k,v in seq.items()}; allpass=exact_ok and all(v['pass'] for v in blocks.values())
 res={'schema':'KMDSB.M20.SIDM.K1NonlinearReference.v2','provider':'shinichiroando/sashimi-si','pin':PIN,'preregistration':PREREG,'w_km_s':W,'sigma0_m_cm2_g':SIGMAS,'catalog_args':ARGS,'reference_support_n':int(mask.sum()),'exact_zero':exact,'exact_zero_identity_pass':exact_ok,'blocks':blocks,'population_diagnostics':pop,'failing_blocks':[k for k,v in blocks.items() if not v['pass']],'K1_reference_limit':'PASS_WITH_SCOPE_NONLINEAR_HALO_EXACT_CDM_LIMIT' if allpass else 'NOT_PROMOTED','K2_physical_geometry':'ONE_SIDED_SIGMA_GE_0_NO_SIGN_QUOTIENT','K4_promoted':False,'physical_falsification':False,'classification':'M20_K1_V2_NONLINEAR_REFERENCE_LIMIT_PASS_WITH_SCOPE' if allpass else 'M20_K1_V2_NONLINEAR_REFERENCE_LIMIT_NOT_ESTABLISHED'}
 out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
if __name__=='__main__': main(Path(sys.argv[1]),Path(sys.argv[2]))
