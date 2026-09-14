#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np

LANES={
 'NDF_T1E5':('ndf15',1e-5),'NDF_T1E6':('ndf15',1e-6),'NDF_T1E7':('ndf15',1e-7),
 'RK_T1E5':('rk',1e-5),'RK_T1E6':('rk',1e-6),'RK_T1E7':('rk',1e-7),
}
CASES=('ref','f2','f3','f4')
COLS={'conf_time':2,'dTb':8,'w_b':9,'c_b2':10,'kappa_b':11}
CHANGE=[('NDF_T1E5','NDF_T1E6'),('NDF_T1E6','NDF_T1E7'),('RK_T1E5','RK_T1E6'),('NDF_T1E7','RK_T1E7')]
CONTROL=[('RK_T1E6','RK_T1E7'),('NDF_T1E5','RK_T1E5'),('NDF_T1E6','RK_T1E6')]
PROTOCOL='protocol/W04_M21_THERMODYNAMICS_SECONDARY_STATE_BRANCH_SIGNATURE_v0.1.md'
PROVIDER='lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540'
PARENT_CLASS='M21_CMB_BRANCH_NOT_LOCALIZED_IN_PRIMARY_THERMO_STATE_COLUMNS'

def load(p:Path):
 rows=[]
 for ln in p.read_text(errors='replace').splitlines():
  s=ln.strip()
  if not s or s.startswith('#'): continue
  try: row=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError: continue
  if row and all(math.isfinite(x) for x in row): rows.append(row)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<10 or a.shape[1]<12:
  raise RuntimeError(f'invalid thermodynamics table {p}: {a.shape}')
 return a

def one(root:Path,case:str):
 ms=sorted((root/'output').glob(f'{case}_*thermodynamics.dat'))+sorted((root/'output').glob(f'{case}_thermodynamics.dat'))
 uniq=[]
 for p in ms:
  if p not in uniq: uniq.append(p)
 if len(uniq)!=1: raise RuntimeError(f'expected one thermo table {case} in {root}: {uniq}')
 return load(uniq[0])

def xy(a,col,zlo=None,zhi=None):
 z=np.asarray(a[:,1],float); y=np.asarray(a[:,col],float)
 m=np.isfinite(z)&np.isfinite(y)&(z>=0)
 if zlo is not None: m &= z>=zlo
 if zhi is not None: m &= z<=zhi
 z,y=z[m],y[m]; q=np.argsort(z); z,y=z[q],y[q]
 z,idx=np.unique(z,return_index=True); y=y[idx]
 if z.size<5: raise RuntimeError('insufficient thermo z support')
 return z,y

def dist(a,b,col,zlo=500.,zhi=2500.):
 za,ya=xy(a,col,zlo,zhi); zb,yb=xy(b,col,zlo,zhi)
 lo=max(float(za.min()),float(zb.min())); hi=min(float(za.max()),float(zb.max()))
 m=(za>=lo)&(za<=hi); za,ya=za[m],ya[m]
 if za.size<5 or hi<=lo: raise RuntimeError('insufficient thermo overlap')
 ybi=np.interp(np.log1p(za),np.log1p(zb),yb)
 den=max(float(np.linalg.norm(ya)),float(np.linalg.norm(ybi)),1e-300)
 return {'R2_symnorm':float(np.linalg.norm(ya-ybi)/den),'n':int(za.size),'z_min':float(za.min()),'z_max':float(za.max())}

