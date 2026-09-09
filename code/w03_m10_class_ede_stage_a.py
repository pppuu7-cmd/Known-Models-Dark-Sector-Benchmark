#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json, math, re
from pathlib import Path
import numpy as np

Z=np.array([0.295,0.51,0.706,0.934,1.317,1.491,2.33],float)
KLOW=np.array([0.001,0.003,0.01,0.03,0.1],float)
KSHAPE=np.array([0.001,0.003,0.006,0.01,0.02,0.03,0.05,0.08,0.1,0.2,0.3,0.5,0.8,1.0],float)
ZSHAPE=0.51
TARGET_ZC_LOG10=3.5
REL_GATE=0.10
ANGLE_GATE=3.0

CASES={"f005":0.005,"f010":0.01,"f030":0.03,"f050":0.05}


def header_titles(path:Path):
    txt=''
    with path.open() as f:
        for _ in range(50):
            line=f.readline()
            if not line: break
            if line.startswith('#'): txt += ' '+line[1:].strip()
            else: break
    ms=list(re.finditer(r'(?:^|\s)(\d+):',txt))
    out={}
    for i,m in enumerate(ms):
        out[int(m.group(1))-1]=txt[m.end():(ms[i+1].start() if i+1<len(ms) else len(txt))].strip()
    return out


def find_col(titles,*needles):
    for i,t in titles.items():
        low=t.lower().replace(' ','')
        if all(n.lower().replace(' ','') in low for n in needles): return i
    raise KeyError(f'column not found needles={needles}; titles={titles}')


def zhdr(path:Path):
    with path.open() as f:
        for _ in range(30):
            s=f.readline(); m=re.search(r'redshift\s+z\s*=\s*([+\-0-9.eE]+)',s,re.I)
            if m: return float(m.group(1))
    raise ValueError(f'no z header {path}')


def load_pk(d:Path,prefix:str,kvals:np.ndarray):
    rows=[]
    for pstr in glob.glob(str(d/f'{prefix}*pk.dat')):
        p=Path(pstr); z=zhdr(p); a=np.loadtxt(p,comments='#'); k,y=a[:,0],a[:,1]
        if kvals.min()<k.min() or kvals.max()>k.max():
            raise ValueError(f'k request outside {p}: [{k.min()},{k.max()}]')
        yi=np.exp(np.interp(np.log(kvals),np.log(k),np.log(y)))
        rows.append((z,yi))
    rows.sort(key=lambda x:x[0])
    if not rows: raise ValueError(f'no pk files {prefix}')
    return np.array([x[0] for x in rows]),np.vstack([x[1] for x in rows])


def frozen_pk(d:Path,prefix:str,kvals:np.ndarray):
    zs,p=load_pk(d,prefix,kvals)
    if len(zs)!=len(Z) or not np.allclose(zs,Z,rtol=0,atol=5e-6):
        raise ValueError(f'bad frozen z grid {prefix}: {zs}')
    return p


def load_bg(d:Path,prefix:str):
    hits=list(d.glob(f'{prefix}*background.dat'))
    if len(hits)!=1: raise ValueError(f'background {prefix}: {hits}')
    p=hits[0]; t=header_titles(p); a=np.loadtxt(p,comments='#')
    iz=find_col(t,'z')
    ih=find_col(t,'H','1/Mpc')
    order=np.argsort(a[:,iz])
    return p,t,a,order,iz,ih


def load_H(d,prefix):
    _,_,a,order,iz,ih=load_bg(d,prefix)
    return np.interp(Z,a[order,iz],a[order,ih])


def response_L(d,prefix,ref='lcdm_'):
    P=frozen_pk(d,prefix,KLOW); P0=frozen_pk(d,ref,KLOW)
    H=load_H(d,prefix); H0=load_H(d,ref)
    return np.log(P/P0).reshape(-1),np.log(H/H0)


def response_S(d,prefix,ref='lcdm_'):
    zs,P=load_pk(d,prefix,KSHAPE); zs0,P0=load_pk(d,ref,KSHAPE)
    if not np.allclose(zs,zs0,rtol=0,atol=5e-6): raise ValueError('shape z grids differ')
    i=int(np.argmin(np.abs(zs-ZSHAPE)))
    if abs(zs[i]-ZSHAPE)>5e-6: raise ValueError(f'missing z={ZSHAPE}')
    r=np.log(P[i]/P0[i]); return r-float(np.mean(r[:2]))


