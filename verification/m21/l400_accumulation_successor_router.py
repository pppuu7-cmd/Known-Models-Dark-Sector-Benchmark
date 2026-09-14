#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path

PROTOCOL='protocol/W04_M21_L400_CONVOLUTION_ACCUMULATION_SUCCESSOR_ROUTER_v0.1.md'
PARENT_EXPECTED='M21_L400_TRANSFER_SPIKE_CONVOLUTION_ACCUMULATION_WITH_SCOPE'
ROUTES={
 'M21_L400_CONVOLUTION_EDGE_CORRECTION_LOCALIZED_WITH_SCOPE':['BESSEL_EDGE_TRIGGER_GEOMETRY'],
 'M21_L400_CONVOLUTION_TRAPEZOID_WEIGHT_GEOMETRY_LOCALIZED_WITH_SCOPE':['TAU_WEIGHT_GRID_GEOMETRY'],
 'M21_L400_CONVOLUTION_WEIGHTED_POINTWISE_INTERACTION_LOCALIZED_WITH_SCOPE':['SIGNED_CONTRIBUTION_FACTOR_DECOMPOSITION'],
 'M21_L400_CONVOLUTION_SIGNED_CANCELLATION_LOCALIZED_WITH_SCOPE':['CUMULATIVE_ZERO_CROSSING_PHASE'],
 'M21_L400_CONVOLUTION_ACCUMULATION_NOT_FURTHER_LOCALIZED_WITH_SCOPE':['ACCUMULATION_WINDOW_LOCALIZATION'],
 'M21_L400_CONVOLUTION_SIGN_CANCELLATION_BLOCKED':[],
 'M21_L400_CONVOLUTION_SIGN_CANCELLATION_NOT_AUTHORIZED':[],
}

def main(inp:Path,out:Path)->int:
 d=json.loads(inp.read_text())
 parent=d.get('parent_classification')
 cls=d.get('classification')
 if parent != PARENT_EXPECTED:
  route_cls='M21_L400_ACCUMULATION_ROUTER_PARENT_INCONSISTENT'
  succ=[]
  ok=False
 elif cls not in ROUTES:
  route_cls='M21_L400_ACCUMULATION_ROUTER_BLOCKED_UNKNOWN_PARENT_CLASS'
  succ=[]
  ok=False
 elif cls=='M21_L400_CONVOLUTION_SIGN_CANCELLATION_BLOCKED':
  route_cls='M21_L400_ACCUMULATION_SUCCESSOR_DEBUG_ONLY'
  succ=[]
  ok=True
 elif cls=='M21_L400_CONVOLUTION_SIGN_CANCELLATION_NOT_AUTHORIZED':
  route_cls='M21_L400_ACCUMULATION_ROUTER_PARENT_INCONSISTENT'
  succ=[]
  ok=False
 else:
  route_cls='M21_L400_ACCUMULATION_SUCCESSOR_ROUTED_WITH_SCOPE'
  succ=ROUTES[cls]
  ok=True
 obj={
  'schema':'KMDSB.W04.M21.L400AccumulationSuccessorRouter.v0.1',
  'protocol':PROTOCOL,
  'required_transfer_parent_classification':PARENT_EXPECTED,
  'observed_transfer_parent_classification':parent,
  'parent_convolution_classification':cls,
  'classification':route_cls,
  'authorized_successors':succ,
  'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,
 }
 out.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
 print(json.dumps(obj,indent=2,sort_keys=True))
 return 0 if ok else 1

if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: l400_accumulation_successor_router.py CONVOLUTION_RESULT.json OUT.json')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2])))
