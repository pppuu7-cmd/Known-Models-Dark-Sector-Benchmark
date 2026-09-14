#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then echo "usage: $0 LANE" >&2; exit 2; fi
lane="$1"
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
CONFIG='verification/m21/m21_perturbation_state_gate_config.json'
PROFILE="pert_state_${lane}.pre"
PMAN="pert_state_${lane}_profile_manifest.json"
python3 -m pip install --disable-pip-version-check --no-input numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$PIN"
test "$(git -C class rev-parse HEAD)" = "$PIN"
python3 verification/m21/prepare_perturbation_state_cases.py "$CONFIG" pert_state_cases
python3 verification/m21/build_perturbation_state_lane_profile.py "$lane" class/cl_permille.pre verification/m21/m21_ncdm_tight.pre "$PROFILE" "$PMAN"
make -C class -j2 > build.log 2>&1
mkdir -p output
: > case_status.tsv
any_fail=0
for c in ref f2 f3 f4; do
  set +e
  timeout 1200 ./class/class "pert_state_cases/${c}.ini" "$PROFILE" > "run_${c}.log" 2>&1
  rc=$?
  set -e
  printf '%s\t%s\n' "$c" "$rc" >> case_status.tsv
  if [ "$rc" -ne 0 ]; then any_fail=1; fi
done
LANE="$lane" PIN_ENV="$PIN" PROFILE="$PROFILE" PMAN="$PMAN" CONFIG_ENV="$CONFIG" python3 - <<'PY'
import hashlib,json,os,pathlib,re,subprocess
H=lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
cases=('ref','f2','f3','f4'); status={}
for x in pathlib.Path('case_status.tsv').read_text().splitlines(): c,rc=x.split('\t'); status[c]=int(rc)
head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip()
pm=json.load(open(os.environ['PMAN'])); cm=json.load(open('pert_state_cases/manifest.json')); cfg=json.load(open(os.environ['CONFIG_ENV']))
files={}; actual_k={}
for c in cases:
    xs=sorted(pathlib.Path('output').glob(f'{c}_*perturbations_k*_s.dat'))+sorted(pathlib.Path('output').glob(f'{c}_perturbations_k*_s.dat'))
    uniq=[]
    for p in xs:
        if p not in uniq: uniq.append(p)
    files[c]=[str(p) for p in uniq]
    actual=[]
    for p in uniq:
        k=None
        for line in p.read_text(errors='replace').splitlines()[:4]:
            m=re.search(r'scalar perturbations for mode k\s*=\s*([0-9eE+\-.]+)',line)
            if m: k=float(m.group(1)); break
        actual.append(k)
    actual_k[c]=actual
obj={'schema':'KMDSB.W04.M21.PerturbationStateLane.v0.1','protocol':'protocol/W04_M21_PERTURBATION_STATE_BRANCH_SIGNATURE_v0.1.md','lane':os.environ['LANE'],'provider_head':head,'exact_head':head==os.environ['PIN_ENV'],'case_rc':status,'all_cases_rc0':set(status)==set(cases) and all(v==0 for v in status.values()),'profile_manifest':pm,'case_manifest_sha256':H('pert_state_cases/manifest.json'),'config_sha256':H(os.environ['CONFIG_ENV']),'config_capability_artifact_id':cfg['capability_artifact_id'],'physical_lines_preserved':all(cm['cases'][c]['physical_lines_preserved'] for c in cases),'perturbation_files':files,'actual_k_Mpc_inv':actual_k,'five_files_each':all(len(files[c])==5 for c in cases)}
pathlib.Path('lane_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
assert obj['exact_head'] and obj['physical_lines_preserved']
if obj['all_cases_rc0']:
    assert obj['five_files_each']
    for c in cases:
        assert all(k is not None and k>0 for k in actual_k[c])
PY
exit "$any_fail"
