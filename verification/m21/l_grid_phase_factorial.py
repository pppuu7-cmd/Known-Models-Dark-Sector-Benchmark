#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
PROTOCOL='protocol/W04_M21_TRANSFER_L_GRID_PHASE_FACTORIAL_v0.1.md'
PROVIDER='lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540'
PARENT_EE=4.3134820992594936
ORDER=['P400_OFF_TAIL_ON','P400_ON_TAIL_OFF','P400_OFF_TAIL_OFF','P400_EVEN_TAIL_OFF']
EXPECTED={
 'P400_OFF_TAIL_ON':{'node_count':815,'contains_l400':False,'contains_l2499':True},
 'P400_ON_TAIL_OFF':{'node_count':817,'contains_l400':True,'contains_l2499':False},
 'P400_OFF_TAIL_OFF':{'node_count':817,'contains_l400':False,'contains_l2499':False},
 'P400_EVEN_TAIL_OFF':{'node_count':817,'contains_l400':True,'contains_l2499':False},
}
def loadmod(n,p):
 s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
INT=loadmod('m21_int',HERE/'integrator_branch_diagnostic.py')
def lane(root,id):
 meta=json.loads((root/'lane_meta.json').read_text()) if (root/'lane_meta.json').is_file() else {}; sig=meta.get('sparse_l_signature',{}); ex=EXPECTED[id]
 ok=(meta.get('lane')==id and meta.get('exact_head') is True and meta.get('all_cases_rc0') is True and meta.get('varied_keys')==['l_logstep','l_linstep'] and meta.get('varied_key_count')==2 and meta.get('duplicate_free_serialization') is True and all(sig.get(k)==v for k,v in ex.items()))
 try:p=INT.response_profile(root/'output')
 except Exception as exc:p=None;err=repr(exc)
 else:err=None
 ee=None; state='BLOCKED'
 if ok and p is not None:
  ee=float(p['excursion_factors']['EE']); state='HIGH' if ee>3.0 else 'CALM'
 return {'lane':id,'evidence_ok':ok,'sparse_l_signature':sig,'response_profile':p,'EE_excursion_factor':ee,'EE_state':state,'analysis_error':err,'lane_meta':meta}
def direct_cl(a:Path,b:Path):
 out={}
 for c in ('ref','f2','f3','f4'):
  aa=INT.one(a/'output',c,'cl'); bb=INT.one(b/'output',c,'cl'); out[c]={ch:INT.cl_metric(aa,bb,col)['R2'] for ch,col in [('TT',1),('EE',2),('TE',3)]}
 return out
def response_change(a:Path,b:Path):
 out={}
 for ch,col in [('TT',1),('EE',2),('TE',3)]:
  out[ch]={}
  ar=INT.one(a/'output','ref','cl'); br=INT.one(b/'output','ref','cl')
  if ar.shape[0]!=br.shape[0] or not np.array_equal(ar[:,0],br[:,0]): raise RuntimeError('ell grids differ')
  for c in ('f2','f3','f4'):
   av=INT.one(a/'output',c,'cl')[:,col]-ar[:,col]; bv=INT.one(b/'output',c,'cl')[:,col]-br[:,col]
   out[ch][c]={'B_over_A_response_norm':float(np.linalg.norm(bv)/max(float(np.linalg.norm(av)),1e-300)),'delta_over_A_response_norm':float(np.linalg.norm(bv-av)/max(float(np.linalg.norm(av)),1e-300))}
 return out
def main(comp:Path,p0:Path,out:Path):
 dirs={p.name[len('m21-lphase-'):]:p for p in comp.iterdir() if p.is_dir() and p.name.startswith('m21-lphase-')} if comp.is_dir() else {}; missing=sorted(set(ORDER)-set(dirs)); unexpected=sorted(set(dirs)-set(ORDER)); lanes={}
 p0meta=json.loads((p0/'lane_meta.json').read_text()) if (p0/'lane_meta.json').is_file() else {}
 p0ok=(p0meta.get('lane')=='LTAIL_T4' and p0meta.get('exact_head') is True and p0meta.get('all_cases_rc0') is True and float(p0meta.get('l_logstep','nan'))==1.005 and int(p0meta.get('l_linstep',-1))==10)
 if p0ok and not missing and not unexpected: lanes={i:lane(dirs[i],i) for i in ORDER}
 identity=p0ok and bool(lanes) and all(v['evidence_ok'] for v in lanes.values())
 metas=[p0meta]+[v['lane_meta'] for v in lanes.values()]
 for c in ('ref','f2','f3','f4'):
  hs={m.get('ini_sha256',{}).get(c) for m in metas}; identity &= len(hs)==1 and None not in hs
 for k in ('cl_permille_sha256','ncdm_tight_sha256'):
  hs={m.get(k) for m in metas}; identity &= len(hs)==1 and None not in hs
 direct={}; changes={}
 if identity:
  for i in ORDER:
   direct[i]=direct_cl(p0,dirs[i]); changes[i]=response_change(p0,dirs[i])
  states={i:lanes[i]['EE_state'] for i in ORDER}; vals=[lanes[i]['EE_excursion_factor'] for i in ORDER]
  if states=={'P400_OFF_TAIL_ON':'CALM','P400_ON_TAIL_OFF':'HIGH','P400_OFF_TAIL_OFF':'CALM','P400_EVEN_TAIL_OFF':'HIGH'}:
   cls='M21_L_GRID_PHASE_L400_SIGNATURE_SUPPORTED_WITH_SCOPE'
  elif states['P400_OFF_TAIL_ON']=='HIGH' and all(states[i]=='CALM' for i in ('P400_ON_TAIL_OFF','P400_OFF_TAIL_OFF','P400_EVEN_TAIL_OFF')):
   cls='M21_L_GRID_PHASE_HIGH_TAIL_SIGNATURE_SUPPORTED_WITH_SCOPE'
  elif max(vals)/max(min(vals),1e-300)>=3.0:
   cls='M21_L_GRID_PHASE_SENSITIVITY_BROADER_THAN_FROZEN_SIGNATURES'
  else: cls='M21_L_GRID_PHASE_SIGNATURE_NOT_ESTABLISHED'
 else:
  states={}; cls='M21_L_GRID_PHASE_FACTORIAL_BLOCKED'
 result={'schema':'KMDSB.W04.M21.LGridPhaseFactorial.v0.1','date':'2026-09-14','protocol':PROTOCOL,'provider':PROVIDER,'classification':cls,'cross_lane_input_identity':bool(identity),'missing_products':missing,'unexpected_products':unexpected,'P0_anchor':{'artifact_id':10364289137,'l_logstep':1.005,'l_linstep':10,'node_count':817,'contains_l400':True,'contains_l2499':True,'EE_excursion_factor':PARENT_EE,'EE_state':'HIGH'},'lanes':lanes,'EE_states':states,'direct_CMB_R2_to_P0_report_only':direct,'response_vector_change_to_P0_report_only':changes,'K1_promoted':False,'physical_falsification':False,'interpretation_ceiling':'Sparse-l grid phase diagnostic only; no CLASS defect, production tuning, global convergence, K1/K3/K4, or physical M21 conclusion.'}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'identity':identity,'EE':{i:lanes[i]['EE_excursion_factor'] for i in lanes},'states':states},indent=2,sort_keys=True))
 if cls=='M21_L_GRID_PHASE_FACTORIAL_BLOCKED': raise SystemExit(1)
if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: l_grid_phase_factorial.py COMPONENTS P0_T4_DIR OUT.json')
 main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
