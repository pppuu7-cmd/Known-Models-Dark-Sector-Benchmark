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
    if len(rows)!=7 or not np.allclose([r[0] for r in rows],Z,rtol=0,atol=1e-10): raise ValueError(f'bad P grid {prefix}')
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
    for i,m in enumerate(ms): out[int(m.group(1))-1]=txt[m.end():(ms[i+1].start() if i+1<len(ms) else len(txt))].strip()
    return out

def load_H(d,prefix):
    hits=list(Path(d).glob(f'{prefix}*background.dat'))
    if len(hits)!=1:raise ValueError(f'background {prefix}: {hits}')
    t=titles(hits[0]); a=np.loadtxt(hits[0],comments='#')
    iz=next(i for i,x in t.items() if x.startswith('z')); ih=next(i for i,x in t.items() if x.startswith('H [1/Mpc]'))
    order=np.argsort(a[:,iz]); return np.interp(Z,a[order,iz],a[order,ih])

def response(d,prefix,refP,refH):
    return np.log(load_pk(d,prefix)/refP).reshape(-1),np.log(load_H(d,prefix)/refH)

def geom(a,b):
    na=np.linalg.norm(a); nb=np.linalg.norm(b); c=float(np.dot(a,b)/(na*nb)); c=max(-1,min(1,c))
    return {'cosine':c,'angle_deg':float(np.degrees(np.arccos(c))),'acute_deg':float(np.degrees(np.arccos(abs(c))))}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--directory',required=True); ap.add_argument('--step',type=float,default=1e-3); ap.add_argument('--json',required=True); args=ap.parse_args()
    d=Path(args.directory); h=args.step
    refP=load_pk(d,'ref_'); refH=load_H(d,'ref_')
    r0P,r0H=response(d,'ref_',refP,refH)
    epP,epH=response(d,'e0p_',refP,refH); emP,emH=response(d,'e0m_',refP,refH)
    apP,apH=response(d,'wap_',refP,refH); amP,amH=response(d,'wam_',refP,refH)
    j0P=(epP-emP)/(2*h); j0H=(epH-emH)/(2*h)
    jaP=(apP-amP)/(2*h); jaH=(apH-amH)/(2*h)
    J=np.column_stack([np.r_[j0P,j0H],np.r_[jaP,jaH]])
    s=np.linalg.svd(J,compute_uv=False)
    asym={
      'epsilon0_P_central_nonlinearity':float(np.linalg.norm(epP+emP)/max(np.linalg.norm(epP-emP),1e-30)),
      'epsilon0_H_central_nonlinearity':float(np.linalg.norm(epH+emH)/max(np.linalg.norm(epH-emH),1e-30)),
      'wa_P_central_nonlinearity':float(np.linalg.norm(apP+amP)/max(np.linalg.norm(apP-amP),1e-30)),
      'wa_H_central_nonlinearity':float(np.linalg.norm(apH+amH)/max(np.linalg.norm(apH-amH),1e-30))
    }
    out={
      'schema':'KMDSB.W03.M08.CPLLocalBasis.v0.1','step':h,'grid':{'z':Z.tolist(),'k_h_mpc':K.tolist()},
      'reference_floor':{'max_abs_lnP':float(np.max(np.abs(r0P))),'max_abs_lnH':float(np.max(np.abs(r0H)))},
      'directions':{
        'epsilon0':{'P':j0P.tolist(),'H':j0H.tolist()},
        'wa':{'P':jaP.tolist(),'H':jaH.tolist()}
      },
      'combined_geometry_epsilon0_vs_wa':geom(np.r_[j0P,j0H],np.r_[jaP,jaH]),
      'singular_values_combined_PH':s.tolist(),
      'sigma2_over_sigma1':float(s[1]/s[0]),
      'central_nonlinearity_ratios':asym,
      'interpretation':'unwhitened local theory-response basis only; no observational claim'
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
