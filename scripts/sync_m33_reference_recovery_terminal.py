#!/usr/bin/env python3
import csv,json,pathlib
R=pathlib.Path('.')

def rw(path, fn):
 p=R/path; rows=list(csv.reader(p.open(encoding='utf-8',newline=''))); rows=fn(rows)
 with p.open('w',encoding='utf-8',newline='') as f: csv.writer(f,lineterminator='\n').writerows(rows)

def census(rows):
 for r in rows[1:]:
  if r and r[0]=='F33':
   r[5]='K0_PASS_K1_REFERENCE_PATH_STABILITY_BOUNDARY_OPEN_K2_K9_OPEN'
   r[8]='Pinned hi_class cubic Galileon K0 PASS_WITH_SCOPE. Parser-compliant recovery run 34660258070 artifact 10286747855 executes Omega_smg={0.5,0.1,0.01}, native provider control, and plain-GR control with finite TT/P(k); Omega_smg=0.001 is rejected by the provider scalar-stability test (ghost-instability diagnostic). K1 not promoted; this is a stability/reference-path boundary, not family falsification. Analysis-only reference-path audit run is queued.'
 return rows

def mandatory(rows):
 for r in rows[1:]:
  if r and r[0]=='F33':
   r[3]='PARTIAL_REFERENCE_MAP_EXECUTABLE_STABILITY_BOUNDARY'
   r[12]='K0_PASS_K1_REFERENCE_PATH_STABILITY_BOUNDARY_OPEN_K2_K9_OPEN'
   r[13]='M33 parser-compliant recovery run 34660258070 job 103461090824 artifact 10286747855 digest sha256:4569fb114ee152b1694d4f14a44ed69aabf94c7df9b5368538d32fdb066528fd. Positive Omega_smg 0.5/0.1/0.01 plus native and GR controls execute finitely. Omega_smg=0.001 fails provider stability_tests_smg with Ghost instability (minimum D=-1.11467e-106 at a=1e-14). K1 not promoted; physical_falsification=false; stability/pathology kept separate from response representability.'
 return rows
rw(pathlib.Path('matrices/model_family_census.csv'),census); rw(pathlib.Path('matrices/mandatory_properties_matrix.csv'),mandatory)
marker='## 2026-09-12 M33 parser-compliant reference-map recovery terminal'
block=f'''\n\n{marker}\n- Run 34660258070, job 103461090824, artifact 10286747855, digest sha256:4569fb114ee152b1694d4f14a44ed69aabf94c7df9b5368538d32fdb066528fd.\n- Parser/configuration blocker is removed. Omega_smg 0.5, 0.1, 0.01 plus native and GR controls execute with finite TT/P(k).\n- Omega_smg=0.001 is rejected by pinned provider stability_tests_smg with Ghost instability (minimum D=-1.11467e-106 at a=1e-14). This is a stability/reference-path boundary, not infrastructure and not family-level falsification. K1 remains unpromoted.\n- Next gate: analysis-only immutable-artifact/source audit preregistered in W06_M33_GALILEON_REFERENCE_PATH_STABILITY_AUDIT_v0.1.md; no retuning or stability-check disabling permitted.\n'''
for fn in ['recovery/STATE.md','recovery/RESTORE_FROM_NEW_CHAT.md','logs/research_log.md']:
 p=R/fn; s=p.read_text(encoding='utf-8')
 if marker not in s: p.write_text(s.rstrip()+block+'\n',encoding='utf-8')
# readiness
rows=list(csv.reader((R/'matrices/mandatory_properties_matrix.csv').open(encoding='utf-8'))); d=rows[1:]; OPEN={'OPEN','NOT_TESTED','QUEUED','PENDING'}
def snap(rr):
 vals=[x for r in rr for x in r[2:12]]; k0=[r[2] for r in rr]
 return {'K0_assessed':sum(x not in OPEN for x in k0),'K0_positive':sum(x.startswith(('PASS','SUPPORTED')) for x in k0),'assessed_cells':sum(x not in OPEN for x in vals),'assessed_fraction':sum(x not in OPEN for x in vals)/len(vals),'families':len(rr),'gate_cells':len(vals),'positive_cells':sum(x.startswith(('PASS','SUPPORTED')) for x in vals),'positive_fraction':sum(x.startswith(('PASS','SUPPORTED')) for x in vals)/len(vals)}
out={'all_rows_including_M00_control':snap(d),'definition_assessed':'status is not exact OPEN, NOT_TESTED, QUEUED, or PENDING; blocked/partial/not-established outcomes count as investigated, not as positive','definition_positive':'status begins PASS or SUPPORTED only','mechanism_rows_excluding_M00_control':snap([r for r in d if r[0]!='F00']),'schema':'kmdsb_readiness_snapshot_v0.1'}
(R/'audits/KMDSB_READINESS_SNAPSHOT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