def main(comp:Path,parent_json:Path,out:Path):
 parent=json.loads(parent_json.read_text())
 identity=(parent.get('classification')==PARENT_CLASS and parent.get('cross_lane_input_identity') is True and parent.get('K1_promoted') is False and parent.get('physical_falsification') is False)
 dirs={p.name[len('m21-thermo-state-'):]:p for p in comp.iterdir() if p.is_dir() and p.name.startswith('m21-thermo-state-')} if comp.is_dir() else {}
 missing=sorted(set(LANES)-set(dirs)); unexpected=sorted(set(dirs)-set(LANES)); metas={}; tables={}
 identity &= (not missing and not unexpected)
 if identity:
  for lane,(solver,tol) in LANES.items():
   meta=json.loads((dirs[lane]/'lane_meta.json').read_text()); metas[lane]=meta
   ok=(meta.get('lane')==lane and meta.get('exact_head') is True and meta.get('all_cases_rc0') is True and meta.get('physical_lines_preserved') is True and meta.get('one_thermodynamics_file_each') is True and meta.get('thermo_evolver')==solver and float(meta.get('tol_thermo_integration','nan'))==tol)
   identity &= ok
   if ok: tables[lane]={c:one(dirs[lane],c) for c in CASES}
 for c in CASES:
  hs={m.get('state_ini_sha256',{}).get(c) for m in metas.values()}; identity &= len(hs)==1 and None not in hs
 for k in ('state_case_manifest_sha256','cl_permille_sha256','ncdm_tight_sha256'):
  hs={m.get(k) for m in metas.values()}; identity &= len(hs)==1 and None not in hs
 edges={}; branch_hits=0; control_hits=0
 if identity:
  for kind,pairs in [('branch_change',CHANGE),('same_branch_control',CONTROL)]:
   for a,b in pairs:
    name=a+'__'+b; ed={'kind':kind,'columns':{}}
    for colname,col in COLS.items():
     primary={c:dist(tables[a][c],tables[b][c],col) for c in CASES}
     full={c:dist(tables[a][c],tables[b][c],col,None,None) for c in CASES}
     j=float(primary['f3']['R2_symnorm']/max(primary['ref']['R2_symnorm'],primary['f2']['R2_symnorm'],primary['f4']['R2_symnorm'],1e-300))
     ed['columns'][colname]={'recombination_window_case_distances':primary,'full_overlap_case_distances_report_only':full,'J_f3_specific':j}
    ed['Jmax']=max(v['J_f3_specific'] for v in ed['columns'].values())
    ed['localized_Jmax_ge_3']=ed['Jmax']>=3.0; edges[name]=ed
    if kind=='branch_change' and ed['localized_Jmax_ge_3']: branch_hits+=1
    if kind=='same_branch_control' and ed['localized_Jmax_ge_3']: control_hits+=1
 if not identity: cls='M21_THERMO_SECONDARY_STATE_BRANCH_SIGNATURE_BLOCKED'
 elif branch_hits==4 and control_hits==0: cls='M21_THERMO_SECONDARY_STATE_BRANCH_SIGNATURE_MATCHES_CMB_MAP_WITH_SCOPE'
 elif branch_hits>=2: cls='M21_THERMO_SECONDARY_STATE_BRANCH_SIGNATURE_PARTIAL'
 else: cls='M21_CMB_BRANCH_NOT_LOCALIZED_IN_EXPOSED_THERMO_STATE_COLUMNS'
 result={'schema':'KMDSB.W04.M21.ThermoSecondaryStateBranchSignature.v0.1','date':'2026-09-14','protocol':PROTOCOL,'provider':PROVIDER,'parent_run_id':34887773207,'parent_classification':parent.get('classification'),'classification':cls,'cross_lane_input_identity':bool(identity),'missing_products':missing,'unexpected_products':unexpected,'primary_redshift_window':[500.0,2500.0],'secondary_columns':COLS,'branch_change_edges':[a+'__'+b for a,b in CHANGE],'same_branch_control_edges':[a+'__'+b for a,b in CONTROL],'edge_results':edges,'branch_change_localized_count':branch_hits,'same_branch_control_localized_count':control_hits,'K1_promoted':False,'physical_falsification':False,'interpretation_ceiling':'Secondary thermodynamics-state localization only; no code-defect, production setting, global convergence, K1/K3/K4, or physical M21 claim.'}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'classification':cls,'identity':identity,'branch_hits':branch_hits,'control_hits':control_hits,'Jmax':{k:v['Jmax'] for k,v in edges.items()}},indent=2,sort_keys=True))
 if cls=='M21_THERMO_SECONDARY_STATE_BRANCH_SIGNATURE_BLOCKED': raise SystemExit(1)

if __name__=='__main__':
 if len(sys.argv)!=4: raise SystemExit('usage: thermo_secondary_state_branch_signature.py COMPONENTS PARENT.json OUT.json')
 main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
