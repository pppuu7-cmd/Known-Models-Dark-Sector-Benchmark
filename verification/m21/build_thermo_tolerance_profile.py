#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json
from collections import OrderedDict
from pathlib import Path

PIN="e85808324f51fc694d12e3ed7439552a3c3f9540"
PROTOCOL="protocol/W04_M21_CONDITIONAL_THERMODYNAMICS_TOLERANCE_DIRECTION_AUDIT_v0.1.md"
VALUES={"T1E4":"1e-4","T3E5":"3e-5","T1E5":"1e-5","T3E6":"3e-6","T1E6":"1e-6","T3E7":"3e-7","T1E7":"1e-7"}

def parse(path:Path):
    out=[]
    for raw in path.read_text(errors='replace').splitlines():
        line=raw.split('#',1)[0].strip()
        if not line: continue
        if '=' not in line: raise RuntimeError(f'unparsed line {path}: {raw!r}')
        k,v=(x.strip() for x in line.split('=',1)); out.append((k,v))
    return out

def H(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('tolerance_id',choices=sorted(VALUES)); ap.add_argument('cl_permille',type=Path); ap.add_argument('ncdm_tight',type=Path); ap.add_argument('output',type=Path); ap.add_argument('manifest',type=Path); a=ap.parse_args()
    vals=OrderedDict(); origin={}; conflicts=[]
    def apply(src,items):
        for k,v in items:
            if k in vals: conflicts.append({'key':k,'previous_value':vals[k],'previous_source':origin[k],'final_value':v,'final_source':src})
            vals[k]=v; origin[k]=src
    apply('cl_permille.pre',parse(a.cl_permille)); apply('m21_ncdm_tight.pre',parse(a.ncdm_tight)); apply('frozen_common_control',[('evolver','0')]); apply(a.tolerance_id,[('tol_thermo_integration',VALUES[a.tolerance_id])])
    if any(x['key']=='tol_thermo_integration' for x in conflicts): raise RuntimeError('baseline unexpectedly sets tol_thermo_integration')
    lines=['# M21 conditional thermodynamics tolerance-direction profile',f'# protocol: {PROTOCOL}',f'# provider: lesgourg/class_public@{PIN}',f'# tolerance_id: {a.tolerance_id}']+[f'{k} = {v}' for k,v in vals.items()]
    a.output.write_text('\n'.join(lines)+'\n')
    reparsed=parse(a.output); keys=[k for k,_ in reparsed]
    if len(keys)!=len(set(keys)): raise RuntimeError('duplicate keys in tolerance profile')
    if dict(reparsed).get('tol_thermo_integration')!=VALUES[a.tolerance_id]: raise RuntimeError('frozen tolerance missing')
    m={'schema':'KMDSB.W04.M21.ThermoToleranceProfile.v0.1','provider':f'lesgourg/class_public@{PIN}','protocol':PROTOCOL,'tolerance_id':a.tolerance_id,'tolerance_value':VALUES[a.tolerance_id],'cl_permille_sha256':H(a.cl_permille),'ncdm_tight_sha256':H(a.ncdm_tight),'output_sha256':H(a.output),'varied_key':'tol_thermo_integration','varied_key_count':1,'conflicts':conflicts,'duplicate_free_serialization':True}
    a.manifest.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n'); print(json.dumps(m,indent=2,sort_keys=True))
if __name__=='__main__': main()
