#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path

BANDS={
  'low':(2,29),
  'acoustic':(30,500),
  'mid':(501,1200),
  'damping':(1201,2500),
}
CASES=['f2','f3','f4']
CHANNELS={'TT':1,'EE':2,'TE':3}


def load_cl(root:Path, case:str):
    fs=sorted(root.glob(f'{case}*_cl.dat'))
    if len(fs)!=1: raise RuntimeError(f'{root}/{case}: {fs}')
    rows=[]
    for line in fs[0].read_text(errors='replace').splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        vals=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
        if len(vals)>=4 and all(math.isfinite(x) for x in vals): rows.append(vals)
    if len(rows)<3: raise RuntimeError(f'invalid {fs[0]}')
    return rows


def norm(v): return math.sqrt(sum(x*x for x in v))

def r2(a,r,col, lo=2, hi=2500):
    av=[x[col] for x in a if lo<=int(round(x[0]))<=hi]
    rv=[x[col] for x in r if lo<=int(round(x[0]))<=hi]
    ae=[int(round(x[0])) for x in a if lo<=int(round(x[0]))<=hi]
    re=[int(round(x[0])) for x in r if lo<=int(round(x[0]))<=hi]
    if ae!=re or not av: raise RuntimeError(f'ell grid mismatch {lo}-{hi}')
    d=[x-y for x,y in zip(av,rv)]
    return norm(d)/max(norm(rv),1e-300)

def residual_energy_share(a,r,col,lo,hi,total_lo=2,total_hi=2500):
    amap={int(round(x[0])):x[col] for x in a}
    rmap={int(round(x[0])):x[col] for x in r}
    ells=sorted(set(amap)&set(rmap))
    total=sum((amap[l]-rmap[l])**2 for l in ells if total_lo<=l<=total_hi)
    band=sum((amap[l]-rmap[l])**2 for l in ells if lo<=l<=hi)
    if total<=0: return 0.0
    return band/total

def close(a,b): return abs(a-b)<=max(1e-15,1e-12*max(abs(a),abs(b),1e-300))

def category(shares):
    best=max(shares,key=shares.get)
    if shares[best]>=0.70:
        return {'low':'LOW_LOCALIZED','acoustic':'ACOUSTIC_LOCALIZED','mid':'MID_LOCALIZED','damping':'DAMPING_LOCALIZED'}[best],best
    return 'BROAD_OR_MULTIBAND',best

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('artifact',type=Path); ap.add_argument('canonical',type=Path); ap.add_argument('out',type=Path); a=ap.parse_args()
    canon=json.loads(a.canonical.read_text())
    branches={'NDF15_default':a.artifact/'ndf_out','RK_evolver0':a.artifact/'rk_out'}
    data={bn:{c:load_cl(root,c) for c in ['ref']+CASES} for bn,root in branches.items()}
    out={'schema':'KMDSB.W04.M21.CMBEllBandLocalization.v0.1','protocol':'protocol/W04_M21_CMB_ELL_BAND_LOCALIZATION_v0.1.md','parent_run':34542162543,'parent_head':'25a74539371fe7bc9304df9fe2e51ff4be050a79','parent_artifact_id':10178334419,'parent_artifact_digest':'sha256:640472f79c7e55d9edf4ed39ed35d4ab692fcf4700fad4d50edbad0642f7c65c','branches':{},'controls':{},'K1_promoted':False,'physical_falsification':False}
    controls_ok=True
    for bn in branches:
        ref=data[bn]['ref']; bo={'channels':{}}
        for ch,col in CHANNELS.items():
            co={'cases':{},'f3_energy_shares':{},'excursion_factors':{}}
            for case in CASES:
                full=r2(data[bn][case],ref,col)
                expected=canon['branches'][bn]['points'][case][ch]['R2']
                ok=close(full,expected); controls_ok &= ok
                bands={b:r2(data[bn][case],ref,col,*rng) for b,rng in BANDS.items()}
                co['cases'][case]={'full_R2':full,'canonical_full_R2':expected,'full_reproduction_pass':ok,'band_R2':bands}
            for b,(lo,hi) in BANDS.items():
                co['f3_energy_shares'][b]=residual_energy_share(data[bn]['f3'],ref,col,lo,hi)
                den=max(co['cases']['f2']['band_R2'][b],co['cases']['f4']['band_R2'][b],1e-300)
                co['excursion_factors'][b]=co['cases']['f3']['band_R2'][b]/den
            share_sum=sum(co['f3_energy_shares'].values()); sok=abs(share_sum-1.0)<=1e-12; controls_ok &= sok
            cat,best=category(co['f3_energy_shares']); co['localization_category']=cat; co['largest_energy_band']=best; co['energy_share_sum']=share_sum; co['energy_share_sum_pass']=sok
            bo['channels'][ch]=co
        out['branches'][bn]=bo
    direct={}
    for case in ['ref']+CASES:
        direct[case]={}
        for ch,col in CHANNELS.items():
            val=r2(data['RK_evolver0'][case],data['NDF15_default'][case],col)
            exp=canon['direct_RK_vs_NDF15'][case][ch]['R2']; ok=close(val,exp); controls_ok &= ok
            direct[case][ch]={'R2':val,'canonical_R2':exp,'reproduction_pass':ok}
    out['direct_RK_vs_NDF15']=direct
    cross={}; strong=[]
    for ch in CHANNELS:
        n=out['branches']['NDF15_default']['channels'][ch]; r=out['branches']['RK_evolver0']['channels'][ch]
        consistent=(n['localization_category']==r['localization_category'] and n['largest_energy_band']==r['largest_energy_band'])
        cross[ch]={'status':'CONSISTENT' if consistent else 'BRANCH_DEPENDENT','NDF15_category':n['localization_category'],'RK_category':r['localization_category'],'NDF15_largest_band':n['largest_energy_band'],'RK_largest_band':r['largest_energy_band']}
        for b in BANDS:
            if n['excursion_factors'][b]>=10 and r['excursion_factors'][b]>=10: strong.append({'channel':ch,'band':b,'E_NDF15':n['excursion_factors'][b],'E_RK':r['excursion_factors'][b]})
    out['cross_branch_localization']=cross; out['strong_excursion_bands']=strong
    out['controls']['canonical_full_metric_reproduction']=controls_ok
    out['classification']='M21_CMB_ELL_BAND_LOCALIZATION_PASS_WITH_SCOPE' if controls_ok else 'M21_CMB_ELL_BAND_LOCALIZATION_INVALID_EVIDENCE'
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':out['classification'],'cross_branch_localization':cross,'strong_excursion_bands':strong},indent=2))
    if not controls_ok: raise SystemExit(1)
if __name__=='__main__': main()
