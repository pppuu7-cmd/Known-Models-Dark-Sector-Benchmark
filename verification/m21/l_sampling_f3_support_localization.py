#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
BANDS=[(2,30),(31,200),(201,800),(801,1500),(1501,2500)]
CHANNELS={'TT':1,'EE':2,'TE':3}
CASES=('f2','f3','f4')
def load(p:Path):
 rows=[]
 for ln in p.read_text(errors='replace').splitlines():
  s=ln.strip()
  if not s or s.startswith('#'): continue
  try: row=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError: continue
  if row and all(math.isfinite(x) for x in row): rows.append(row)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<3 or a.shape[1]<4: raise RuntimeError(f'invalid Cl table {p}: {a.shape}')
 return a
def one(root:Path,case:str):
 direct=root/'output'/f'{case}_cl.dat'; matches=[direct] if direct.exists() else sorted((root/'output').glob(f'{case}_*_cl.dat'))
 if len(matches)!=1: raise RuntimeError(f'expected one Cl file for {case} in {root}: {matches}')
 return load(matches[0])
def response(root:Path):
 ref=one(root,'ref'); out={'channels':{}}
 cases={c:one(root,c) for c in CASES}
 for c,a in cases.items():
  if not np.array_equal(a[:,0],ref[:,0]): raise RuntimeError(f'ell grid mismatch {c}')
 for ch,col in CHANNELS.items():
  r=ref[:,col]; norm=max(float(np.linalg.norm(r)),1e-300); ds={c:cases[c][:,col]-r for c in CASES}; rr={c:float(np.linalg.norm(ds[c])/norm) for c in CASES}
  e=float(rr['f3']/max(rr['f2'],rr['f4'],1e-300)); den=float(np.sum(ds['f3']**2)); bands={}
  for lo,hi in BANDS:
   m=(ref[:,0]>=lo)&(ref[:,0]<=hi); bands[f'{lo}-{hi}']=float(np.sum(ds['f3'][m]**2)/den) if den>0 else 0.0
  idx=np.argsort(ds['f3']**2)[-10:][::-1]
  top=[{'ell':int(ref[i,0]),'delta':float(ds['f3'][i]),'abs_fractional':float(abs(ds['f3'][i])/max(abs(r[i]),1e-300))} for i in idx]
  out['channels'][ch]={'R2':rr,'excursion_factor':e,'f3_squared_response_band_fraction':bands,'f3_top10_ell_contributors':top}
 return out
def cross(a:Path,b:Path):
 ra,rb=one(a,'ref'),one(b,'ref'); out={}
 if not np.array_equal(ra[:,0],rb[:,0]): raise RuntimeError('reference ell grids differ')
 for ch,col in CHANNELS.items():
  out[ch]={}
  for c in CASES:
   aa=one(a,c); bb=one(b,c); va=aa[:,col]-ra[:,col]; vb=bb[:,col]-rb[:,col]
   out[ch][c]={
    'response_vector_change_over_R':float(np.linalg.norm(vb-va)/max(float(np.linalg.norm(va)),1e-300)),
    'T2_over_R_response_norm':float(np.linalg.norm(vb)/max(float(np.linalg.norm(va)),1e-300))
   }
 return out
def main(r,t2,out):
 result={'schema':'KMDSB.W04.M21.LSamplingF3SupportLocalization.v0.1','date':'2026-09-14','parent_run':34879864684,'parent_R_artifact':10363039828,'parent_T2_artifact':10363566453,'classification':'M21_L_SAMPLING_F3_SUPPORT_LOCALIZED_POST_TERMINAL_DESCRIPTIVE','R':response(r),'T2':response(t2),'R_to_T2_response_change':cross(r,t2),'K1_promoted':False,'physical_falsification':False,'interpretation_ceiling':'Post-terminal descriptive localization only; no threshold, convergence promotion, code-defect claim, or K1/K3/K4 promotion.'}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'classification':result['classification'],'R_E':{k:v['excursion_factor'] for k,v in result['R']['channels'].items()},'T2_E':{k:v['excursion_factor'] for k,v in result['T2']['channels'].items()},'f3_T2_over_R':{k:result['R_to_T2_response_change'][k]['f3']['T2_over_R_response_norm'] for k in CHANNELS}},indent=2,sort_keys=True))
if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: l_sampling_f3_support_localization.py R_DIR T2_DIR OUT.json')
 main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
