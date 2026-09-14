#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json,math,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
PROTOCOL='protocol/W04_M21_CONDITIONAL_K1_V2_NUMERICAL_REFERENCE_PREREGISTRATION_v0.1.md'
PROVIDER='lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540'
CASES=['f0','f1','f2','f3','f4']; FRACS=np.array([0.10,0.03,0.01,0.003,0.001],float)
def loadmod(n,p): s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
INT=loadmod('m21_int',HERE/'integrator_branch_diagnostic.py')
def sorted_xy(a,xcol,ycol,positive=False):
 x=np.asarray(a[:,xcol],float); y=np.asarray(a[:,ycol],float); m=np.isfinite(x)&np.isfinite(y)
 if positive: m &= x>0
 x=x[m]; y=y[m]; q=np.argsort(x); x=x[q]; y=y[q]
 if x.size<3: raise RuntimeError('insufficient finite support')
 ux,idx=np.unique(x,return_index=True); return ux,y[idx]
def align(a,b,xcol,ycol,positive=False,lo=None,hi=None):
 x,y=sorted_xy(a,xcol,ycol,positive); xr,yr=sorted_xy(b,xcol,ycol,positive)
 L=max(float(x.min()),float(xr.min())) if lo is None else max(float(lo),float(x.min()),float(xr.min()))
 H=min(float(x.max()),float(xr.max())) if hi is None else min(float(hi),float(x.max()),float(xr.max()))
 m=(x>=L)&(x<=H); x=x[m]; y=y[m]
 if x.size<3 or H<=L: raise RuntimeError('insufficient overlap')
 xx=np.log(x) if positive else x; xrr=np.log(xr) if positive else xr
 ref=np.interp(xx,xrr,yr); return x,y,ref
def metrics(y,r):
 y=np.asarray(y,float); r=np.asarray(r,float); floor=1e-12*max(float(np.max(np.abs(y))),float(np.max(np.abs(r))),1e-300)
 sym=2*(y-r)/(np.abs(y)+np.abs(r)+floor); ab=np.abs(sym)
 return {'R2':float(np.linalg.norm(y-r)/max(float(np.linalg.norm(r)),1e-300)),'p95_abs':float(np.percentile(ab,95)),'rms':float(np.sqrt(np.mean(sym*sym))),'median_abs':float(np.median(ab)),'n':int(y.size),'floor':float(floor)}
def cl_aligned(a,b,col):
 if a.shape[1]<=col or b.shape[1]<=col: raise RuntimeError('missing CMB column')
 da={int(round(row[0])):float(row[col]) for row in a if np.isfinite(row[0]) and np.isfinite(row[col])}
 db={int(round(row[0])):float(row[col]) for row in b if np.isfinite(row[0]) and np.isfinite(row[col])}
 ell=np.array(sorted(set(da)&set(db)),float)
 if ell.size<3: raise RuntimeError('insufficient common ell')
 return ell,np.array([da[int(x)] for x in ell]),np.array([db[int(x)] for x in ell])
def tables(root,case): return {'cl':INT.one(root,case,'cl'),'pk':INT.one(root,case,'pk'),'bg':INT.one(root,case,'background')}
def pass_route(resp,floors):
 R=np.array(resp,float); F=np.array(floors,float); Q=R/np.maximum(F,1e-300); ident=Q>3.0
 finite=bool(np.all(np.isfinite(R)) and np.all(np.isfinite(F)) and np.all(R>=0) and np.all(F>=0))
 if not finite: return {'pass':False,'route':'NONE','Q':Q.tolist(),'identified':ident.tolist(),'reason':'nonfinite'}
 mono=lambda vals: all(vals[i+1] <= vals[i]*1.05 for i in range(len(vals)-1))
 if bool(np.all(ident)):
  p=float(np.polyfit(np.log(FRACS[-3:]),np.log(np.maximum(R[-3:],1e-300)),1)[0])
  ok=mono(R) and R[-1]<R[0] and p>0.5
  return {'pass':bool(ok),'route':'A_IDENTIFIED' if ok else 'NONE','Q':Q.tolist(),'identified':ident.tolist(),'tail_exponent':p,'monotonic_5pct':bool(mono(R))}
 # route B: equivalence must persist once entered; if f=0.10 is itself
 # equivalent there is no identified-prefix amplitude condition. Otherwise
 # the last identified point must be strictly below the f=0.10 response.
 if not ident[-1]:
  first_eq=int(np.where(~ident)[0][0]); no_reemerge=not bool(np.any(ident[first_eq+1:])); ids=R[:first_eq]
  prefix_mono=True if ids.size<2 else mono(ids)
  if first_eq==0:
   lower=True
  elif first_eq==1:
   lower=False
  else:
   lower=bool(R[first_eq-1] < R[0])
  ok=no_reemerge and prefix_mono and lower
  return {'pass':bool(ok),'route':'B_NUMERICAL_EQUIVALENCE' if ok else 'NONE','Q':Q.tolist(),'identified':ident.tolist(),'first_equivalent_index':first_eq,'no_reemergence':bool(no_reemerge),'identified_prefix_monotonic_5pct':bool(prefix_mono),'last_identified_lower_than_first':bool(lower)}
 return {'pass':False,'route':'NONE','Q':Q.tolist(),'identified':ident.tolist(),'reason':'smallest fraction remains identified while earlier equivalence occurred'}
