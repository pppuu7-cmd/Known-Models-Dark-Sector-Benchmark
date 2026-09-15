#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then echo "usage: $0 CASE PARENT_ARTIFACT_DIR" >&2; exit 2; fi
case_id="$1"; parent_dir="$2"
case "$case_id" in ref|f2|f3|f4) ;; *) echo "bad case $case_id" >&2; exit 2;; esac
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
profile='flat_distance_P400_ON_TAIL_OFF.pre'
profile_manifest='flat_distance_P400_ON_TAIL_OFF_profile_manifest.json'
patch_manifest='flat_distance_identity_component_patch_manifest.json'
diag="flat_distance_${case_id}.dat"

python3 -m pip install --disable-pip-version-check --no-input -q numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$PIN"
test "$(git -C class rev-parse HEAD)" = "$PIN"
python3 verification/m21/apply_flat_distance_identity_component_diag.py class/source/thermodynamics.c "$patch_manifest"
test "$(git -C class diff --name-only)" = 'source/thermodynamics.c'
git -C class diff --check
python3 verification/m21/mixed_cold_warm_k1_reference.py prepare m21_cases
python3 verification/m21/build_l_grid_phase_profile.py P400_ON_TAIL_OFF class/cl_permille.pre verification/m21/m21_ncdm_tight.pre "$profile" "$profile_manifest"
make -C class -j2 > build.log 2>&1
mkdir -p output

set +e
OMP_NUM_THREADS=1 KMDSB_M21_FLAT_DISTANCE_IDENTITY_DIAG="$(pwd)/$diag" timeout 2700 ./class/class "m21_cases/${case_id}.ini" "$profile" > "run_${case_id}.log" 2>&1
rc=$?
set -e
printf '%s\t%s\n' "$case_id" "$rc" > case_status.tsv

CASE_ID="$case_id" RC="$rc" PIN_ENV="$PIN" PROFILE="$profile" PMAN="$profile_manifest" PATCH="$patch_manifest" PARENT_DIR="$parent_dir" DIAG="$diag" python3 - <<'PY'
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
c=os.environ['CASE_ID']; rc=int(os.environ['RC']); head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip(); diag=pathlib.Path(os.environ['DIAG'])
new_cl=find_cl('.',c); parent_cl=find_cl(os.environ['PARENT_DIR'],c); a=numeric(new_cl); b=numeric(parent_cl)
null_l2=float('inf') if a.shape!=b.shape else float(np.linalg.norm(a-b)/max(float(np.linalg.norm(a)),float(np.linalg.norm(b)),1e-300))
rows=[]
if diag.exists():
 for raw in diag.read_text(errors='replace').splitlines():
  p=raw.split()
  if not p: continue
  if len(p)!=11: continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in p]
  except ValueError: continue
  if all(math.isfinite(x) for x in r): rows.append(r)
obj={
 'schema':'KMDSB.W04.M21.FlatDistanceIdentityComponentCase.v0.1','protocol':'protocol/W04_M21_FLAT_DISTANCE_IDENTITY_COMPONENT_AUDIT_v0.1.md',
 'case':c,'provider_head':head,'exact_head':head==os.environ['PIN_ENV'],'class_rc':rc,'class_rc0':rc==0,'thread_control':'OMP_NUM_THREADS=1',
 'ini_sha256':H('m21_cases/'+c+'.ini'),'profile_sha256':H(os.environ['PROFILE']),'profile_manifest_sha256':H(os.environ['PMAN']),'patch_manifest_sha256':H(os.environ['PATCH']),
 'only_thermodynamics_source_modified':subprocess.check_output(['git','-C','class','diff','--name-only'],text=True).strip()=='source/thermodynamics.c',
 'diagnostic_rows':len(rows),'diagnostic_schema_clean':len(rows)==1,'flat_sgnK':(len(rows)==1 and int(round(rows[0][0]))==0),
 'parent_cl_sha256':H(parent_cl),'new_cl_sha256':H(new_cl),'null_cl_l2':null_l2,'null_cl_l2_le_1e12':null_l2<=1e-12,
 'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
obj['authority_clean']=all([obj['exact_head'],obj['class_rc0'],obj['only_thermodynamics_source_modified'],obj['diagnostic_schema_clean'],obj['flat_sgnK'],obj['null_cl_l2_le_1e12']])
pathlib.Path('case_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps(obj,indent=2,sort_keys=True))
PY
if [ "$rc" -ne 0 ]; then exit "$rc"; fi
python3 - <<'PY'
import json
assert json.load(open('case_meta.json'))['authority_clean']
PY
