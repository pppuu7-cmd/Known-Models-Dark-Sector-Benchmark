#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
from annihilating_dm_k1_v2_continuity import common,load,clm,pkm

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PREREG='protocol/W04_M22_K4_PRECISION_LADDER_LOCALIZATION_PREREGISTRATION_v0.1.md'
POINTS={'p0':1.11e-23,'p3':3.33e-25,'p5':3.33e-26}
PROFILES=['default','permille','reference']
BLOCKS=[('TT','cl',1),('EE','cl',2),('TE','cl',3),('Pk','pk',None)]

def prepare(out:Path):
    out.mkdir(parents=True,exist_ok=True)
    for prof in PROFILES:
        (out/f'{prof}_ref.ini').write_text('\n'.join(common(f'output/{prof}_ref'))+'\n')
        (out/f'{prof}_zero.ini').write_text('\n'.join(common(f'output/{prof}_zero')+['DM_annihilation_efficiency = 0'])+'\n')
        for tag,p in POINTS.items():
            (out/f'{prof}_{tag}.ini').write_text('\n'.join(common(f'output/{prof}_{tag}')+[f'DM_annihilation_efficiency = {p:.12e}'])+'\n')
    (out/'manifest.json').write_text(json.dumps({'schema':'KMDSB.M22.K4PrecisionManifest.v1','provider_commit':PIN,'preregistration':PREREG,'points':POINTS,'profiles':PROFILES},indent=2,sort_keys=True)+'\n')

def sym(a,b): return float(2*abs(a-b)/(abs(a)+abs(b)+1e-30))

def analyze(root:Path,statusp:Path,outp:Path):
    st=json.loads(statusp.read_text())
    out={'schema':'KMDSB.M22.K4PrecisionLadder.v1','model_id':'M22','family_id':'F22','provider_commit':PIN,'preregistration':PREREG,'status':st,'diagnostic_only':True,'K4_promoted':False,'physical_falsification':False,'scientific_fail':False}
    required=[]
    for prof in PROFILES:
        required += [f'{prof}_ref',f'{prof}_zero']+[f'{prof}_{t}' for t in POINTS]
    if any(st.get(k)!=0 for k in ['build']+required):
        out['classification']='M22_K4_PRECISION_LADDER_BLOCKED';outp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');return
    results={}; integrity=True
    for prof in PROFILES:
        rc=load(root/f'output/{prof}_ref_cl.dat'); zc=load(root/f'output/{prof}_zero_cl.dat')
        rp=load(root/f'output/{prof}_ref_pk.dat'); zp=load(root/f'output/{prof}_zero_pk.dat')
        exact={'TT':clm(zc,rc,1)['R2'],'EE':clm(zc,rc,2)['R2'],'TE':clm(zc,rc,3)['R2'],'Pk':pkm(zp,rp)['R2']}
        exact_pass=all(v<=1e-12 for v in exact.values()); integrity &= exact_pass
        responses={}
        for tag,p in POINTS.items():
            c=load(root/f'output/{prof}_{tag}_cl.dat'); pk=load(root/f'output/{prof}_{tag}_pk.dat')
            responses[tag]={'p_ann':p,'TT':clm(c,zc,1)['R2'],'EE':clm(c,zc,2)['R2'],'TE':clm(c,zc,3)['R2'],'Pk':pkm(pk,zp)['R2']}
        results[prof]={'exact_zero_vs_omitted':exact,'exact_zero_identity_pass':exact_pass,'responses':responses}
    out['profiles']=results
    steps={}
    for name,a,b in [('default_to_permille','default','permille'),('permille_to_reference','permille','reference')]:
        cells=[]; ds=[]
        for tag in POINTS:
            for block,_,__ in BLOCKS:
                x=float(results[a]['responses'][tag][block]);y=float(results[b]['responses'][tag][block]);d=sym(x,y);ds.append(d);cells.append({'point':tag,'block':block,'a':x,'b':y,'D':d})
        steps[name]={'max':float(max(ds)),'median':float(np.median(ds)),'cells':cells}
    out['profile_steps']=steps
    d1=steps['default_to_permille']['max'];d2=steps['permille_to_reference']['max']
    if not integrity: cls='M22_K4_PRECISION_LADDER_BLOCKED'
    elif d2<=0.10 and d2<=d1: cls='M22_K4_PRECISION_CONVERGENCE_CANDIDATE_DIAGNOSTIC'
    elif d2<d1: cls='M22_K4_PRECISION_IMPROVING_NOT_CONVERGED_DIAGNOSTIC'
    else: cls='M22_K4_PRECISION_NONMONOTONE_OR_NONCONVERGED_DIAGNOSTIC'
    out['classification']=cls
    outp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('prepare');p.add_argument('out',type=Path)
    a=sp.add_parser('analyze');a.add_argument('root',type=Path);a.add_argument('status',type=Path);a.add_argument('out',type=Path)
    args=ap.parse_args();prepare(args.out) if args.cmd=='prepare' else analyze(args.root,args.status,args.out)
