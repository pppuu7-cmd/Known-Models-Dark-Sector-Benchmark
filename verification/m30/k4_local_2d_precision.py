#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import numpy as np
PREREG='protocol/W07_M30_K4_LOCAL_2D_PRECISION_PREREGISTRATION_v0.1.md'
PIN='0009f51d89e6465c79e570b496c66fc90058fa77'

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
 if len(ell)<20:raise RuntimeError('insufficient common ell')
 x=np.asarray([ia[e][col] for e in ell]);y=np.asarray([ib[e][col] for e in ell]);return nl2(x,y)
def pkm(a,b):
 xa,ya=a[:,0],a[:,1];xb,yb=b[:,0],b[:,1];ia=np.argsort(xa);ib=np.argsort(xb);xa,ya=xa[ia],ya[ia];xb,yb=xb[ib],yb[ib]
 m=(xa>0)&np.isfinite(ya);n=(xb>0)&np.isfinite(yb);xa,ya=xa[m],ya[m];xb,yb=xb[n],yb[n]
 lo=max(xa.min(),xb.min());hi=min(xa.max(),xb.max());m=(xa>=lo)&(xa<=hi);x=xa[m];y=ya[m]
 if x.size<20:raise RuntimeError('insufficient common k')
 z=np.interp(np.log(x),np.log(xb),yb);return nl2(y,z)
def gate(c,f):return bool(f<=1e-4 and (f<=0.5*c or (c<=1e-8 and f<=1e-8)))
def point(base,statusp,point,outp):
 st=json.loads(Path(statusp).read_text());out={'schema':'KMDSB.M30.K4Local2DPrecisionPoint.v1','model_id':'M30','family_id':'F30','point':point,'provider_commit':PIN,'preregistration':PREREG,'status':st,'K4_promoted':False,'physical_falsification':False}
 try:
  if any(st.get(k)!=0 for k in ['build','default','permille','reference']):raise RuntimeError('provider/profile execution blocked')
  tabs={}
  for p in ['default','permille','reference']:
   tabs[p]=(load(Path(base)/f'{p}_cl.dat'),load(Path(base)/f'{p}_pk.dat'))
  blocks={}
  for name,col in [('TT',1),('EE',2),('TE',3)]:
   c=clm(tabs['default'][0],tabs['permille'][0],col);f=clm(tabs['permille'][0],tabs['reference'][0],col);blocks[name]={'R_coarse':c,'R_fine':f,'pass':gate(c,f)}
  c=pkm(tabs['default'][1],tabs['permille'][1]);f=pkm(tabs['permille'][1],tabs['reference'][1]);blocks['Pk']={'R_coarse':c,'R_fine':f,'pass':gate(c,f)}
  out['blocks']=blocks;out['point_pass']=all(v['pass'] for v in blocks.values());out['classification']='M30_K4_POINT_PROVIDER_PRECISION_PASS' if out['point_pass'] else 'M30_K4_POINT_PROVIDER_PRECISION_NOT_ESTABLISHED'
 except Exception as e:
  out['point_pass']=False;out['classification']='M30_K4_PROVIDER_OR_PRECISION_EXECUTION_BLOCKED';out['error']=repr(e)
 Path(outp).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
def aggregate(indir,outp):
 files=sorted(Path(indir).glob('**/M30_K4_POINT_*.json'));pts=[json.loads(p.read_text()) for p in files]
 out={'schema':'KMDSB.M30.K4Local2DPrecisionAggregate.v1','model_id':'M30','family_id':'F30','provider_commit':PIN,'preregistration':PREREG,'physical_falsification':False,'points':pts}
 names={p.get('point') for p in pts};blocked=any(p.get('classification')=='M30_K4_PROVIDER_OR_PRECISION_EXECUTION_BLOCKED' for p in pts)
 if names!={'base','radial','cT'} or blocked:cls='M30_K4_PROVIDER_OR_PRECISION_EXECUTION_BLOCKED';prom=False
 elif all(p.get('point_pass') for p in pts):cls='M30_K4_PASS_WITH_SCOPE_LOCAL_2D_PROVIDER_PRECISION_LADDER';prom=True
 else:cls='M30_K4_NUMERICAL_ROBUSTNESS_NOT_ESTABLISHED_LOCAL_2D';prom=False
 out['classification']=cls;out['K4_promoted']=prom
 Path(outp).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':
 ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='cmd',required=True)
 p=sp.add_parser('point');p.add_argument('base');p.add_argument('status');p.add_argument('point');p.add_argument('out')
 a=sp.add_parser('aggregate');a.add_argument('indir');a.add_argument('out')
 z=ap.parse_args(); point(z.base,z.status,z.point,z.out) if z.cmd=='point' else aggregate(z.indir,z.out)
