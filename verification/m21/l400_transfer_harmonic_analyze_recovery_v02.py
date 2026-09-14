#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_L400_TRANSFER_VS_HARMONIC_DIAGNOSTIC_v0.1.md'
RECOVERY='protocol/W04_M21_L400_TRANSFER_HARMONIC_OUTPUT_NORMALIZATION_RECOVERY_v0.1.md'
CASES=('ref','f2','f3','f4')
LANES={
 'A':{'name':'P400_ON_TAIL_OFF','neighbors':[399,401],'required':{399,400,401}},
 'B':{'name':'P400_EVEN_TAIL_OFF','neighbors':[398,402],'required':{398,400,402}},
}
NULL_MAX=1e-12
SERIAL_REL_MAX=5e-12
HIGH=3.0

def numeric(path:Path)->np.ndarray:
 rows=[]
 for raw in path.read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s or s.startswith('#'): continue
  try: row=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError: continue
  if row and all(math.isfinite(x) for x in row): rows.append(row)
 a=np.asarray(rows,dtype=float)
 if a.ndim!=2 or a.shape[0]<3: raise RuntimeError(f'invalid numeric table {path}: {a.shape}')
 return a

def find_cl(root:Path,c:str)->Path:
 xs=[]
 for pat in (f'output/{c}_*_cl.dat',f'output/{c}_cl.dat'):
  for p in root.glob(pat):
   if p not in xs: xs.append(p)
 if len(xs)!=1: raise RuntimeError(f'expected one cl table {root}/{c}: {[str(x) for x in xs]}')
 return xs[0]

def cl_ee_at(root:Path,c:str,l:int)->float:
 a=numeric(find_cl(root,c)); idx=np.where(np.isclose(a[:,0],l,rtol=0,atol=1e-12))[0]
 if len(idx)!=1 or a.shape[1]<3: raise RuntimeError(f'bad cl lookup c={c} l={l} shape={a.shape}')
 return float(a[idx[0],2])

def diag(path:Path)->dict[int,np.ndarray]:
 a=numeric(path)
 if a.shape[1]!=9: raise RuntimeError(f'diagnostic schema mismatch {path}: {a.shape}')
 out={}
 for lv in sorted(set(int(round(x)) for x in a[:,0])):
  b=a[np.isclose(a[:,0],lv,rtol=0,atol=1e-12)]
  b=b[np.argsort(b[:,4])]
  if b.shape[0]<100 or np.any(np.diff(b[:,4])<=0): raise RuntimeError(f'bad k grid l={lv}: {b.shape}')
  if np.max(np.abs(b[:,8]-b[0,8]))>1e-25*max(abs(b[0,8]),1.0): raise RuntimeError(f'raw internal cl column not constant over q for l={lv}')
  out[lv]=b
 return out

def interp_logk(knew:np.ndarray,k:np.ndarray,y:np.ndarray)->np.ndarray:
 return np.interp(np.log(knew),np.log(k),y)

def metric_for_l(ds:dict[str,dict[int,np.ndarray]],l:int,col:int)->dict:
 mins=[ds[c][l][:,4].min() for c in CASES]; maxs=[ds[c][l][:,4].max() for c in CASES]
 lo=max(mins); hi=min(maxs)
 kr=ds['ref'][l][:,4]; mask=(kr>=lo)&(kr<=hi); kg=kr[mask]
 if kg.size<100: raise RuntimeError(f'insufficient common reference k nodes at l={l}: {kg.size}')
 vals={}
 for c in CASES:
  b=ds[c][l]; vals[c]=interp_logk(kg,b[:,4],b[:,col])
 ref=vals['ref']; refnorm=max(float(np.linalg.norm(ref)),1e-300)
 D={c:float(np.linalg.norm(vals[c]-ref)/refnorm) for c in ('f2','f3','f4')}
 E=D['f3']/max(D['f2'],D['f4'],1e-300)
 resp={c:vals[c]-ref for c in ('f2','f3','f4')}
 scale=max(*(float(np.max(np.abs(x))) for x in resp.values()),1e-300); floor=1e-12*scale
 point=np.abs(resp['f3'])/np.maximum(np.maximum(np.abs(resp['f2']),np.abs(resp['f4'])),floor)
 area={c:float(abs(np.trapezoid(resp[c],kg))) for c in ('f2','f3','f4')}
 area_ratio=area['f3']/max(area['f2'],area['f4'],1e-300)
 return {'n_common_k':int(kg.size),'k_min':float(kg[0]),'k_max':float(kg[-1]),'D':D,'E':float(E),'high':bool(E>HIGH),'max_pointwise_specificity_report_only':float(np.max(point)),'p95_pointwise_specificity_report_only':float(np.percentile(point,95)),'signed_response_area_abs_report_only':area,'area_specificity_report_only':float(area_ratio)}

