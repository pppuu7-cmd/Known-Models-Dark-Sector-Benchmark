#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 3 ]; then echo "usage: $0 CASE LANE PARENT_ARTIFACT_DIR" >&2; exit 2; fi
case_id="$1"; lane_id="$2"; parent_dir="$3"
case "$case_id" in ref|f2|f3|f4) ;; *) echo "bad case $case_id" >&2; exit 2;; esac
case "$lane_id" in native|flat_identity_predicate) ;; *) echo "bad lane $lane_id" >&2; exit 2;; esac
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
profile='flat_identity_P400_ON_TAIL_OFF.pre'
profile_manifest='flat_identity_P400_ON_TAIL_OFF_profile_manifest.json'
patch_manifest='l400_flat_identity_predicate_patch_manifest.json'
diag="flat_identity_${case_id}_${lane_id}.dat"

python3 -m pip install --disable-pip-version-check --no-input -q numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$PIN"
test "$(git -C class rev-parse HEAD)" = "$PIN"
python3 verification/m21/apply_l400_flat_identity_predicate_counterfactual.py class/source/transfer.c "$patch_manifest"
test "$(git -C class diff --name-only)" = 'source/transfer.c'
git -C class diff --check
python3 verification/m21/mixed_cold_warm_k1_reference.py prepare m21_cases
python3 verification/m21/build_l_grid_phase_profile.py P400_ON_TAIL_OFF class/cl_permille.pre verification/m21/m21_ncdm_tight.pre "$profile" "$profile_manifest"
make -C class -j2 > build.log 2>&1
mkdir -p output

set +e
if [ "$lane_id" = flat_identity_predicate ]; then
  OMP_NUM_THREADS=1 KMDSB_M21_FLAT_IDENTITY_PREDICATE_CF=1 KMDSB_M21_FLAT_IDENTITY_DIAG="$(pwd)/$diag" timeout 2700 ./class/class "m21_cases/${case_id}.ini" "$profile" > "run_${case_id}_${lane_id}.log" 2>&1
else
  OMP_NUM_THREADS=1 KMDSB_M21_FLAT_IDENTITY_DIAG="$(pwd)/$diag" timeout 2700 ./class/class "m21_cases/${case_id}.ini" "$profile" > "run_${case_id}_${lane_id}.log" 2>&1
fi
rc=$?
set -e
printf '%s\t%s\t%s\n' "$case_id" "$lane_id" "$rc" > case_status.tsv

CASE_ID="$case_id" LANE_ID="$lane_id" RC="$rc" PIN_ENV="$PIN" PROFILE="$profile" PMAN="$profile_manifest" PATCH="$patch_manifest" PARENT_DIR="$parent_dir" DIAG="$diag" python3 - <<'PY'
import hashlib,json,math,os,pathlib,subprocess
import numpy as np
H=lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def numeric(p):
 rows=[]
 for raw in pathlib.Path(p).read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s or s.startswith('#'): continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError: continue
  if r and all(math.isfinite(x) for x in r): rows.append(r)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<3: raise RuntimeError(f'bad table {p}: {a.shape}')
 return a
def find_cl(root,c):
 out=pathlib.Path(root)/'output'; xs=[]
 for pat in (f'{c}_*_cl.dat',f'{c}_cl.dat'):
  for p in out.glob(pat):
   if p not in xs: xs.append(p)
 if len(xs)!=1: raise RuntimeError(f'cl discovery {out}/{c}: {xs}')
 return xs[0]
c=os.environ['CASE_ID']; lane=os.environ['LANE_ID']; rc=int(os.environ['RC']); diag=pathlib.Path(os.environ['DIAG'])
head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip(); patch=json.load(open(os.environ['PATCH']))
new_cl=find_cl('.',c); parent_cl=find_cl(os.environ['PARENT_DIR'],c); a=numeric(new_cl); b=numeric(parent_cl)
parent_l2=float('inf') if a.shape!=b.shape else float(np.linalg.norm(a-b)/max(float(np.linalg.norm(a)),float(np.linalg.norm(b)),1e-300))
rows=[]; malformed=0
if diag.exists():
 for raw in diag.read_text(errors='replace').splitlines():
  p=raw.split()
  if len(p)!=17: malformed+=1; continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in p]
  except ValueError: malformed+=1; continue
  if not all(math.isfinite(x) for x in r): malformed+=1; continue
  rows.append(r)
cf_flags={int(round(r[16])) for r in rows}; eff={r[4] for r in rows}
expected_cf=(lane=='flat_identity_predicate')
cf_state_ok=(cf_flags==({1} if expected_cf else {0}))
eff_state_ok=(len(eff)==1 and ((next(iter(eff))==1.0) if expected_cf else True))
obj={
 'schema':'KMDSB.W04.M21.FlatIdentityPredicateCase.v0.1','protocol':'protocol/W04_M21_L400_CONDITIONAL_FLAT_IDENTITY_PREDICATE_COUNTERFACTUAL_v0.1.md',
 'case':c,'lane':lane,'provider_head':head,'exact_head':head==os.environ['PIN_ENV'],'class_rc':rc,'class_rc0':rc==0,
 'thread_control':'OMP_NUM_THREADS=1','ini_sha256':H('m21_cases/'+c+'.ini'),'profile_sha256':H(os.environ['PROFILE']),'profile_manifest_sha256':H(os.environ['PMAN']),'patch_manifest_sha256':H(os.environ['PATCH']),
 'only_transfer_source_modified':subprocess.check_output(['git','-C','class','diff','--name-only'],text=True).strip()=='source/transfer.c',
 'diagnostic_rows':len(rows),'diagnostic_malformed_rows':malformed,'diagnostic_schema_clean':len(rows)>0 and malformed==0,'counterfactual_state_ok':cf_state_ok,'effective_rescaling_state_ok':eff_state_ok,
 'parent_cl_sha256':H(parent_cl),'new_cl_sha256':H(new_cl),'parent_full_cmb_l2':parent_l2,'native_null_l2_le_1e12':(parent_l2<=1e-12 if lane=='native' else None),
 'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
checks=[obj['exact_head'],obj['class_rc0'],obj['only_transfer_source_modified'],obj['diagnostic_schema_clean'],obj['counterfactual_state_ok'],obj['effective_rescaling_state_ok']]
if lane=='native': checks.append(obj['native_null_l2_le_1e12'])
obj['authority_clean']=all(checks)
pathlib.Path('case_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps(obj,indent=2,sort_keys=True))
PY
if [ "$rc" -ne 0 ]; then exit "$rc"; fi
python3 - <<'PY'
import json
assert json.load(open('case_meta.json'))['authority_clean']
PY
