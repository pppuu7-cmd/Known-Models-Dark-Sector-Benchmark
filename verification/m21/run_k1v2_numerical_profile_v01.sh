#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then echo "usage: $0 ROLE SOLVER" >&2; exit 2; fi
role="$1"; solver="$2"; PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'; profile="k1v2_${role}.pre"; manifest="k1v2_${role}_manifest.json"
python3 -m pip install --disable-pip-version-check --no-input numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$PIN"
test "$(git -C class rev-parse HEAD)" = "$PIN"
python3 verification/m21/mixed_cold_warm_k1_reference.py prepare m21_cases
make -C class -j2 > build.log 2>&1
python3 verification/m21/build_k1v2_numerical_profile.py "$role" "$solver" class/cl_permille.pre verification/m21/m21_ncdm_tight.pre "$profile" "$manifest"
mkdir -p output; : > case_status.tsv; any_fail=0
for c in ref f0 f1 f2 f3 f4; do
 set +e; timeout 3600 ./class/class "m21_cases/${c}.ini" "$profile" > "run_${c}.log" 2>&1; rc=$?; set -e
 printf '%s\t%s\n' "$c" "$rc" >> case_status.tsv; if [ "$rc" -ne 0 ]; then any_fail=1; fi
done
ROLE="$role" SOLVER="$solver" PIN_ENV="$PIN" PROFILE="$profile" MANIFEST="$manifest" python3 - <<'PY'
import hashlib,json,os,pathlib,subprocess
H=lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest(); m=json.load(open(os.environ['MANIFEST'])); status={}
for x in pathlib.Path('case_status.tsv').read_text().splitlines(): c,rc=x.split('\t'); status[c]=int(rc)
head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip(); cases=('ref','f0','f1','f2','f3','f4')
obj={'schema':'KMDSB.W04.M21.K1V2ExecutionLane.v0.1','protocol':'protocol/W04_M21_CONDITIONAL_K1_V2_NUMERICAL_REFERENCE_PREREGISTRATION_v0.1.md','role':os.environ['ROLE'],'thermo_evolver':os.environ['SOLVER'],'thermo_evolver_serialized':m['thermo_evolver_serialized'],'tol_thermo_integration':m['tol_thermo_integration'],'l_logstep':m['l_logstep'],'l_linstep':m['l_linstep'],'provider_head':head,'exact_head':head==os.environ['PIN_ENV'],'case_rc':status,'all_cases_rc0':set(status)==set(cases) and all(v==0 for v in status.values()),'ini_sha256':{c:H('m21_cases/'+c+'.ini') for c in cases},'cl_permille_sha256':H('class/cl_permille.pre'),'ncdm_tight_sha256':H('verification/m21/m21_ncdm_tight.pre'),'profile_sha256':H(os.environ['PROFILE']),'manifest_sha256':H(os.environ['MANIFEST']),'duplicate_free_serialization':m['duplicate_free_serialization']}
pathlib.Path('lane_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
assert obj['exact_head'] and obj['thermo_evolver'] in {'rk','ndf15'} and obj['duplicate_free_serialization']
PY
exit "$any_fail"