def achieved_ede_peak(d:Path,prefix:str):
    p,t,a,_,iz,_=load_bg(d,prefix)
    iphi=find_col(t,"phi'_scf")
    ive=find_col(t,'V_e_scf')
    irc=find_col(t,'rho_crit')
    z=a[:,iz]; scale=1.0/(1.0+z)
    frac=((a[:,iphi]**2/(2.0*scale**2)+a[:,ive])/3.0)/a[:,irc]
    if not np.all(np.isfinite(frac)): raise ValueError('nonfinite fEDE fraction')
    j=int(np.argmax(frac)); zpeak=float(z[j]); fpeak=float(frac[j])
    # Local parabolic refinement in x=ln(1+z), only when peak is interior and concave.
    refined=False
    if 0<j<len(z)-1:
        inds=np.array([j-1,j,j+1]); x=np.log1p(z[inds]); y=frac[inds]
        try:
            q=np.polyfit(x,y,2)
            if q[0] < 0:
                xv=-q[1]/(2*q[0])
                if min(x)<=xv<=max(x):
                    yr=float(np.polyval(q,xv)); zr=float(np.expm1(xv))
                    if yr>=0 and zr>0:
                        fpeak,zpeak,refined=yr,zr,True
        except Exception:
            pass
    return {'background_file':p.name,'fEDE_achieved':fpeak,'z_c_achieved':zpeak,'log10z_c_achieved':float(np.log10(zpeak)),'quadratic_refined':refined}


def geometry(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float); na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
    if na<1e-14 or nb<1e-14:
        return {'state':'NEAR_NULL','norm_a':na,'norm_b':nb,'relative_l2':None,'angle_deg':None,'pass':True}
    rel=float(np.linalg.norm(a-b)/max(na,nb)); c=float(np.dot(a,b)/(na*nb)); c=max(-1,min(1,c)); ang=float(np.degrees(np.arccos(c)))
    return {'state':'DEFINED','norm_a':na,'norm_b':nb,'relative_l2':rel,'angle_deg':ang,'pass':bool(rel<=REL_GATE and ang<=ANGLE_GATE)}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--directory',required=True); ap.add_argument('--json',required=True); args=ap.parse_args(); d=Path(args.directory)
    # Ensure same-solver Lambda reference has all required outputs.
    refP=frozen_pk(d,'lcdm_',KLOW); refH=load_H(d,'lcdm_'); refS=response_S(d,'lcdm_','lcdm_')
    ref={'finite':bool(np.all(np.isfinite(refP)) and np.all(np.isfinite(refH)) and np.all(np.isfinite(refS))),
         'self_max_abs_shape':float(np.max(np.abs(refS)))}

    cases={}; responses={}
    for tag,target in CASES.items():
        peak=achieved_ede_peak(d,tag+'_')
        f_tol=max(1e-4,0.01*target)
        peak['target_fEDE']=target; peak['target_log10z_c']=TARGET_ZC_LOG10; peak['fEDE_abs_error']=abs(peak['fEDE_achieved']-target); peak['log10z_c_abs_error']=abs(peak['log10z_c_achieved']-TARGET_ZC_LOG10)
        peak['fEDE_tolerance']=f_tol; peak['shooting_pass']=bool(peak['fEDE_abs_error']<=f_tol and peak['log10z_c_abs_error']<=0.015)
        P,H=response_L(d,tag+'_'); S=response_S(d,tag+'_')
        responses[tag]={'P':P,'H':H,'S':S}
        cases[tag]={**peak,'response_max_abs':{'P':float(np.max(np.abs(P))),'H':float(np.max(np.abs(H))),'S':float(np.max(np.abs(S)))},'response_norms':{'P':float(np.linalg.norm(P)),'H':float(np.linalg.norm(H)),'S':float(np.linalg.norm(S))}}

    t1,t2='f005','f010'; f1,f2=CASES[t1],CASES[t2]
    conv={k:geometry(responses[t1][k]/f1,responses[t2][k]/f2) for k in ('P','H','S')}
    local_pass=all(x['pass'] for x in conv.values())
    shooting_pass=all(c['shooting_pass'] for c in cases.values())
    classification='PASS_WITH_SCOPE' if ref['finite'] and shooting_pass and local_pass else ('BLOCKED_NUMERICAL_SHOOTING' if not shooting_pass else 'PARTIAL_LOCAL_RESPONSE')
    out={
      'schema':'KMDSB.W03.M10.CLASS_EDE.StageA.v0.1',
      'solver':'mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97',
      'branch':{'n_scf':3.0,'thetai_scf':2.6,'CC_scf':1.0,'target_log10z_c':3.5,'coordinate':'fEDE>0'},
      'reference':ref,
      'cases':cases,
      'local_convergence_pair':[f1,f2],
      'local_convergence':conv,
      'local_tangent_pass_with_scope':bool(local_pass),
      'all_shooting_pass':bool(shooting_pass),
      'classification':classification,
      'frozen_grids':{'z':Z.tolist(),'k_low_h_mpc':KLOW.tolist(),'z_shape':ZSHAPE,'k_shape_h_mpc':KSHAPE.tolist()},
      'anti_overclaim':['Stage A is implementation and unwhitened theory-response control only','finite grid is not B8 evidence','M10 does not overwrite blocked M09']
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))

if __name__=='__main__': main()
