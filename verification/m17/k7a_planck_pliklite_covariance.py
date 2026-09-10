#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,re,sys
from pathlib import Path
import numpy as np

W0=-1.2498700663555409
WA=0.8082964747357178
K6='models/holographic_dark_energy/M17_C060_JOINT_CPL_K6_REFINEMENT_RESULT.json'

def ro(s,o,n):
    c=s.count(o)
    if c!=1: raise RuntimeError(f'anchor count {o!r}={c}')
    return s.replace(o,n,1)
def rk(s,k,v):
    p=re.compile(rf'(?m)^(\s*{re.escape(k)}\s*=).*?$'); m=list(p.finditer(s))
    if len(m)!=1: raise RuntimeError(f'{k}: active count={len(m)}')
    return p.sub(lambda x:f'{x.group(1)} {v}',s,count=1)

def prepare(base:Path,out:Path):
    r=json.loads(Path(K6).read_text())
    assert r['classification']=='M17_C060_K6_REFINEMENT_SURVIVOR'
    assert abs(r['best']['w0']-W0)<1e-14 and abs(r['best']['wa']-WA)<1e-14
    s=base.read_text()
    likes=['DEFAULT(batch3/plik_rd12_HM_v22_TTTEEE.ini)','DEFAULT(batch3/lowl.ini)','DEFAULT(batch3/lowE.ini)','DEFAULT(batch3/lensing.ini)','DEFAULT(batch3/BAO.ini)','DEFAULT(batch3/Pantheon18.ini)']
    for x in likes: s=ro(s,x,'#'+x)
    s=ro(s,'DEFAULT(batch3/common.ini)','DEFAULT(batch3/common.ini)\nuse_nonlinear_lensing = F\nlmax_computed_cl = 2600')
    s=ro(s,'#Use_PPF = F','Use_PPF = T')
    s=ro(s,'test_check_compare = 1820.775','#test_check_compare = 1820.775')
    s=ro(s,'#test_output_root = output_ide','test_output_root = PLACEHOLDER')
    out.mkdir(parents=True,exist_ok=True)
    for n,kind in [('h06','hde'),('cpl','cpl')]:
        t=s.replace('test_output_root = PLACEHOLDER',f'test_output_root = m17k7a_{n}')
        t=rk(t,'param[beta_cf]','0')
        if kind=='hde':
            t=rk(t,'WForm_CF','2'); t=rk(t,'param[c_hde]','0.6')
        else:
            t=rk(t,'WForm_CF','1'); t=rk(t,'param[w0]',repr(W0)); t=rk(t,'param[w1]',repr(WA))
        (out/f'{n}.ini').write_text(t)

def theory(p:Path):
    rows=[]; header=''
    for line in p.read_text(errors='replace').splitlines():
        s=line.strip()
        if s.startswith('#'):
            header += s+'\n'; continue
        if not s: continue
        try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
        except ValueError: continue
        if len(r)!=4 or not all(math.isfinite(x) for x in r): raise RuntimeError(f'bad row {p}')
        rows.append(r)
    a=np.asarray(rows,float)
    if a.shape[0]<2507 or a[-1,0]<2508: raise RuntimeError(f'insufficient ell coverage last={a[-1,0] if len(a) else None}')
    if 'L TT TE EE' not in header: raise RuntimeError('theory header contract missing')
    return a

