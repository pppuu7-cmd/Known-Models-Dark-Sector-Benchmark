#!/usr/bin/env python3
import json,pathlib,sys
PINS={'P0':'e85808324f51fc694d12e3ed7439552a3c3f9540','P1':'64bbab707faf4de4779a9e04edd180fef18d98fa'}
def main(root,parent,out):
 root=pathlib.Path(root); E={}
 for p in root.rglob('case_meta.json'):
  m=json.load(open(p)); k=(m.get('provider_label'),m.get('cosmology_id'))
  if k[0] in PINS and k[1] in ('base','h105'): E[k]=m
 if set(E)!={(p,c) for p in PINS for c in ('base','h105')}: raise RuntimeError('missing intervention cells')
 par=json.load(open(parent)); assert par.get('classification')=='M21_LATE_SOURCE_CROSS_COSMOLOGY_PROVIDER_REGRESSION_BLOCKED' and par.get('all_authority_clean') is True
 parent_inert=True
 for p in PINS:
  cells=par['providers'][p]['cells']
  parent_inert &= all(cells[c]['below_one'] and not cells[c]['structural_rule_pass'] for c in ('h95','ob95','ob105','odm95','odm105'))
 clean=all(m.get('authority_clean') is True and m.get('provider_pin')==PINS[k[0]] for k,m in E.items())
 pat={(p,c):(bool(E[(p,c)]['l400_count_changed']),bool(E[(p,c)]['cl_changed'])) for p in PINS for c in ('base','h105')}
 same=all(pat[('P0',c)]==pat[('P1',c)] for c in ('base','h105'))
 active=all(a and b for a,b in pat.values()); inert=all((not a) and (not b) for a,b in pat.values())
 if clean and parent_inert and active: cls='M21_LATE_SOURCE_BRANCH_TOPOLOGY_INTERACTION_CAUSALLY_SUPPORTED_WITH_SCOPE';rc=0
 elif clean and inert: cls='M21_LATE_SOURCE_BRANCH_INTERVENTION_INERT_WITH_SCOPE';rc=0
 elif clean and same: cls='M21_LATE_SOURCE_BRANCH_SENSITIVITY_COSMOLOGY_DEPENDENT_WITH_SCOPE';rc=0
 else: cls='M21_LATE_SOURCE_BRANCH_TOPOLOGY_INTERACTION_BLOCKED';rc=1
 o={'schema':'KMDSB.W04.M21.BranchTopologyInteraction.v0.1','protocol':'protocol/W04_M21_LATE_SOURCE_BRANCH_TOPOLOGY_INTERACTION_v0.1.md','parent_run':34918945022,'parent_artifact':10377492480,'classification':cls,'parent_below_unity_interventions_inert':parent_inert,'all_authority_clean':clean,'provider_pattern_agrees':same,'cases':{f'{p}:{c}':E[(p,c)] for p in PINS for c in ('base','h105')},'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False,'class_defect_claimed':False,'production_fix_claimed':False}
 pathlib.Path(out).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n');print(json.dumps(o,indent=2,sort_keys=True));return rc
if __name__=='__main__': raise SystemExit(main(sys.argv[1],sys.argv[2],sys.argv[3]))
