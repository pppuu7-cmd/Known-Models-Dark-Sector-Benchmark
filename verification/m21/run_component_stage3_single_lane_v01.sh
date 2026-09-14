#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: $0 PARAMETER_ID" >&2
  exit 2
fi

parameter="$1"
CLASS_PIN="e85808324f51fc694d12e3ed7439552a3c3f9540"
profile="stage3_${parameter}.pre"
manifest="stage3_${parameter}_manifest.json"

python3 -m pip install --disable-pip-version-check --no-input numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$CLASS_PIN"
test "$(git -C class rev-parse HEAD)" = "$CLASS_PIN"
python3 verification/m21/mixed_cold_warm_k1_reference.py prepare m21_cases
make -C class -j2 > build.log 2>&1
python3 verification/m21/build_component_stage3_single_profile.py \
  "$parameter" \
  class/cl_permille.pre \
  verification/m21/m21_ncdm_tight.pre \
  "$profile" \
  "$manifest"

mkdir -p output
: > case_status.tsv
any_fail=0
for case_name in ref f2 f3 f4; do
  set +e
  timeout 2700 ./class/class "m21_cases/${case_name}.ini" "$profile" > "run_${case_name}.log" 2>&1
  rc=$?
  set -e
  printf '%s\t%s\n' "$case_name" "$rc" >> case_status.tsv
  if [ "$rc" -ne 0 ]; then
    any_fail=1
  fi
done

PARAMETER_NAME="$parameter" CLASS_PIN_ENV="$CLASS_PIN" PROFILE="$profile" MANIFEST="$manifest" python3 - <<'PY'
import hashlib
import json
import os
import pathlib
import subprocess

parameter=os.environ['PARAMETER_NAME']
pin=os.environ['CLASS_PIN_ENV']
profile=pathlib.Path(os.environ['PROFILE'])
manifest_path=pathlib.Path(os.environ['MANIFEST'])
H=lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip()
manifest=json.loads(manifest_path.read_text())
status={}
for line in pathlib.Path('case_status.tsv').read_text().splitlines():
    case, rc=line.split('\t')
    status[case]=int(rc)
obj={
  'schema':'KMDSB.W04.M21.Stage3SingleParameterLane.v0.1',
  'protocol':'protocol/W04_M21_CMB_PRECISION_STAGE3_SINGLE_PARAMETER_DECOMPOSITION_v0.1.md',
  'parameter':parameter,
  'subgroup':manifest['subgroup'],
  'parameter_key':manifest['parameter_key'],
  'parameter_value':manifest['parameter_value'],
  'provider_head':head,
  'exact_head':head==pin,
  'case_rc':status,
  'all_cases_rc0':set(status)=={'ref','f2','f3','f4'} and all(v==0 for v in status.values()),
  'ini_sha256':{c:H('m21_cases/'+c+'.ini') for c in ('ref','f2','f3','f4')},
  'base_cl_permille_sha256':H('class/cl_permille.pre'),
  'ncdm_tight_sha256':H('verification/m21/m21_ncdm_tight.pre'),
  'stage3_pre_sha256':H(profile),
  'manifest_sha256':H(manifest_path),
  'duplicate_free_serialization':manifest.get('duplicate_free_serialization') is True,
  'stage3_assignment_count':manifest.get('stage3_assignment_count'),
  'expected_conflict_keys':manifest.get('expected_conflict_keys'),
  'observed_conflict_keys':sorted(x['key'] for x in manifest.get('observed_conflicts',[])),
}
pathlib.Path('lane_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
assert obj['exact_head']
assert obj['duplicate_free_serialization']
assert obj['stage3_assignment_count']==1
assert obj['observed_conflict_keys']==obj['expected_conflict_keys']
PY

exit "$any_fail"
