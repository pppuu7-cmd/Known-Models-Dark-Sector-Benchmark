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
    d=a-b
    scale=np.maximum(np.maximum(np.abs(a),np.abs(b)),1e-30)
    rel=np.abs(d)/scale
    na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b)); nd=float(np.linalg.norm(d))
    return {
        'max_symmetric_relative_difference':float(rel.max()),
        'l2_relative_difference':float(nd/max(na,nb,1e-30)),
        'l2_absolute_difference':nd,
        'l2_norm_a':na,
        'l2_norm_b':nb,
        'max_absolute_difference':float(np.max(np.abs(d)))
    }

def safe_log_abs_ratio(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    if np.any(a==0) or np.any(b==0): raise ValueError('zero in log-abs ratio')
    return np.log(np.abs(a)/np.abs(b))

def fractional_response(model,ref):
    model=np.asarray(model,float); ref=np.asarray(ref,float)
    if np.any(np.abs(ref)<1e-30): raise ValueError('near-zero reference in fractional response')
    return (model-ref)/ref

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--sync',required=True); ap.add_argument('--newt',required=True); ap.add_argument('--json',required=True); args=ap.parse_args()
    out={'schema':'KMDSB-W03-M07-gauge-bookkeeping-v0.3','grid':{'z':Z.tolist(),'k_h_mpc':K.tolist()},'comparisons':{}}
    p={}; t={}
    for case,prefix in [('ref','ref_'),('m07','m07_')]:
        ps=load_pk(args.sync,prefix); pn=load_pk(args.newt,prefix)
        p[(case,'sync')]=ps; p[(case,'newt')]=pn
        out['comparisons'][f'{case}_P']=metrics(ps,pn)
        ts=load_tk(args.sync,prefix); tn=load_tk(args.newt,prefix)
        t[(case,'sync')]=ts; t[(case,'newt')]=tn
        for name in ('d_m','phi','psi'): out['comparisons'][f'{case}_{name}']=metrics(ts[name],tn[name])
    rps=np.log(p[('m07','sync')]/p[('ref','sync')])
    rpn=np.log(p[('m07','newt')]/p[('ref','newt')])
    out['comparisons']['response_lnP']=metrics(rps,rpn)

    # Direct transfer-level representations, avoiding the separate mPk pipeline.
    rdms=safe_log_abs_ratio(t[('m07','sync')]['d_m'],t[('ref','sync')]['d_m'])
    rdmn=safe_log_abs_ratio(t[('m07','newt')]['d_m'],t[('ref','newt')]['d_m'])
    out['comparisons']['response_ln_abs_d_m']=metrics(rdms,rdmn)

    ws=t[('m07','sync')]['phi']+t[('m07','sync')]['psi']
    wrs=t[('ref','sync')]['phi']+t[('ref','sync')]['psi']
    wn=t[('m07','newt')]['phi']+t[('m07','newt')]['psi']
    wrn=t[('ref','newt')]['phi']+t[('ref','newt')]['psi']
    rws=fractional_response(ws,wrs)
    rwn=fractional_response(wn,wrn)
    out['comparisons']['response_fractional_Weyl_phi_plus_psi']=metrics(rws,rwn)

    # Cross-gauge raw-log errors for common-mode calibration diagnosis.
    dg_ref=np.log(p[('ref','sync')]/p[('ref','newt')])
    dg_m07=np.log(p[('m07','sync')]/p[('m07','newt')])
    out['gauge_error_common_mode']={
        'ref_logP_gauge_error_norm':float(np.linalg.norm(dg_ref)),
        'm07_logP_gauge_error_norm':float(np.linalg.norm(dg_m07)),
        'model_minus_ref_gauge_error_norm':float(np.linalg.norm(dg_m07-dg_ref)),
        'cosine_ref_vs_model_gauge_error':float(np.dot(dg_ref.reshape(-1),dg_m07.reshape(-1))/(max(np.linalg.norm(dg_ref)*np.linalg.norm(dg_m07),1e-30)))
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
