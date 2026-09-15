#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 3 ]; then echo "usage: $0 CASE LANE PARENT_ARTIFACT_DIR" >&2; exit 2; fi
c="$1"; lane="$2"; parent="$3"
case "$c" in ref|f2|f3|f4);;*) exit 2;; esac
case "$lane" in native|flat_identity_predicate);;*) exit 2;; esac
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'; profile='neighbor_P400_ON_TAIL_OFF.pre'; diag="neighbor_${c}_${lane}.dat"
python3 -m pip install --disable-pip-version-check --no-input -q numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class && git -C class checkout -q --detach "$PIN"
python3 verification/m21/apply_late_source_neighbor_multipole_counterfactual.py class/source/transfer.c neighbor_patch_manifest.json
test "$(git -C class diff --name-only)" = 'source/transfer.c' && git -C class diff --check
python3 verification/m21/mixed_cold_warm_k1_reference.py prepare m21_cases
python3 verification/m21/build_l_grid_phase_profile.py P400_ON_TAIL_OFF class/cl_permille.pre verification/m21/m21_ncdm_tight.pre "$profile" neighbor_profile_manifest.json
make -C class -j2 > build.log 2>&1; mkdir -p output
set +e
if [ "$lane" = flat_identity_predicate ]; then
 OMP_NUM_THREADS=1 KMDSB_M21_NEIGHBOR_CF=1 KMDSB_M21_NEIGHBOR_DIAG="$(pwd)/$diag" timeout 2700 ./class/class "m21_cases/${c}.ini" "$profile" > "run_${c}_${lane}.log" 2>&1
else
 OMP_NUM_THREADS=1 KMDSB_M21_NEIGHBOR_DIAG="$(pwd)/$diag" timeout 2700 ./class/class "m21_cases/${c}.ini" "$profile" > "run_${c}_${lane}.log" 2>&1
fi
rc=$?; set -e
CASE="$c" LANE="$lane" RC="$rc" PARENT="$parent" DIAG="$diag" PIN="$PIN" python3 - <<'PY'
import hashlib,json,math,os,pathlib,subprocess,numpy as np
H=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def table(p):
 rows=[]
 for z in pathlib.Path(p).read_text(errors='replace').splitlines():
  if not z.strip() or z.lstrip().startswith('#'):continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in z.split()]
  except:continue
  if r and all(math.isfinite(x) for x in r):rows.append(r)
 return np.asarray(rows,float)
def cl(root,c):
 out=pathlib.Path(root)/'output'; xs=list(out.glob(f'{c}_*_cl.dat'))+list(out.glob(f'{c}_cl.dat'))
 xs=list(dict.fromkeys(xs))
 if len(xs)!=1:raise RuntimeError(xs)
 return xs[0]
c=os.environ['CASE'];lane=os.environ['LANE'];new=cl('.',c);par=cl(os.environ['PARENT'],c);a=table(new);b=table(par)
l2=float('inf') if a.shape!=b.shape else float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),1e-300))
rows=[];bad=0
for z in pathlib.Path(os.environ['DIAG']).read_text(errors='replace').splitlines():
 try:r=[float(x) for x in z.split()]
 except:bad+=1;continue
 if len(r)!=15 or not all(math.isfinite(x) for x in r):bad+=1;continue
 rows.append(r)
ls={int(round(r[2])) for r in rows}; flags={int(round(r[14])) for r in rows}; want=1 if lane!='native' else 0
m={'schema':'KMDSB.W04.M21.NeighborMultipoleCase.v0.1','case':c,'lane':lane,'provider_head':subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip(),'exact_head':subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip()==os.environ['PIN'],'class_rc':int(os.environ['RC']),'only_transfer_source_modified':subprocess.check_output(['git','-C','class','diff','--name-only'],text=True).strip()=='source/transfer.c','diagnostic_rows':len(rows),'malformed_rows':bad,'multipoles':sorted(ls),'cf_flags':sorted(flags),'parent_l2':l2,'native_null':(l2<=1e-12 if lane=='native' else None)}
m['authority_clean']=all([m['exact_head'],m['class_rc']==0,m['only_transfer_source_modified'],bad==0,len(rows)>0,ls=={399,400,401},flags=={want},(m['native_null'] if lane=='native' else True)])
pathlib.Path('case_meta.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
PY
if [ "$rc" -ne 0 ]; then exit "$rc"; fi
python3 -c "import json; assert json.load(open('case_meta.json'))['authority_clean']"
