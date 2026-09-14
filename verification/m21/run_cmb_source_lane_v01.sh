#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then echo "usage: $0 LANE" >&2; exit 2; fi
lane="$1"
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
CONFIG='verification/m21/m21_perturbation_state_gate_config.json'
PROFILE="cmb_source_${lane}.pre"
PMAN="cmb_source_${lane}_profile_manifest.json"
python3 -m pip install --disable-pip-version-check --no-input numpy==2.2.6 scipy==1.15.3 Cython==3.1.3 > python_deps.log 2>&1
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$PIN"
test "$(git -C class rev-parse HEAD)" = "$PIN"
python3 -m pip install --disable-pip-version-check --no-input --no-build-isolation ./class > classy_build.log 2>&1
python3 verification/m21/mixed_cold_warm_k1_reference.py prepare cmb_source_cases
python3 verification/m21/build_perturbation_state_lane_profile.py "$lane" class/cl_permille.pre verification/m21/m21_ncdm_tight.pre "$PROFILE" "$PMAN"
python3 verification/m21/extract_cmb_sources_v01.py cmb_source_cases "$PROFILE" "$CONFIG" source_out "$lane" > source_extract.log 2>&1
LANE="$lane" PIN_ENV="$PIN" PROFILE="$PROFILE" PMAN="$PMAN" CONFIG_ENV="$CONFIG" python3 - <<'PY'
import hashlib,json,os,pathlib,subprocess
H=lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip()
pm=json.load(open(os.environ['PMAN'])); sm=json.load(open('source_out/lane_sources_meta.json'))
obj={'schema':'KMDSB.W04.M21.DirectCMBSourcesWorkflowLane.v0.1','protocol':'protocol/W04_M21_CONDITIONAL_CMB_SOURCE_BRANCH_SIGNATURE_v0.1.md','lane':os.environ['LANE'],'provider_head':head,'exact_head':head==os.environ['PIN_ENV'],'profile_manifest':pm,'profile_sha256':H(os.environ['PROFILE']),'config_sha256':H(os.environ['CONFIG_ENV']),'sources_meta_sha256':H('source_out/lane_sources_meta.json'),'all_four_cases_present':set(sm.get('cases',{}))=={'ref','f2','f3','f4'}}
pathlib.Path('lane_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
assert obj['exact_head'] and obj['all_four_cases_present'] and pm['lane']==os.environ['LANE']
PY
