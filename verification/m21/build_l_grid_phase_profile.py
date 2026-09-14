#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from collections import OrderedDict
from pathlib import Path
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_TRANSFER_L_GRID_PHASE_FACTORIAL_v0.1.md'
LANES={
 'P400_OFF_TAIL_ON':('1.0050130','10',815,False,True,[394,395,396,397,398,399,401,403,405],[2439,2449,2459,2469,2479,2489,2499,2500]),
 'P400_ON_TAIL_OFF':('1.0049900','10',817,True,False,[394,395,396,397,398,399,400,401,403,405],[2431,2441,2451,2461,2471,2481,2491,2500]),
 'P400_OFF_TAIL_OFF':('1.0050400','9',817,False,False,[394,395,396,397,399,401,403,405],[2437,2446,2455,2464,2473,2482,2491,2500]),
 'P400_EVEN_TAIL_OFF':('1.0051400','8',817,True,False,[394,396,398,400,402,404,406],[2446,2454,2462,2470,2478,2486,2494,2500]),
}
def parse(p):
 out=[]
 for raw in p.read_text(errors='replace').splitlines():
  s=raw.split('#',1)[0].strip()
  if not s: continue
  if '=' not in s: raise RuntimeError(f'unparsed {p}: {raw!r}')
  k,v=(x.strip() for x in s.split('=',1)); out.append((k,v))
 return out
def H(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def llist(logstep,linstep,lmax=2500):
 out=[2]; cur=2; inc=max(int(cur*(logstep-1.0)),1)
 while cur+inc<lmax and inc<linstep:
  cur+=inc; out.append(cur); inc=max(int(cur*(logstep-1.0)),1)
 inc=linstep
 while cur+inc<=lmax: cur+=inc; out.append(cur)
 if out[-1]!=lmax: out.append(lmax)
 return out
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('lane',choices=sorted(LANES)); ap.add_argument('cl_permille',type=Path); ap.add_argument('ncdm_tight',type=Path); ap.add_argument('output',type=Path); ap.add_argument('manifest',type=Path); a=ap.parse_args()
 ls,li,n400,on400,on2499,local_frozen,tail_frozen=LANES[a.lane]; L=llist(float(ls),int(li)); local=[x for x in L if 394<=x<=406]; tail=L[-8:]
 sig={'node_count':len(L),'contains_l400':400 in L,'contains_l2499':2499 in L,'nodes_394_406':local,'tail_nodes':tail}
 expected={'node_count':n400,'contains_l400':on400,'contains_l2499':on2499,'nodes_394_406':local_frozen,'tail_nodes':tail_frozen}
 if sig!=expected: raise RuntimeError(f'frozen sparse-l signature mismatch: got={sig} expected={expected}')
 vals=OrderedDict(); origin={}; conflicts=[]
 def apply(src,items):
  for k,v in items:
   if k in vals: conflicts.append({'key':k,'previous_value':vals[k],'previous_source':origin[k],'final_value':v,'final_source':src})
   vals[k]=v; origin[k]=src
 apply('cl_permille.pre',parse(a.cl_permille)); apply('m21_ncdm_tight.pre',parse(a.ncdm_tight)); apply('frozen_common_control',[('evolver','0')]); apply(a.lane,[('l_logstep',ls),('l_linstep',li)])
 if any(x['key'] in {'l_logstep','l_linstep'} for x in conflicts): raise RuntimeError('baseline unexpectedly sets phase keys')
 lines=['# M21 transfer-l grid-phase profile',f'# protocol: {PROTOCOL}',f'# provider: lesgourg/class_public@{PIN}',f'# lane: {a.lane}']+[f'{k} = {v}' for k,v in vals.items()]; a.output.write_text('\n'.join(lines)+'\n')
 r=parse(a.output); keys=[k for k,_ in r]; d=dict(r)
 if len(keys)!=len(set(keys)): raise RuntimeError('duplicate keys')
 if d.get('evolver')!='0' or d.get('l_logstep')!=ls or d.get('l_linstep')!=li: raise RuntimeError('frozen phase controls missing')
 m={'schema':'KMDSB.W04.M21.LGridPhaseProfile.v0.1','provider':f'lesgourg/class_public@{PIN}','protocol':PROTOCOL,'lane':a.lane,'l_logstep':ls,'l_linstep':li,'sparse_l_signature':sig,'varied_keys':['l_logstep','l_linstep'],'varied_key_count':2,'generic_evolver':'0','cl_permille_sha256':H(a.cl_permille),'ncdm_tight_sha256':H(a.ncdm_tight),'output_sha256':H(a.output),'conflicts':conflicts,'duplicate_free_serialization':True}
 a.manifest.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n'); print(json.dumps(m,indent=2,sort_keys=True))
if __name__=='__main__': main()
