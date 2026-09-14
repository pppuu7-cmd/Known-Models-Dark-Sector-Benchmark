#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path

PROTOCOL='protocol/W04_M21_L400_CONVOLUTION_CONDITIONAL_SUCCESSOR_ROUTER_v0.1.md'
PARENT_RUN=34907528331
ROUTES={
 'M21_L400_TRANSFER_SPIKE_SOURCE_PROFILE_LOCALIZED_WITH_SCOPE':['SOURCE_FACTORIZATION'],
 'M21_L400_TRANSFER_SPIKE_RADIAL_KERNEL_LOCALIZED_WITH_SCOPE':['RADIAL_KERNEL_GEOMETRY'],
 'M21_L400_TRANSFER_SPIKE_SOURCE_AND_RADIAL_MIXED_WITH_SCOPE':['SOURCE_FACTORIZATION','RADIAL_KERNEL_GEOMETRY'],
 'M21_L400_TRANSFER_SPIKE_SOURCE_RADIAL_INTERACTION_WITH_SCOPE':['CONVOLUTION_SIGN_CANCELLATION'],
 'M21_L400_TRANSFER_SPIKE_CONVOLUTION_ACCUMULATION_WITH_SCOPE':['CONVOLUTION_SIGN_CANCELLATION'],
 'M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_BLOCKED':[],
}

def main(inp:Path,out:Path)->int:
 d=json.loads(inp.read_text())
 cls=d.get('classification')
 known=cls in ROUTES
 succ=ROUTES.get(cls,[])
 route_class=(
   'M21_L400_SUCCESSOR_ROUTED_WITH_SCOPE' if known and cls!='M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_BLOCKED'
   else 'M21_L400_SUCCESSOR_DEBUG_ONLY' if cls=='M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_BLOCKED'
   else 'M21_L400_SUCCESSOR_ROUTER_BLOCKED_UNKNOWN_PARENT_CLASS'
 )
 obj={
  'schema':'KMDSB.W04.M21.L400ConvolutionSuccessorRouter.v0.1',
  'protocol':PROTOCOL,
  'parent_recovery_run_id':PARENT_RUN,
  'parent_classification':cls,
  'classification':route_class,
  'authorized_successors':succ,
  'parallel_successors':len(succ)>1,
  'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,
 }
 out.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
 print(json.dumps(obj,indent=2,sort_keys=True))
 return 0 if known else 1

if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: l400_convolution_successor_router.py PARENT_RESULT.json OUT.json')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2])))
