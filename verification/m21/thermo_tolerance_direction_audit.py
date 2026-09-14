#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
PROTOCOL='protocol/W04_M21_CONDITIONAL_THERMODYNAMICS_TOLERANCE_DIRECTION_AUDIT_v0.1.md'
PROVIDER='lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540'
PARENT_EMAX=534.8355868817356
ORDER=['T1E4','T3E5','T1E5','T3E6','T1E6','T3E7','T1E7']
VALUES={'T1E4':1e-4,'T3E5':3e-5,'T1E5':1e-5,'T3E6':3e-6,'T1E6':1e-6,'T3E7':3e-7,'T1E7':1e-7}
TIGHT=['T3E6','T1E6','T3E7','T1E7']

def loadmod(name,path):
 s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
INT=loadmod('m21_int',HERE/'integrator_branch_diagnostic.py')

def classify_profile(p):
 e=p['excursion_factors']; emax=max(float(e[x]) for x in ('TT','EE','TE'))
 if all(float(e[x])<=3.0 for x in ('TT','EE','TE')): c='REMOVES'
 elif emax<=PARENT_EMAX/3.0: c='REDUCES'
 else: c='INSUFFICIENT'
 return c,emax

def lane(root,id):
 meta=json.loads((root/'lane_meta.json').read_text()) if (root/'lane_meta.json').is_file() else {}
 ok=meta.get('tolerance_id')==id and meta.get('exact_head') is True and meta.get('all_cases_rc0') is True and meta.get('varied_key')=='tol_thermo_integration' and meta.get('varied_key_count')==1 and meta.get('duplicate_free_serialization') is True
 try: profile=INT.response_profile(root/'output')
 except Exception as exc: profile=None; err=repr(exc)
 else: err=None
 if not ok or profile is None: cls='BLOCKED'; emax=None
 else: cls,emax=classify_profile(profile)
 return {'tolerance_id':id,'tolerance_value':VALUES[id],'classification':cls,'Emax':emax,'response_profile':profile,'analysis_error':err,'lane_meta':meta,'evidence_ok':ok}

def cl_distance(a_root,b_root):
 out={}
 for case in ('ref','f2','f3','f4'):
  a=INT.one(a_root/'output',case,'cl'); b=INT.one(b_root/'output',case,'cl')
  out[case]={name:INT.cl_metric(a,b,col)['R2'] for name,col in [('TT',1),('EE',2),('TE',3)]}
 return out

def maxdist(d): return max(v for x in d.values() for v in x.values())

def main(components,parent,out):
 parentd=json.loads(parent.read_text())
 activated=parentd.get('classification')=='M21_CMB_PRECISION_STAGE3_COMPLETE' and parentd.get('cross_lane_input_identity') is True and parentd.get('parameters',{}).get('G1A__tol_thermo_integration',{}).get('classification') in {'PARAMETER_REMOVES_EXCURSION','PARAMETER_REDUCES_EXCURSION'} and parentd.get('subgroup_stage3',{}).get('G1A',{}).get('classification')!='G1A_STAGE3_BLOCKED'
 dirs={}
 for p in components.iterdir() if components.is_dir() else []:
  if p.is_dir() and p.name.startswith('m21-thermo-tol-'): dirs[p.name[len('m21-thermo-tol-'):]]=p
 missing=sorted(set(ORDER)-set(dirs)); unexpected=sorted(set(dirs)-set(ORDER)); lanes={}
 if activated and not missing and not unexpected:
  lanes={i:lane(dirs[i],i) for i in ORDER}
 identity=bool(lanes)
 for case in ('ref','f2','f3','f4'):
  hs={x['lane_meta'].get('ini_sha256',{}).get(case) for x in lanes.values()}; identity &= len(hs)==1 and None not in hs
 for key in ('cl_permille_sha256','ncdm_tight_sha256'):
  hs={x['lane_meta'].get(key) for x in lanes.values()}; identity &= len(hs)==1 and None not in hs
 blocked=not activated or bool(missing or unexpected) or not identity or any(x['classification']=='BLOCKED' for x in lanes.values())
 anchor={}; adjacent={}
 if not blocked:
  for i in ORDER[:-1]: anchor[i]=cl_distance(dirs[i],dirs['T1E7'])
  anchor['T1E7']={c:{ch:0.0 for ch in ('TT','EE','TE')} for c in ('ref','f2','f3','f4')}
  for a,b in zip(ORDER[:-1],ORDER[1:]): adjacent[f'{a}->{b}']=cl_distance(dirs[a],dirs[b])
  tightcls=[lanes[i]['classification'] for i in TIGHT]
  if all(c=='REMOVES' for c in tightcls): classification='M21_THERMO_TOL_TIGHTENING_PRESERVES_REMOVAL'
  elif all(c in {'REMOVES','REDUCES'} for c in tightcls): classification='M21_THERMO_TOL_TIGHTENING_PRESERVES_SUFFICIENCY'
  elif lanes['T1E5']['classification'] in {'REMOVES','REDUCES'} and lanes['T3E7']['classification']=='INSUFFICIENT' and lanes['T1E7']['classification']=='INSUFFICIENT': classification='M21_THERMO_TOL_REFERENCE_VALUE_PATH_SPECIFIC'
  else: classification='M21_THERMO_TOL_NONMONOTONE_DIRECTIONAL_RESPONSE'
 else: classification='M21_THERMO_TOL_DIRECTION_AUDIT_BLOCKED'
 result={'schema':'KMDSB.W04.M21.ThermoToleranceDirectionAudit.v0.1','date':'2026-09-14','protocol':PROTOCOL,'provider':PROVIDER,'stage3_parent_activated':activated,'stage3_parent_classification':parentd.get('classification'),'required_ladder':ORDER,'tolerance_values':VALUES,'missing_products':missing,'unexpected_products':unexpected,'cross_lane_input_identity':identity,'lanes':lanes,'distance_to_T1E7':anchor,'adjacent_distances':adjacent,'max_distance_to_T1E7':{i:maxdist(d) for i,d in anchor.items()},'classification':classification,'K1_promoted':False,'physical_falsification':False,'interpretation_ceiling':'Directional numerical tolerance audit only; no global convergence, tuning authorization, CLASS bug claim, K1/K3/K4 promotion, or physical M21 conclusion.'}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'classification':classification,'activated':activated,'identity':identity,'lane_classes':{i:x['classification'] for i,x in lanes.items()},'Emax':{i:x['Emax'] for i,x in lanes.items()},'max_distance_to_T1E7':result['max_distance_to_T1E7']},indent=2,sort_keys=True))
 if classification=='M21_THERMO_TOL_DIRECTION_AUDIT_BLOCKED': raise SystemExit(1)
if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: thermo_tolerance_direction_audit.py COMPONENTS STAGE3.json OUT.json')
 main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
