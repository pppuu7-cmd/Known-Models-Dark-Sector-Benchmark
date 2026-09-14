#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PROTOCOL='protocol/W04_M21_G1A_SINGLE_KEY_DECOMPOSITION_v0.1.md'
PROVIDER='lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540'
PARENT_EMAX=534.8355868817356
ARMS=['A_NZ','A_THERMO','A_HE','A_H']
CASES=['ref','f2','f3','f4']
CHANNELS=['TT','EE','TE']

def load(name,path):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
INT=load('m21_integrator',HERE/'integrator_branch_diagnostic.py')

def arm_result(products,meta_root,arm):
    meta={}
    for case in CASES:
        p=meta_root/arm.lower()/f'{case}.json'
        if p.is_file(): meta[case]=json.loads(p.read_text())
    evidence=(set(meta)==set(CASES) and all(x.get('arm')==arm for x in meta.values()) and
              all(x.get('provider_rc')==0 and x.get('exact_head') is True for x in meta.values()) and
              all(x.get('duplicate_free_serialization') is True for x in meta.values()) and
              len({x.get('profile_sha256') for x in meta.values()})==1)
    try:
        for c in CASES: INT.files(products,c)
        profile=INT.response_profile(products); err=None
    except Exception as exc:
        profile=None; err=repr(exc)
    excursion=profile['excursion_factors'] if profile else {}
    emax=max((float(excursion[x]) for x in CHANNELS),default=None)
    if not evidence or profile is None or emax is None: cls='SINGLE_KEY_BLOCKED'
    elif all(float(excursion[x])<=3.0 for x in CHANNELS): cls='SINGLE_KEY_REMOVES_EXCURSION'
    elif emax<=PARENT_EMAX/3.0: cls='SINGLE_KEY_REDUCES_EXCURSION'
    else: cls='SINGLE_KEY_INSUFFICIENT'
    return {'arm':arm,'classification':cls,'evidence_ok':evidence,'analysis_error':err,'Emax':emax,'excursion_factors':excursion,'response_profile':profile,'lane_meta':meta}

def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('products',type=Path); ap.add_argument('meta',type=Path); ap.add_argument('output',type=Path); a=ap.parse_args()
    results={arm:arm_result(a.products/arm.lower(),a.meta,arm) for arm in ARMS}
    classes=[results[x]['classification'] for x in ARMS]
    if any(c=='SINGLE_KEY_BLOCKED' for c in classes): overall='M21_G1A_SINGLE_KEY_DECOMPOSITION_BLOCKED'
    elif any(c in {'SINGLE_KEY_REMOVES_EXCURSION','SINGLE_KEY_REDUCES_EXCURSION'} for c in classes): overall='M21_G1A_SINGLE_KEY_SUFFICIENCY_IDENTIFIED'
    else: overall='M21_G1A_WITHIN_SUBGROUP_INTERACTION_REQUIRED'
    out={'schema':'KMDSB.W04.M21.G1ASingleKeyDecomposition.v0.1','date':'2026-09-14','protocol':PROTOCOL,'provider':PROVIDER,'parent_stage2_run':34872522336,'parent_stage2_artifact':10360228613,'Emax_parent_RK':PARENT_EMAX,'arms':results,'classification':overall,'K1_promoted':False,'physical_falsification':False,'interpretation_ceiling':'Numerical localization only; no unique-bug claim, physical verdict, or K1/K3/K4 promotion.'}
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'classification':overall,'arm_classes':{k:v['classification'] for k,v in results.items()},'Emax':{k:v['Emax'] for k,v in results.items()}},indent=2,sort_keys=True))
    if overall=='M21_G1A_SINGLE_KEY_DECOMPOSITION_BLOCKED': raise SystemExit(1)
if __name__=='__main__': main()
