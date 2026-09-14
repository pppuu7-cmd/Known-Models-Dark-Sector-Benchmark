#!/usr/bin/env python3
from __future__ import annotations
import json,math,struct,sys
from pathlib import Path
import numpy as np

PROTOCOL='protocol/W04_M21_L400_LATE_SOURCE_PREDICATE_ULP_AUDIT_v0.1.md'
CASES=('ref','f2','f3','f4')

def find_one(root:Path,name:str)->Path:
 xs=list(root.rglob(name))
 if len(xs)!=1: raise RuntimeError(f'expected one {name} under {root}, got {xs}')
 return xs[0]

def read_rows(p:Path,n:int):
 rows=[]
 for raw in p.read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s: continue
  parts=s.split()
  if len(parts)!=n: raise RuntimeError(f'{p}: expected {n} fields, got {len(parts)}: {raw[:160]!r}')
  r=[float(x.replace('D','E').replace('d','e')) for x in parts]
  if not all(math.isfinite(x) for x in r): raise RuntimeError(f'{p}: nonfinite row')
  rows.append(r)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<1 or a.shape[1]!=n: raise RuntimeError(f'invalid {p}: {a.shape}')
 return a

def qdict(a):
 out={}
 for r in a:
  q=int(round(r[0]))
  if q in out: raise RuntimeError(f'duplicate q={q}')
  out[q]=r
 return out

def recovery_final(p:Path):
 a=read_rows(p,12); out={}
 for q in sorted(set(int(round(x)) for x in a[:,0])):
  b=a[np.isclose(a[:,0],q,rtol=0,atol=1e-12)]
  finals=set(int(round(x)) for x in b[:,10]); ks=set(float(x) for x in b[:,1])
  if len(finals)!=1 or len(ks)!=1: raise RuntimeError(f'recovery block q={q} inconsistent')
  out[q]={'index_tau_max':next(iter(finals)),'k':next(iter(ks))}
 return out

def bits(x:float)->int:
 if x<0: raise RuntimeError('ULP helper expects positive double')
 return struct.unpack('>Q',struct.pack('>d',x))[0]

def main(pred_root:Path,recovery_root:Path,outp:Path)->int:
 P={c:qdict(read_rows(find_one(pred_root,f'late_source_{c}.dat'),15)) for c in CASES}
 R={c:recovery_final(find_one(recovery_root,f'conv_{c}.dat')) for c in CASES}
 M={c:json.loads(find_one(pred_root,f'{c}_case_meta.json').read_text()) for c in CASES}
 checks={f'{c}_authority_clean':M[c].get('authority_clean') is True for c in CASES}
 qsets=[set(P[c]) for c in CASES]; checks['predicate_same_q_set']=all(s==qsets[0] for s in qsets[1:]); qs=sorted(set.intersection(*qsets)) if qsets else []
 checks['q_nonempty']=len(qs)>0
 checks['matches_recovery_q_sets']=all(set(P[c])==set(R[c]) for c in CASES)
 max_krel=0.; case_summary={}; perq={}
 for c in CASES:
  vals=P[c]
  ang={float(r[3]) for r in vals.values()}; thr={float(r[4]) for r in vals.values()}; pred={int(round(r[6])) for r in vals.values()}; actual={int(round(r[7])) for r in vals.values()}; ell={float(r[2]) for r in vals.values()}
  const=(len(ang)==len(thr)==len(pred)==len(actual)==len(ell)==1)
  checks[f'{c}_case_constants']=const
  checks[f'{c}_predicate_equals_actual']=all(int(round(r[6]))==int(round(r[7])) for r in vals.values())
  checks[f'{c}_l400']=ell=={400.0}
  if const:
   a=next(iter(ang)); t=next(iter(thr)); pr=bool(next(iter(actual))); rhs=t*a
   case_summary[c]={'angular_rescaling':a,'angular_rescaling_minus_1':a-1.0,'signed_ulp_from_1':bits(a)-bits(1.0),'transfer_neglect_late_source':t,'predicate_rhs':rhs,'predicate_margin_l_minus_rhs':400.0-rhs,'neglect_late_source':pr}
 for q in qs:
  row={}; kref=P['ref'][q][1]
  for c in CASES:
   r=P[c][q]; rec=R[c][q]; kr=abs(float(r[1])-float(kref))/max(abs(float(kref)),1e-300); max_krel=max(max_krel,kr)
   matches=int(round(r[10]))==int(rec['index_tau_max'])
   row[c]={'k':float(r[1]),'predicate':bool(round(r[6])),'actual_neglect':bool(round(r[7])),'tau_size':int(round(r[8])),'index_tau_max_Bessel':int(round(r[9])),'index_tau_max':int(round(r[10])),'tau0_minus_tau_cut':float(r[11]),'u_final':float(r[12]),'u_min_bessel':float(r[13]),'transfer_final':float(r[14]),'ends_before_bessel':int(round(r[10]))<int(round(r[9])),'ends_at_bessel':int(round(r[10]))==int(round(r[9])),'matches_recovery_final_index':matches}
  perq[str(q)]=row
 checks['same_q_k_clean']=max_krel<=1e-6
 checks['all_final_indices_match_recovery']=all(perq[str(q)][c]['matches_recovery_final_index'] for q in qs for c in CASES)
 expected_pattern=all(c in case_summary for c in CASES) and case_summary['ref']['neglect_late_source'] and case_summary['f2']['neglect_late_source'] and case_summary['f4']['neglect_late_source'] and not case_summary['f3']['neglect_late_source']
 all_same=(all(c in case_summary for c in CASES) and len({case_summary[c]['neglect_late_source'] for c in CASES})==1)
 consequence_expected=(expected_pattern and all(perq[str(q)][c]['ends_before_bessel'] for q in qs for c in ('ref','f2','f4')) and all(perq[str(q)]['f3']['ends_at_bessel'] for q in qs))
 checks['expected_pattern_consequence']=consequence_expected if expected_pattern else True
 if not all(checks.values()): cls='M21_L400_LATE_SOURCE_PREDICATE_AUDIT_BLOCKED'
 elif expected_pattern and consequence_expected: cls='M21_L400_LATE_SOURCE_PREDICATE_ULP_SPLIT_LOCALIZED_WITH_SCOPE'
 elif expected_pattern and not consequence_expected: cls='M21_L400_LATE_SOURCE_PREDICATE_CONSEQUENCE_MISMATCH_BLOCKED'
 elif all_same: cls='M21_L400_LATE_SOURCE_PREDICATE_NOT_EXPLANATORY_WITH_SCOPE'
 else: cls='M21_L400_LATE_SOURCE_PREDICATE_OTHER_SPLIT_WITH_SCOPE'
 obj={'schema':'KMDSB.W04.M21.L400LateSourcePredicateULPAudit.v0.1','protocol':PROTOCOL,'classification':cls,'checks':checks,'q_count':len(qs),'max_same_q_k_relative_difference':max_krel,'case_summary':case_summary,'expected_pattern':expected_pattern,'expected_pattern_consequence':consequence_expected,'per_q':perq,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'q_count':len(qs),'case_summary':case_summary,'expected_pattern':expected_pattern,'expected_pattern_consequence':consequence_expected},indent=2,sort_keys=True)); return 1 if cls.endswith('_BLOCKED') else 0

if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: l400_late_source_predicate_ulp_audit.py PREDICATE_COMPONENTS RECOVERY_COMPONENTS OUT.json')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])))
