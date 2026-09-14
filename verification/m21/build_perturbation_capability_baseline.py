#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sys
from collections import OrderedDict
from pathlib import Path

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_v0.1.md'

def H(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def parse(p: Path):
    out=[]
    for raw in p.read_text(errors='replace').splitlines():
        s=raw.split('#',1)[0].strip()
        if not s: continue
        if '=' not in s: raise RuntimeError(f'unparsed line in {p}: {raw!r}')
        k,v=(x.strip() for x in s.split('=',1))
        out.append((k,v))
    return out

def main(clp: Path, ncdm: Path, out: Path, manifest: Path):
    vals=OrderedDict(); origins={}; conflicts=[]
    def apply(src, items):
        for k,v in items:
            if k in vals:
                conflicts.append({'key':k,'previous_value':vals[k],'previous_source':origins[k],'final_value':v,'final_source':src})
            vals[k]=v; origins[k]=src
    apply('cl_permille.pre',parse(clp))
    apply('m21_ncdm_tight.pre',parse(ncdm))
    apply('frozen_common_control',[('evolver','0')])
    # For the current exact baseline the three sources have disjoint keys.
    # Fail closed if a future edit introduces an implicit override.
    if conflicts:
        raise RuntimeError(f'unexpected common-baseline override(s): {conflicts}')
    lines=['# M21 perturbation-output capability common baseline',f'# protocol: {PROTOCOL}',f'# provider: lesgourg/class_public@{PIN}']+[f'{k} = {v}' for k,v in vals.items()]
    out.write_text('\n'.join(lines)+'\n')
    reparsed=parse(out); ks=[k for k,_ in reparsed]
    if len(ks)!=len(set(ks)): raise RuntimeError('serialized capability profile has duplicate keys')
    d=dict(reparsed)
    if d.get('evolver')!='0': raise RuntimeError('generic evolver baseline drift')
    for forbidden in ['thermo_evolver','tol_thermo_integration','l_logstep','l_linstep']:
        if forbidden in d and forbidden not in dict(parse(clp)) and forbidden not in dict(parse(ncdm)):
            raise RuntimeError(f'unexpected capability override: {forbidden}')
    m={'schema':'KMDSB.W04.M21.PerturbationCapabilityBaseline.v0.1','protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}','cl_permille_sha256':H(clp),'ncdm_tight_sha256':H(ncdm),'output_sha256':H(out),'duplicate_free_serialization':True,'conflicts':conflicts,'final_assignments':dict(vals)}
    manifest.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    print(json.dumps(m,indent=2,sort_keys=True))

if __name__=='__main__':
    if len(sys.argv)!=5: raise SystemExit('usage: build_perturbation_capability_baseline.py CL_PERMILLE NCDM_TIGHT OUT PRE_MANIFEST')
    main(*(Path(x) for x in sys.argv[1:]))
