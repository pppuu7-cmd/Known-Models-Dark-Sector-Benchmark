#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from collections import OrderedDict
from pathlib import Path
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'; PROTOCOL='protocol/W04_M21_G2B_L_SAMPLING_TAIL_CONVERGENCE_v0.1.md'
PAIRS={'LTAIL_T3':('1.0075','12'),'LTAIL_T4':('1.005','10')}
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
 ap=argparse.ArgumentParser(); ap.add_argument('lane',choices=sorted(PAIRS)); ap.add_argument('cl_permille',type=Path); ap.add_argument('ncdm_tight',type=Path); ap.add_argument('output',type=Path); ap.add_argument('manifest',type=Path); a=ap.parse_args(); logstep,linstep=PAIRS[a.lane]
 vals=OrderedDict(); origin={}; conflicts=[]
 def apply(src,items):
  for k,v in items:
   if k in vals: conflicts.append({'key':k,'previous_value':vals[k],'previous_source':origin[k],'final_value':v,'final_source':src})
   vals[k]=v; origin[k]=src
 apply('cl_permille.pre',parse(a.cl_permille)); apply('m21_ncdm_tight.pre',parse(a.ncdm_tight)); apply('frozen_common_control',[('evolver','0')]); apply(a.lane,[('l_logstep',logstep),('l_linstep',linstep)])
 if any(x['key'] in {'l_logstep','l_linstep'} for x in conflicts): raise RuntimeError('baseline unexpectedly sets l sampling')
 lines=['# M21 G2B transfer-l tail profile',f'# protocol: {PROTOCOL}',f'# provider: lesgourg/class_public@{PIN}',f'# lane: {a.lane}']+[f'{k} = {v}' for k,v in vals.items()]; a.output.write_text('\n'.join(lines)+'\n')
 r=parse(a.output); ks=[k for k,_ in r]; d=dict(r)
 if len(ks)!=len(set(ks)): raise RuntimeError('duplicate keys')
 if d.get('l_logstep')!=logstep or d.get('l_linstep')!=linstep: raise RuntimeError('frozen tail point missing')
 m={'schema':'KMDSB.W04.M21.LSamplingTailProfile.v0.1','provider':f'lesgourg/class_public@{PIN}','protocol':PROTOCOL,'lane':a.lane,'l_logstep':logstep,'l_linstep':linstep,'varied_keys':['l_logstep','l_linstep'],'varied_key_count':2,'cl_permille_sha256':H(a.cl_permille),'ncdm_tight_sha256':H(a.ncdm_tight),'output_sha256':H(a.output),'conflicts':conflicts,'duplicate_free_serialization':True}
 a.manifest.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n'); print(json.dumps(m,indent=2,sort_keys=True))
if __name__=='__main__': main()
