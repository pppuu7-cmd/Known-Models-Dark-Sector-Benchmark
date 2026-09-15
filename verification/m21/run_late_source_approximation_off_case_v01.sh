#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 3 ]; then echo "usage: $0 PROVIDER_LABEL COSMOLOGY_ID PARENT_DIR" >&2; exit 2; fi
p="$1"; c="$2"; parent="$3"
case "$p" in P0) PIN='e85808324f51fc694d12e3ed7439552a3c3f9540';; P1) PIN='64bbab707faf4de4779a9e04edd180fef18d98fa';; *) exit 2;; esac
case "$c" in base|h95|h105|ob95|ob105|odm95|odm105);;*) exit 2;; esac
python3 -m pip install --disable-pip-version-check --no-input -q numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class && git -C class checkout -q --detach "$PIN"
python3 verification/m21/build_late_source_cross_cosmology_case.py "$c" cases
python3 verification/m21/build_l_grid_phase_profile.py P400_ON_TAIL_OFF class/cl_permille.pre verification/m21/m21_ncdm_tight.pre base.pre base_profile_manifest.json
python3 - <<'PY'
from pathlib import Path
p=Path('base.pre');t=p.read_text();
if 'transfer_neglect_late_source' in t: raise RuntimeError('baseline unexpectedly sets transfer_neglect_late_source')
Path('off.pre').write_text(t+'transfer_neglect_late_source = 1000000000\n')
PY
python3 - <<PY
from pathlib import Path
src=Path('cases/${c}_patched_native.ini').read_text();Path('off.ini').write_text(src.replace('root = native_output/${c}_','root = off_output/${c}_',1))
PY
python3 verification/m21/apply_late_source_cross_provider_counterfactual.py class/source/transfer.c off_patch_manifest.json "$PIN"
test "$(git -C class diff --name-only)" = 'source/transfer.c' && git -C class diff --check
make -C class -j2 > build.log 2>&1; mkdir -p off_output
set +e
OMP_NUM_THREADS=1 KMDSB_M21_CROSS_DIAG="$(pwd)/off.dat" timeout 2700 ./class/class off.ini off.pre > run_off.log 2>&1
rc=$?;set -e
P="$p" C="$c" PIN="$PIN" RC="$rc" PARENT="$parent" python3 - <<'PY'
import json,math,os,pathlib,subprocess
P=pathlib.Path(os.environ['PARENT'])
def load(p):
 d={};bad=0
 for z in pathlib.Path(p).read_text(errors='replace').splitlines():
  x=z.split()
  if len(x)!=15:bad+=1;continue
  try:r=[float(v.replace('D','E').replace('d','e')) for v in x]
  except:bad+=1;continue
  if not all(math.isfinite(v) for v in r):bad+=1;continue
  k=(int(round(r[2])),int(round(r[0])));d[k]=r
 return d,bad
def one(root,pat):
 x=list(pathlib.Path(root).rglob(pat))
 if len(x)!=1:raise RuntimeError((pat,x))
 return x[0]
o,bad=load('off.dat'); n,_=load(one(P,'native.dat')); cf,_=load(one(P,'cf.dat')); keys=set(o); same=keys==set(n)==set(cf) and len(keys)>0
maxk=float('inf')
if same:
 maxk=max(max(abs(o[k][1]-n[k][1]),abs(o[k][1]-cf[k][1]))/max(abs(o[k][1]),abs(n[k][1]),abs(cf[k][1]),1e-300) for k in keys)
th={r[5] for r in o.values()}; preds={int(round(r[7])) for r in o.values()}; actual={int(round(r[8])) for r in o.values()}; ls={k[0] for k in keys}
m={'schema':'KMDSB.W04.M21.ApproximationOffCase.v0.1','protocol':'protocol/W04_M21_CONDITIONAL_LATE_SOURCE_APPROXIMATION_OFF_ACCURACY_REFERENCE_v0.1.md','provider_label':os.environ['P'],'provider_pin':os.environ['PIN'],'cosmology_id':os.environ['C'],'provider_head':subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip(),'class_rc':int(os.environ['RC']),'only_transfer_source_modified':subprocess.check_output(['git','-C','class','diff','--name-only'],text=True).strip()=='source/transfer.c','diagnostic_rows':len(o),'malformed_rows':bad,'shape_clean':same and ls=={399,400,401},'threshold_values':sorted(th),'predicate_values':sorted(preds),'actual_neglect_values':sorted(actual),'max_parent_same_q_k_relative_difference':maxk}
m['authority_clean']=all([m['provider_head']==m['provider_pin'],m['class_rc']==0,m['only_transfer_source_modified'],bad==0,m['shape_clean'],th=={1e9},preds=={0},actual=={0},maxk<=1e-12])
pathlib.Path('case_meta.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
PY
if [ "$rc" -ne 0 ];then exit "$rc";fi
python3 -c "import json;assert json.load(open('case_meta.json'))['authority_clean']"
