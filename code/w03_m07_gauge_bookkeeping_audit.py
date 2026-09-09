#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json, math, re
from pathlib import Path
import numpy as np

Z=np.array([0.295,0.51,0.706,0.934,1.317,1.491,2.33],float)
K=np.array([0.001,0.003,0.01,0.03,0.1],float)

def z_from_header(path):
    with open(path) as f:
        for _ in range(12):
            s=f.readline()
            m=re.search(r'redshift\s+z\s*=\s*([+\-0-9.eE]+)',s,re.I)
            if m:return float(m.group(1))
    raise ValueError(path)

def load_pk(directory,prefix):
    rows=[]
    for p in glob.glob(str(Path(directory)/f'{prefix}*pk.dat')):
        z=z_from_header(p); a=np.loadtxt(p,comments='#'); k=a[:,0]; y=a[:,1]
        v=np.exp(np.interp(np.log(K),np.log(k),np.log(y)))
        rows.append((z,v))
    rows.sort()
    if len(rows)!=len(Z) or not np.allclose([x[0] for x in rows],Z,atol=1e-10,rtol=0): raise ValueError('bad z grid pk')
    return np.vstack([x[1] for x in rows])

def tk_columns(path):
    with open(path) as f:
        for _ in range(20):
            s=f.readline()
            if ':k ' in s and ':d_m' in s and ':phi' in s and ':psi' in s:
                pairs=re.findall(r'(\d+):([^\s]+)',s)
                return {name:int(n)-1 for n,name in pairs}
    raise ValueError('no tk title line')

def load_tk(directory,prefix):
    rows=[]
    for p in glob.glob(str(Path(directory)/f'{prefix}*tk.dat')):
        z=z_from_header(p); cols=tk_columns(p); a=np.loadtxt(p,comments='#')
        k=a[:,cols['k']]
        vals={}
        for name in ('d_m','phi','psi'):
            vals[name]=np.interp(np.log(K),np.log(k),a[:,cols[name]])
        rows.append((z,vals))
    rows.sort()
    if len(rows)!=len(Z) or not np.allclose([x[0] for x in rows],Z,atol=1e-10,rtol=0): raise ValueError('bad z grid tk')
    return {name:np.vstack([x[1][name] for x in rows]) for name in ('d_m','phi','psi')}

def metrics(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    scale=np.maximum(np.maximum(np.abs(a),np.abs(b)),1e-30)
    rel=np.abs(a-b)/scale
    return {'max_symmetric_relative_difference':float(rel.max()),'l2_relative_difference':float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),1e-30))}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--sync',required=True); ap.add_argument('--newt',required=True); ap.add_argument('--json',required=True); args=ap.parse_args()
    out={'schema':'KMDSB-W03-M07-gauge-bookkeeping-v0.1','grid':{'z':Z.tolist(),'k_h_mpc':K.tolist()},'comparisons':{}}
    for case,prefix in [('ref','ref_'),('m07','m07_')]:
        ps=load_pk(args.sync,prefix); pn=load_pk(args.newt,prefix)
        out['comparisons'][f'{case}_P']=metrics(ps,pn)
        ts=load_tk(args.sync,prefix); tn=load_tk(args.newt,prefix)
        for name in ('d_m','phi','psi'): out['comparisons'][f'{case}_{name}']=metrics(ts[name],tn[name])
    # response comparison is more stringent than comparing only raw model outputs
    rps=np.log(load_pk(args.sync,'m07_')/load_pk(args.sync,'ref_'))
    rpn=np.log(load_pk(args.newt,'m07_')/load_pk(args.newt,'ref_'))
    out['comparisons']['response_lnP']=metrics(rps,rpn)
    Path(args.json).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
