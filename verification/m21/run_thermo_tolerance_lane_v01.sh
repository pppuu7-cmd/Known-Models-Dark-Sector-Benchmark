#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then echo "usage: $0 TOLERANCE_ID TOLERANCE_VALUE" >&2; exit 2; fi
id="$1"; value="$2"; PIN="e85808324f51fc694d12e3ed7439552a3c3f9540"; profile="thermo_tol_${id}.pre"; manifest="thermo_tol_${id}_manifest.json"
python3 -m pip install --disable-pip-version-check --no-input numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$PIN"
test "$(git -C class rev-parse HEAD)" = "$PIN"
python3 verification/m21/mixed_cold_warm_k1_reference.py prepare m21_cases
make -C class -j2 > build.log 2>&1
python3 verification/m21/build_thermo_tolerance_profile.py "$id" class/cl_permille.pre verification/m21/m21_ncdm_tight.pre "$profile" "$manifest"
test "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["tolerance_value"])' "$manifest")" = "$value"
mkdir -p output
: > case_status.tsv
any_fail=0
for c in ref f2 f3 f4; do
  set +e
  timeout 2700 ./class/class "m21_cases/${c}.ini" "$profile" > "run_${c}.log" 2>&1
  rc=$?
  set -e
  printf '%s\t%s\n' "$c" "$rc" >> case_status.tsv
  if [ "$rc" -ne 0 ]; then any_fail=1; fi
done
TOL_ID="$id" TOL_VALUE="$value" PIN_ENV="$PIN" PROFILE="$profile" MANIFEST="$manifest" python3 - <<'PY'
import hashlib,json,os,pathlib,subprocess
H=lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
id=os.environ['TOL_ID']; val=os.environ['TOL_VALUE']; pin=os.environ['PIN_ENV']; manifest=json.load(open(os.environ['MANIFEST']))
status={}
for line in pathlib.Path('case_status.tsv').read_text().splitlines(): c,rc=line.split('\t'); status[c]=int(rc)
head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip()
obj={'schema':'KMDSB.W04.M21.ThermoToleranceLane.v0.1','protocol':'protocol/W04_M21_CONDITIONAL_THERMODYNAMICS_TOLERANCE_DIRECTION_AUDIT_v0.1.md','tolerance_id':id,'tolerance_value':val,'provider_head':head,'exact_head':head==pin,'case_rc':status,'all_cases_rc0':set(status)=={'ref','f2','f3','f4'} and all(x==0 for x in status.values()),'ini_sha256':{c:H('m21_cases/'+c+'.ini') for c in ('ref','f2','f3','f4')},'cl_permille_sha256':H('class/cl_permille.pre'),'ncdm_tight_sha256':H('verification/m21/m21_ncdm_tight.pre'),'profile_sha256':H(os.environ['PROFILE']),'manifest_sha256':H(os.environ['MANIFEST']),'varied_key':manifest['varied_key'],'varied_key_count':manifest['varied_key_count'],'duplicate_free_serialization':manifest['duplicate_free_serialization']}
pathlib.Path('lane_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
assert obj['exact_head'] and obj['varied_key']=='tol_thermo_integration' and obj['varied_key_count']==1 and obj['duplicate_free_serialization']
PY
exit "$any_fail"
