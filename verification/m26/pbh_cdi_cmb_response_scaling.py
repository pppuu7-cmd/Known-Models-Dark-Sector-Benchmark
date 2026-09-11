#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from verification.m26.pbh_cdi_transfer_gate import fcdi

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PREREG='protocol/W04_M26_PBH_CDI_CMB_RESPONSE_SCALING_PREREGISTRATION_v0.1.md'
FRACS=[1.0,0.1,0.01,0.001]

def common(root:str):
    return [f'root = output/{root}_','output = tCl,pCl,mPk','headers = yes','format = class','lensing = no','non linear = none','modes = s','gauge = synchronous','h = 0.675','omega_b = 0.0222','omega_cdm = 0.12','N_ur = 3.046','Omega_k = 0','YHe = 0.24','T_cmb = 2.7255','A_s = 2.1e-9','n_s = 0.965','k_pivot = 0.05','tau_reio = 0.054','l_max_scalars = 2500','P_k_max_h/Mpc = 100','z_pk = 0']

def prepare(out:Path,mass:float):
    out.mkdir(parents=True,exist_ok=True)
    (out/'ref.ini').write_text('\n'.join(common('ref')+['ic = ad'])+'\n')
    for i,f in enumerate(FRACS):
        lines=common(f'f{i}')+['ic = ad,cdi',f'f_cdi = {fcdi(mass,f):.17e}','n_cdi = 4','alpha_cdi = 0','c_ad_cdi = 0']
        (out/f'f{i}.ini').write_text('\n'.join(lines)+'\n')
    (out/'manifest.json').write_text(json.dumps({'schema':'KMDSB.M26.PBHCDICMBResponse.Manifest.v1','class_pin':PIN,'preregistration':PREREG,'mass_Msun':mass,'fractions':FRACS,'f_cdi':[fcdi(mass,f) for f in FRACS]},indent=2,sort_keys=True)+'\n')

def table(path:Path):
    rows=[]
    for ln in path.read_text(errors='replace').splitlines():
        s=ln.strip()
        if not s or s.startswith('#'): continue
        try: row=[float(x.replace('D','E')) for x in s.split()]
        except: continue
        if len(row)>=2 and all(math.isfinite(x) for x in row): rows.append(row)
    a=np.asarray(rows,float)
    if a.ndim!=2 or a.shape[0]<5: raise RuntimeError(f'invalid table {path} {a.shape}')
    return a[np.argsort(a[:,0])]

def findout(root:Path,prefix:str,suffix:str):
    hits=sorted((root/'output').glob(f'{prefix}_*{suffix}.dat'))+sorted((root/'output').glob(f'{prefix}_{suffix}.dat'))
    uniq=[]
    for p in hits:
        if p not in uniq: uniq.append(p)
    if len(uniq)!=1: raise RuntimeError(f'{prefix}/{suffix}: {uniq}')
    return table(uniq[0])

def relnorm(model:np.ndarray,ref:np.ndarray,col:int):
    lo=max(model[:,0].min(),ref[:,0].min()); hi=min(model[:,0].max(),ref[:,0].max())
    m=(model[:,0]>=lo)&(model[:,0]<=hi)
    x=model[m,0]; y=model[m,col]; yr=np.interp(x,ref[:,0],ref[:,col])
    return float(np.linalg.norm(y-yr)/max(float(np.linalg.norm(yr)),1e-300))

def analyze(root:Path,status:Path,manifest:Path,out:Path):
    st=json.loads(status.read_text()); man=json.loads(manifest.read_text()); mass=float(man['mass_Msun'])
    req=['ref']+[f'f{i}' for i in range(4)]
    r={'schema':'KMDSB.M26.PBHCDICMBResponseScaling.v1','preregistration':PREREG,'class_pin':PIN,'mass_Msun':mass,'fractions':FRACS,'status':st,'K1_promoted':False,'K4_promoted':False,'physical_falsification':False}
    if any(st.get(k)!=0 for k in req):
        r['classification']='M26_PBH_CDI_CMB_RESPONSE_PROVIDER_BLOCKED'; r['failed_status_keys']=[k for k in req if st.get(k)!=0]; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); return
    refcl=findout(root,'ref','cl'); refpk=findout(root,'ref','pk')
    vals={k:[] for k in ['TT','EE','TE','Pk']}
    for i,f in enumerate(FRACS):
        cl=findout(root,f'f{i}','cl'); pk=findout(root,f'f{i}','pk')
        vals['TT'].append(relnorm(cl,refcl,1)); vals['EE'].append(relnorm(cl,refcl,2)); vals['TE'].append(relnorm(cl,refcl,3)); vals['Pk'].append(relnorm(pk,refpk,1))
    blocks={}; ok=True
    for k,y0 in vals.items():
        y=np.asarray(y0,float); positive=bool(np.all(np.isfinite(y)) and np.all(y>0)); mono=bool(np.all(y[1:]<y[:-1])) if positive else False
        slope=float(np.polyfit(np.log(np.asarray(FRACS)),np.log(y),1)[0]) if positive else None
        passed=bool(positive and mono and abs(slope-1)<=0.05); ok &= passed
        blocks[k]={'responses':y0,'fraction_loglog_slope':slope,'positive':positive,'monotonic':mono,'pass':passed}
    r['blocks']=blocks; r['classification']='M26_PBH_CDI_CMB_RESPONSE_SCALING_PASS_WITH_SCOPE' if ok else 'M26_PBH_CDI_CMB_RESPONSE_SCALING_NOT_ESTABLISHED'
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('prepare'); p.add_argument('out',type=Path); p.add_argument('mass',type=float)
    a=sp.add_parser('analyze'); a.add_argument('root',type=Path); a.add_argument('status',type=Path); a.add_argument('manifest',type=Path); a.add_argument('out',type=Path)
    x=ap.parse_args(); prepare(x.out,x.mass) if x.cmd=='prepare' else analyze(x.root,x.status,x.manifest,x.out)
