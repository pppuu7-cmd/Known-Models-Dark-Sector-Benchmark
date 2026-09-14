#!/usr/bin/env python3
from __future__ import annotations
import json,math,struct,sys
from pathlib import Path
import numpy as np

PROTOCOL='protocol/W04_M21_L400_CONDITIONAL_SUMMATION_ARITHMETIC_STABILITY_v0.1.md'
ALLOWED={
 'M21_L400_CONVOLUTION_SIGNED_CANCELLATION_LOCALIZED_WITH_SCOPE',
 'M21_L400_CONVOLUTION_ACCUMULATION_NOT_FURTHER_LOCALIZED_WITH_SCOPE',
}
CASES=('ref','f2','f3','f4')

def find_one(root:Path,name:str)->Path:
 xs=list(root.rglob(name))
 if len(xs)!=1: raise RuntimeError(f'expected one {name} under {root}, got {xs}')
 return xs[0]

def table(p:Path)->np.ndarray:
 rows=[]
 malformed=0
 for raw in p.read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s or s.startswith('#'): continue
  parts=s.split()
  if len(parts)!=12:
   malformed+=1; continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in parts]
  except ValueError:
   malformed+=1; continue
  if not all(math.isfinite(x) for x in r):
   malformed+=1; continue
  rows.append(r)
 if malformed: raise RuntimeError(f'{p}: malformed rows={malformed}')
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<1 or a.shape[1]!=12: raise RuntimeError(f'invalid {p}: {a.shape}')
 return a

def blocks(p:Path):
 a=table(p); out={}
 for q in sorted(set(int(round(x)) for x in a[:,0])):
  b=a[np.isclose(a[:,0],q,rtol=0,atol=1e-12)]
  out[q]=b[np.argsort(b[:,2])]
 return out

def seqsum(xs):
 s=0.0
 for x in xs: s += float(x)
 return s

def kahan(xs):
 s=0.0; c=0.0
 for xv in xs:
  y=float(xv)-c
  t=s+y
  c=(t-s)-y
  s=t
 return s

def ordered_int(x:float)->int:
 b=struct.unpack('>q',struct.pack('>d',float(x)))[0]
 return 0x8000000000000000-b if b<0 else b

def ulpdiff(a:float,b:float):
 if not (math.isfinite(a) and math.isfinite(b)): return None
 return abs(ordered_int(a)-ordered_int(b))

