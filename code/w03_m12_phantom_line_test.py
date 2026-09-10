#!/usr/bin/env python3
from __future__ import annotations
import argparse,glob,json,re
from pathlib import Path
import numpy as np
Z=np.array([.295,.51,.706,.934,1.317,1.491,2.33]); K=np.array([.001,.003,.01,.03,.1])
def zh(p):
  with open(p) as f:
    for _ in range(24):
      m=re.search(r'redshift\s+z\s*=\s*([+\-0-9.eE]+)',f.readline(),re.I)
      if m:return float(m.group(1))
  raise ValueError(p)
def pk(d,p):
  r=[]
  for x in glob.glob(str(Path(d)/f'{p}*pk.dat')):
    a=np.loadtxt(x,comments='#'); r.append((zh(x),np.exp(np.interp(np.log(K),np.log(a[:,0]),np.log(a[:,1])))))
  r.sort()
  if len(r)!=7:raise ValueError(p)
  return np.vstack([x[1] for x in r])
def titles(p):
  s=''
  with open(p) as f:
    for _ in range(40):
      x=f.readline()
      if not x or not x.startswith('#'):break
      s+=' '+x[1:].strip()
  ms=list(re.finditer(r'(?:^|\s)(\d+):',s)); o={}
  for i,m in enumerate(ms):o[int(m.group(1))-1]=s[m.end():(ms[i+1].start() if i+1<len(ms) else len(s))].strip()
  return o
def H(d,p):
  q=list(Path(d).glob(f'{p}*background.dat')); t=titles(q[0]); a=np.loadtxt(q[0],comments='#'); iz=next(i for i,x in t.items() if x.startswith('z')); ih=next(i for i,x in t.items() if x.startswith('H [1/Mpc]')); j=np.argsort(a[:,iz]); return np.interp(Z,a[j,iz],a[j,ih])
def geo(a,b):
  c=float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)));c=max(-1,min(1,c));return {'cosine':c,'oriented_deg':float(np.degrees(np.arccos(c))),'acute_deg':float(np.degrees(np.arccos(abs(c))))}
def conv(a,b):return {'relative_difference':float(np.linalg.norm(a-b)/np.linalg.norm(a)),'geometry':geo(a,b)}
def main():
  ap=argparse.ArgumentParser();ap.add_argument('--directory',required=True);ap.add_argument('--json',required=True);x=ap.parse_args();d=Path(x.directory)
  tags=['lcdm','fld0','np1','np2','ph1','ph2'];P={t:pk(d,t+'_') for t in tags};Q={t:H(d,t+'_') for t in tags}
  refP=np.log(P['fld0']/P['lcdm']).reshape(-1);refH=np.log(Q['fld0']/Q['lcdm'])
  def r(t):return np.r_[np.log(P[t]/P['fld0']).reshape(-1),np.log(Q[t]/Q['fld0'])]
  jp1=r('np1')/.001;jp2=r('np2')/.002;jm1=r('ph1')/.001;jm2=r('ph2')/.002
  cp,cm=conv(jp1,jp2),conv(jm1,jm2);g=geo(jp1,jm1)
  # best unoriented line projection of phantom ray onto nonphantom ray
  a=float(np.dot(jp1,jm1)/np.dot(jp1,jp1));res=float(np.linalg.norm(jm1-a*jp1)/np.linalg.norm(jm1))
  if g['acute_deg']<=1 and res<=.02:cl='PHANTOM_RESPONSE_REPRESENTED_BY_CONSTANT_W_LINE_WITH_SCOPE'
  elif res>=.20:cl='PHANTOM_RESPONSE_SEPARATED_FROM_LOCAL_CONSTANT_W_LINE_WITH_SCOPE'
  else:cl='INCONCLUSIVE_LOCAL_LINE_RELATION'
  hard={'reference_pass':bool(np.max(np.abs(refP))<=1e-6 and np.max(np.abs(refH))<=1e-8),'nonphantom_convergence_pass':bool(cp['relative_difference']<=.02 and cp['geometry']['acute_deg']<=1),'phantom_convergence_pass':bool(cm['relative_difference']<=.02 and cm['geometry']['acute_deg']<=1)}
  out={'schema':'KMDSB.W03.M12.PhantomLine.v0.1','reference':{'max_abs_lnP':float(np.max(np.abs(refP))),'max_abs_lnH':float(np.max(np.abs(refH)))},'nonphantom_convergence':cp,'phantom_convergence':cm,'phantom_vs_nonphantom':g,'best_line_projection_coefficient':a,'line_residual_fraction':res,'hard_gates':hard,'classification':cl,'physical_scope':'phenomenological smooth phantom response; minimal wrong-sign scalar ghost/stability issue recorded separately; not all effective w<-1 theories','interpretation':'theory-response only'}
  Path(x.json).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
