#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then echo "usage: $0 ARM ref|f2|f3|f4" >&2; exit 2; fi
arm="$1"; case_name="$2"; CLASS_PIN="e85808324f51fc694d12e3ed7439552a3c3f9540"
case "$arm" in A_NZ|A_THERMO|A_HE|A_H) ;; *) echo "invalid arm" >&2; exit 2;; esac
case "$case_name" in ref|f2|f3|f4) ;; *) echo "invalid case" >&2; exit 2;; esac
python3 -m pip install --disable-pip-version-check --no-input numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$CLASS_PIN"
test "$(git -C class rev-parse HEAD)" = "$CLASS_PIN"
python3 verification/m21/mixed_cold_warm_k1_reference.py prepare m21_cases
make -C class -j2 > "build_${case_name}.log" 2>&1
profile="g1a_single_${arm}.pre"
ARM="$arm" PROFILE="$profile" python3 - <<'PY'
from collections import OrderedDict
from pathlib import Path
import os
arm=os.environ['ARM']; out=Path(os.environ['PROFILE'])
targets={'A_NZ':('recfast_Nz0','100000'),'A_THERMO':('tol_thermo_integration','1.e-5'),'A_HE':('recfast_x_He0_trigger_delta','0.01'),'A_H':('recfast_x_H0_trigger_delta','0.01')}
def parse(p):
    z=[]
    for raw in Path(p).read_text(errors='replace').splitlines():
        line=raw.split('#',1)[0].strip()
        if not line: continue
        if '=' not in line: raise RuntimeError(f'unparsed line {raw!r}')
        k,v=(x.strip() for x in line.split('=',1)); z.append((k,v))
    return z
vals=OrderedDict()
for src in ('class/cl_permille.pre','verification/m21/m21_ncdm_tight.pre'):
    for k,v in parse(src): vals[k]=v
vals['evolver']='0'
k,v=targets[arm]
if k in vals: raise RuntimeError(f'preregistered G1A key unexpectedly already in baseline: {k}')
vals[k]=v
out.write_text('# KMDSB M21 G1A single-key profile\n# protocol: protocol/W04_M21_G1A_SINGLE_KEY_DECOMPOSITION_v0.1.md\n'+'\n'.join(f'{k} = {v}' for k,v in vals.items())+'\n')
keys=[k for k,_ in parse(out)]
assert len(keys)==len(set(keys))
PY
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
ARM="$arm" CASE_NAME="$case_name" CLASS_PIN_ENV="$CLASS_PIN" PROFILE="$profile" python3 - <<'PY'
import hashlib,json,os,pathlib,subprocess
H=lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
arm=os.environ['ARM']; case=os.environ['CASE_NAME']; pin=os.environ['CLASS_PIN_ENV']; profile=pathlib.Path(os.environ['PROFILE'])
head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip()
keys=[]
for raw in profile.read_text().splitlines():
    line=raw.split('#',1)[0].strip()
    if line and '=' in line: keys.append(line.split('=',1)[0].strip())
obj={'schema':'KMDSB.W04.M21.G1ASingleKeyLane.v0.1','protocol':'protocol/W04_M21_G1A_SINGLE_KEY_DECOMPOSITION_v0.1.md','arm':arm,'case':case,'provider_head':head,'exact_head':head==pin,'provider_rc':int(pathlib.Path('provider_rc.txt').read_text()),'profile_sha256':H(profile),'duplicate_free_serialization':len(keys)==len(set(keys)),'ini_sha256':H('m21_cases/'+case+'.ini')}
pathlib.Path('lane_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
assert obj['exact_head'] and obj['provider_rc']==0 and obj['duplicate_free_serialization']
PY