def main(components:Path,recovery_parent:Path,cancellation_result:Path,outp:Path)->int:
 parent=json.loads(recovery_parent.read_text())
 cancel=json.loads(cancellation_result.read_text())
 cls=cancel.get('classification')
 if cls not in ALLOWED:
  obj={'schema':'KMDSB.W04.M21.L400SummationArithmeticStability.v0.1','protocol':PROTOCOL,'parent_cancellation_classification':cls,'classification':'M21_L400_SUMMATION_ARITHMETIC_STABILITY_NOT_AUTHORIZED','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
  outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); return 0
 weights={int(q):float(v['W_parent']) for q,v in parent.get('per_q',{}).items() if 'W_parent' in v}
 B={c:blocks(find_one(components,f'conv_{c}.dat')) for c in CASES}
 metas={c:json.loads(find_one(components,f'{c}_case_meta.json').read_text()) for c in CASES}
 checks={f'{c}_authority_clean':metas[c].get('authority_clean') is True for c in CASES}
 qsets=[set(B[c]) for c in CASES]
 checks['same_q_set']=all(s==qsets[0] for s in qsets[1:])
 qs=sorted(set.intersection(*qsets)) if qsets else []
 checks['parent_weights_cover_q']=set(qs).issubset(weights)
 checks['positive_parent_weight']=sum(weights.get(q,0.0) for q in qs)>0
 if not all(checks.values()):
  obj={'schema':'KMDSB.W04.M21.L400SummationArithmeticStability.v0.1','protocol':PROTOCOL,'parent_cancellation_classification':cls,'classification':'M21_L400_SUMMATION_ARITHMETIC_STABILITY_BLOCKED','checks':checks,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
  outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); return 1
 methods=('reverse','kahan','fsum')
 sensitivity={m:{c:{} for c in CASES} for m in methods}
 relfinal={m:{c:{} for c in CASES} for m in methods}
 ulps={m:{c:{} for c in CASES} for m in methods}
 cancellation={c:{} for c in CASES}
 perq={}
 max_native_recon=0.0
 for q in qs:
  perq[str(q)]={}
  for c in CASES:
   a=B[c][q]
   idx=a[:,2].astype(int)
   if len(a)<20 or not np.array_equal(idx,np.arange(len(a))): raise RuntimeError(f'{c} q={q}: tau integrity')
   C=[float(x) for x in a[:,7]]
   edge=float(a[0,9]); native=float(a[0,8])
   s_native=seqsum(C)+edge
   rr=abs(s_native-native)/max(abs(s_native),abs(native),1e-300)
   max_native_recon=max(max_native_recon,rr)
   if rr>1e-10: raise RuntimeError(f'{c} q={q}: native reconstruction {rr}')
   budget=sum(abs(x) for x in C)+abs(edge)
   if not math.isfinite(budget) or budget<=0: raise RuntimeError(f'{c} q={q}: bad budget {budget}')
   vals={
    'reverse':seqsum(reversed(C))+edge,
    'kahan':kahan(C)+edge,
    'fsum':math.fsum(C)+edge,
   }
   cancellation[c][q]=budget/max(abs(native),1e-300)
   row={'native':native,'native_order_reconstruction':s_native,'absolute_budget':budget,'cancellation_factor':cancellation[c][q],'methods':{}}
   for m,t in vals.items():
    aa=abs(t-native)/budget
    rf=abs(t-native)/max(abs(native),1e-300)
    sensitivity[m][c][q]=aa; relfinal[m][c][q]=rf; ulps[m][c][q]=ulpdiff(t,native)
    row['methods'][m]={'transfer':t,'budget_normalized_difference':aa,'relative_to_native_transfer':rf,'ulp_distance':ulps[m][c][q]}
   perq[str(q)][c]=row
 den=sum(weights[q] for q in qs)
 R={m:{c:math.sqrt(sum(weights[q]*sensitivity[m][c][q]**2 for q in qs)/den) for c in CASES} for m in methods}
 E={m:R[m]['f3']/max(R[m]['f2'],R[m]['f4'],1e-300) for m in methods}
 max_rel={m:{c:max(relfinal[m][c].values()) for c in CASES} for m in methods}
 max_ulp={m:{c:max((x for x in ulps[m][c].values() if x is not None),default=None) for c in CASES} for m in methods}
 material=bool(max_rel['fsum']['f3']>1e-6 and E['fsum']>3.0)
 out_cls='M21_L400_ACCUMULATION_FLOATING_SUMMATION_SENSITIVITY_LOCALIZED_WITH_SCOPE' if material else 'M21_L400_ACCUMULATION_FLOATING_SUMMATION_NOT_MATERIAL_WITH_SCOPE'
 obj={'schema':'KMDSB.W04.M21.L400SummationArithmeticStability.v0.1','protocol':PROTOCOL,'parent_recovery_classification':parent.get('classification'),'parent_cancellation_classification':cls,'classification':out_cls,'checks':checks,'max_native_reconstruction_relative_error':max_native_recon,'weighted_budget_normalized_amplitude':R,'specificity':E,'max_relative_to_native_transfer':max_rel,'max_ulp_distance':max_ulp,'material_rule':{'f3_max_fsum_relative_to_native_gt':1e-6,'fsum_specificity_gt':3.0,'passed':material},'per_q':perq,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'classification':out_cls,'specificity':E,'f3_max_relative':max_rel['fsum']['f3'],'max_native_reconstruction_relative_error':max_native_recon},indent=2,sort_keys=True))
 return 0

if __name__=='__main__':
 if len(sys.argv)!=5: raise SystemExit('usage: l400_summation_arithmetic_stability.py COMPONENTS_DIR RECOVERY_RESULT.json CANCELLATION_RESULT.json OUT.json')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4])))
