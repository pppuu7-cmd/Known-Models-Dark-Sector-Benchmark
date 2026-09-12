#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
PIN='d9a20bd0c7b7a6c8957410fd245ed06b30b915c1'
PREREG='protocol/W07_M35_K4_LOCAL_2D_PRECISION_PREREGISTRATION_v0.1.md'
POINTS=['base','gravity','Y']; PROFILES=['default','permille','reference']
def load(p):
 rows=[]
 for line in Path(p).read_text(errors='replace').splitlines():
  s=line.strip()
  if not s or s.startswith('#'):continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError:continue
  if r and all(math.isfinite(v) for v in r):rows.append(r)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<5 or a.shape[1]<2:raise RuntimeError(f'bad table {p}: {a.shape}')
 return a
def nl2(a,b):return float(np.linalg.norm(a-b)/max(float(np.linalg.norm(b)),1e-300))
def clm(a,b,col):
 ia={int(r[0]):r for r in a};ib={int(r[0]):r for r in b};ell=sorted(set(ia)&set(ib))
 if len(ell)<20:raise RuntimeError('common ell')
 return nl2(np.asarray([ia[e][col] for e in ell]),np.asarray([ib[e][col] for e in ell]))
def pkm(a,b):
 xa,ya=a[:,0],a[:,1];xb,yb=b[:,0],b[:,1];ia=np.argsort(xa);ib=np.argsort(xb);xa,ya=xa[ia],ya[ia];xb,yb=xb[ib],yb[ib]
 ma=(xa>0)&np.isfinite(ya);mb=(xb>0)&np.isfinite(yb);xa,ya=xa[ma],ya[ma];xb,yb=xb[mb],yb[mb]
 lo=max(xa.min(),xb.min());hi=min(xa.max(),xb.max());m=(xa>=lo)&(xa<=hi);x=xa[m];y=ya[m]
 if x.size<20:raise RuntimeError('common k')
 return nl2(y,np.interp(np.log(x),np.log(xb),yb))
def gate(c,f):return bool(f<=1e-4 and (f<=0.5*c or (c<=1e-8 and f<=1e-8)))
def main(base,statusp,outp):
 st=json.loads(Path(statusp).read_text());out={'schema':'KMDSB.M35.K4Local2DPrecision.v1','model_id':'M35','family_id':'F35','provider_commit':PIN,'preregistration':PREREG,'status':st,'physical_falsification':False}
 try:
  needed=[f'{p}_{q}' for p in POINTS for q in PROFILES]
  if st.get('build')!=0 or any(st.get(k)!=0 for k in needed):raise RuntimeError('provider/profile execution blocked')
  res={}
  for point in POINTS:
   t={q:(load(Path(base)/f'{point}_{q}_cl.dat'),load(Path(base)/f'{point}_{q}_pk.dat')) for q in PROFILES};blocks={}
   for name,col in [('TT',1),('EE',2),('TE',3)]:
    c=clm(t['default'][0],t['permille'][0],col);f=clm(t['permille'][0],t['reference'][0],col);blocks[name]={'R_coarse':c,'R_fine':f,'pass':gate(c,f)}
   c=pkm(t['default'][1],t['permille'][1]);f=pkm(t['permille'][1],t['reference'][1]);blocks['Pk']={'R_coarse':c,'R_fine':f,'pass':gate(c,f)}
   res[point]={'blocks':blocks,'pass':all(v['pass'] for v in blocks.values())}
  out['points']=res
  if all(v['pass'] for v in res.values()):out['classification']='M35_K4_PASS_WITH_SCOPE_LOCAL_2D_PROVIDER_PRECISION_LADDER';out['K4_promoted']=True
  else:out['classification']='M35_K4_NUMERICAL_ROBUSTNESS_NOT_ESTABLISHED_LOCAL_2D';out['K4_promoted']=False
 except Exception as e:
  out['classification']='M35_K4_PROVIDER_OR_PRECISION_EXECUTION_BLOCKED';out['K4_promoted']=False;out['error']=repr(e)
 Path(outp).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
