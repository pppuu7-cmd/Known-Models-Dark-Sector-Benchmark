#!/usr/bin/env python3
import json,sys,math
from pathlib import Path
P='protocol/W04_M21_L400_SUPPORT_TRIGGER_Q_SCALING_v0.1.md'
def fit(xs,ys):
 x0=sum(xs)/len(xs); y0=sum(ys)/len(ys); den=sum((x-x0)**2 for x in xs)
 b=sum((x-x0)*(y-y0) for x,y in zip(xs,ys))/den; a=y0-b*x0
 pred=[a+b*x for x in xs]; rng=max(ys)-min(ys)
 nr=(sum((y-p)**2 for y,p in zip(ys,pred))/len(ys))**.5/max(rng,1e-300)
 mono=sum(ys[i+1]>=ys[i] for i in range(len(ys)-1))/(len(ys)-1)
 return a,b,nr,mono

def main(topf,supf,outf):
 top=json.load(open(topf)); sup=json.load(open(supf)); qs=list(range(261,334)); ok=True; dN=[]; du=[]
 ok &= top.get('classification')=='M21_L400_F3_NATIVE_GRID_SUPPORT_AND_DENSITY_CHANGE_WITH_SCOPE'
 ok &= sup.get('classification')=='M21_L400_F3_EXTENDED_SUPPORT_AMPLITUDE_SUFFICIENT_WITH_SCOPE'
 try:
  for q in qs:
   t=top['per_q'][str(q)]
   # topology schema stores case summaries under cases
   c=t.get('cases',t)
   r=c['ref']; f=c['f3']
   nr=int(r.get('N',r.get('n'))); nf=int(f.get('N',f.get('n')))
   ur=float(r.get('u_min',r.get('umin'))); uf=float(f.get('u_min',f.get('umin')))
   dn=nf-nr; dd=ur-uf
   if not (math.isfinite(dd) and dn>0 and dd>0): ok=False
   dN.append(dn); du.append(dd)
 except Exception:
  ok=False
 if ok:
  x=[q-261 for q in qs]; aN,bN,nN,mN=fit(x,dN); au,bu,nu,mu=fit(x,du)
  if mN>=.95 and mu>=.95 and nN<=.10 and nu<=.10: cls='M21_L400_F3_SUPPORT_EXTENSION_SMOOTH_Q_DEPENDENT_WITH_SCOPE'
  elif mN>=.90 and mu>=.90: cls='M21_L400_F3_SUPPORT_EXTENSION_MONOTONE_NONLINEAR_WITH_SCOPE'
  else: cls='M21_L400_F3_SUPPORT_EXTENSION_IRREGULAR_Q_DEPENDENCE_WITH_SCOPE'
  metrics={'dN_fit':[aN,bN],'du_lo_fit':[au,bu],'NRMS_N':nN,'NRMS_u':nu,'monotonic_fraction_N':mN,'monotonic_fraction_u':mu,'dN_first_last':[dN[0],dN[-1]],'du_first_last':[du[0],du[-1]]}
 else:
  cls='M21_L400_SUPPORT_TRIGGER_Q_SCALING_BLOCKED'; metrics={}
 out={'schema':'KMDSB.W04.M21.L400SupportTriggerQScaling.v0.1','protocol':P,'classification':cls,'metrics':metrics,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 Path(outf).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps(out,indent=2,sort_keys=True)); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main(*sys.argv[1:]))