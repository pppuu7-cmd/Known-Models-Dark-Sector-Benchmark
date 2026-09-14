#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np

PROTOCOL='protocol/W04_M21_L400_SOURCE_FACTORIZATION_v0.1.md'
CASES=('ref','f2','f3','f4')
HIGH=3.0
COL={'ik':0,'it':1,'k':2,'tau':3,'G':4,'P':5,'S':6,'rsa':7,'tca':8,'sl2':9,'shear_valid':10,'shear':11,'pol_valid':12,'pol0':13,'pol2':14}

def find_one(root:Path,name:str)->Path:
 xs=list(root.rglob(name))
 if len(xs)!=1: raise RuntimeError(f'expected one {name} under {root}, got {xs}')
 return xs[0]

def load_diag(p:Path):
 rows=[]
 for raw in p.read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s: continue
  parts=s.split()
  if len(parts)!=15: raise RuntimeError(f'malformed row in {p}: {raw[:160]!r}')
  r=[float(x.replace('D','E').replace('d','e')) for x in parts]
  if not all(math.isfinite(x) for x in r): raise RuntimeError(f'nonfinite row in {p}')
  rows.append(r)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<1 or a.shape[1]!=15: raise RuntimeError(f'invalid diag {p}: {a.shape}')
 out=[]
 for ik in sorted(set(int(round(x)) for x in a[:,COL['ik']])):
  b=a[np.isclose(a[:,COL['ik']],ik,rtol=0,atol=1e-12)]
  b=b[np.argsort(b[:,COL['it']])]
  if len(b)<3: raise RuntimeError(f'{p}: short k block {ik}')
  if not np.array_equal(b[:,COL['it']].astype(int),np.arange(int(b[0,COL['it']]),int(b[0,COL['it']])+len(b))):
   raise RuntimeError(f'{p}: nonconsecutive tau indices in k block {ik}')
  kval=float(np.median(b[:,COL['k']]))
  if np.max(np.abs(b[:,COL['k']]-kval))/max(abs(kval),1e-300)>1e-12: raise RuntimeError(f'{p}: k drift in block {ik}')
  out.append({'ik':ik,'k':kval,'a':b})
 out.sort(key=lambda x:x['k'])
 return out

def bracket(blocks,k):
 ks=np.asarray([b['k'] for b in blocks])
 if k<ks[0] or k>ks[-1]: raise RuntimeError(f'k={k} outside [{ks[0]},{ks[-1]}]')
 j=int(np.searchsorted(ks,k,side='left'))
 if j<len(ks) and abs(ks[j]-k)<=1e-14*max(abs(k),1.0): return blocks[j],blocks[j]
 if j==0 or j==len(ks): raise RuntimeError('no k bracket')
 return blocks[j-1],blocks[j]

def eval_component(blocks,k,tau_grid,key):
 b0,b1=bracket(blocks,k); vals=[]
 for b in (b0,b1):
  t=b['a'][:,COL['tau']]; y=b['a'][:,COL[key]]; order=np.argsort(t); t=t[order]; y=y[order]
  if tau_grid[0]<t[0] or tau_grid[-1]>t[-1]: raise RuntimeError(f'tau grid outside block at k={b["k"]}')
  vals.append(np.interp(tau_grid,t,y))
 if b0 is b1: return vals[0]
 f=(k-b0['k'])/(b1['k']-b0['k'])
 return vals[0]*(1.-f)+vals[1]*f

def D(y,yr): return float(np.linalg.norm(y-yr)/max(float(np.linalg.norm(yr)),1e-300))

def state_summary(blocks):
 out=[]
 for b in blocks:
  a=b['a']; rsa=a[:,COL['rsa']].astype(int); tca=a[:,COL['tca']].astype(int)
  trans=int(np.sum((rsa[1:]!=rsa[:-1]) | (tca[1:]!=tca[:-1])))
  out.append({'k':b['k'],'rows':len(a),'rsa_on_fraction':float(np.mean(rsa!=0)),'tca_on_fraction':float(np.mean(tca!=0)),'state_transition_count':trans})
 return out

