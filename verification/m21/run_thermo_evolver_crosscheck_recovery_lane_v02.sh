#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then echo "usage: $0 LANE" >&2; exit 2; fi
lane="$1"; PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'; profile="thermo_evolver_recovery_${lane}.pre"; manifest="thermo_evolver_recovery_${lane}_manifest.json"
python3 -m pip install --disable-pip-version-check --no-input numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$PIN"
test "$(git -C class rev-parse HEAD)" = "$PIN"
python3 verification/m21/mixed_cold_warm_k1_reference.py prepare m21_cases
make -C class -j2 > build.log 2>&1
python3 verification/m21/build_thermo_evolver_crosscheck_profile_recovery_v02.py "$lane" class/cl_permille.pre verification/m21/m21_ncdm_tight.pre "$profile" "$manifest"
python3 - "$profile" "$manifest" <<'PY'
import json,sys
from pathlib import Path
p=Path(sys.argv[1]); m=json.loads(Path(sys.argv[2]).read_text()); vals={}
for raw in p.read_text().splitlines():
 s=raw.split('#',1)[0].strip()
 if s and '=' in s:
  k,v=(x.strip() for x in s.split('=',1)); vals[k]=v
expected='1' if m['thermo_evolver']=='ndf15' else '0'
assert vals['thermo_evolver']==expected==m['thermo_evolver_serialized']
assert vals['tol_thermo_integration']==m['tol_thermo_integration']
PY
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
obj={'schema':'KMDSB.W04.M21.ThermoEvolverCrosscheckRecoveryLane.v0.2','protocol':'protocol/W04_M21_THERMO_EVOLVER_ENUM_SERIALIZATION_RECOVERY_v0.1.md','parent_protocol':'protocol/W04_M21_CONDITIONAL_THERMO_EVOLVER_CROSSCHECK_v0.1.md','lane':os.environ['LANE'],'thermo_evolver':m['thermo_evolver'],'thermo_evolver_serialized':m['thermo_evolver_serialized'],'tol_thermo_integration':m['tol_thermo_integration'],'generic_evolver':m['generic_evolver'],'provider_head':head,'exact_head':head==os.environ['PIN_ENV'],'case_rc':status,'all_cases_rc0':set(status)=={'ref','f2','f3','f4'} and all(v==0 for v in status.values()),'ini_sha256':{c:H('m21_cases/'+c+'.ini') for c in ('ref','f2','f3','f4')},'cl_permille_sha256':H('class/cl_permille.pre'),'ncdm_tight_sha256':H('verification/m21/m21_ncdm_tight.pre'),'profile_sha256':H(os.environ['PROFILE']),'manifest_sha256':H(os.environ['MANIFEST']),'varied_keys':m['varied_keys'],'varied_key_count':m['varied_key_count'],'duplicate_free_serialization':m['duplicate_free_serialization']}
pathlib.Path('lane_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
assert obj['exact_head'] and obj['generic_evolver']=='0' and obj['thermo_evolver_serialized'] in {'0','1'} and obj['varied_keys']==['thermo_evolver','tol_thermo_integration'] and obj['varied_key_count']==2
PY
exit "$any_fail"
