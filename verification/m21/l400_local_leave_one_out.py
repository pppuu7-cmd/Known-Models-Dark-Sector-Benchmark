#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_L400_LOCAL_LEAVE_ONE_OUT_SMOOTHNESS_v0.1.md'
PARENT='waves/wave_04_dark_matter/M21_L400_KNOT_PROPAGATION_TERMINAL.json'
EXPECTED_CL='b6614adedad02f6e22cd42cc9274d048778e5c546c7a8fcfa282b30e24997199'
EXPECTED_NCDM='9696ee08fe5176e68b1b539716caa31dc2b47cd93b626766c2eef0cd02f1e5e8'
EXPECTED_INI={
 'ref':'fbdbf066fd04951636e1837810146b77121b5253c8fd3d0eb90d93b2f62b09bd',
 'f2':'a5633b92d659b48cddd2055792657c41cf8dc204ad4c5a01c5dd6083aa7eadd1',
 'f3':'78b3a444480d176eee8e19600631707425a737746852f5b0fd06a83cb4829ca1',
 'f4':'a756c6f12a7469f6738e279c1e044ac10a310ced0a0e771b70c8f03b47797d93',
}
LANES={
 'A': {'lane':'P400_ON_TAIL_OFF','left':399,'right':401,'required_nodes':{399,400,401}},
 'B': {'lane':'P400_EVEN_TAIL_OFF','left':398,'right':402,'required_nodes':{398,400,402}},
}
CASES=('ref','f2','f3','f4')


def find_one(root:Path, pattern:str)->Path:
 xs=sorted(root.glob(pattern))
 if len(xs)!=1:
  raise RuntimeError(f'expected one {pattern}, got {[str(x) for x in xs]}')
 return xs[0]


def load_ee(path:Path)->dict[int,float]:
 out={}
 for raw in path.read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s or s.startswith('#'): continue
  parts=s.replace('D','E').replace('d','e').split()
  try:
   vals=[float(x) for x in parts]
  except ValueError:
   continue
  if len(vals)<3 or not all(math.isfinite(x) for x in vals[:3]): continue
  l=int(round(vals[0]))
  if abs(vals[0]-l)>1e-9: continue
  out[l]=vals[2]
 if not out: raise RuntimeError(f'no C_l rows in {path}')
 return out


def safe_ratio(a:float,b:float,c:float)->float:
 return abs(a)/max(abs(b),abs(c),1e-300)


def main(root:Path,pair_id:str,outp:Path):
 if pair_id not in LANES: raise RuntimeError(f'bad pair_id {pair_id}')
 cfg=LANES[pair_id]
 parent=json.loads(Path(PARENT).read_text())
 if parent.get('classification')!='M21_L400_SINGLE_KNOT_VALUE_SUFFICIENT_FOR_HIGH_STATE_WITH_SCOPE':
  raise RuntimeError('parent authority mismatch')
 meta=json.loads((root/'lane_meta.json').read_text())
 checks={
  'provider_head': meta.get('provider_head')==PIN,
  'lane': meta.get('lane')==cfg['lane'],
  'all_cases_rc0': meta.get('all_cases_rc0') is True and all(meta.get('case_rc',{}).get(c)==0 for c in CASES),
  'cl_permille_sha': meta.get('cl_permille_sha256')==EXPECTED_CL,
  'ncdm_tight_sha': meta.get('ncdm_tight_sha256')==EXPECTED_NCDM,
  'ini_identity': meta.get('ini_sha256')==EXPECTED_INI,
  'contains_l400': meta.get('sparse_l_signature',{}).get('contains_l400') is True,
 }
 local=set(meta.get('sparse_l_signature',{}).get('nodes_394_406',[]))
 checks['required_direct_sparse_nodes']=cfg['required_nodes'].issubset(local)
 if not all(checks.values()):
  obj={'schema':'KMDSB.W04.M21.L400LocalLeaveOneOut.Pair.v0.1','protocol':PROTOCOL,'pair_id':pair_id,'lane':cfg['lane'],'classification':'PAIR_BLOCKED','checks':checks,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
  outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps(obj,indent=2,sort_keys=True)); return 1
 ee={}
 for c in CASES:
  ee[c]=load_ee(find_one(root/'output',f'{c}_*_cl.dat'))
 for c in CASES:
  for l in (cfg['left'],400,cfg['right']):
   if l not in ee[c]: raise RuntimeError(f'missing l={l} in {c}')
 d={}
 dhat={}
 q={}
 for c in ('f2','f3','f4'):
  d[c]={l:ee[c][l]-ee['ref'][l] for l in (cfg['left'],400,cfg['right'])}
  dhat[c]=0.5*(d[c][cfg['left']]+d[c][cfg['right']])
  denom=max(abs(dhat[c]),0.5*(abs(d[c][cfg['left']])+abs(d[c][cfg['right']])),1e-300)
  q[c]=abs(d[c][400]-dhat[c])/denom
 E400=safe_ratio(d['f3'][400],d['f2'][400],d['f4'][400])
 Ehat=safe_ratio(dhat['f3'],dhat['f2'],dhat['f4'])
 J=q['f3']/max(q['f2'],q['f4'],1e-300)
 refhat=0.5*(ee['ref'][cfg['left']]+ee['ref'][cfg['right']])
 qref=abs(ee['ref'][400]-refhat)/max(abs(refhat),0.5*(abs(ee['ref'][cfg['left']])+abs(ee['ref'][cfg['right']])),1e-300)
 isolated=(E400>3.0 and Ehat<=3.0 and J>=3.0)
 cls='PAIR_ISOLATED_L400_SPIKE' if isolated else 'PAIR_LOCAL_SPIKE_NOT_ESTABLISHED'
 obj={
  'schema':'KMDSB.W04.M21.L400LocalLeaveOneOut.Pair.v0.1',
  'protocol':PROTOCOL,
  'provider':f'lesgourg/class_public@{PIN}',
  'parent_run_id':34901952566,
  'factorial_run_id':34887488405,
  'pair_id':pair_id,
  'lane':cfg['lane'],
  'neighbors':[cfg['left'],cfg['right']],
  'checks':checks,
  'responses':d,
  'predicted_response_at_400':dhat,
  'Q':q,
  'E400':E400,
  'Ehat':Ehat,
  'J_resid':J,
  'reference_leave_one_out_residual_report_only':qref,
  'isolated_l400_spike':isolated,
  'classification':cls,
  'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,
 }
 outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'pair_id':pair_id,'classification':cls,'E400':E400,'Ehat':Ehat,'J_resid':J,'qref':qref},indent=2,sort_keys=True))
 return 0

if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: l400_local_leave_one_out.py LANE_DIR PAIR_ID OUT.json')
 raise SystemExit(main(Path(sys.argv[1]),sys.argv[2],Path(sys.argv[3])))
