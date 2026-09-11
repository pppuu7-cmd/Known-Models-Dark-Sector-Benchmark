#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import numpy as np

CLASS_PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PREREG='protocol/W04_M26_PBH_CDI_TRANSFER_GATE_PREREGISTRATION_v0.1.md'
A_S=2.1e-9; K0=0.05; OMEGA_CDM=0.12; RHO=2.77536627e11*OMEGA_CDM
FRACS=[1.0,0.1,0.01,0.001]

def common(root:str):
    return [f'root = {root}','output = mPk','headers = yes','format = class','lensing = no','non linear = none','modes = s','gauge = synchronous','h = 0.675','omega_b = 0.0222',f'omega_cdm = {OMEGA_CDM}','N_ur = 3.046','Omega_k = 0','YHe = 0.24','T_cmb = 2.7255',f'A_s = {A_S}','n_s = 0.965',f'k_pivot = {K0}','tau_reio = 0.054','P_k_max_h/Mpc = 100','z_pk = 0']

def fcdi(mass:float,f:float)->float:
    ps=f*mass/RHO
    return math.sqrt(ps*K0**3/(2*math.pi**2*A_S)) if f>0 else 0.0

def prepare(out:Path,mass:float):
    out.mkdir(parents=True,exist_ok=True)
    (out/'ref.ini').write_text('\n'.join(common('output/ref_')+['ic = ad'])+'\n')
    def mix(name,f):
        lines=common(f'output/{name}_')+['ic = ad,cdi',f'f_cdi = {fcdi(mass,f):.17e}','n_cdi = 4','alpha_cdi = 0','c_ad_cdi = 0']
        (out/f'{name}.ini').write_text('\n'.join(lines)+'\n')
    mix('zero',0.0)
    for i,f in enumerate(FRACS): mix(f'f{i}',f)
    (out/'manifest.json').write_text(json.dumps({'schema':'KMDSB.M26.PBHCDITransfer.Manifest.v1','class_pin':CLASS_PIN,'preregistration':PREREG,'mass_Msun':mass,'fractions':FRACS,'f_cdi':[fcdi(mass,f) for f in FRACS]},indent=2,sort_keys=True)+'\n')

def load_pk(root:Path,prefix:str):
    cand=sorted((root/'output').glob(f'{prefix}_*pk.dat'))+sorted((root/'output').glob(f'{prefix}_pk.dat'))
    uniq=[]
    for p in cand:
        if p not in uniq: uniq.append(p)
    if len(uniq)!=1: raise RuntimeError(f'{prefix} pk candidates={uniq}')
    rows=[]
    for ln in uniq[0].read_text(errors='replace').splitlines():
        s=ln.strip()
        if not s or s.startswith('#'): continue
        try: row=[float(x.replace('D','E')) for x in s.split()]
        except: continue
        if len(row)>=2 and all(math.isfinite(x) for x in row[:2]): rows.append(row[:2])
    a=np.asarray(rows,float)
    if a.shape[0]<20: raise RuntimeError(f'bad pk {uniq[0]} {a.shape}')
    return a

def symdiff(a,b):
    x=a[:,0]; xr=b[:,0]; lo=max(x.min(),xr.min()); hi=min(x.max(),xr.max()); m=(x>=lo)&(x<=hi); x=x[m]; y=a[m,1]; yr=np.interp(x,xr,b[:,1]); floor=1e-300; r=2*(y-yr)/(np.abs(y)+np.abs(yr)+floor); return float(np.percentile(np.abs(r),95))

def analyze(root:Path,status_path:Path,manifest_path:Path,out:Path):
    st=json.loads(status_path.read_text()); man=json.loads(manifest_path.read_text()); mass=float(man['mass_Msun'])
    r={'schema':'KMDSB.M26.PBHCDITransfer.v1','preregistration':PREREG,'class_pin':CLASS_PIN,'mass_Msun':mass,'status':st,'fractions':FRACS,'K1_promoted':False,'K4_promoted':False,'physical_falsification':False}
    required=['ref','zero']+[f'f{i}' for i in range(len(FRACS))]
    if any(st.get(k)!=0 for k in required):
        r['classification']='M26_PBH_CDI_TRANSFER_PROVIDER_BLOCKED'; r['failed_status_keys']=[k for k in required if st.get(k)!=0]; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); return
    ref=load_pk(root,'ref'); zero=load_pk(root,'zero'); r['zero_p95_symmetric_relative_difference']=symdiff(zero,ref)
    plateaus=[]; cases={}; all_white=True; all_pos=True
    for i,f in enumerate(FRACS):
        a=load_pk(root,f'f{i}'); x=a[:,0]; y=a[:,1]; yr=np.interp(x,ref[:,0],ref[:,1]); d=y-yr; m=(x>=5)&(x<=50)&(d>0)
        if m.sum()<5:
            cases[str(f)]={'valid':False,'n_highk':int(m.sum())}; all_white=False; all_pos=False; plateaus.append(float('nan')); continue
        xx=x[m]; dd=d[m]; slope=float(np.polyfit(np.log(xx),np.log(dd),1)[0]); med=float(np.median(dd)); cases[str(f)]={'valid':True,'n_highk':int(m.sum()),'median_delta_P':med,'highk_log_slope':slope,'white_slope_pass':abs(slope)<=0.15}; plateaus.append(med); all_white &= abs(slope)<=0.15; all_pos &= med>0
    arr=np.asarray(plateaus,float); valid=np.all(np.isfinite(arr)) and np.all(arr>0)
    fslope=float(np.polyfit(np.log(np.asarray(FRACS)),np.log(arr),1)[0]) if valid else None
    r['cases']=cases; r['plateau_medians']=plateaus; r['fraction_scaling_exponent']=fslope; r['fraction_scaling_pass']=bool(valid and abs(fslope-1)<=0.05); r['zero_identity_pass']=r['zero_p95_symmetric_relative_difference']<=1e-10
    ok=r['zero_identity_pass'] and all_white and all_pos and r['fraction_scaling_pass']
    r['classification']='M26_PBH_CDI_TRANSFER_PASS_WITH_SCOPE' if ok else 'M26_PBH_CDI_TRANSFER_NOT_ESTABLISHED'
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('prepare'); p.add_argument('out',type=Path); p.add_argument('mass',type=float)
    a=sp.add_parser('analyze'); a.add_argument('root',type=Path); a.add_argument('status',type=Path); a.add_argument('manifest',type=Path); a.add_argument('out',type=Path)
    x=ap.parse_args(); prepare(x.out,x.mass) if x.cmd=='prepare' else analyze(x.root,x.status,x.manifest,x.out)
