#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
BANDS=[(2,30),(31,200),(201,800),(801,1500),(1501,2500)]
CH={'TT':1,'EE':2,'TE':3}; CASES=('f2','f3','f4')
def load(root:Path,c:str):
 p=root/'output'/f'{c}_00_cl.dat'; rows=[]
 for ln in p.read_text(errors='replace').splitlines():
  s=ln.strip()
  if not s or s.startswith('#'): continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError:continue
  if len(r)>=4 and all(math.isfinite(x) for x in r):rows.append(r)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<100 or a.shape[1]<4: raise RuntimeError(f'invalid {p}: {a.shape}')
 return a
def llist(logstep,linstep,lmax=2500):
 out=[2]; cur=2; inc=max(int(cur*(logstep-1.0)),1)
 while cur+inc<lmax and inc<linstep:
  cur+=inc; out.append(cur); inc=max(int(cur*(logstep-1.0)),1)
 inc=linstep
 while cur+inc<=lmax: cur+=inc; out.append(cur)
 if out[-1]!=lmax: out.append(lmax)
 return out
def main(t3:Path,t4:Path,out:Path):
 A={tag:{c:load(root,c) for c in ('ref',)+CASES} for tag,root in [('T3',t3),('T4',t4)]}
 result={'schema':'KMDSB.W04.M21.LTailT3T4PhaseLocalization.v0.1','date':'2026-09-14','parent_run':34883823728,'T3_artifact':10364077936,'T4_artifact':10364289137,'classification':'M21_LTAIL_T3_T4_PHASE_LOCALIZED_POST_TERMINAL_DESCRIPTIVE','channels':{},'grid_signatures':{},'K1_promoted':False,'physical_falsification':False,'interpretation_ceiling':'Post-terminal descriptive localization only; no PASS/FAIL, convergence promotion, code-defect claim, or physical M21 conclusion.'}
 for name,ls,li in [('T3',1.0075,12),('T4',1.005,10)]:
  L=llist(ls,li); result['grid_signatures'][name]={'l_logstep':ls,'l_linstep':li,'node_count':len(L),'contains_l400':400 in L,'contains_l2499':2499 in L,'nodes_394_406':[x for x in L if 394<=x<=406],'tail_nodes':L[-8:]}
 for ch,col in CH.items():
  rr={}
  for tag in ('T3','T4'):
   ref=A[tag]['ref']; d={c:A[tag][c][:,col]-ref[:,col] for c in CASES}; norm=max(float(np.linalg.norm(ref[:,col])),1e-300)
   rr[tag]={'R2':{c:float(np.linalg.norm(d[c])/norm) for c in CASES}}
   rr[tag]['EE_or_channel_excursion_factor']=rr[tag]['R2']['f3']/max(rr[tag]['R2']['f2'],rr[tag]['R2']['f4'],1e-300)
  cross={}
  for c in CASES:
   v3=A['T3'][c][:,col]-A['T3']['ref'][:,col]; v4=A['T4'][c][:,col]-A['T4']['ref'][:,col]; dv=v4-v3; den=max(float(np.linalg.norm(v3)),1e-300); s=float(np.sum(dv*dv)); ell=A['T3']['ref'][:,0]
   cross[c]={'T4_over_T3_response_norm':float(np.linalg.norm(v4)/den),'delta_over_T3_response_norm':float(np.linalg.norm(dv)/den),'delta_squared_band_fraction':{f'{lo}-{hi}':float(np.sum(dv[(ell>=lo)&(ell<=hi)]**2)/s) if s>0 else 0.0 for lo,hi in BANDS},'delta_top12_ell':[int(ell[i]) for i in np.argsort(dv*dv)[-12:][::-1]]}
  result['channels'][ch]={'profiles':rr,'T3_to_T4_response_change':cross}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'classification':result['classification'],'grid_signatures':result['grid_signatures'],'EE_f3':result['channels']['EE']['T3_to_T4_response_change']['f3']},indent=2,sort_keys=True))
if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: ltail_t3_t4_phase_localization.py T3_DIR T4_DIR OUT.json')
 main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
