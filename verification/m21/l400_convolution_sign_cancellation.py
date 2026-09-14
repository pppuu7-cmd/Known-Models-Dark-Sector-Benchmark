#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np

PROTOCOL='protocol/W04_M21_L400_CONVOLUTION_SIGN_CANCELLATION_v0.1.md'
CASES=('ref','f2','f3','f4')
HIGH=3.0

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

def D(y,yr): return float(np.linalg.norm(y-yr)/max(float(np.linalg.norm(yr)),1e-300))

def interp_profile(arr:np.ndarray,kind:str):
 u=arr[:,3]
 if kind=='Wtau': y=arr[:,6]
 elif kind=='C': y=arr[:,7]
 elif kind=='Q': y=np.cumsum(arr[:,7])
 else: raise ValueError(kind)
 order=np.argsort(u)
 return u[order],y[order]

def quantiles(u:np.ndarray,w:np.ndarray):
 order=np.argsort(u); u=u[order]; w=np.maximum(w[order],0.0); s=float(w.sum())
 if s<=0: return None
 c=np.cumsum(w)/s
 out={}
 for p in (0.05,0.5,0.95):
  i=int(np.searchsorted(c,p,side='left')); i=min(max(i,0),len(u)-1); out[str(p)]=float(u[i])
 return out

