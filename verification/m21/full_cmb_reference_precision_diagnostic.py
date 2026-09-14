#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, json, math
from pathlib import Path

HERE=Path(__file__).resolve().parent

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod); return mod
INT=load_module('m21_int',HERE/'integrator_branch_diagnostic.py')
BAND=load_module('m21_band',HERE/'cmb_ell_band_localization.py')
PARENT_EMAX=534.8355868817356
CASES=['f2','f3','f4']
CHANNELS=['TT','EE','TE']
COL={'TT':1,'EE':2,'TE':3}

def direct(new:Path,parent_rk:Path):
    out={}
    for case in ['ref']+CASES:
        a=INT.files(new,case); r=INT.files(parent_rk,case)
        out[case]={
          'TT':INT.cl_metric(a['cl'],r['cl'],1),
          'EE':INT.cl_metric(a['cl'],r['cl'],2),
          'TE':INT.cl_metric(a['cl'],r['cl'],3),
          'Pk':INT.overlap_metric(a['pk'],r['pk'],0,1,logx=True),
          'H':INT.overlap_metric(a['bg'],r['bg'],0,3,logx=False),
        }
    return out

def bands(root:Path):
    out={}; ref=BAND.load_cl(root,'ref')
    cases={c:BAND.load_cl(root,c) for c in CASES}
    for ch,col in BAND.CHANNELS.items():
        cc={'f3_energy_shares':{},'excursion_factors':{},'cases':{}}
        for c in CASES:
            cc['cases'][c]={'band_R2':{b:BAND.r2(cases[c],ref,col,*rng) for b,rng in BAND.BANDS.items()}}
        for b,(lo,hi) in BAND.BANDS.items():
            cc['f3_energy_shares'][b]=BAND.residual_energy_share(cases['f3'],ref,col,lo,hi)
            cc['excursion_factors'][b]=cc['cases']['f3']['band_R2'][b]/max(cc['cases']['f2']['band_R2'][b],cc['cases']['f4']['band_R2'][b],1e-300)
        cat,best=BAND.category(cc['f3_energy_shares']); cc['localization_category']=cat; cc['largest_energy_band']=best; cc['energy_share_sum']=sum(cc['f3_energy_shares'].values())
        out[ch]=cc
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('new',type=Path); ap.add_argument('parent_rk',type=Path); ap.add_argument('lane_meta',type=Path); ap.add_argument('out',type=Path); a=ap.parse_args()
    profile=INT.response_profile(a.new); d=direct(a.new,a.parent_rk); b=bands(a.new)
    meta={}
    for p in sorted(a.lane_meta.glob('**/lane_meta.json')):
        x=json.loads(p.read_text()); meta[x['case']]=x
    evidence_ok=(set(meta)=={'ref','f2','f3','f4'} and all(x.get('provider_rc')==0 and x.get('exact_head') for x in meta.values()) and len({x.get('cl_ref_sha256') for x in meta.values()})==1)
    finite_ok=True
    for case in ['ref']+CASES:
        try: INT.files(a.new,case)
        except Exception: finite_ok=False
    e={ch:profile['excursion_factors'][ch] for ch in CHANNELS}; emax=max(e.values())
    if evidence_ok and finite_ok:
        if all(e[ch]<=3.0 for ch in CHANNELS): cls='M21_FULL_CMB_REFERENCE_PRECISION_REMOVES_EXCURSION'
        elif emax<=PARENT_EMAX/3.0: cls='M21_FULL_CMB_REFERENCE_PRECISION_REDUCES_EXCURSION'
        else: cls='M21_FULL_CMB_REFERENCE_PRECISION_EXCURSION_PERSISTS'
    else: cls='M21_FULL_CMB_REFERENCE_PRECISION_BLOCKED'
    result={
      'schema':'KMDSB.W04.M21.FullCMBReferencePrecisionDiagnostic.v0.1',
      'protocol':'protocol/W04_M21_FULL_CMB_REFERENCE_PRECISION_DIAGNOSTIC_v0.1.md',
      'provider':'lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540',
      'parent_run':34542162543,'parent_artifact_id':10178334419,'parent_artifact_digest':'sha256:640472f79c7e55d9edf4ed39ed35d4ab692fcf4700fad4d50edbad0642f7c65c',
      'lane_meta':meta,'evidence_ok':evidence_ok,'finite_outputs':finite_ok,
      'reference_precision_response':profile,'ell_band_localization':b,'direct_clref_vs_parent_RK_P2':d,
      'Emax_reference_precision':emax,'Emax_parent_RK_P2':PARENT_EMAX,'classification':cls,
      'K1_promoted':False,'physical_falsification':False
    }
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'excursion_factors':e,'Emax':emax,'localization':{k:(v['localization_category'],v['largest_energy_band']) for k,v in b.items()}},indent=2))
    if cls=='M21_FULL_CMB_REFERENCE_PRECISION_BLOCKED': raise SystemExit(1)
if __name__=='__main__': main()
