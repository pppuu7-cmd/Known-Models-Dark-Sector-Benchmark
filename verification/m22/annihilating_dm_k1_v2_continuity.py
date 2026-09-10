#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np

CLASS_PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PREREG='protocol/W04_M22_ANNIHILATING_DM_K1_V2_CONTINUITY_PREREGISTRATION_v0.1.md'
PANN=[1.11e-23,3.33e-24,1.11e-24,3.33e-25,1.11e-25,3.33e-26]

def common(root):
 return [f'root = {root}','overwrite_root = yes','output = tCl,pCl,mPk','lensing = no','non linear = none','recombination = HyRec','omega_b = 2.255065e-2','omega_cdm = 1.193524e-1','H0 = 67.76953','A_s = 2.123257e-9','n_s = 0.9686025','z_reio = 8.227371','P_k_max_1/Mpc = 3.0','l_max_scalars = 2500']

def prepare(out):
 out.mkdir(parents=True,exist_ok=True)
 (out/'ref.ini').write_text('\n'.join(common('output/ref'))+'\n')
 (out/'zero.ini').write_text('\n'.join(common('output/zero')+['DM_annihilation_efficiency = 0'])+'\n')
 for i,p in enumerate(PANN):
  (out/f'p{i}.ini').write_text('\n'.join(common(f'output/p{i}')+[f'DM_annihilation_efficiency = {p:.12e}'])+'\n')
 (out/'manifest.json').write_text(json.dumps({'schema':'KMDSB.M22.K1V2Manifest.v1','class_pin':CLASS_PIN,'p_ann_m3_s_J':PANN,'preregistration':PREREG},indent=2,sort_keys=True)+'\n')

def load(path):
 rows=[]
 for line in path.read_text(errors='replace').splitlines():
  s=line.strip()
  if not s or s.startswith('#'): continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError:continue
  if r and all(math.isfinite(v) for v in r):rows.append(r)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<3 or a.shape[1]<2:raise RuntimeError(f'invalid table {path}: {a.shape}')
 return a

def nl2(y,r): return float(np.linalg.norm(y-r)/max(float(np.linalg.norm(r)),1e-300))

def clm(a,r,col):
 if a.shape[0]!=r.shape[0] or not np.array_equal(a[:,0],r[:,0]): raise RuntimeError('CMB ell mismatch')
 return {'R2':nl2(a[:,col],r[:,col]),'n':int(a.shape[0])}

def pkm(a,r):
 x,y=a[:,0],a[:,1];xr,yr=r[:,0],r[:,1]
 ia=np.argsort(x);ir=np.argsort(xr);x,y=x[ia],y[ia];xr,yr=xr[ir],yr[ir]
 m=(x>0)&np.isfinite(y);mr=(xr>0)&np.isfinite(yr);x,y=x[m],y[m];xr,yr=xr[mr],yr[mr]
 lo=max(x.min(),xr.min());hi=min(x.max(),xr.max());m=(x>=lo)&(x<=hi);x,y=x[m],y[m]
 rr=np.interp(np.log(x),np.log(xr),yr)
 return {'R2':nl2(y,rr),'n':int(x.size)}

def judge(points):
 seq=[q['R2'] for q in points]
 mono=all(seq[i+1]<=1.02*seq[i] for i in range(len(seq)-1))
 x=np.asarray(PANN[-3:]);y=np.asarray(seq[-3:])
 fit={'valid':False,'p':None}
 if np.all(y>0) and np.all(np.isfinite(y)):
  p,la=np.polyfit(np.log(x),np.log(y),1);fit={'valid':True,'p':float(p),'logA':float(la)}
 return {'points':points,'R2_sequence':seq,'monotonic_with_2pct_slack':mono,'first_gt_1e-10':seq[0]>1e-10,'final_le_tenth_first':seq[-1]<=0.10*seq[0],'fit_new_smallest3':fit,'pass':bool(mono and seq[0]>1e-10 and seq[-1]<=0.10*seq[0] and fit['valid'] and fit['p']>0.20)}

def analyze(root,statusp,out):
 st=json.loads(statusp.read_text()); keys=['build','ref','zero']+[f'p{i}' for i in range(len(PANN))]
 res={'schema':'KMDSB.M22.annihilatingDM.K1V2.v1','class_pin':CLASS_PIN,'preregistration':PREREG,'p_ann_m3_s_J':PANN,'status':st,'K0_provenance':'PASS_WITH_SCOPE_PINNED_NATIVE_CLASS_ENERGY_INJECTION','K1_reference_limit':'NOT_PROMOTED','K2_physical_geometry':'ONE_SIDED_PANN_GE_0_NO_SIGN_QUOTIENT','K4_promoted':False,'physical_falsification':False}
 if any(st.get(k)!=0 for k in keys):res['classification']='M22_K1_V2_PROVIDER_EXECUTION_BLOCKED';out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n');return
 rc=load(root/'output/ref_cl.dat');zc=load(root/'output/zero_cl.dat');rp=load(root/'output/ref_pk.dat');zp=load(root/'output/zero_pk.dat')
 exact={'TT':clm(zc,rc,1),'EE':clm(zc,rc,2),'TE':clm(zc,rc,3),'Pk':pkm(zp,rp)};res['exact_zero_vs_omitted']=exact;res['exact_zero_identity_pass']=all(v['R2']<=1e-12 for v in exact.values())
 cls=[load(root/f'output/p{i}_cl.dat') for i in range(len(PANN))];pks=[load(root/f'output/p{i}_pk.dat') for i in range(len(PANN))]
 blocks={}
 for name,col in [('TT',1),('EE',2),('TE',3)]:
  pts=[]
  for p,a in zip(PANN,cls):q=clm(a,zc,col);q['p_ann']=p;pts.append(q)
  blocks[name]=judge(pts)
 pts=[]
 for p,a in zip(PANN,pks):q=pkm(a,zp);q['p_ann']=p;pts.append(q)
 blocks['Pk']=judge(pts);res['blocks']=blocks;res['failing_blocks']=[k for k,v in blocks.items() if not v['pass']]
 ok=res['exact_zero_identity_pass'] and not res['failing_blocks']
 if ok:res['classification']='M22_K1_V2_REFERENCE_LIMIT_PASS_WITH_SCOPE_NATIVE_ENERGY_INJECTION';res['K1_reference_limit']='PASS_WITH_SCOPE_NATIVE_ENERGY_INJECTION_EXACT_ZERO'
 else:res['classification']='M22_K1_V2_REFERENCE_LIMIT_NOT_ESTABLISHED'
 out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
 ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='cmd',required=True);p=sp.add_parser('prepare');p.add_argument('out',type=Path);a=sp.add_parser('analyze');a.add_argument('root',type=Path);a.add_argument('status',type=Path);a.add_argument('out',type=Path);args=ap.parse_args();prepare(args.out) if args.cmd=='prepare' else analyze(args.root,args.status,args.out)
