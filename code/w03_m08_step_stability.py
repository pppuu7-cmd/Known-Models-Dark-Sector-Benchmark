#!/usr/bin/env python3
from __future__ import annotations

import argparse, glob, json, re
from pathlib import Path
import numpy as np

Z=np.array([0.295,0.51,0.706,0.934,1.317,1.491,2.33],float)
K=np.array([0.001,0.003,0.01,0.03,0.1],float)


def zhdr(path):
    with open(path) as f:
        for _ in range(20):
            s=f.readline(); m=re.search(r'redshift\s+z\s*=\s*([+\-0-9.eE]+)',s,re.I)
            if m:return float(m.group(1))
    raise ValueError(path)


def load_pk(d,prefix):
    rows=[]
    for p in glob.glob(str(Path(d)/f'{prefix}*pk.dat')):
        z=zhdr(p); a=np.loadtxt(p,comments='#'); k,y=a[:,0],a[:,1]
        rows.append((z,np.exp(np.interp(np.log(K),np.log(k),np.log(y)))))
    rows.sort()
    if len(rows)!=7 or not np.allclose([r[0] for r in rows],Z,rtol=0,atol=1e-10):
        raise ValueError(f'bad P grid {prefix}')
    return np.vstack([r[1] for r in rows])


def titles(path):
    txt=''
    with open(path) as f:
        for _ in range(30):
            s=f.readline()
            if not s:break
            if s.startswith('#'):txt+=' '+s[1:].strip()
            else:break
    ms=list(re.finditer(r'(?:^|\s)(\d+):',txt)); out={}
    for i,m in enumerate(ms):
        out[int(m.group(1))-1]=txt[m.end():(ms[i+1].start() if i+1<len(ms) else len(txt))].strip()
    return out


def load_H(d,prefix):
    hits=list(Path(d).glob(f'{prefix}*background.dat'))
    if len(hits)!=1:raise ValueError(f'background {prefix}: {hits}')
    t=titles(hits[0]); a=np.loadtxt(hits[0],comments='#')
    iz=next(i for i,x in t.items() if x.startswith('z'))
    ih=next(i for i,x in t.items() if x.startswith('H [1/Mpc]'))
    order=np.argsort(a[:,iz])
    return np.interp(Z,a[order,iz],a[order,ih])


def response(d,prefix,refP,refH):
    return np.log(load_pk(d,prefix)/refP).reshape(-1),np.log(load_H(d,prefix)/refH)


def direction(d,refP,refH,prefix_plus,prefix_minus,h):
    pP,pH=response(d,prefix_plus,refP,refH)
    mP,mH=response(d,prefix_minus,refP,refH)
    return (pP-mP)/(2*h),(pH-mH)/(2*h)


def metrics(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    na=np.linalg.norm(a); nb=np.linalg.norm(b)
    rel=float(np.linalg.norm(a-b)/max(na,nb,1e-30))
    c=float(np.dot(a,b)/max(na*nb,1e-30)); c=max(-1,min(1,c))
    angle=float(np.degrees(np.arccos(c)))
    return {'relative_l2_difference':rel,'angle_deg':angle,'norm_a':float(na),'norm_b':float(nb)}


def fit_m07(J,target):
    c,*_=np.linalg.lstsq(J,target,rcond=None)
    pred=J@c
    nP=35
    return {
      'coefficients':{'epsilon0':float(c[0]),'wa':float(c[1])},
      'combined_residual_fraction':float(np.linalg.norm(target-pred)/np.linalg.norm(target)),
      'P_residual_fraction':float(np.linalg.norm(target[:nP]-pred[:nP])/np.linalg.norm(target[:nP])),
      'H_residual_fraction':float(np.linalg.norm(target[nP:]-pred[nP:])/np.linalg.norm(target[nP:]))
    }


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--directory',required=True); ap.add_argument('--h1',type=float,default=1e-3); ap.add_argument('--h2',type=float,default=5e-4); ap.add_argument('--m07',required=True); ap.add_argument('--json',required=True); args=ap.parse_args()
    d=Path(args.directory)
    refP=load_pk(d,'ref_'); refH=load_H(d,'ref_')
    e1P,e1H=direction(d,refP,refH,'e0p1_','e0m1_',args.h1)
    a1P,a1H=direction(d,refP,refH,'wap1_','wam1_',args.h1)
    e2P,e2H=direction(d,refP,refH,'e0p2_','e0m2_',args.h2)
    a2P,a2H=direction(d,refP,refH,'wap2_','wam2_',args.h2)
    e1=np.r_[e1P,e1H]; a1=np.r_[a1P,a1H]; e2=np.r_[e2P,e2H]; a2=np.r_[a2P,a2H]
    J1=np.column_stack([e1,a1]); J2=np.column_stack([e2,a2])
    s1=np.linalg.svd(J1,compute_uv=False); s2=np.linalg.svd(J2,compute_uv=False)
    m07=json.load(open(args.m07)); target=np.r_[np.asarray(m07['local_q_response_vector_lnP'],float),np.asarray(m07['local_q_response_lnH'],float)]
    f1=fit_m07(J1,target); f2=fit_m07(J2,target)
    out={
      'schema':'KMDSB.W03.M08.StepStability.v0.1',
      'h1':args.h1,'h2':args.h2,
      'direction_stability':{
        'epsilon0_combined':metrics(e1,e2),
        'wa_combined':metrics(a1,a2),
        'epsilon0_P':metrics(e1P,e2P),'epsilon0_H':metrics(e1H,e2H),
        'wa_P':metrics(a1P,a2P),'wa_H':metrics(a1H,a2H)
      },
      'basis':{
        'h1':{'singular_values':s1.tolist(),'sigma2_over_sigma1':float(s1[1]/s1[0])},
        'h2':{'singular_values':s2.tolist(),'sigma2_over_sigma1':float(s2[1]/s2[0])},
        'sigma_ratio_relative_change':float(abs(s2[1]/s2[0]-s1[1]/s1[0])/(s1[1]/s1[0]))
      },
      'm07_absorption':{
        'h1':f1,'h2':f2,
        'combined_residual_absolute_change':float(abs(f2['combined_residual_fraction']-f1['combined_residual_fraction'])),
        'coefficient_relative_change':float(np.linalg.norm(np.array(list(f2['coefficients'].values()))-np.array(list(f1['coefficients'].values())))/np.linalg.norm(np.array(list(f1['coefficients'].values()))))
      },
      'interpretation':'step-stability control only; no observation-space claim'
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))

if __name__=='__main__':main()
