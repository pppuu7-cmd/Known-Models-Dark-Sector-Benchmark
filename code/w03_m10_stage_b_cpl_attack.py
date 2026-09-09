#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json, re
from pathlib import Path
import numpy as np

Z=np.array([0.295,0.51,0.706,0.934,1.317,1.491,2.33],float)
KLOW=np.array([0.001,0.003,0.01,0.03,0.1],float)
KSHAPE=np.array([0.001,0.003,0.006,0.01,0.02,0.03,0.05,0.08,0.1,0.2,0.3,0.5,0.8,1.0],float)
ZSHAPE=0.51
HF=5e-4


def titles(path):
    txt=''
    with open(path) as f:
        for _ in range(50):
            s=f.readline()
            if not s: break
            if s.startswith('#'): txt+=' '+s[1:].strip()
            else: break
    ms=list(re.finditer(r'(?:^|\s)(\d+):',txt)); out={}
    for i,m in enumerate(ms): out[int(m.group(1))-1]=txt[m.end():(ms[i+1].start() if i+1<len(ms) else len(txt))].strip()
    return out


def col(t,*needles):
    for i,s in t.items():
        q=s.lower().replace(' ','')
        if all(n.lower().replace(' ','') in q for n in needles): return i
    raise KeyError((needles,t))


def zhdr(path):
    with open(path) as f:
        for _ in range(30):
            s=f.readline(); m=re.search(r'redshift\s+z\s*=\s*([+\-0-9.eE]+)',s,re.I)
            if m:return float(m.group(1))
    raise ValueError(path)


def load_pk(d,prefix,kvals):
    rows=[]
    for p in glob.glob(str(Path(d)/f'{prefix}*pk.dat')):
        a=np.loadtxt(p,comments='#'); k,y=a[:,0],a[:,1]; z=zhdr(p)
        yi=np.exp(np.interp(np.log(kvals),np.log(k),np.log(y)))
        rows.append((z,yi))
    rows.sort();
    if not rows: raise ValueError(f'no P {prefix}')
    return np.array([x[0] for x in rows]),np.vstack([x[1] for x in rows])


def pkf(d,prefix,kvals):
    zs,p=load_pk(d,prefix,kvals)
    if len(zs)!=7 or not np.allclose(zs,Z,rtol=0,atol=5e-6): raise ValueError(f'bad z {prefix}: {zs}')
    return p


def Hf(d,prefix):
    hits=list(Path(d).glob(f'{prefix}*background.dat'))
    if len(hits)!=1: raise ValueError((prefix,hits))
    t=titles(hits[0]); a=np.loadtxt(hits[0],comments='#'); iz=col(t,'z'); ih=col(t,'H','1/Mpc'); o=np.argsort(a[:,iz])
    return np.interp(Z,a[o,iz],a[o,ih])


def response(d,prefix,ref='lcdm_'):
    P=np.log(pkf(d,prefix,KLOW)/pkf(d,ref,KLOW)).reshape(-1)
    H=np.log(Hf(d,prefix)/Hf(d,ref))
    zs,p=load_pk(d,prefix,KSHAPE); zs0,p0=load_pk(d,ref,KSHAPE)
    if not np.allclose(zs,zs0,rtol=0,atol=5e-6): raise ValueError('shape z mismatch')
    i=int(np.argmin(np.abs(zs-ZSHAPE)))
    if abs(zs[i]-ZSHAPE)>5e-6: raise ValueError('shape z missing')
    r=np.log(p[i]/p0[i]); S=r-np.mean(r[:2])
    return {'P':P,'H':H,'S':S}


def frac(target,pred):
    nt=float(np.linalg.norm(target)); return float(np.linalg.norm(target-pred)/nt) if nt>1e-30 else None


def angle(target,pred):
    nt=float(np.linalg.norm(target)); npd=float(np.linalg.norm(pred))
    if nt<1e-30 or npd<1e-30:return None
    c=float(np.dot(target,pred)/(nt*npd)); c=max(-1,min(1,c)); return float(np.degrees(np.arccos(c)))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--directory',required=True); ap.add_argument('--json',required=True); args=ap.parse_args(); d=args.directory
    # Same-solver CPL zero point must bridge pure Lambda.
    c0=response(d,'cpl0_')
    bridge={'max_abs_lnP':float(np.max(np.abs(c0['P']))),'max_abs_lnH':float(np.max(np.abs(c0['H']))),'max_abs_shape':float(np.max(np.abs(c0['S'])))}
    bridge['pass']=bool(bridge['max_abs_lnP']<=1e-6 and bridge['max_abs_lnH']<=1e-6)

    # Frozen M10 target: componentwise mean of r/f at f=.005,.01.
    e1=response(d,'f005_'); e2=response(d,'f010_')
    target={k:0.5*(e1[k]/0.005+e2[k]/0.01) for k in ('P','H','S')}

    ep=response(d,'e0p_'); em=response(d,'e0m_'); apv=response(d,'wap_'); amv=response(d,'wam_')
    J={}
    for k in ('P','H','S'):
        j0=(ep[k]-em[k])/(2*HF); ja=(apv[k]-amv[k])/(2*HF); J[k]=np.column_stack([j0,ja])
    JL=np.vstack([J['P'],J['H']]); tL=np.r_[target['P'],target['H']]
    beta,*_=np.linalg.lstsq(JL,tL,rcond=None)
    pred={k:J[k]@beta for k in ('P','H','S')}
    primary={
      'beta_L_per_unit_fEDE':beta.tolist(),
      'residual_fraction':{k:frac(target[k],pred[k]) for k in ('P','H','S')},
      'angle_deg':{k:angle(target[k],pred[k]) for k in ('P','H','S')},
      'L_residual_fraction':frac(tL,np.r_[pred['P'],pred['H']]),
      'L_angle_deg':angle(tL,np.r_[pred['P'],pred['H']])
    }
    betaS,*_=np.linalg.lstsq(J['S'],target['S'],rcond=None); predS=J['S']@betaS
    secondary={'beta_S_only':betaS.tolist(),'S_residual_fraction':frac(target['S'],predS),'S_angle_deg':angle(target['S'],predS)}
    sL=np.linalg.svd(JL,compute_uv=False); sS=np.linalg.svd(J['S'],compute_uv=False)
    out={
      'schema':'KMDSB.W03.M10.StageB.CPLAttack.v0.1',
      'solver':'mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97',
      'cpl_step':HF,
      'cpl_zero_bridge':bridge,
      'target_norms':{k:float(np.linalg.norm(target[k])) for k in target},
      'cpl_rank_geometry':{'L_singular_values':sL.tolist(),'L_sigma2_over_sigma1':float(sL[1]/sL[0]),'S_singular_values':sS.tolist(),'S_sigma2_over_sigma1':float(sS[1]/sS[0]) if sS[0]>0 else None},
      'primary_L_fit_crosschannel_test':primary,
      'secondary_S_only_projection':secondary,
      'classification':'PASS_WITH_SCOPE' if bridge['pass'] else 'BLOCKED_REFERENCE_BRIDGE',
      'interpretation':'unwhitened same-solver theory-response manifold comparison; primary coefficients are fit only on P+H and transferred without refit to S',
      'anti_overclaim':['no observation-space claim','S-only fit is diagnostic and cannot replace the shared L-fit coefficients','no threshold for novelty is added after output']
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))

if __name__=='__main__':main()
