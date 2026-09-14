#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path

CH={'TT':1,'EE':2,'TE':3}
W=(0.003-0.001)/(0.01-0.001)
LO,HI=501,1200

def load(root:Path,case:str):
    fs=sorted(root.glob(f'{case}*_cl.dat'))
    if len(fs)!=1: raise RuntimeError((root,case,fs))
    out=[]
    for line in fs[0].read_text(errors='replace').splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        v=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
        if len(v)>=4 and all(math.isfinite(x) for x in v): out.append(v)
    return out

def vec(rows,col): return [(int(round(r[0])),r[col]) for r in rows if LO<=int(round(r[0]))<=HI]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def norm(a): return math.sqrt(dot(a,a))
def unit(a):
    n=norm(a)
    if n<1e-300: raise RuntimeError('zero template')
    return [x/n for x in a]
def close(a,b): return abs(a-b)<=max(1e-15,1e-12*max(abs(a),abs(b),1e-300))
def category(af,sf,ef):
    if ef>=0.80 and af>=0.70:return 'AMPLITUDE_LIKE'
    if ef>=0.80 and sf>=0.70:return 'PEAK_SHIFT_LIKE'
    if ef>=0.80:return 'LOW_RANK_MIXED'
    return 'COMPLEX_SHAPE'
def channel(root:Path,col:int):
    rows={c:load(root,c) for c in ['ref','f2','f3','f4']}
    vv={c:vec(rows[c],col) for c in rows}
    ells=[l for l,_ in vv['ref']]
    if any([l for l,_ in vv[c]]!=ells for c in vv): raise RuntimeError('ell mismatch')
    ref=[x for _,x in vv['ref']]; f2=[x for _,x in vv['f2']]; f3=[x for _,x in vv['f3']]; f4=[x for _,x in vv['f4']]
    pred=[d+W*(b-d) for b,d in zip(f2,f4)]; anomaly=[c-p for c,p in zip(f3,pred)]
    A=unit(ref)
    ln=[math.log(float(l)) for l in ells]; deriv=[]
    for i in range(len(ref)):
        if i==0: deriv.append((ref[1]-ref[0])/(ln[1]-ln[0]))
        elif i==len(ref)-1: deriv.append((ref[-1]-ref[-2])/(ln[-1]-ln[-2]))
        else: deriv.append((ref[i+1]-ref[i-1])/(ln[i+1]-ln[i-1]))
    proj=dot(deriv,A); S=unit([x-proj*y for x,y in zip(deriv,A)])
    n2=dot(anomaly,anomaly)
    if n2<=1e-300: raise RuntimeError('zero anomaly')
    ca=dot(anomaly,A); cs=dot(anomaly,S); af=ca*ca/n2; sf=cs*cs/n2; ef=af+sf
    residual=[x-ca*a-cs*s for x,a,s in zip(anomaly,A,S)]
    return {'ells':ells,'anomaly':anomaly,'anomaly_norm':math.sqrt(n2),'amplitude_energy_fraction':af,'shift_energy_fraction':sf,'two_template_explained_fraction':ef,'residual_fraction':dot(residual,residual)/n2,'amplitude_coefficient':ca,'shift_coefficient':cs,'amplitude_sign':1 if ca>0 else (-1 if ca<0 else 0),'shift_sign':1 if cs>0 else (-1 if cs<0 else 0),'category':category(af,sf,ef)}
def mid_exc(root:Path,col:int):
    rows={c:load(root,c) for c in ['ref','f2','f3','f4']}; ref=vec(rows['ref'],col); e=[l for l,_ in ref]; rv=[x for _,x in ref]
    vals={}
    for c in ['f2','f3','f4']:
        cv=vec(rows[c],col); assert [l for l,_ in cv]==e; x=[z for _,z in cv]; vals[c]=norm([u-v for u,v in zip(x,rv)])/max(norm(rv),1e-300)
    return vals['f3']/max(vals['f2'],vals['f4'],1e-300)
def cosine(a,b): return dot(a,b)/max(norm(a)*norm(b),1e-300)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('artifact',type=Path); ap.add_argument('canonical',type=Path); ap.add_argument('out',type=Path); a=ap.parse_args()
    canon=json.loads(a.canonical.read_text()); roots={'NDF15_default':a.artifact/'ndf_out','RK_evolver0':a.artifact/'rk_out'}
    res={'schema':'KMDSB.W04.M21.CMBMidEllShapeDecomposition.v0.1','protocol':'protocol/W04_M21_CMB_MIDELL_SHAPE_DECOMPOSITION_v0.1.md','parent_run':34542162543,'parent_artifact_id':10178334419,'parent_artifact_digest':'sha256:640472f79c7e55d9edf4ed39ed35d4ab692fcf4700fad4d50edbad0642f7c65c','interpolation_weight':W,'branches':{},'cross_solver':{},'controls':{},'K1_promoted':False,'physical_falsification':False}
    ok=close(W,2.0/9.0)
    for bn,root in roots.items():
        res['branches'][bn]={}
        for ch,col in CH.items():
            x=channel(root,col); exc=mid_exc(root,col); expected=canon[bn][ch]['mid_excursion_factor']; cp=close(exc,expected); ok &= cp
            x.pop('ells'); x['mid_excursion_factor']=exc; x['canonical_mid_excursion_factor']=expected; x['excursion_reproduction_pass']=cp; res['branches'][bn][ch]=x
    for ch in CH:
        n=res['branches']['NDF15_default'][ch]; r=res['branches']['RK_evolver0'][ch]
        cos=cosine(channel(roots['NDF15_default'],CH[ch])['anomaly'],channel(roots['RK_evolver0'],CH[ch])['anomaly'])
        consistent=(n['category']==r['category'] and cos>=0.995)
        res['cross_solver'][ch]={'cosine_similarity':cos,'NDF15_category':n['category'],'RK_category':r['category'],'status':'CONSISTENT' if consistent else 'BRANCH_DEPENDENT'}
    res['controls']={'weight_exact':close(W,2/9),'parent_mid_excursion_reproduced':ok}
    res['classification']='M21_CMB_MIDELL_SHAPE_DECOMPOSITION_PASS_WITH_SCOPE' if ok else 'M21_CMB_MIDELL_SHAPE_DECOMPOSITION_INVALID_EVIDENCE'
    a.out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':res['classification'],'cross_solver':res['cross_solver'],'categories':{b:{c:res['branches'][b][c]['category'] for c in CH} for b in roots}},indent=2))
    if not ok: raise SystemExit(1)
if __name__=='__main__': main()