def planck_vector(obj,a):
    ell=a[:,0].astype(int); dtt=a[:,1]; dte=a[:,2]; dee=a[:,3]
    if ell[0]>2 or ell[-1]<2508: raise RuntimeError('ell range')
    # Build dense D_l arrays using exact integer theory rows.
    lm=int(ell[-1]); tt=np.zeros(lm+1); te=np.zeros(lm+1); ee=np.zeros(lm+1)
    tt[ell]=dtt; te[ell]=dte; ee[ell]=dee
    ls=np.arange(lm+1); fac=ls*(ls+1)/(2*np.pi); fac[:2]=1.0
    cltt=tt/fac; clte=te/fac; clee=ee/fac
    xt=np.zeros(obj.nbintt); xte=np.zeros(obj.nbinte); xee=np.zeros(obj.nbinee)
    for i in range(obj.nbintt):
        lo=obj.blmin_TT[i]+obj.plmin_TT; hi=obj.blmax_TT[i]+obj.plmin_TT
        xt[i]=np.sum(cltt[lo:hi+1]*obj.bin_w_TT[obj.blmin_TT[i]:obj.blmax_TT[i]+1])
    for i in range(obj.nbinte):
        lo=obj.blmin[i]+obj.plmin; hi=obj.blmax[i]+obj.plmin
        w=obj.bin_w[obj.blmin[i]:obj.blmax[i]+1]
        xte[i]=np.sum(clte[lo:hi+1]*w); xee[i]=np.sum(clee[lo:hi+1]*w)
    return np.concatenate([xt,xte,xee])

def analyze(work:Path,planck:Path,status:Path,out:Path):
    st=json.loads(status.read_text())
    res={'schema':'KMDSB.M17.K7a.PlanckPlikLiteCovariance.v1','status':st,'physical_falsification':False,'K7':'PARTIAL_COVARIANCE_WEIGHTING_ONLY','preregistration':'protocol/W03_M17_K7A_PLANCK_PLIKLITE_COVARIANCE_PREREGISTRATION_v0.1.md'}
    if any(st.get(k)!=0 for k in ['h06','cpl']):
        res['classification']='M17_K7A_OPERATOR_OR_OUTPUT_BLOCKED'; res['reason']='theory execution'; out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n'); return
    try:
        h=theory(work/'m17k7a_h06.theory_cl'); c=theory(work/'m17k7a_cpl.theory_cl')
        sys.path.insert(0,str(planck.resolve()))
        from planck_lite_py import PlanckLitePy
        obj=PlanckLitePy(data_directory=str((planck/'data').resolve()),year=2018,spectra='TTTEEE',use_low_ell_bins=False)
        xh=planck_vector(obj,h); xc=planck_vector(obj,c); d=xh-xc; F=np.asarray(obj.fisher,float)
        if F.shape!=(613,613): raise RuntimeError(f'F shape {F.shape}')
        ev=np.linalg.eigvalsh((F+F.T)/2)
        if ev[0]<=0: raise RuntimeError(f'non-positive Fisher min={ev[0]}')
        s2=float(d@F@d)
        cuts=[('TT',0,215),('TE',215,414),('EE',414,613)]
        blocks={}
        for name,lo,hi in cuts:
            q=d[lo:hi]; fb=F[lo:hi,lo:hi]; blocks[name]={'S_cov':float(math.sqrt(max(0,q@fb@q))),'S_cov2':float(q@fb@q),'euclidean_norm':float(np.linalg.norm(q))}
        res.update({'classification':'M17_K7A_PLANCK_PLIKLITE_COVARIANCE_MEASURED','operator':{'repo':'heatherprince/planck-lite-py','pin':'2c0d0f67e59ce781654cf62dd7fb10757b0e60be','n_bins':613,'fisher_min_eigenvalue':float(ev[0]),'fisher_max_eigenvalue':float(ev[-1])},'S_cov':math.sqrt(max(0,s2)),'S_cov2':s2,'euclidean_norm':float(np.linalg.norm(d)),'blocks':blocks,'best_cpl':{'w0':W0,'wa':WA},'hde_c':0.6,'observational_distinguishability_claim':False,'next':'K7b nuisance/cosmological profiling'})
    except Exception as e:
        res['classification']='M17_K7A_OPERATOR_OR_OUTPUT_BLOCKED'; res['reason']=str(e)
    out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('prepare'); p.add_argument('base',type=Path); p.add_argument('out',type=Path)
    a=sp.add_parser('analyze'); a.add_argument('work',type=Path); a.add_argument('planck',type=Path); a.add_argument('status',type=Path); a.add_argument('out',type=Path)
    n=ap.parse_args(); prepare(n.base,n.out) if n.cmd=='prepare' else analyze(n.work,n.planck,n.status,n.out)
