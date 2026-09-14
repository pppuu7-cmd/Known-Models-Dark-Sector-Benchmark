#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np

PROTOCOL='protocol/W04_M21_L400_EDGE_ABSOLUTE_SUFFICIENCY_v0.1.md'
CASES=('ref','f2','f3','f4')

def find_one(root:Path,name:str)->Path:
 xs=list(root.rglob(name))
 if len(xs)!=1: raise RuntimeError(f'expected one {name} under {root}, got {xs}')
 return xs[0]

def table(p:Path)->np.ndarray:
 rows=[]
 for raw in p.read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s or s.startswith('#'): continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError: continue
  if len(r)==12 and all(math.isfinite(x) for x in r): rows.append(r)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<1 or a.shape[1]!=12: raise RuntimeError(f'invalid {p}: {a.shape}')
 return a

def blocks(p:Path):
 a=table(p); out={}
 for q in sorted(set(int(round(x)) for x in a[:,0])):
  b=a[np.isclose(a[:,0],q,rtol=0,atol=1e-12)]
  b=b[np.argsort(b[:,2])]
  out[q]=b
 return out

def main(components:Path,cancel_result:Path,outp:Path)->int:
 cr=json.loads(cancel_result.read_text()); parent_cls=cr.get('classification')
 if parent_cls!='M21_L400_CONVOLUTION_EDGE_CORRECTION_LOCALIZED_WITH_SCOPE':
  obj={'schema':'KMDSB.W04.M21.L400EdgeAbsoluteSufficiency.v0.1','protocol':PROTOCOL,'parent_classification':parent_cls,'classification':'M21_L400_EDGE_ABSOLUTE_SUFFICIENCY_NOT_AUTHORIZED','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}; outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); return 0
 B={c:blocks(find_one(components,f'conv_{c}.dat')) for c in CASES}; metas={c:json.loads(find_one(components,f'{c}_case_meta.json').read_text()) for c in CASES}
 checks={f'{c}_authority_clean':metas[c].get('authority_clean') is True for c in CASES}; qsets=[set(B[c]) for c in CASES]; checks['same_q_set']=all(s==qsets[0] for s in qsets[1:]); qs=sorted(set.intersection(*qsets)) if qsets else []
 checks['q_nonempty']=len(qs)>0
 WT={}; WB={}; WTcf={}; detail={}; max_recon=0.; max_krel=0.
 if all(checks.values()):
  for q in qs:
   arr={c:B[c][q] for c in CASES}; kref=float(arr['ref'][0,1])
   for c in CASES:
    if len(arr[c])<20 or not np.array_equal(arr[c][:,2].astype(int),np.arange(len(arr[c]))): raise RuntimeError(f'q={q} {c}: bad tau integrity')
    recon=float(arr[c][:,7].sum()+arr[c][0,9]); tf=float(arr[c][0,8]); rr=abs(recon-tf)/max(abs(recon),abs(tf),1e-300); max_recon=max(max_recon,rr)
    if rr>1e-10: raise RuntimeError(f'q={q} {c}: reconstruction {rr}')
    max_krel=max(max_krel,abs(float(arr[c][0,1])-kref)/max(abs(kref),1e-300))
   T={c:float(arr[c][0,8]) for c in CASES}; edge={c:float(arr[c][0,9]) for c in CASES}
   r={c:T[c]-T['ref'] for c in ('f2','f3','f4')}; b={c:edge[c]-edge['ref'] for c in ('f2','f3','f4')}
   wt=max(r['f3']**2-max(r['f2']**2,r['f4']**2),0.0); wb=max(b['f3']**2-max(b['f2']**2,b['f4']**2),0.0)
   Tcf=T['f3']-b['f3']; rcf=Tcf-T['ref']; wtcf=max(rcf**2-max(r['f2']**2,r['f4']**2),0.0)
   WT[q]=wt; WB[q]=wb; WTcf[q]=wtcf
   detail[str(q)]={'k_ref':kref,'transfer_difference':r,'edge_difference':b,'W_total':wt,'W_edge':wb,'W_counterfactual':wtcf}
 checks['reconstruction_clean']=max_recon<=1e-10; checks['same_q_k_clean']=max_krel<=1e-6
 sumT=sum(WT.values()); sumB=sum(WB.values()); sumCF=sum(WTcf.values())
 if not all(checks.values()) or sumT<=0:
  cls='M21_L400_EDGE_ABSOLUTE_SUFFICIENCY_BLOCKED'; R=None; residual=None
 else:
  R=math.sqrt(sumB/sumT); residual=math.sqrt(sumCF/sumT)
  cls='M21_L400_EDGE_SPECIFICITY_ABSOLUTELY_INSUFFICIENT_WITH_SCOPE' if R<1.0 else 'M21_L400_EDGE_AMPLITUDE_CAPABLE_NOT_SUFFICIENTLY_PROVEN_WITH_SCOPE'
 obj={'schema':'KMDSB.W04.M21.L400EdgeAbsoluteSufficiency.v0.1','protocol':PROTOCOL,'parent_classification':parent_cls,'classification':cls,'checks':checks,'q_count':len(qs),'sum_W_total':sumT,'sum_W_edge':sumB,'sum_W_counterfactual':sumCF,'R_edge':R,'counterfactual_residual_amplitude_ratio':residual,'max_reconstruction_relative_error':max_recon,'max_same_q_k_relative_difference':max_krel,'per_q':detail,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'R_edge':R,'counterfactual_residual_amplitude_ratio':residual,'q_count':len(qs)},indent=2,sort_keys=True)); return 1 if cls.endswith('_BLOCKED') else 0

if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: l400_edge_absolute_sufficiency.py COMPONENTS_DIR CANCELLATION_RESULT.json OUT.json')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])))
