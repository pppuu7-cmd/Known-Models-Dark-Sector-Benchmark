#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from annihilating_dm_k1_v2_continuity import common,load,clm,pkm

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PREREG='protocol/W04_M22_K4_TAIL_PRECISION_TRANSITION_PREREGISTRATION_v0.1.md'
PRIOR=Path('waves/wave_04_dark_matter/M22_K4_PRECISION_LADDER_LOCALIZATION_RESULT.json')
P4=1.11e-25
PROFILES=('permille','reference')
BLOCKS=('TT','EE','TE','Pk')

def prepare(out:Path,profile:str):
    if profile not in PROFILES: raise ValueError(profile)
    out.mkdir(parents=True,exist_ok=True)
    (out/f'{profile}_zero.ini').write_text('\n'.join(common(f'output/{profile}_zero')+['DM_annihilation_efficiency = 0'])+'\n')
    (out/f'{profile}_p4.ini').write_text('\n'.join(common(f'output/{profile}_p4')+[f'DM_annihilation_efficiency = {P4:.12e}'])+'\n')

def response(root:Path,profile:str):
    zc=load(root/f'output/{profile}_zero_cl.dat'); zp=load(root/f'output/{profile}_zero_pk.dat')
    c=load(root/f'output/{profile}_p4_cl.dat'); p=load(root/f'output/{profile}_p4_pk.dat')
    return {'TT':clm(c,zc,1)['R2'],'EE':clm(c,zc,2)['R2'],'TE':clm(c,zc,3)['R2'],'Pk':pkm(p,zp)['R2']}

def sym(a,b): return float(2*abs(a-b)/(abs(a)+abs(b)+1e-30))

def analyze(root:Path,statusp:Path,outp:Path):
    st=json.loads(statusp.read_text()); prior=json.loads(PRIOR.read_text())
    out={'schema':'KMDSB.M22.K4TailPrecisionTransition.v1','model_id':'M22','family_id':'F22','provider_commit':PIN,'preregistration':PREREG,'prior_result':str(PRIOR),'status':st,'p4':P4,'diagnostic_only':True,'K4_promoted':False,'scientific_fail':False,'physical_falsification':False}
    req=[f'{p}_{t}' for p in PROFILES for t in ('zero','p4')]
    if any(st.get(k)!=0 for k in ['build']+req):
        out['classification']='M22_K4_TAIL_PRECISION_TRANSITION_BLOCKED';outp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');return
    if not all(prior['profiles'][p]['exact_zero_identity_pass'] for p in PROFILES):
        out['classification']='M22_K4_TAIL_PRECISION_TRANSITION_BLOCKED';out['error']='prior zero identity integrity failed';outp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');return
    r={p:response(root,p) for p in PROFILES}
    d4={b:sym(r['permille'][b],r['reference'][b]) for b in BLOCKS}; D4=max(d4.values())
    cells=prior['profile_steps']['permille_to_reference']['cells']
    D3=max(float(c['D']) for c in cells if c['point']=='p3'); D5=max(float(c['D']) for c in cells if c['point']=='p5')
    out['responses']=r;out['D_by_block_p4']=d4;out['Dmax']={'p3':D3,'p4':D4,'p5':D5};out['threshold']=0.10
    if not (D3 <= D4 <= D5): cls='M22_K4_TAIL_PRECISION_STRUCTURE_NONMONOTONE_DIAGNOSTIC'
    elif D4 <= 0.10: cls='M22_K4_TAIL_PRECISION_TRANSITION_LOCALIZED_P4_TO_P5_DIAGNOSTIC'
    else: cls='M22_K4_TAIL_PRECISION_TRANSITION_LOCALIZED_P3_TO_P4_DIAGNOSTIC'
    out['classification']=cls
    outp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('prepare');p.add_argument('out',type=Path);p.add_argument('profile',choices=PROFILES)
    a=sp.add_parser('analyze');a.add_argument('root',type=Path);a.add_argument('status',type=Path);a.add_argument('out',type=Path)
    z=ap.parse_args();prepare(z.out,z.profile) if z.cmd=='prepare' else analyze(z.root,z.status,z.out)
