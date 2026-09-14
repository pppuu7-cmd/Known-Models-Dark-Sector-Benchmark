#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then echo "usage: $0 LANE" >&2; exit 2; fi
lane="$1"; PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'; profile="ltail_${lane}.pre"; manifest="ltail_${lane}_manifest.json"
python3 -m pip install --disable-pip-version-check --no-input numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$PIN"
test "$(git -C class rev-parse HEAD)" = "$PIN"
python3 verification/m21/mixed_cold_warm_k1_reference.py prepare m21_cases
make -C class -j2 > build.log 2>&1
python3 verification/m21/build_l_sampling_tail_profile.py "$lane" class/cl_permille.pre verification/m21/m21_ncdm_tight.pre "$profile" "$manifest"
mkdir -p output; : > case_status.tsv; any_fail=0
for c in ref f2 f3 f4; do
 set +e; timeout 2700 ./class/class "m21_cases/${c}.ini" "$profile" > "run_${c}.log" 2>&1; rc=$?; set -e
 printf '%s\t%s\n' "$c" "$rc" >> case_status.tsv; if [ "$rc" -ne 0 ]; then any_fail=1; fi
done
LANE="$lane" PIN_ENV="$PIN" PROFILE="$profile" MANIFEST="$manifest" python3 - <<'PY'
import hashlib,json,os,pathlib,subprocess
H=lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest(); m=json.load(open(os.environ['MANIFEST'])); status={}
for x in pathlib.Path('case_status.tsv').read_text().splitlines(): c,rc=x.split('\t'); status[c]=int(rc)
head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip()
obj={'schema':'KMDSB.W04.M21.LSamplingTailLane.v0.1','protocol':'protocol/W04_M21_G2B_L_SAMPLING_TAIL_CONVERGENCE_v0.1.md','lane':os.environ['LANE'],'l_logstep':m['l_logstep'],'l_linstep':m['l_linstep'],'provider_head':head,'exact_head':head==os.environ['PIN_ENV'],'case_rc':status,'all_cases_rc0':set(status)=={'ref','f2','f3','f4'} and all(v==0 for v in status.values()),'ini_sha256':{c:H('m21_cases/'+c+'.ini') for c in ('ref','f2','f3','f4')},'cl_permille_sha256':H('class/cl_permille.pre'),'ncdm_tight_sha256':H('verification/m21/m21_ncdm_tight.pre'),'profile_sha256':H(os.environ['PROFILE']),'manifest_sha256':H(os.environ['MANIFEST']),'varied_keys':m['varied_keys'],'varied_key_count':m['varied_key_count'],'duplicate_free_serialization':m['duplicate_free_serialization']}
pathlib.Path('lane_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
assert obj['exact_head'] and obj['varied_keys']==['l_logstep','l_linstep'] and obj['varied_key_count']==2 and obj['duplicate_free_serialization']
PY
exit "$any_fail"