def main(primary,shadow,selection,out):
 sel=json.loads(selection.read_text()); solver=sel.get('thermo_evolver'); activated=sel.get('authorized') is True and solver in {'rk','ndf15'}
 result={'schema':'KMDSB.W04.M21.K1V2NumericallyResolvedReference.v0.1','date':'2026-09-14','protocol':PROTOCOL,'provider':PROVIDER,'selection':sel,'activated':activated,'K1_promoted':False,'physical_falsification':False,'blocks':{}}
 if not activated:
  result['classification']='M21_K1_V2_BLOCKED_NUMERICAL_REFERENCE'; out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); raise SystemExit(1)
 P={c:tables(primary,c) for c in ['ref']+CASES}; S={c:tables(shadow,c) for c in ['ref']+CASES}
 # global primary positive-k support
 mins=[]; maxs=[]
 for c in ['ref']+CASES:
  k,_=sorted_xy(P[c]['pk'],0,1,True); mins.append(float(k.min())); maxs.append(float(k.max()))
 kmin=max(mins); kmax=min(maxs); loglo,loghi=math.log(kmin),math.log(kmax); cuts=np.exp([loglo,loglo+(loghi-loglo)/3,loglo+2*(loghi-loglo)/3,loghi])
 result['pk_global_support']={'k_min':kmin,'k_max':kmax,'log_thirds':[float(x) for x in cuts]}
 specs=[('H','bg',0,3,False,None,None),('PK_LOW','pk',0,1,True,cuts[0],cuts[1]),('PK_MID','pk',0,1,True,cuts[1],cuts[2]),('PK_HIGH','pk',0,1,True,cuts[2],cuts[3])]
 for name,kind,xc,yc,pos,lo,hi in specs:
  responses=[]; floors=[]; points=[]
  # exact-CDM numerical floor for block
  _,yp,ys=align(P['ref'][kind],S['ref'][kind],xc,yc,pos,lo,hi); dref=metrics(yp,ys)['R2']
  for c,f in zip(CASES,FRACS):
   _,y,r=align(P[c][kind],P['ref'][kind],xc,yc,pos,lo,hi); pm=metrics(y,r)
   _,yp,ys=align(P[c][kind],S[c][kind],xc,yc,pos,lo,hi); dcase=metrics(yp,ys)['R2']; floor=max(dcase,dref)
   responses.append(pm['R2']); floors.append(floor); points.append({'case':c,'fraction':float(f),'primary_response':pm,'primary_shadow_R2':dcase,'reference_primary_shadow_R2':dref,'numerical_floor_R2':floor})
  gate=pass_route(responses,floors); result['blocks'][name]={'points':points,'gate':gate,'pass':gate['pass']}
 for name,col in [('CMB_TT',1),('CMB_EE',2),('CMB_TE',3)]:
  responses=[]; floors=[]; points=[]
  _,yp,ys=cl_aligned(P['ref']['cl'],S['ref']['cl'],col); dref=metrics(yp,ys)['R2']
  for c,f in zip(CASES,FRACS):
   _,y,r=cl_aligned(P[c]['cl'],P['ref']['cl'],col); pm=metrics(y,r)
   _,yp,ys=cl_aligned(P[c]['cl'],S[c]['cl'],col); dcase=metrics(yp,ys)['R2']; floor=max(dcase,dref)
   responses.append(pm['R2']); floors.append(floor); points.append({'case':c,'fraction':float(f),'primary_response':pm,'primary_shadow_R2':dcase,'reference_primary_shadow_R2':dref,'numerical_floor_R2':floor})
  gate=pass_route(responses,floors); result['blocks'][name]={'points':points,'gate':gate,'pass':gate['pass']}
 required=['H','PK_LOW','PK_MID','PK_HIGH','CMB_TT','CMB_EE','CMB_TE']; failing=[x for x in required if not result['blocks'][x]['pass']]
 result['required_blocks']=required; result['failing_blocks']=failing
 if not failing:
  result['classification']='M21_K1_V2_PASS_WITH_SCOPE_SAME_PROVIDER_NUMERICALLY_RESOLVED_ZERO_FRACTION_LIMIT'; result['K1_promoted']=True
 else: result['classification']='M21_K1_V2_REFERENCE_LIMIT_NOT_ESTABLISHED'
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':result['classification'],'failing_blocks':failing,'routes':{k:result['blocks'][k]['gate']['route'] for k in required}},indent=2,sort_keys=True))
if __name__=='__main__':
 if len(sys.argv)!=5: raise SystemExit('usage: k1v2_numerically_resolved_reference.py PRIMARY_DIR SHADOW_DIR SELECTION.json OUT.json')
 main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]))
