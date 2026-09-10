#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np

PREREG='protocol/W04_M21_DEFAULT_PRECISION_EXCURSION_DIAGNOSTIC_PREREGISTRATION_v0.1.md'
V1='models/mixed_cold_warm_dark_matter/M21_K1_REFERENCE_RESULT.json'
FRACS=[0.01,0.003,0.001]
CASES=['f2','f3','f4']

def load(p):
 rows=[]
 for line in p.read_text(errors='replace').splitlines():
  s=line.strip()
  if not s or s.startswith('#'): continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError: continue
  if r and all(math.isfinite(x) for x in r):rows.append(r)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<3:raise RuntimeError(f'invalid {p}')
 return a

def one(root,prefix,suffix):
 m=sorted(root.glob(f'{prefix}_*_{suffix}.dat'))
 if len(m)!=1: raise RuntimeError(f'{root} {prefix} {suffix}: {m}')
 return load(m[0])

def sym(a,b):
 scale=max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300); floor=1e-12*scale
 r=2*(a-b)/(np.abs(a)+np.abs(b)+floor);q=np.abs(r).ravel()
 return {'median_abs':float(np.median(q)),'rms':float(np.sqrt(np.mean(r*r))),'p95_abs':float(np.percentile(q,95)),'n':int(q.size)}

def cmb(model,ref,col):
 if not np.array_equal(model[:,0],ref[:,0]): raise RuntimeError('CMB ell grids differ')
 return sym(model[:,col],ref[:,col])

def pk(model,ref):
 x=model[:,0]; xr=ref[:,0]; lo=max(x.min(),xr.min());hi=min(x.max(),xr.max());mask=(x>=lo)&(x<=hi);x=x[mask];ym=model[mask,1]
 if np.any(xr<=0) or np.any(ref[:,1]<=0) or np.any(x<=0) or np.any(ym<=0): raise RuntimeError('nonpositive Pk')
 yr=np.exp(np.interp(np.log(x),np.log(xr),np.log(ref[:,1])))
 return sym(ym,yr)

def hubble(model,ref):
 x=model[:,0]; y=model[:,3]; xr=ref[:,0];yr0=ref[:,3]
 ir=np.argsort(xr); xr=xr[ir];yr0=yr0[ir]; im=np.argsort(x);x=x[im];y=y[im]
 lo=max(x.min(),xr.min());hi=min(x.max(),xr.max());mask=(x>=lo)&(x<=hi);x=x[mask];y=y[mask]
 yr=np.interp(x,xr,yr0)
 return sym(y,yr)

def profile(root):
 refcl=one(root,'ref','cl');refpk=one(root,'ref','pk');refbg=one(root,'ref','background')
 out={'points':{},'excursion_factors':{}}
 for case,f in zip(CASES,FRACS):
  cl=one(root,case,'cl');pkm=one(root,case,'pk');bg=one(root,case,'background')
  out['points'][case]={'fraction':f,'CMB_TT':cmb(cl,refcl,1),'CMB_EE':cmb(cl,refcl,2),'CMB_TE':cmb(cl,refcl,3),'Pk':pk(pkm,refpk),'H':hubble(bg,refbg)}
 for ch in ['CMB_TT','CMB_EE','CMB_TE']:
  r=[out['points'][c][ch]['p95_abs'] for c in CASES];out['excursion_factors'][ch]=float(r[1]/max(r[0],r[2],1e-300))
 return out

def main(p1,p2,out):
 v1=json.loads(Path(V1).read_text()); default={}
 for ch in ['CMB_TT','CMB_EE','CMB_TE']:
  pts=v1['blocks'][ch]['points']; r=[pts[i]['p95_abs'] for i in [2,3,4]]; default[ch]=float(r[1]/max(r[0],r[2],1e-300))
 default_max=max(default.values())
 profiles={'P1_cl_permille':profile(p1),'P2_cl_permille_plus_ncdm_tight':profile(p2)}
 suppressed=False; reduced=False
 for q in profiles.values():
  mx=max(q['excursion_factors'].values())
  if all(v<=3 for v in q['excursion_factors'].values()): cls='EXCURSION_SUPPRESSED';suppressed=True
  elif mx <= default_max/3: cls='EXCURSION_REDUCED';reduced=True
  else: cls='EXCURSION_PERSISTS'
  q['classification']=cls;q['max_CMB_excursion_factor']=mx
 if suppressed: overall='M21_DEFAULT_PRECISION_EXCURSION_LOCALIZED_TO_NUMERICAL_PROFILE'
 elif reduced: overall='M21_DEFAULT_PRECISION_EXCURSION_REDUCED_NOT_RESOLVED'
 else: overall='M21_DEFAULT_PRECISION_EXCURSION_PERSISTS'
 res={'schema':'KMDSB.M21.defaultPrecisionExcursionDiagnostic.v1','classification':overall,'preregistration':PREREG,'default_v1_excursion_factors':default,'default_v1_max_excursion_factor':default_max,'profiles':profiles,'K1_promoted':False,'physical_falsification':False}
 out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
