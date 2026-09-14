#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "usage: $0 G1|G2|G3 ref|f2|f3|f4" >&2
  exit 2
fi

group="$1"
case_name="$2"
CLASS_PIN="e85808324f51fc694d12e3ed7439552a3c3f9540"

case "$group" in
  G1|G2|G3) ;;
  *) echo "invalid group: $group" >&2; exit 2 ;;
esac
case "$case_name" in
  ref|f2|f3|f4) ;;
  *) echo "invalid case: $case_name" >&2; exit 2 ;;
esac

python3 -m pip install --disable-pip-version-check --no-input numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$CLASS_PIN"
test "$(git -C class rev-parse HEAD)" = "$CLASS_PIN"
python3 verification/m21/mixed_cold_warm_k1_reference.py prepare m21_cases
make -C class -j2 > "build_${case_name}.log" 2>&1

profile="component_${group}_v02.pre"
manifest="component_${group}_merge_manifest.json"
python3 verification/m21/build_component_precision_profile.py \
  "$group" \
  class/cl_permille.pre \
  verification/m21/m21_ncdm_tight.pre \
  "$profile" \
  "$manifest"

mkdir -p output
set +e
timeout 2700 ./class/class "m21_cases/${case_name}.ini" "$profile" > "run_${case_name}.log" 2>&1
rc=$?
set -e
echo "$rc" > provider_rc.txt
test "$rc" -eq 0
test -s "output/${case_name}_00_cl.dat" -o -s "output/${case_name}_cl.dat"
test -s "output/${case_name}_00_pk.dat" -o -s "output/${case_name}_pk.dat"
test -s "output/${case_name}_00_background.dat" -o -s "output/${case_name}_background.dat"

GROUP_NAME="$group" CASE_NAME="$case_name" CLASS_PIN_ENV="$CLASS_PIN" PROFILE="$profile" MERGE_MANIFEST="$manifest" python3 - <<'PY'
import hashlib
import json
import os
import pathlib
import subprocess

group=os.environ['GROUP_NAME']
case=os.environ['CASE_NAME']
pin=os.environ['CLASS_PIN_ENV']
profile=pathlib.Path(os.environ['PROFILE'])
merge_path=pathlib.Path(os.environ['MERGE_MANIFEST'])
H=lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip()
merge=json.loads(merge_path.read_text())
obj={
  'schema':'KMDSB.W04.M21.CMBPrecisionComponentLaneRecovery.v0.2',
  'recovery_protocol':'protocol/W04_M21_CMB_PRECISION_COMPONENT_SERIALIZATION_RECOVERY_v0.2.md',
  'group':group,
  'case':case,
  'provider_head':head,
  'exact_head':head==pin,
  'provider_rc':int(pathlib.Path('provider_rc.txt').read_text()),
  'ini_sha256':H('m21_cases/'+case+'.ini'),
  'base_cl_permille_sha256':H('class/cl_permille.pre'),
  'ncdm_tight_sha256':H('verification/m21/m21_ncdm_tight.pre'),
  'component_pre_sha256':H(profile),
  'merge_manifest_sha256':H(merge_path),
  'duplicate_free_serialization':merge.get('duplicate_free_serialization') is True,
  'observed_conflict_keys':sorted(x['key'] for x in merge.get('observed_conflicts',[])),
  'expected_conflict_keys':merge.get('expected_conflict_keys'),
}
pathlib.Path('lane_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
assert obj['exact_head'] and obj['provider_rc']==0 and obj['duplicate_free_serialization']
assert obj['observed_conflict_keys']==obj['expected_conflict_keys']
PY
