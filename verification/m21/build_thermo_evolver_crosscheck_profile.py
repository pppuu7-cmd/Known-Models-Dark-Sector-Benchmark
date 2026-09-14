#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from collections import OrderedDict
from pathlib import Path

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_CONDITIONAL_THERMO_EVOLVER_CROSSCHECK_v0.1.md'
LANES={
 'NDF_T1E5':('ndf15','1e-5'), 'NDF_T1E6':('ndf15','1e-6'), 'NDF_T1E7':('ndf15','1e-7'),
 'RK_T1E5':('rk','1e-5'), 'RK_T1E6':('rk','1e-6'), 'RK_T1E7':('rk','1e-7'),
}

def parse(p:Path):
 out=[]
 for raw in p.read_text(errors='replace').splitlines():
  s=raw.split('#',1)[0].strip()
  if not s: continue
  if '=' not in s: raise RuntimeError(f'unparsed line {p}: {raw!r}')
  k,v=(x.strip() for x in s.split('=',1)); out.append((k,v))
 return out

def H(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('lane',choices=sorted(LANES)); ap.add_argument('cl_permille',type=Path); ap.add_argument('ncdm_tight',type=Path); ap.add_argument('output',type=Path); ap.add_argument('manifest',type=Path); a=ap.parse_args()
 solver,tol=LANES[a.lane]; vals=OrderedDict(); origin={}; conflicts=[]
 def apply(src,items):
  for k,v in items:
   if k in vals: conflicts.append({'key':k,'previous_value':vals[k],'previous_source':origin[k],'final_value':v,'final_source':src})
   vals[k]=v; origin[k]=src
 apply('cl_permille.pre',parse(a.cl_permille)); apply('m21_ncdm_tight.pre',parse(a.ncdm_tight)); apply('frozen_common_control',[('evolver','0')]); apply(a.lane,[('thermo_evolver',solver),('tol_thermo_integration',tol)])
 if any(x['key'] in {'thermo_evolver','tol_thermo_integration'} for x in conflicts): raise RuntimeError('baseline unexpectedly sets thermodynamics crosscheck key')
 lines=['# M21 thermodynamics evolver crosscheck profile',f'# protocol: {PROTOCOL}',f'# provider: lesgourg/class_public@{PIN}',f'# lane: {a.lane}']+[f'{k} = {v}' for k,v in vals.items()]
 a.output.write_text('\n'.join(lines)+'\n'); r=parse(a.output); keys=[k for k,_ in r]
 if len(keys)!=len(set(keys)): raise RuntimeError('duplicate keys')
 d=dict(r)
 if d.get('evolver')!='0' or d.get('thermo_evolver')!=solver or d.get('tol_thermo_integration')!=tol: raise RuntimeError('frozen solver/tolerance controls missing')
 m={'schema':'KMDSB.W04.M21.ThermoEvolverCrosscheckProfile.v0.1','provider':f'lesgourg/class_public@{PIN}','protocol':PROTOCOL,'lane':a.lane,'thermo_evolver':solver,'tol_thermo_integration':tol,'varied_keys':['thermo_evolver','tol_thermo_integration'],'varied_key_count':2,'generic_evolver':'0','cl_permille_sha256':H(a.cl_permille),'ncdm_tight_sha256':H(a.ncdm_tight),'output_sha256':H(a.output),'conflicts':conflicts,'duplicate_free_serialization':True}
 a.manifest.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n'); print(json.dumps(m,indent=2,sort_keys=True))
if __name__=='__main__': main()