def main(components:Path,parent_result:Path,outp:Path)->int:
 parent=json.loads(parent_result.read_text()); pcl=parent.get('classification','')
 authorized=pcl in {'M21_L400_TRANSFER_SPIKE_SOURCE_RADIAL_INTERACTION_WITH_SCOPE','M21_L400_TRANSFER_SPIKE_CONVOLUTION_ACCUMULATION_WITH_SCOPE'}
 if not authorized:
  obj={'schema':'KMDSB.W04.M21.L400ConvolutionSignCancellation.v0.1','protocol':PROTOCOL,'parent_classification':pcl,'classification':'M21_L400_CONVOLUTION_SIGN_CANCELLATION_NOT_AUTHORIZED','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}; outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); return 0
 B={c:blocks(find_one(components,f'conv_{c}.dat')) for c in CASES}; metas={c:json.loads(find_one(components,f'{c}_case_meta.json').read_text()) for c in CASES}
 checks={f'{c}_authority_clean':metas[c].get('authority_clean') is True for c in CASES}; qsets=[set(B[c]) for c in CASES]; checks['same_q_set']=all(s==qsets[0] for s in qsets[1:]); qs=sorted(set.intersection(*qsets)) if qsets else []
 weights={int(q):float(v['W_parent']) for q,v in parent.get('per_q',{}).items() if 'W_parent' in v}; checks['parent_weights_cover_q']=set(qs).issubset(weights)
 if not all(checks.values()):
  obj={'schema':'KMDSB.W04.M21.L400ConvolutionSignCancellation.v0.1','protocol':PROTOCOL,'parent_classification':pcl,'classification':'M21_L400_CONVOLUTION_SIGN_CANCELLATION_BLOCKED','checks':checks,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}; outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); return 1
 dist={x:{c:{} for c in ('f2','f3','f4')} for x in ('Wtau','C','Q')}; edge_diff={c:{} for c in ('f2','f3','f4')}; perq={}; max_recon=0.
 for q in qs:
  arr={c:B[c][q] for c in CASES}
  iq={c:arr[c][:,2].astype(int) for c in CASES}
  for c in CASES:
   if len(arr[c])<20 or not np.array_equal(iq[c],np.arange(len(arr[c]))): raise RuntimeError(f'q={q} {c}: nonconsecutive tau')
   recon=float(arr[c][:,7].sum()+arr[c][0,9]); tf=float(arr[c][0,8]); rr=abs(recon-tf)/max(abs(recon),abs(tf),1e-300); max_recon=max(max_recon,rr)
   if rr>1e-10: raise RuntimeError(f'q={q} {c}: reconstruction {rr}')
  pd={}; common_meta={}
  for X in ('Wtau','C','Q'):
   curves={c:interp_profile(arr[c],X) for c in CASES}; lo=max(curves[c][0].min() for c in CASES); hi=min(curves[c][0].max() for c in CASES); ur,yr=curves['ref']; mask=(ur>=lo)&(ur<=hi); ug=ur[mask]; yrg=yr[mask]
   if len(ug)<20: raise RuntimeError(f'q={q} {X}: insufficient common u')
   d={}
   for c in ('f2','f3','f4'):
    uc,yc=curves[c]; ycg=np.interp(ug,uc,yc); d[c]=D(ycg,yrg); dist[X][c][q]=d[c]
   pd[X]=d; common_meta[X]={'u_min':float(lo),'u_max':float(hi),'n':int(len(ug))}
  eref=float(arr['ref'][0,9]); ed={c:float(arr[c][0,9]-eref) for c in ('f2','f3','f4')}
  for c in ed: edge_diff[c][q]=ed[c]
  cancel={c:float(np.sum(np.abs(arr[c][:,7]))/max(abs(float(arr[c][0,8])),1e-300)) for c in CASES}
  # Report-only f3-specific excess quantiles on reference-u grid for pointwise weighted contribution.
  curvesC={c:interp_profile(arr[c],'C') for c in CASES}; lo=max(curvesC[c][0].min() for c in CASES); hi=min(curvesC[c][0].max() for c in CASES); ur,cr=curvesC['ref']; mask=(ur>=lo)&(ur<=hi); ug=ur[mask]; cr=cr[mask]
  dc={};
  for c in ('f2','f3','f4'):
   uc,cc=curvesC[c]; dc[c]=np.interp(ug,uc,cc)-cr
  excess=np.maximum(dc['f3']**2-np.maximum(dc['f2']**2,dc['f4']**2),0.0)
  perq[str(q)]={'W_parent':weights[q],'distances':pd,'common_support':common_meta,'edge_difference':ed,'cancellation_factor':cancel,'f3_specific_deltaC_u_quantiles':quantiles(ug,excess)}
 den=sum(weights[q] for q in qs)
 if den<=0: raise RuntimeError('non-positive parent weight')
 A={X:{c:math.sqrt(sum(weights[q]*dist[X][c][q]**2 for q in qs)/den) for c in ('f2','f3','f4')} for X in ('Wtau','C','Q')}
 E={X:A[X]['f3']/max(A[X]['f2'],A[X]['f4'],1e-300) for X in A}
 Ae={c:math.sqrt(sum(weights[q]*edge_diff[c][q]**2 for q in qs)/den) for c in ('f2','f3','f4')}; Eedge=Ae['f3']/max(Ae['f2'],Ae['f4'],1e-300)
 if Eedge>HIGH: cls='M21_L400_CONVOLUTION_EDGE_CORRECTION_LOCALIZED_WITH_SCOPE'
 elif E['Wtau']>HIGH: cls='M21_L400_CONVOLUTION_TRAPEZOID_WEIGHT_GEOMETRY_LOCALIZED_WITH_SCOPE'
 elif E['C']>HIGH: cls='M21_L400_CONVOLUTION_WEIGHTED_POINTWISE_INTERACTION_LOCALIZED_WITH_SCOPE'
 elif E['Q']>HIGH: cls='M21_L400_CONVOLUTION_SIGNED_CANCELLATION_LOCALIZED_WITH_SCOPE'
 else: cls='M21_L400_CONVOLUTION_ACCUMULATION_NOT_FURTHER_LOCALIZED_WITH_SCOPE'
 obj={'schema':'KMDSB.W04.M21.L400ConvolutionSignCancellation.v0.1','protocol':PROTOCOL,'parent_classification':pcl,'classification':cls,'checks':checks,'profile_amplitudes':A,'specificity':E,'edge_amplitudes':Ae,'E_edge':Eedge,'max_reconstruction_relative_error':max_recon,'per_q':perq,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}; outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'E':E,'E_edge':Eedge},indent=2,sort_keys=True)); return 0

if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: l400_convolution_sign_cancellation.py COMPONENTS_DIR PARENT_RESULT.json OUT.json')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])))