def main(pair_id:str,newroot:Path,parentroot:Path,outp:Path)->int:
 cfg=LANES[pair_id]
 meta=json.loads((newroot/'lane_meta.json').read_text())
 patch=json.loads((newroot/'l400_transfer_harmonic_patch_manifest.json').read_text())
 parent_meta=json.loads((parentroot/'lane_meta.json').read_text())
 checks={
  'provider_head':meta.get('provider_head')==PIN,
  'exact_head':meta.get('exact_head') is True,
  'lane':meta.get('lane')==cfg['name'],
  'all_cases_rc0':meta.get('all_cases_rc0') is True,
  'patch_protocol':patch.get('protocol')==PROTOCOL,
  'patch_anchor_count':patch.get('anchor_count')==1,
  'patch_after_harmonic_cls':patch.get('insertion_after_harmonic_cls') is True,
  'patch_state_nonmutating_claim':patch.get('mutates_class_state') is False,
  'parent_lane_identity':parent_meta.get('lane')==cfg['name'],
  'ini_hash_identity':meta.get('ini_sha256')==parent_meta.get('ini_sha256'),
  'cl_permille_hash_identity':meta.get('cl_permille_sha256')==parent_meta.get('cl_permille_sha256'),
  'ncdm_tight_hash_identity':meta.get('ncdm_tight_sha256')==parent_meta.get('ncdm_tight_sha256'),
  'l_logstep_identity':str(meta.get('l_logstep'))==str(parent_meta.get('l_logstep')),
  'l_linstep_identity':str(meta.get('l_linstep'))==str(parent_meta.get('l_linstep')),
  'sparse_l_signature_identity':meta.get('sparse_l_signature')==parent_meta.get('sparse_l_signature'),
  'recovery_no_class_execution':True,
 }
 local=set(meta.get('sparse_l_signature',{}).get('nodes_394_406',[])); checks['direct_sparse_nodes']=cfg['required'].issubset(local)
 null={}; null_ok=True
 try:
  for c in CASES:
   a=numeric(find_cl(newroot,c)); b=numeric(find_cl(parentroot,c))
   if a.shape!=b.shape: raise RuntimeError(f'null shape mismatch {c}: {a.shape} vs {b.shape}')
   r=float(np.linalg.norm(a-b)/max(float(np.linalg.norm(a)),float(np.linalg.norm(b)),1e-300))
   null[c]=r; null_ok &= r<=NULL_MAX
 except Exception as e:
  null={'error':str(e)}; null_ok=False
 checks['null_cl_l2_le_1e12']=bool(null_ok)
 if not all(checks.values()):
  obj={'schema':'KMDSB.W04.M21.L400TransferHarmonicRecoveryLane.v0.2','protocol':PROTOCOL,'recovery_protocol':RECOVERY,'pair_id':pair_id,'lane':cfg['name'],'classification':'LANE_BLOCKED','checks':checks,'null_cl_l2':null,'no_class_execution':True,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
  outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps(obj,indent=2,sort_keys=True)); return 1
 ds={c:diag(newroot/f'diag_{c}.dat') for c in CASES}
 for c in CASES:
  if not cfg['required'].issubset(set(ds[c])): raise RuntimeError(f'missing direct diag l nodes for {c}: {sorted(ds[c])}')
 # Recovery-only normalization: class-format output is l(l+1)/(2pi) times raw internal C_l.
 serial_ok=True; serial_rel={}
 for c in CASES:
  serial_rel[c]={}
  for l in sorted(cfg['required']):
   raw=float(ds[c][l][0,8]); expected=l*(l+1)/(2*math.pi)*raw; actual=cl_ee_at(newroot,c,l)
   rel=abs(expected-actual)/max(abs(expected),abs(actual),1e-300); serial_rel[c][str(l)]=rel
   serial_ok &= rel<=SERIAL_REL_MAX
 checks['raw_internal_to_class_output_normalization']=bool(serial_ok)
 if not serial_ok:
  obj={'schema':'KMDSB.W04.M21.L400TransferHarmonicRecoveryLane.v0.2','protocol':PROTOCOL,'recovery_protocol':RECOVERY,'pair_id':pair_id,'lane':cfg['name'],'classification':'LANE_BLOCKED','checks':checks,'serialization_relative_error':serial_rel,'serialization_threshold':SERIAL_REL_MAX,'null_cl_l2':null,'no_class_execution':True,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
  outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps(obj,indent=2,sort_keys=True)); return 1
 transfer={l:metric_for_l(ds,l,5) for l in sorted(cfg['required'])}
 integ={l:metric_for_l(ds,l,7) for l in sorted(cfg['required'])}
 transfer_local=transfer[400]['high'] and all(not transfer[x]['high'] for x in cfg['neighbors'])
 integ_local=integ[400]['high'] and all(not integ[x]['high'] for x in cfg['neighbors'])
 dc={c:cl_ee_at(newroot,c,400)-cl_ee_at(newroot,'ref',400) for c in ('f2','f3','f4')}
 Ecl=abs(dc['f3'])/max(abs(dc['f2']),abs(dc['f4']),1e-300); checks['reproduces_high_direct_cl_l400']=bool(Ecl>HIGH)
 if not checks['reproduces_high_direct_cl_l400']:
  cls='LANE_BLOCKED'; rc=1
 elif transfer_local:
  cls='LANE_TRANSFER_LOCALIZED'; rc=0
 elif integ_local:
  cls='LANE_INTEGRAND_LOCALIZED'; rc=0
 else:
  cls='LANE_PREINTEGRATION_NOT_LOCALIZED'; rc=0
 obj={'schema':'KMDSB.W04.M21.L400TransferHarmonicRecoveryLane.v0.2','protocol':PROTOCOL,'recovery_protocol':RECOVERY,'provider':f'lesgourg/class_public@{PIN}','parent_instrumented_run_id':34904313450,'factorial_parent_run_id':34887488405,'pair_id':pair_id,'lane':cfg['name'],'neighbors':cfg['neighbors'],'checks':checks,'normalization_rule':'class_output_EE = l*(l+1)/(2*pi) * raw_internal_phr_cl_EE','serialization_relative_error':serial_rel,'serialization_threshold':SERIAL_REL_MAX,'null_cl_l2':null,'null_max':float(max(null.values())),'transfer':transfer,'ee_integrand':integ,'transfer_locally_l400_specific':bool(transfer_local),'integrand_locally_l400_specific':bool(integ_local),'direct_sparse_cl_l400_response':dc,'direct_sparse_cl_l400_E':float(Ecl),'classification':cls,'no_class_execution':True,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 outp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'pair_id':pair_id,'classification':cls,'R_null_max':obj['null_max'],'serialization_rel_max':max(max(v.values()) for v in serial_rel.values()),'Ecl400':Ecl,'E_transfer':{str(l):transfer[l]['E'] for l in sorted(transfer)},'E_integrand':{str(l):integ[l]['E'] for l in sorted(integ)}},indent=2,sort_keys=True))
 return rc
if __name__=='__main__':
 if len(sys.argv)!=5: raise SystemExit('usage: l400_transfer_harmonic_analyze_recovery_v02.py PAIR_ID DIAG_LANE_ROOT FACTORIAL_PARENT_ROOT OUT.json')
 raise SystemExit(main(sys.argv[1],Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4])))
