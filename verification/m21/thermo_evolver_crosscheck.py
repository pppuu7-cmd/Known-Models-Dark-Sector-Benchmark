#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
PROTOCOL='protocol/W04_M21_CONDITIONAL_THERMO_EVOLVER_CROSSCHECK_v0.1.md'
PROVIDER='lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540'
PARENT_EMAX=534.8355868817356
ORDER=['NDF_T1E5','NDF_T1E6','NDF_T1E7','RK_T1E5','RK_T1E6','RK_T1E7']
VALUES={
 'NDF_T1E5':('ndf15',1e-5),'NDF_T1E6':('ndf15',1e-6),'NDF_T1E7':('ndf15',1e-7),
 'RK_T1E5':('rk',1e-5),'RK_T1E6':('rk',1e-6),'RK_T1E7':('rk',1e-7),
}

def loadmod(n,p): s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
INT=loadmod('m21_int',HERE/'integrator_branch_diagnostic.py')

def classify(p):
 e=p['excursion_factors']; emax=max(float(e[x]) for x in ('TT','EE','TE'))
 if all(float(e[x])<=3.0 for x in ('TT','EE','TE')): return 'REMOVES',emax
 if emax<=PARENT_EMAX/3.0: return 'REDUCES',emax
 return 'INSUFFICIENT',emax

def lane(root,id):
 meta=json.loads((root/'lane_meta.json').read_text()) if (root/'lane_meta.json').is_file() else {}; solver,tol=VALUES[id]
 ok=(meta.get('lane')==id and meta.get('exact_head') is True and meta.get('all_cases_rc0') is True and meta.get('thermo_evolver')==solver and float(meta.get('tol_thermo_integration','nan'))==tol and meta.get('generic_evolver')=='0' and meta.get('varied_keys')==['thermo_evolver','tol_thermo_integration'] and meta.get('varied_key_count')==2 and meta.get('duplicate_free_serialization') is True)
 try: p=INT.response_profile(root/'output')
 except Exception as exc: p=None; err=repr(exc)
 else: err=None
 if not ok or p is None: cls='BLOCKED'; emax=None
 else: cls,emax=classify(p)
 return {'lane':id,'thermo_evolver':solver,'tol_thermo_integration':tol,'classification':cls,'Emax':emax,'response_profile':p,'analysis_error':err,'evidence_ok':ok,'lane_meta':meta}

def cldist(a,b):
 out={}
 for c in ('ref','f2','f3','f4'):
  aa=INT.one(a/'output',c,'cl'); bb=INT.one(b/'output',c,'cl')
  out[c]={ch:INT.cl_metric(aa,bb,col)['R2'] for ch,col in [('TT',1),('EE',2),('TE',3)]}
 return out

def main(comp,parent,out):
 pd=json.loads(parent.read_text()); allowed={'M21_THERMO_TOL_REFERENCE_VALUE_PATH_SPECIFIC','M21_THERMO_TOL_NONMONOTONE_DIRECTIONAL_RESPONSE'}
 activated=pd.get('classification') in allowed and pd.get('cross_lane_input_identity') is True
 dirs={p.name[len('m21-thermo-evolver-'):]:p for p in comp.iterdir() if p.is_dir() and p.name.startswith('m21-thermo-evolver-')} if comp.is_dir() else {}
 missing=sorted(set(ORDER)-set(dirs)); unexpected=sorted(set(dirs)-set(ORDER)); lanes={}
 if activated and not missing and not unexpected: lanes={i:lane(dirs[i],i) for i in ORDER}
 identity=bool(lanes)
 for c in ('ref','f2','f3','f4'):
  hs={x['lane_meta'].get('ini_sha256',{}).get(c) for x in lanes.values()}; identity &= len(hs)==1 and None not in hs
 for k in ('cl_permille_sha256','ncdm_tight_sha256'):
  hs={x['lane_meta'].get(k) for x in lanes.values()}; identity &= len(hs)==1 and None not in hs
 blocked=(not activated or bool(missing or unexpected) or not identity or any(x['classification']=='BLOCKED' for x in lanes.values()))
 direct={}
 if not blocked:
  for tag in ('T1E5','T1E6','T1E7'): direct[tag]=cldist(dirs['RK_'+tag],dirs['NDF_'+tag])
  suff=lambda x: lanes[x]['classification'] in {'REMOVES','REDUCES'}
  ndf_tight=(suff('NDF_T1E6'),suff('NDF_T1E7')); rk_tight=(suff('RK_T1E6'),suff('RK_T1E7'))
  ndf_nonmono=pd.get('classification') in allowed and not all(ndf_tight)
  if ndf_nonmono and all(rk_tight): cls='M21_THERMO_NDF15_SPECIFIC_SENSITIVITY_SUPPORTED'
  elif all(ndf_tight) and all(rk_tight): cls='M21_THERMO_SOLVER_INDEPENDENT_TIGHT_LIMIT_SUPPORTED_WITH_SCOPE'
  elif not any(ndf_tight) and not any(rk_tight): cls='M21_THERMO_TOLERANCE_EFFECT_NOT_SUPPORTED_AT_TIGHT_LIMIT'
  else: cls='M21_THERMO_EVOLVER_DEPENDENCE_MIXED'
 else: cls='M21_THERMO_EVOLVER_CROSSCHECK_BLOCKED'
 result={'schema':'KMDSB.W04.M21.ThermoEvolverCrosscheck.v0.1','date':'2026-09-14','protocol':PROTOCOL,'provider':PROVIDER,'parent_classification':pd.get('classification'),'activated':activated,'required_lanes':ORDER,'missing_products':missing,'unexpected_products':unexpected,'cross_lane_input_identity':identity,'lanes':lanes,'direct_RK_vs_NDF15_CMB_R2':direct,'classification':cls,'K1_promoted':False,'physical_falsification':False,'interpretation_ceiling':'Thermodynamics solver diagnostic only; no CLASS bug claim, global convergence, production tuning, K1/K3/K4 promotion, or physical M21 conclusion.'}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'identity':identity,'Emax':{k:v['Emax'] for k,v in lanes.items()},'classes':{k:v['classification'] for k,v in lanes.items()}},indent=2,sort_keys=True))
 if cls=='M21_THERMO_EVOLVER_CROSSCHECK_BLOCKED': raise SystemExit(1)
if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: thermo_evolver_crosscheck.py COMPONENTS PARENT.json OUT.json')
 main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
