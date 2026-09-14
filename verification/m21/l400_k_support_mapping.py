#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_CONDITIONAL_L400_K_SUPPORT_MAPPING_v0.1.md'
PARENT='waves/wave_04_dark_matter/M21_L400_TRANSFER_VS_HARMONIC_RECOVERY_TERMINAL.json'
CASES=('ref','f2','f3','f4')


def numeric(path:Path)->np.ndarray:
 rows=[]
 for raw in path.read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s or s.startswith('#'): continue
  try: row=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError: continue
  if row and all(math.isfinite(x) for x in row): rows.append(row)
 a=np.asarray(rows,dtype=float)
 if a.ndim!=2 or a.shape[0]<100 or a.shape[1]!=9:
  raise RuntimeError(f'invalid diagnostic table {path}: {a.shape}')
 return a


def l400(path:Path)->np.ndarray:
 a=numeric(path)
 b=a[np.isclose(a[:,0],400.0,rtol=0,atol=1e-12)]
 b=b[np.argsort(b[:,4])]
 if b.shape[0]<100 or np.any(np.diff(b[:,4])<=0):
  raise RuntimeError(f'invalid l400 k grid {path}: {b.shape}')
 return b


def interp_logk(knew:np.ndarray,k:np.ndarray,y:np.ndarray)->np.ndarray:
 return np.interp(np.log(knew),np.log(k),y)


def cumulative_trapz_logk(k:np.ndarray,w:np.ndarray):
 x=np.log(k)
 seg=0.5*(w[:-1]+w[1:])*np.diff(x)
 cum=np.concatenate(([0.0],np.cumsum(seg)))
 return x,seg,cum


def quantile_k(x:np.ndarray,cum:np.ndarray,total:float,q:float)->float:
 target=q*total
 i=int(np.searchsorted(cum,target,side='left'))
 if i<=0: return float(np.exp(x[0]))
 if i>=len(cum): return float(np.exp(x[-1]))
 c0,c1=float(cum[i-1]),float(cum[i])
 if c1<=c0: return float(np.exp(x[i]))
 t=(target-c0)/(c1-c0)
 return float(np.exp(x[i-1]+t*(x[i]-x[i-1])))


def integrate_window(x:np.ndarray,w:np.ndarray,lo:float,hi:float)->float:
 lo=max(lo,float(x[0])); hi=min(hi,float(x[-1]))
 if not hi>lo: return 0.0
 interior=(x>lo)&(x<hi)
 xx=np.concatenate(([lo],x[interior],[hi]))
 ww=np.interp(xx,x,w)
 return float(np.trapezoid(ww,xx))


def main(lane_dir:Path,pair_id:str,outp:Path)->int:
 parent=json.loads(Path(PARENT).read_text())
 checks={
  'parent_classification':parent.get('classification')=='M21_L400_SPIKE_PRESENT_IN_E_TRANSFER_KERNEL_WITH_SCOPE',
  'parent_run_id':parent.get('run_id')==34905311127,
  'physical_falsification_false':parent.get('physical_falsification') is False,
 }
 if pair_id not in ('A','B'): raise RuntimeError(f'bad pair_id {pair_id}')
 ds={c:l400(lane_dir/f'diag_{c}.dat') for c in CASES}
 # Transfer-localized parent => active X is Delta_E, diagnostic column 5.
 lo=max(float(ds[c][:,4].min()) for c in CASES)
 hi=min(float(ds[c][:,4].max()) for c in CASES)
 kr=ds['ref'][:,4]
 mask=(kr>=lo)&(kr<=hi)
 kg=kr[mask]
 checks['common_reference_nodes_ge_100']=bool(kg.size>=100)
 checks['strict_positive_k']=bool(np.all(kg>0) and np.all(np.diff(kg)>0))
 vals={c:interp_logk(kg,ds[c][:,4],ds[c][:,5]) for c in CASES}
 r={c:vals[c]-vals['ref'] for c in ('f2','f3','f4')}
 W=np.maximum(r['f3']*r['f3']-np.maximum(r['f2']*r['f2'],r['f4']*r['f4']),0.0)
 x,seg,cum=cumulative_trapz_logk(kg,W)
 total=float(cum[-1])
 checks['finite_positive_total_excess']=bool(math.isfinite(total) and total>0)
 if not all(checks.values()):
  obj={'schema':'KMDSB.W04.M21.L400KSupportLane.v0.1','protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}','pair_id':pair_id,'classification':'LANE_BLOCKED','checks':checks,'total_excess_ln_k':total,'active_quantity':'Delta_E','no_class_execution':True,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
  outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps(obj,indent=2,sort_keys=True)); return 1
 k05=quantile_k(x,cum,total,0.05); k50=quantile_k(x,cum,total,0.50); k95=quantile_k(x,cum,total,0.95)
 imax=int(np.argmax(W)); kpeak=float(kg[imax]); wpeak=float(W[imax])
 factor2=integrate_window(x,W,math.log(kpeak)-math.log(2),math.log(kpeak)+math.log(2))/total
 below=integrate_window(x,W,float(x[0]),math.log(k50))/total
 above=integrate_window(x,W,math.log(k50),float(x[-1]))/total
 obj={
  'schema':'KMDSB.W04.M21.L400KSupportLane.v0.1',
  'protocol':PROTOCOL,
  'provider':f'lesgourg/class_public@{PIN}',
  'parent_run_id':34905311127,
  'parent_classification':'M21_L400_SPIKE_PRESENT_IN_E_TRANSFER_KERNEL_WITH_SCOPE',
  'pair_id':pair_id,
  'active_quantity':'Delta_E',
  'diagnostic_column':5,
  'common_k':{'n':int(kg.size),'k_min':float(kg[0]),'k_max':float(kg[-1])},
  'checks':checks,
  'total_excess_ln_k':total,
  'k05':k05,'k50':k50,'k95':k95,
  'support_width_log10_k95_over_k05':float(math.log10(k95/k05)),
  'k_peak_W':kpeak,
  'W_peak':wpeak,
  'fraction_excess_within_factor2_of_k_peak':float(factor2),
  'fraction_excess_below_k50_check':float(below),
  'fraction_excess_above_k50_check':float(above),
  'response_norms_on_common_grid':{c:float(np.linalg.norm(r[c])) for c in ('f2','f3','f4')},
  'classification':'LANE_K_SUPPORT_MAPPED',
  'no_class_execution':True,
  'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,
 }
 outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'pair_id':pair_id,'k05':k05,'k50':k50,'k95':k95,'dex_width':obj['support_width_log10_k95_over_k05'],'k_peak':kpeak,'factor2_fraction':factor2},indent=2,sort_keys=True))
 return 0

if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: l400_k_support_mapping.py DIAG_LANE_DIR A|B OUT.json')
 raise SystemExit(main(Path(sys.argv[1]),sys.argv[2],Path(sys.argv[3])))
