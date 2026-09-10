#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json, re
from pathlib import Path
import numpy as np
Z=np.array([0.295,0.51,0.706,0.934,1.317,1.491,2.33],float)
K=np.array([0.001,0.003,0.01,0.03,0.1],float)
def zhdr(path):
    with open(path) as f:
        for _ in range(24):
            m=re.search(r'redshift\s+z\s*=\s*([+\-0-9.eE]+)',f.readline(),re.I)
            if m:return float(m.group(1))
    raise ValueError(path)
def load_pk(d,p):
    r=[]
    for x in glob.glob(str(Path(d)/f'{p}*pk.dat')):
        a=np.loadtxt(x,comments='#'); r.append((zhdr(x),np.exp(np.interp(np.log(K),np.log(a[:,0]),np.log(a[:,1])))))
    r.sort()
    if len(r)!=7 or not np.allclose([x[0] for x in r],Z,atol=1e-10,rtol=0):raise ValueError(p)
    return np.vstack([x[1] for x in r])
def titles(path):
    txt=''
    with open(path) as f:
        for _ in range(40):
            s=f.readline()
            if not s or not s.startswith('#'):break
            txt+=' '+s[1:].strip()
    ms=list(re.finditer(r'(?:^|\s)(\d+):',txt)); o={}
    for i,m in enumerate(ms):o[int(m.group(1))-1]=txt[m.end():(ms[i+1].start() if i+1<len(ms) else len(txt))].strip()
    return o
def load_H(d,p):
    h=list(Path(d).glob(f'{p}*background.dat'))
    if len(h)!=1:raise ValueError(p)
    t=titles(h[0]); a=np.loadtxt(h[0],comments='#'); iz=next(i for i,x in t.items() if x.startswith('z')); ih=next(i for i,x in t.items() if x.startswith('H [1/Mpc]'))
    q=np.argsort(a[:,iz]); return np.interp(Z,a[q,iz],a[q,ih])
def resp(P,H,P0,H0):return np.log(P/P0).reshape(-1),np.log(H/H0)
def geom(a,b):
    c=float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))); c=max(-1,min(1,c)); return {'cosine':c,'acute_deg':float(np.degrees(np.arccos(abs(c))))}
def stability(a,b):return {'relative_difference':float(np.linalg.norm(a-b)/np.linalg.norm(b)),'geometry':geom(a,b)}
def residual(t,J):
    c,*_=np.linalg.lstsq(J,t,rcond=None); r=t-J@c
    return c,float(np.linalg.norm(r)/np.linalg.norm(t))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--directory',required=True); ap.add_argument('--json',required=True); a=ap.parse_args(); d=Path(a.directory)
    tags=['anchor','cs005','w0p1','w0m1','wap1','wam1','w0p05','w0m05','wap05','wam05']
    P={t:load_pk(d,t+'_') for t in tags}; H={t:load_H(d,t+'_') for t in tags}; P0=P['anchor'];H0=H['anchor']
    R={t:resp(P[t],H[t],P0,H0) for t in tags if t!='anchor'}
    jsP,jsH=R['cs005'][0]/.05,R['cs005'][1]/.05; js=np.r_[jsP,jsH]
    def cd(p,m,h): return np.r_[(R[p][0]-R[m][0])/(2*h),(R[p][1]-R[m][1])/(2*h)]
    j0_1=cd('w0p1','w0m1',1e-3); ja_1=cd('wap1','wam1',1e-3); j0_05=cd('w0p05','w0m05',5e-4); ja_05=cd('wap05','wam05',5e-4)
    st0,sta=stability(j0_1,j0_05),stability(ja_1,ja_05)
    J=np.column_stack([j0_05,ja_05]); c,rf=residual(js,J); pred=J@c; rp=float(np.linalg.norm(jsP-pred[:35])/np.linalg.norm(jsP)); rh=float(np.linalg.norm(jsH-pred[35:])/max(np.linalg.norm(jsH),1e-30)) if np.linalg.norm(jsH)>0 else None
    cp,rpopt=residual(jsP,J[:35,:]); s=np.linalg.svd(J,compute_uv=False)
    if rf<=.10: cls='CPL_ABSORBS_M11_WITH_SCOPE'
    elif rf>=.30: cls='M11_SEPARATED_FROM_LOCAL_CPL_WITH_SCOPE'
    else: cls='INCONCLUSIVE_MANIFOLD_SEPARATION'
    stable=st0['relative_difference']<=.01 and st0['geometry']['acute_deg']<=.5 and sta['relative_difference']<=.01 and sta['geometry']['acute_deg']<=.5
    out={'schema':'KMDSB.W03.M11.CPLManifoldAttack.v0.1','anchor':{'w0':-.95,'wa':0,'cs2':1},'target':'J_s from q_s=.05','cpl_step_stability':{'w0':st0,'wa':sta,'passes':bool(stable)},'cpl_small_step_singular_values':s.tolist(),'sigma2_over_sigma1':float(s[1]/s[0]),'shared_PH_fit':{'coefficients_delta_w0_delta_wa_per_qs':c.tolist(),'combined_residual_fraction':rf,'P_residual_fraction':rp,'H_residual_fraction':rh},'P_only_diagnostic':{'coefficients':cp.tolist(),'residual_fraction':rpopt},'classification':cls if stable else 'BLOCKED_NUMERICAL_CPL_TANGENT','interpretation':'unwhitened theory-response manifold attack only; no K7 observational claim'}
    Path(a.json).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
