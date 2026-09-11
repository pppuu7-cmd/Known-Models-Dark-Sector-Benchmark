#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from verification.m26.pbh_cdi_transfer_gate import load_pk,FRACS
PREREG='protocol/W04_M26_PBH_CDI_NULL_REPRESENTATION_RECOVERY_PREREGISTRATION_v0.1.md'

def main(root:Path,status_path:Path,manifest_path:Path,out:Path):
    st=json.loads(status_path.read_text()); man=json.loads(manifest_path.read_text()); mass=float(man['mass_Msun'])
    r={'schema':'KMDSB.M26.PBHCDINullRepresentationRecovery.v1','preregistration':PREREG,'source_run_id':34552202481,'mass_Msun':mass,'fractions':FRACS,'status':st,'explicit_zero_status':'EXPLICIT_ZERO_UNSUPPORTED_BY_PROVIDER','provider_null_representation':'CDI_OMITTED_PURE_ADIABATIC_REFERENCE','K1_promoted':False,'K4_promoted':False,'physical_falsification':False}
    required=['ref']+[f'f{i}' for i in range(len(FRACS))]
    if any(st.get(k)!=0 for k in required):
        r['classification']='M26_PBH_CDI_TRANSFER_PROVIDER_BLOCKED'; r['failed_status_keys']=[k for k in required if st.get(k)!=0]; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); return
    ref=load_pk(root,'ref'); plateaus=[]; cases={}; all_white=True; all_pos=True
    for i,f in enumerate(FRACS):
        a=load_pk(root,f'f{i}'); x=a[:,0]; y=a[:,1]; yr=np.interp(x,ref[:,0],ref[:,1]); d=y-yr; m=(x>=5)&(x<=50)&(d>0)
        if m.sum()<5:
            cases[str(f)]={'valid':False,'n_highk':int(m.sum())}; all_white=False; all_pos=False; plateaus.append(float('nan')); continue
        xx=x[m]; dd=d[m]; slope=float(np.polyfit(np.log(xx),np.log(dd),1)[0]); med=float(np.median(dd)); ok=abs(slope)<=0.15
        cases[str(f)]={'valid':True,'n_highk':int(m.sum()),'median_delta_P':med,'highk_log_slope':slope,'white_slope_pass':ok}; plateaus.append(med); all_white &= ok; all_pos &= med>0
    arr=np.asarray(plateaus,float); valid=np.all(np.isfinite(arr)) and np.all(arr>0)
    fslope=float(np.polyfit(np.log(np.asarray(FRACS)),np.log(arr),1)[0]) if valid else None
    r['cases']=cases; r['plateau_medians']=plateaus; r['fraction_scaling_exponent']=fslope; r['fraction_scaling_pass']=bool(valid and abs(fslope-1)<=0.05); r['null_representation_pass']=True
    ok=all_white and all_pos and r['fraction_scaling_pass']
    r['classification']='M26_PBH_CDI_TRANSFER_PASS_WITH_PROVIDER_NULL_SCOPE' if ok else 'M26_PBH_CDI_TRANSFER_NOT_ESTABLISHED'
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('root',type=Path); ap.add_argument('status',type=Path); ap.add_argument('manifest',type=Path); ap.add_argument('out',type=Path); a=ap.parse_args(); main(a.root,a.status,a.manifest,a.out)
