#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
PROTOCOL='protocol/W04_M21_G2B_L_SAMPLING_TAIL_CONVERGENCE_v0.1.md'; PROVIDER='lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540'; PARENT_EMAX=534.8355868817356
TAIL={'LTAIL_T3':(1.0075,12),'LTAIL_T4':(1.005,10)}
def loadmod(n,p): s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
INT=loadmod('m21_int',HERE/'integrator_branch_diagnostic.py')
def classify(p):
 e=p['excursion_factors']; emax=max(float(e[x]) for x in ('TT','EE','TE'))
 if all(float(e[x])<=3.0 for x in ('TT','EE','TE')): return 'REMOVES',emax
 if emax<=PARENT_EMAX/3.0: return 'REDUCES',emax
 return 'INSUFFICIENT',emax
def tail_lane(root,id):
 meta=json.loads((root/'lane_meta.json').read_text()) if (root/'lane_meta.json').is_file() else {}; logstep,linstep=TAIL[id]
 ok=(meta.get('lane')==id and meta.get('exact_head') is True and meta.get('all_cases_rc0') is True and float(meta.get('l_logstep','nan'))==logstep and int(meta.get('l_linstep',-1))==linstep and meta.get('varied_keys')==['l_logstep','l_linstep'] and meta.get('varied_key_count')==2 and meta.get('duplicate_free_serialization') is True)
 try: p=INT.response_profile(root/'output')
 except Exception as exc: p=None; err=repr(exc)
 else: err=None
 if not ok or p is None: cls='BLOCKED'; emax=None
 else: cls,emax=classify(p)
 return {'lane':id,'l_logstep':logstep,'l_linstep':linstep,'classification':cls,'Emax':emax,'response_profile':p,'analysis_error':err,'evidence_ok':ok,'lane_meta':meta}
def cldist(a,b):
 out={}
 for c in ('ref','f2','f3','f4'):
  aa=INT.one(a/'output',c,'cl'); bb=INT.one(b/'output',c,'cl')
  out[c]={ch:INT.cl_metric(aa,bb,col)['R2'] for ch,col in [('TT',1),('EE',2),('TE',3)]}
 return out
def maxdist(d): return max(v for c in d.values() for v in c.values())
def main(comp,parent_t2,parent_agg,out):
 pd=json.loads(parent_agg.read_text()); activated=(pd.get('classification')=='M21_G2B_L_SAMPLING_INTERACTION_AND_DIRECTION_SUPPORTED' and pd.get('cross_lane_input_identity') is True and pd.get('direction_monotone_supported') is True and pd.get('pairs',{}).get('LPAIR_T2',{}).get('classification')=='REMOVES')
 dirs={p.name[len('m21-ltail-'):]:p for p in comp.iterdir() if p.is_dir() and p.name.startswith('m21-ltail-')} if comp.is_dir() else {}; missing=sorted(set(TAIL)-set(dirs)); unexpected=sorted(set(dirs)-set(TAIL)); lanes={}
 t2meta=json.loads((parent_t2/'lane_meta.json').read_text()) if (parent_t2/'lane_meta.json').is_file() else {}
 t2ok=(t2meta.get('pair')=='LPAIR_T2' and t2meta.get('exact_head') is True and t2meta.get('all_cases_rc0') is True and t2meta.get('varied_keys')==['l_logstep','l_linstep'] and t2meta.get('varied_key_count')==2)
 try: t2prof=INT.response_profile(parent_t2/'output')
 except Exception as exc: t2prof=None; t2err=repr(exc)
 else: t2err=None
 if activated and t2ok and t2prof is not None and not missing and not unexpected: lanes={i:tail_lane(dirs[i],i) for i in sorted(TAIL)}
 identity=bool(lanes) and t2ok
 metas=[t2meta]+[x['lane_meta'] for x in lanes.values()]
 for c in ('ref','f2','f3','f4'):
  hs={m.get('ini_sha256',{}).get(c) for m in metas}; identity &= len(hs)==1 and None not in hs
 for k in ('cl_permille_sha256','ncdm_tight_sha256'):
  hs={m.get(k) for m in metas}; identity &= len(hs)==1 and None not in hs
 blocked=(not activated or not t2ok or t2prof is None or bool(missing or unexpected) or not identity or any(x['classification']=='BLOCKED' for x in lanes.values()))
 distances={}; maxd={}; t2cls,t2emax=('BLOCKED',None) if t2prof is None else classify(t2prof)
 if not blocked:
  distances['T2_to_T3']=cldist(parent_t2,dirs['LTAIL_T3']); distances['T3_to_T4']=cldist(dirs['LTAIL_T3'],dirs['LTAIL_T4']); maxd={k:maxdist(v) for k,v in distances.items()}
  removal=lanes['LTAIL_T3']['classification']=='REMOVES' and lanes['LTAIL_T4']['classification']=='REMOVES'
  contraction=maxd['T3_to_T4']<=maxd['T2_to_T3']
  if removal and contraction: cls='M21_G2B_L_SAMPLING_TAIL_CONTRACTION_SUPPORTED_WITH_SCOPE'
  elif removal: cls='M21_G2B_L_SAMPLING_TAIL_REMOVAL_STABLE_DISTANCE_NONMONOTONE'
  else: cls='M21_G2B_L_SAMPLING_TAIL_REMOVAL_NOT_STABLE'
 else: cls='M21_G2B_L_SAMPLING_TAIL_AUDIT_BLOCKED'; contraction=None
 result={'schema':'KMDSB.W04.M21.LSamplingTailConvergence.v0.1','date':'2026-09-14','protocol':PROTOCOL,'provider':PROVIDER,'activated':activated,'parent_classification':pd.get('classification'),'cross_lane_input_identity':identity,'T2_anchor':{'l_logstep':1.01,'l_linstep':15,'classification':t2cls,'Emax':t2emax,'analysis_error':t2err},'tail_lanes':lanes,'direct_CMB_R2':distances,'max_adjacent_CMB_R2':maxd,'distance_contraction_supported':contraction,'missing_products':missing,'unexpected_products':unexpected,'classification':cls,'K1_promoted':False,'physical_falsification':False,'interpretation_ceiling':'Transfer-l tail convergence diagnostic only; no global convergence, code-defect, production tuning, K1/K3/K4 promotion, or physical M21 conclusion.'}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'T2_Emax':t2emax,'tail_Emax':{k:v['Emax'] for k,v in lanes.items()},'max_adjacent_CMB_R2':maxd},indent=2,sort_keys=True))
 if cls=='M21_G2B_L_SAMPLING_TAIL_AUDIT_BLOCKED': raise SystemExit(1)
if __name__=='__main__':
 if len(sys.argv)!=5: raise SystemExit('usage: l_sampling_tail_convergence.py COMPONENTS PARENT_T2_DIR PARENT_AGG.json OUT.json')
 main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]))
