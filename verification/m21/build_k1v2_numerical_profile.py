#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from collections import OrderedDict
from pathlib import Path
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_CONDITIONAL_K1_V2_NUMERICAL_REFERENCE_PREREGISTRATION_v0.1.md'
SETTINGS={'primary':{'tol':'1e-7','l_logstep':'1.005','l_linstep':'10'},'shadow':{'tol':'1e-6','l_logstep':'1.0075','l_linstep':'12'}}
ENUM={'rk':'0','ndf15':'1'}
def parse(p):
 out=[]
 for raw in p.read_text(errors='replace').splitlines():
  s=raw.split('#',1)[0].strip()
  if not s: continue
  if '=' not in s: raise RuntimeError(f'unparsed {p}: {raw!r}')
  k,v=(x.strip() for x in s.split('=',1)); out.append((k,v))
 return out
def H(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('role',choices=['primary','shadow']); ap.add_argument('solver',choices=['rk','ndf15']); ap.add_argument('cl_permille',type=Path); ap.add_argument('ncdm_tight',type=Path); ap.add_argument('output',type=Path); ap.add_argument('manifest',type=Path); a=ap.parse_args(); s=SETTINGS[a.role]
 vals=OrderedDict(); origin={}; conflicts=[]
 def apply(src,items):
  for k,v in items:
   if k in vals: conflicts.append({'key':k,'previous_value':vals[k],'previous_source':origin[k],'final_value':v,'final_source':src})
   vals[k]=v; origin[k]=src
 apply('cl_permille.pre',parse(a.cl_permille)); apply('m21_ncdm_tight.pre',parse(a.ncdm_tight)); apply('frozen_common_control',[('evolver','0')]); apply(a.role,[('thermo_evolver',ENUM[a.solver]),('tol_thermo_integration',s['tol']),('l_logstep',s['l_logstep']),('l_linstep',s['l_linstep'])])
 if any(x['key'] in {'thermo_evolver','tol_thermo_integration','l_logstep','l_linstep'} for x in conflicts): raise RuntimeError('baseline unexpectedly sets K1-v2 selected numerical key')
 lines=['# M21 conditional K1-v2 numerical profile',f'# protocol: {PROTOCOL}',f'# role: {a.role}',f'# semantic_solver: {a.solver}']+[f'{k} = {v}' for k,v in vals.items()]; a.output.write_text('\n'.join(lines)+'\n')
 r=parse(a.output); ks=[k for k,_ in r]; d=dict(r)
 if len(ks)!=len(set(ks)): raise RuntimeError('duplicate keys')
 expected={'evolver':'0','thermo_evolver':ENUM[a.solver],'tol_thermo_integration':s['tol'],'l_logstep':s['l_logstep'],'l_linstep':s['l_linstep']}
 if any(d.get(k)!=v for k,v in expected.items()): raise RuntimeError(f'profile mismatch {expected} vs {d}')
 m={'schema':'KMDSB.W04.M21.K1V2NumericalProfile.v0.1','provider':f'lesgourg/class_public@{PIN}','protocol':PROTOCOL,'role':a.role,'thermo_evolver':a.solver,'thermo_evolver_serialized':ENUM[a.solver],'tol_thermo_integration':s['tol'],'l_logstep':s['l_logstep'],'l_linstep':s['l_linstep'],'generic_evolver':'0','varied_keys':['thermo_evolver','tol_thermo_integration','l_logstep','l_linstep'],'cl_permille_sha256':H(a.cl_permille),'ncdm_tight_sha256':H(a.ncdm_tight),'output_sha256':H(a.output),'conflicts':conflicts,'duplicate_free_serialization':True}
 a.manifest.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n'); print(json.dumps(m,indent=2,sort_keys=True))
if __name__=='__main__': main()
