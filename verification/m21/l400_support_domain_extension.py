#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np

PROTOCOL='protocol/W04_M21_L400_SUPPORT_DOMAIN_EXTENSION_v0.1.md'
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

def excess(v):
 return max(v['f3']**2-max(v['f2']**2,v['f4']**2),0.0)

def main(components:Path,recovery_result:Path,outp:Path)->int:
 parent=json.loads(recovery_result.read_text()); pcl=parent.get('classification')
 if pcl!='M21_L400_TRANSFER_SPIKE_CONVOLUTION_ACCUMULATION_WITH_SCOPE':
  obj={'schema':'KMDSB.W04.M21.L400SupportDomainExtension.v0.1','protocol':PROTOCOL,'parent_classification':pcl,'classification':'M21_L400_SUPPORT_DOMAIN_EXTENSION_NOT_AUTHORIZED','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}; outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); return 0
 B={c:blocks(find_one(components,f'conv_{c}.dat')) for c in CASES}; metas={c:json.loads(find_one(components,f'{c}_case_meta.json').read_text()) for c in CASES}
 checks={f'{c}_authority_clean':metas[c].get('authority_clean') is True for c in CASES}; qsets=[set(B[c]) for c in CASES]; checks['same_q_set']=all(s==qsets[0] for s in qsets[1:]); qs=sorted(set.intersection(*qsets)) if qsets else []; checks['q_nonempty']=len(qs)>0
 perq={}; WT={}; WX={r:{} for r in ('low','high','all')}; WCF={r:{} for r in ('low','high','all')}; max_recon=0.; max_krel=0.
 if all(checks.values()):
  for q in qs:
   a={c:B[c][q] for c in CASES}; kref=float(a['ref'][0,1])
   for c in CASES:
    idx=a[c][:,2].astype(int)
    if len(a[c])<20 or not np.array_equal(idx,np.arange(len(a[c]))): raise RuntimeError(f'q={q} {c}: native index integrity')
    recon=float(a[c][:,7].sum()+a[c][0,9]); tf=float(a[c][0,8]); rr=abs(recon-tf)/max(abs(recon),abs(tf),1e-300); max_recon=max(max_recon,rr)
    max_krel=max(max_krel,abs(float(a[c][0,1])-kref)/max(abs(kref),1e-300))
   ulo=max(float(a[c][:,3].min()) for c in CASES); uhi=min(float(a[c][:,3].max()) for c in CASES)
   T={c:float(a[c][0,8]) for c in CASES}; rd={c:T[c]-T['ref'] for c in ('f2','f3','f4')}; WT[q]=excess(rd)
   reg={}; cf={}; wx={}; wcf={}
   for region in ('low','high','all'):
    X={}
    for c in CASES:
     u=a[c][:,3]
     mask=(u<ulo) if region=='low' else (u>uhi) if region=='high' else ((u<ulo)|(u>uhi))
     X[c]=float(a[c][mask,7].sum())
    xd={c:X[c]-X['ref'] for c in ('f2','f3','f4')}; wx[region]=excess(xd); WX[region][q]=wx[region]
    Tcf={c:T[c]-xd[c] for c in ('f2','f3','f4')}; rcf={c:Tcf[c]-T['ref'] for c in ('f2','f3','f4')}; wcf[region]=excess(rcf); WCF[region][q]=wcf[region]
    reg[region]={'native_contribution':X,'difference_from_reference':xd,'W_candidate':wx[region],'W_counterfactual':wcf[region]}
   perq[str(q)]={'k_ref':kref,'row_count':{c:int(len(a[c])) for c in CASES},'u_min':{c:float(a[c][:,3].min()) for c in CASES},'u_max':{c:float(a[c][:,3].max()) for c in CASES},'u_lo_common':ulo,'u_hi_common':uhi,'transfer':T,'transfer_difference':rd,'W_total':WT[q],'regions':reg}
 checks['reconstruction_clean']=max_recon<=1e-10; checks['same_q_k_clean']=max_krel<=1e-6
 sumT=sum(WT.values()); checks['positive_parent_excess']=sumT>0
 sums={r:{'candidate':sum(WX[r].values()),'counterfactual':sum(WCF[r].values())} for r in ('low','high','all')}
 for r in sums:
  sums[r]['R_candidate']=math.sqrt(sums[r]['candidate']/sumT) if sumT>0 else None
  sums[r]['R_residual']=math.sqrt(sums[r]['counterfactual']/sumT) if sumT>0 else None
  sums[r]['reduction_fraction']=1.-sums[r]['counterfactual']/sumT if sumT>0 else None
 if not all(checks.values()): cls='M21_L400_SUPPORT_DOMAIN_EXTENSION_BLOCKED'
 elif sums['low']['counterfactual']<sumT and sums['low']['counterfactual']<=sums['high']['counterfactual'] and sums['low']['candidate']>=sums['low']['counterfactual']: cls='M21_L400_LOWER_U_SUPPORT_EXTENSION_DOMINANT_WITH_SCOPE'
 elif sums['high']['counterfactual']<sumT and sums['high']['counterfactual']<sums['low']['counterfactual'] and sums['high']['candidate']>=sums['high']['counterfactual']: cls='M21_L400_UPPER_U_SUPPORT_EXTENSION_DOMINANT_WITH_SCOPE'
 elif sums['all']['counterfactual']<sumT and sums['all']['candidate']>=sums['all']['counterfactual']: cls='M21_L400_NONCOMMON_SUPPORT_MIXED_DOMINANT_WITH_SCOPE'
 elif sums['all']['counterfactual']<sumT: cls='M21_L400_NONCOMMON_SUPPORT_PARTIAL_WITH_SCOPE'
 else: cls='M21_L400_NONCOMMON_SUPPORT_NOT_EXPLANATORY_WITH_SCOPE'
 obj={'schema':'KMDSB.W04.M21.L400SupportDomainExtension.v0.1','protocol':PROTOCOL,'parent_classification':pcl,'classification':cls,'checks':checks,'q_count':len(qs),'sum_W_total':sumT,'region_summary':sums,'max_reconstruction_relative_error':max_recon,'max_same_q_k_relative_difference':max_krel,'per_q':perq,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'q_count':len(qs),'region_summary':sums},indent=2,sort_keys=True)); return 1 if cls.endswith('_BLOCKED') else 0

if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: l400_support_domain_extension.py COMPONENTS_DIR RECOVERY_RESULT.json OUT.json')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])))
