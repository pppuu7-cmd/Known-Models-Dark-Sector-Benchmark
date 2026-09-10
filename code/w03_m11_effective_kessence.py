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
            s=f.readline()
            m=re.search(r'redshift\s+z\s*=\s*([+\-0-9.eE]+)',s,re.I)
            if m:return float(m.group(1))
    raise ValueError(f'no z header in {path}')

def load_pk(d,prefix):
    rows=[]
    for p in glob.glob(str(Path(d)/f'{prefix}*pk.dat')):
        z=zhdr(p); a=np.loadtxt(p,comments='#'); k,y=a[:,0],a[:,1]
        rows.append((z,np.exp(np.interp(np.log(K),np.log(k),np.log(y)))))
    rows.sort()
    if len(rows)!=len(Z) or not np.allclose([r[0] for r in rows],Z,rtol=0,atol=1e-10):
        raise ValueError(f'bad P grid {prefix}: {[r[0] for r in rows]}')
    return np.vstack([r[1] for r in rows])

def titles(path):
    txt=''
    with open(path) as f:
        for _ in range(40):
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
    if len(hits)!=1: raise ValueError(f'background {prefix}: {hits}')
    t=titles(hits[0]); a=np.loadtxt(hits[0],comments='#')
    iz=next(i for i,x in t.items() if x.startswith('z'))
    ih=next(i for i,x in t.items() if x.startswith('H [1/Mpc]'))
    order=np.argsort(a[:,iz])
    return np.interp(Z,a[order,iz],a[order,ih])

def response(P,H,baseP,baseH):
    return np.log(P/baseP).reshape(-1),np.log(H/baseH)

def geom(a,b):
    na=np.linalg.norm(a); nb=np.linalg.norm(b)
    if na==0 or nb==0:return {'cosine':None,'angle_deg':None,'acute_deg':None}
    c=float(np.dot(a,b)/(na*nb)); c=max(-1,min(1,c))
    return {'cosine':c,'angle_deg':float(np.degrees(np.arccos(c))),'acute_deg':float(np.degrees(np.arccos(abs(c))))}

def proj_residual(target,basis):
    den=float(np.dot(basis,basis))
    if den==0:return {'coefficient':None,'residual_fraction':None}
    c=float(np.dot(basis,target)/den)
    r=target-c*basis
    return {'coefficient':c,'residual_fraction':float(np.linalg.norm(r)/max(np.linalg.norm(target),1e-30))}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--directory',required=True); ap.add_argument('--json',required=True)
    args=ap.parse_args(); d=Path(args.directory)
    tags=['lcdm','fld0','anchor','wp','wm','cs005','cs010']
    P={t:load_pk(d,t+'_') for t in tags}; H={t:load_H(d,t+'_') for t in tags}

    refP=np.log(P['fld0']/P['lcdm']).reshape(-1); refH=np.log(H['fld0']/H['lcdm'])
    baseP=P['anchor']; baseH=H['anchor']
    rp={}; rh={}
    for t in ['wp','wm','cs005','cs010']:
        rp[t],rh[t]=response(P[t],H[t],baseP,baseH)

    hw=1e-3
    jwP=(rp['wp']-rp['wm'])/(2*hw); jwH=(rh['wp']-rh['wm'])/(2*hw)
    js05P=rp['cs005']/0.05; js05H=rh['cs005']/0.05
    js10P=rp['cs010']/0.10; js10H=rh['cs010']/0.10
    jw=np.r_[jwP,jwH]; js05=np.r_[js05P,js05H]; js10=np.r_[js10P,js10H]
    conv_rel=float(np.linalg.norm(js05-js10)/max(np.linalg.norm(js05),1e-30))
    conv_geom=geom(js05,js10)
    J=np.column_stack([jw,js05]); s=np.linalg.svd(J,compute_uv=False)

    out={
      'schema':'KMDSB.W03.M11.EffectiveKessenceStratified.v0.1',
      'scope':'effective fluid sound-speed representative; not full covariant P(phi,X) k-essence',
      'grid':{'z':Z.tolist(),'k_h_mpc':K.tolist()},
      'reference_regression':{
        'max_abs_lnP_fld0_vs_lcdm':float(np.max(np.abs(refP))),
        'max_abs_lnH_fld0_vs_lcdm':float(np.max(np.abs(refH)))
      },
      'anchor':{'w':-0.95,'cs2':1.0},
      'coordinates':{'epsilon_w_step':hw,'q_s_definition':'1-cs2 >= 0','q_s_steps':[0.05,0.10]},
      'directions':{
        'smooth_w_at_anchor':{'P':jwP.tolist(),'H':jwH.tolist(),'norm_combined':float(np.linalg.norm(jw))},
        'sound_speed_qs_h005':{'P':js05P.tolist(),'H':js05H.tolist(),'norm_combined':float(np.linalg.norm(js05))},
        'sound_speed_qs_h010':{'P':js10P.tolist(),'H':js10H.tolist(),'norm_combined':float(np.linalg.norm(js10))}
      },
      'sound_speed_convergence':{
        'relative_norm_difference':conv_rel,
        'geometry':conv_geom,
        'passes_frozen_gate':bool(conv_rel<=0.10 and conv_geom['acute_deg'] is not None and conv_geom['acute_deg']<=3.0)
      },
      'smooth_w_vs_sound_speed_geometry':geom(jw,js05),
      'sound_speed_residual_after_smooth_w_projection':proj_residual(js05,jw),
      'singular_values_combined_PH':s.tolist(),
      'sigma2_over_sigma1':float(s[1]/s[0]) if s[0]>0 else None,
      'hard_gates':{
        'reference_pass':bool(np.max(np.abs(refP))<=1e-6 and np.max(np.abs(refH))<=1e-8),
        'sound_speed_nonnull_pass':bool(np.linalg.norm(js05P)>1e-8),
        'sound_speed_convergence_pass':bool(conv_rel<=0.10 and conv_geom['acute_deg'] is not None and conv_geom['acute_deg']<=3.0)
      },
      'interpretation':'unwhitened theory-response geometry only; K7 observation-space remains open'
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
