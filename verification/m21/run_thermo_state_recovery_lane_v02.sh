#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then echo "usage: $0 LANE" >&2; exit 2; fi
lane="$1"; PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'; profile="thermo_state_recovery_${lane}.pre"; manifest="thermo_state_recovery_${lane}_profile_manifest.json"
python3 -m pip install --disable-pip-version-check --no-input numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$PIN"
test "$(git -C class rev-parse HEAD)" = "$PIN"
python3 verification/m21/prepare_thermo_state_cases_recovery_v02.py thermo_cases
make -C class -j2 > build.log 2>&1
python3 verification/m21/build_thermo_evolver_crosscheck_profile_recovery_v02.py "$lane" class/cl_permille.pre verification/m21/m21_ncdm_tight.pre "$profile" "$manifest"
mkdir -p output; : > case_status.tsv; any_fail=0
for c in ref f2 f3 f4; do
 set +e; timeout 900 ./class/class "thermo_cases/${c}.ini" "$profile" > "run_${c}.log" 2>&1; rc=$?; set -e
 printf '%s\t%s\n' "$c" "$rc" >> case_status.tsv; if [ "$rc" -ne 0 ]; then any_fail=1; fi
done
LANE="$lane" PIN_ENV="$PIN" PROFILE="$profile" PMAN="$manifest" python3 - <<'PY'
import hashlib,json,os,pathlib,subprocess
H=lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest(); pm=json.load(open(os.environ['PMAN'])); cm=json.load(open('thermo_cases/manifest.json')); status={}
for x in pathlib.Path('case_status.tsv').read_text().splitlines(): c,rc=x.split('\t'); status[c]=int(rc)
head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip(); cases=('ref','f2','f3','f4')
thermo_files={}
for c in cases:
 ms=sorted(pathlib.Path('output').glob(f'{c}_*thermodynamics.dat'))+sorted(pathlib.Path('output').glob(f'{c}_thermodynamics.dat'))
 uniq=[]
 for p in ms:
  if p not in uniq: uniq.append(p)
 thermo_files[c]=[str(p) for p in uniq]
obj={'schema':'KMDSB.W04.M21.ThermoStateRecoveryLane.v0.2','protocol':'protocol/W04_M21_THERMO_STATE_DOWNSTREAM_OUTPUT_RECOVERY_v0.1.md','parent_protocol':'protocol/W04_M21_THERMODYNAMICS_STATE_BRANCH_SIGNATURE_v0.1.md','lane':os.environ['LANE'],'thermo_evolver':pm['thermo_evolver'],'thermo_evolver_serialized':pm['thermo_evolver_serialized'],'tol_thermo_integration':pm['tol_thermo_integration'],'provider_head':head,'exact_head':head==os.environ['PIN_ENV'],'case_rc':status,'all_cases_rc0':set(status)==set(cases) and all(v==0 for v in status.values()),'state_ini_sha256':{c:H('thermo_cases/'+c+'.ini') for c in cases},'state_case_manifest_sha256':H('thermo_cases/manifest.json'),'physical_lines_preserved':all(cm['cases'][c]['physical_lines_preserved'] for c in cases),'removed_lines':cm['removed_lines'],'added_line':cm['added_line'],'cl_permille_sha256':H('class/cl_permille.pre'),'ncdm_tight_sha256':H('verification/m21/m21_ncdm_tight.pre'),'profile_sha256':H(os.environ['PROFILE']),'profile_manifest_sha256':H(os.environ['PMAN']),'thermodynamics_files':thermo_files,'one_thermodynamics_file_each':all(len(thermo_files[c])==1 for c in cases)}
pathlib.Path('lane_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
assert obj['exact_head'] and obj['physical_lines_preserved'] and obj['removed_lines']==['output = tCl,pCl,mPk','non linear = halofit'] and obj['added_line']=='write_thermodynamics = yes' and obj['thermo_evolver_serialized'] in {'0','1'}
if obj['all_cases_rc0']: assert obj['one_thermodynamics_file_each']
PY
exit "$any_fail"
