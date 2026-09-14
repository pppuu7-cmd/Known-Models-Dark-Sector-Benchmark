#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then echo "usage: $0 A|B" >&2; exit 2; fi
pair="$1"
case "$pair" in
  A) lane='P400_ON_TAIL_OFF' ;;
  B) lane='P400_EVEN_TAIL_OFF' ;;
  *) echo "bad pair: $pair" >&2; exit 2 ;;
esac
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
profile="l400_diag_${lane}.pre"
profile_manifest="l400_diag_${lane}_profile_manifest.json"
patch_manifest='l400_transfer_harmonic_patch_manifest.json'

python3 -m pip install --disable-pip-version-check --no-input numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$PIN"
test "$(git -C class rev-parse HEAD)" = "$PIN"
python3 verification/m21/apply_l400_transfer_harmonic_diag.py class/source/harmonic.c "$patch_manifest"
test "$(git -C class diff --name-only)" = 'source/harmonic.c'
git -C class diff --check

python3 verification/m21/mixed_cold_warm_k1_reference.py prepare m21_cases
python3 verification/m21/build_l_grid_phase_profile.py "$lane" class/cl_permille.pre verification/m21/m21_ncdm_tight.pre "$profile" "$profile_manifest"
make -C class -j2 > build.log 2>&1

mkdir -p output
: > case_status.tsv
any_fail=0
for c in ref f2 f3 f4; do
  set +e
  KMDSB_M21_L400_TRANSFER_DIAG="$(pwd)/diag_${c}.dat" timeout 2700 ./class/class "m21_cases/${c}.ini" "$profile" > "run_${c}.log" 2>&1
  rc=$?
  set -e
  printf '%s\t%s\n' "$c" "$rc" >> case_status.tsv
  if [ "$rc" -ne 0 ]; then any_fail=1; fi
done

PAIR="$pair" LANE="$lane" PIN_ENV="$PIN" PROFILE="$profile" PMAN="$profile_manifest" PATCH="$patch_manifest" python3 - <<'PY'
import hashlib,json,os,pathlib,subprocess
H=lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
status={}
for x in pathlib.Path('case_status.tsv').read_text().splitlines():
    c,rc=x.split('\t'); status[c]=int(rc)
pm=json.load(open(os.environ['PMAN']))
patch=json.load(open(os.environ['PATCH']))
head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip()
cases=('ref','f2','f3','f4')
diag_files={c:f'diag_{c}.dat' for c in cases}
obj={
  'schema':'KMDSB.W04.M21.L400TransferHarmonicLaneMeta.v0.1',
  'protocol':'protocol/W04_M21_L400_TRANSFER_VS_HARMONIC_DIAGNOSTIC_v0.1.md',
  'pair_id':os.environ['PAIR'],
  'lane':os.environ['LANE'],
  'provider_head':head,
  'exact_head':head==os.environ['PIN_ENV'],
  'case_rc':status,
  'all_cases_rc0':set(status)==set(cases) and all(v==0 for v in status.values()),
  'ini_sha256':{c:H('m21_cases/'+c+'.ini') for c in cases},
  'cl_permille_sha256':H('class/cl_permille.pre'),
  'ncdm_tight_sha256':H('verification/m21/m21_ncdm_tight.pre'),
  'profile_sha256':H(os.environ['PROFILE']),
  'profile_manifest_sha256':H(os.environ['PMAN']),
  'patch_manifest_sha256':H(os.environ['PATCH']),
  'patch_original_harmonic_sha256':patch['original_sha256'],
  'patch_patched_harmonic_sha256':patch['patched_sha256'],
  'l_logstep':pm['l_logstep'],
  'l_linstep':pm['l_linstep'],
  'sparse_l_signature':pm['sparse_l_signature'],
  'varied_keys':pm['varied_keys'],
  'varied_key_count':pm['varied_key_count'],
  'duplicate_free_serialization':pm['duplicate_free_serialization'],
  'diagnostic_files':diag_files,
  'all_diag_files_present_nonempty':all(pathlib.Path(p).exists() and pathlib.Path(p).stat().st_size>0 for p in diag_files.values()),
  'only_tracked_source_modified':'source/harmonic.c'==subprocess.check_output(['git','-C','class','diff','--name-only'],text=True).strip(),
}
pathlib.Path('lane_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
assert obj['exact_head'] and obj['varied_keys']==['l_logstep','l_linstep'] and obj['varied_key_count']==2 and obj['duplicate_free_serialization'] and obj['only_tracked_source_modified']
if obj['all_cases_rc0']:
    assert obj['all_diag_files_present_nonempty']
print(json.dumps(obj,indent=2,sort_keys=True))
PY

exit "$any_fail"
