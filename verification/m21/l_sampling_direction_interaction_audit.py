#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; PROTOCOL='protocol/W04_M21_G2B_TRANSFER_L_SAMPLING_DIRECTION_INTERACTION_AUDIT_v0.1.md'; PROVIDER='lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540'; PARENT_EMAX=534.8355868817356; ELOG=70.53199679337801; ELIN=78.37222398394675
ORDER=['LPAIR_I','LPAIR_R','LPAIR_T1','LPAIR_T2']; VALUES={'LPAIR_I':(1.05,32),'LPAIR_R':(1.026,25),'LPAIR_T1':(1.015,20),'LPAIR_T2':(1.010,15)}
def loadmod(n,p): s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
INT=loadmod('m21_int',HERE/'integrator_branch_diagnostic.py')
def lane(root,id):
 meta=json.loads((root/'lane_meta.json').read_text()) if (root/'lane_meta.json').is_file() else {}; ok=meta.get('pair')==id and meta.get('exact_head') is True and meta.get('all_cases_rc0') is True and meta.get('varied_keys')==['l_logstep','l_linstep'] and meta.get('varied_key_count')==2 and meta.get('duplicate_free_serialization') is True
 try: p=INT.response_profile(root/'output')
 except Exception as exc: p=None; err=repr(exc)
 else: err=None
 if not ok or p is None: cls='BLOCKED'; emax=None
 else:
  e=p['excursion_factors']; emax=max(float(e[x]) for x in ('TT','EE','TE'))
  if all(float(e[x])<=3 for x in ('TT','EE','TE')): cls='REMOVES'
  elif emax<=PARENT_EMAX/3: cls='REDUCES'
  else: cls='INSUFFICIENT'
 return {'pair':id,'l_logstep':VALUES[id][0],'l_linstep':VALUES[id][1],'classification':cls,'Emax':emax,'response_profile':p,'analysis_error':err,'evidence_ok':ok,'lane_meta':meta}
def cldist(a,b):
 out={}
 for c in ('ref','f2','f3','f4'):
  aa=INT.one(a/'output',c,'cl'); bb=INT.one(b/'output',c,'cl'); out[c]={ch:INT.cl_metric(aa,bb,col)['R2'] for ch,col in [('TT',1),('EE',2),('TE',3)]}
 return out
def main(comp,out):
 dirs={p.name[len('m21-lpair-'):]:p for p in comp.iterdir() if p.is_dir() and p.name.startswith('m21-lpair-')} if comp.is_dir() else {}; missing=sorted(set(ORDER)-set(dirs)); unexpected=sorted(set(dirs)-set(ORDER)); lanes={}
 if not missing and not unexpected: lanes={i:lane(dirs[i],i) for i in ORDER}
 identity=bool(lanes)
 for c in ('ref','f2','f3','f4'):
  hs={x['lane_meta'].get('ini_sha256',{}).get(c) for x in lanes.values()}; identity &= len(hs)==1 and None not in hs
 for key in ('cl_permille_sha256','ncdm_tight_sha256'):
  hs={x['lane_meta'].get(key) for x in lanes.values()}; identity &= len(hs)==1 and None not in hs
 blocked=bool(missing or unexpected) or not identity or any(x['classification']=='BLOCKED' for x in lanes.values())
 dist={}
 if not blocked:
  for i in ORDER[:-1]: dist[i]=cldist(dirs[i],dirs['LPAIR_T2'])
  dist['LPAIR_T2']={c:{ch:0.0 for ch in ('TT','EE','TE')} for c in ('ref','f2','f3','f4')}
  er=lanes['LPAIR_R']['Emax']; interaction=er < min(ELOG,ELIN); es=[lanes[i]['Emax'] for i in ORDER]; monotone=all(es[j+1] <= 1.05*es[j] for j in range(len(es)-1))
  if interaction and monotone: cls='M21_G2B_L_SAMPLING_INTERACTION_AND_DIRECTION_SUPPORTED'
  elif interaction: cls='M21_G2B_L_SAMPLING_INTERACTION_SUPPORTED_DIRECTION_NONMONOTONE'
  elif monotone: cls='M21_G2B_L_SAMPLING_DIRECTION_SUPPORTED_NO_PAIR_INTERACTION'
  else: cls='M21_G2B_L_SAMPLING_NONMONOTONE_NO_PAIR_INTERACTION'
  gain=min(ELOG,ELIN)/er
 else: cls='M21_G2B_L_SAMPLING_AUDIT_BLOCKED'; interaction=None; monotone=None; gain=None
 result={'schema':'KMDSB.W04.M21.LSamplingDirectionInteractionAudit.v0.1','date':'2026-09-14','protocol':PROTOCOL,'provider':PROVIDER,'stage3_single_axis_Emax':{'l_logstep':ELOG,'l_linstep':ELIN},'required_pairs':ORDER,'pair_values':{k:{'l_logstep':v[0],'l_linstep':v[1]} for k,v in VALUES.items()},'missing_products':missing,'unexpected_products':unexpected,'cross_lane_input_identity':identity,'pairs':lanes,'distance_to_LPAIR_T2':dist,'interaction_supported':interaction,'direction_monotone_supported':monotone,'interaction_gain':gain,'classification':cls,'K1_promoted':False,'physical_falsification':False,'interpretation_ceiling':'Numerical transfer-l sampling diagnostic only; no global convergence, code-defect, production-tuning, K1/K3/K4, or physical M21 claim.'}; out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'identity':identity,'Emax':{k:v['Emax'] for k,v in lanes.items()},'classes':{k:v['classification'] for k,v in lanes.items()},'interaction_gain':gain},indent=2,sort_keys=True));
 if cls=='M21_G2B_L_SAMPLING_AUDIT_BLOCKED': raise SystemExit(1)
if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: l_sampling_direction_interaction_audit.py COMPONENTS OUT.json')
 main(Path(sys.argv[1]),Path(sys.argv[2]))