def main(components:Path,parent_result:Path,outp:Path)->int:
 parent=json.loads(parent_result.read_text()); pcl=parent.get('classification','')
 authorized=pcl in {'M21_L400_TRANSFER_SPIKE_SOURCE_PROFILE_LOCALIZED_WITH_SCOPE','M21_L400_TRANSFER_SPIKE_SOURCE_AND_RADIAL_MIXED_WITH_SCOPE'}
 if not authorized:
  obj={'schema':'KMDSB.W04.M21.L400SourceFactorization.v0.1','protocol':PROTOCOL,'parent_classification':pcl,'classification':'M21_L400_SOURCE_FACTORIZATION_NOT_AUTHORIZED','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}; outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); return 0
 blocks={c:load_diag(find_one(components,f'source_{c}.dat')) for c in CASES}; metas={c:json.loads(find_one(components,f'{c}_source_case_meta.json').read_text()) for c in CASES}
 checks={f'{c}_authority_clean':metas[c].get('authority_clean') is True for c in CASES}
 k_lo=max(bs[0]['k'] for bs in blocks.values()); k_hi=min(bs[-1]['k'] for bs in blocks.values()); checks['common_k_overlap']=k_lo<k_hi
 pq=[]
 for q,v in parent.get('per_q',{}).items():
  if 'k_ref' in v and 'W_parent' in v: pq.append((float(v['k_ref']),float(v['W_parent'])))
 pq=sorted(pq); checks['parent_weights_present']=len(pq)>0 and sum(w for _,w in pq)>0
 if not all(checks.values()):
  obj={'schema':'KMDSB.W04.M21.L400SourceFactorization.v0.1','protocol':PROTOCOL,'parent_classification':pcl,'classification':'M21_L400_SOURCE_FACTORIZATION_BLOCKED','checks':checks,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}; outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); return 1
 # Frozen evaluation grid: reference perturbation k nodes inside strict four-case and parent-W overlap.
 pkmin,pkmax=pq[0][0],pq[-1][0]; targets=[b['k'] for b in blocks['ref'] if k_lo<=b['k']<=k_hi and pkmin<=b['k']<=pkmax]
 if len(targets)<3: raise RuntimeError(f'insufficient common target k nodes: {targets}')
 qk=np.asarray([x for x,_ in pq]); qw=np.asarray([w for _,w in pq]); weights=np.interp(np.asarray(targets),qk,qw)
 if float(weights.sum())<=0: raise RuntimeError('interpolated parent weight non-positive')
 distances={X:{c:[] for c in ('f2','f3','f4')} for X in ('G','P','S')}; per_k=[]
 for k,w in zip(targets,weights):
  # Reference native tau grid at this exact reference k; then restrict to all bracketing-block tau supports in all cases.
  rb0,rb1=bracket(blocks['ref'],k); rb=rb0 if rb0 is rb1 else rb0
  tref=np.sort(rb['a'][:,COL['tau']]); lo=tref[0]; hi=tref[-1]
  br={}
  for c in CASES:
   b0,b1=bracket(blocks[c],k); br[c]=(b0,b1)
   for b in (b0,b1):
    t=b['a'][:,COL['tau']]; lo=max(lo,float(t.min())); hi=min(hi,float(t.max()))
  tg=tref[(tref>=lo)&(tref<=hi)]
  if len(tg)<20: raise RuntimeError(f'k={k}: insufficient common tau {len(tg)}')
  dk={}
  for X in ('G','P','S'):
   yr=eval_component(blocks['ref'],k,tg,X); dd={}
   for c in ('f2','f3','f4'):
    y=eval_component(blocks[c],k,tg,X); dd[c]=D(y,yr); distances[X][c].append(dd[c])
   dk[X]=dd
  per_k.append({'k':float(k),'W_interp':float(w),'tau_min':float(lo),'tau_max':float(hi),'n_tau':int(len(tg)),'distances':dk})
 den=float(weights.sum()); A={}; E={}
 for X in ('G','P','S'):
  A[X]={c:math.sqrt(float(np.sum(weights*np.square(np.asarray(distances[X][c]))))/den) for c in ('f2','f3','f4')}
  E[X]=A[X]['f3']/max(A[X]['f2'],A[X]['f4'],1e-300)
 if E['G']>HIGH and E['P']<=HIGH: cls='M21_L400_SOURCE_VISIBILITY_LOCALIZED_WITH_SCOPE'
 elif E['G']<=HIGH and E['P']>HIGH: cls='M21_L400_SOURCE_POLARIZATION_MOMENT_LOCALIZED_WITH_SCOPE'
 elif E['G']>HIGH and E['P']>HIGH: cls='M21_L400_SOURCE_VISIBILITY_AND_POLARIZATION_MIXED_WITH_SCOPE'
 elif E['G']<=HIGH and E['P']<=HIGH and E['S']>HIGH: cls='M21_L400_SOURCE_MULTIPLICATIVE_INTERACTION_WITH_SCOPE'
 else: cls='M21_L400_SOURCE_FACTORIZATION_NOT_LOCALIZED_WITH_SCOPE'
 obj={'schema':'KMDSB.W04.M21.L400SourceFactorization.v0.1','protocol':PROTOCOL,'parent_classification':pcl,'classification':cls,'checks':checks,'common_k_range':[float(k_lo),float(k_hi)],'target_k_count':len(targets),'profile_amplitudes':A,'specificity':E,'per_k':per_k,'approximation_state_report':{c:state_summary(blocks[c]) for c in CASES},'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}; outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'E':E,'target_k_count':len(targets)},indent=2,sort_keys=True)); return 0

if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: l400_source_factorization.py COMPONENTS_DIR PARENT_RESULT.json OUT.json')
 raise SystemExit(main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])))
