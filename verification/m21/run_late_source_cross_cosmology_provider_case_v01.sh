#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then echo "usage: $0 PROVIDER_LABEL COSMOLOGY_ID" >&2; exit 2; fi
provider_label="$1"; cid="$2"
case "$provider_label" in
  P0) PIN='e85808324f51fc694d12e3ed7439552a3c3f9540' ;;
  P1) PIN='64bbab707faf4de4779a9e04edd180fef18d98fa' ;;
  *) echo "bad provider label $provider_label" >&2; exit 2;;
esac
case "$cid" in base|h95|h105|ob95|ob105|odm95|odm105) ;; *) echo "bad cosmology $cid" >&2; exit 2;; esac
profile='cross_P400_ON_TAIL_OFF.pre'; pman='cross_P400_ON_TAIL_OFF_profile_manifest.json'; patchman='cross_provider_patch_manifest.json'

python3 -m pip install --disable-pip-version-check --no-input -q numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$PIN"
test "$(git -C class rev-parse HEAD)" = "$PIN"
python3 verification/m21/build_late_source_cross_cosmology_case.py "$cid" cross_cases
python3 verification/m21/build_l_grid_phase_profile.py P400_ON_TAIL_OFF class/cl_permille.pre verification/m21/m21_ncdm_tight.pre "$profile" "$pman"
mkdir -p clean_output native_output cf_output
make -C class -j2 > build_clean.log 2>&1

set +e
timeout 2700 ./class/class "cross_cases/${cid}_clean_native.ini" "$profile" > run_clean.log 2>&1
rc_clean=$?
set -e

python3 verification/m21/apply_late_source_cross_provider_counterfactual.py class/source/transfer.c "$patchman" "$PIN"
test "$(git -C class diff --name-only)" = 'source/transfer.c'
git -C class diff --check
make -C class -j2 > build_patched.log 2>&1

set +e
OMP_NUM_THREADS=1 KMDSB_M21_CROSS_DIAG="$(pwd)/native.dat" timeout 2700 ./class/class "cross_cases/${cid}_patched_native.ini" "$profile" > run_native.log 2>&1
rc_native=$?
OMP_NUM_THREADS=1 KMDSB_M21_CROSS_CF=1 KMDSB_M21_CROSS_DIAG="$(pwd)/cf.dat" timeout 2700 ./class/class "cross_cases/${cid}_flat_identity_predicate.ini" "$profile" > run_cf.log 2>&1
rc_cf=$?
set -e
printf '%s\t%s\t%s\t%s\t%s\n' "$provider_label" "$cid" "$rc_clean" "$rc_native" "$rc_cf" > status.tsv

PROVIDER_LABEL="$provider_label" CID="$cid" PIN_ENV="$PIN" RC_CLEAN="$rc_clean" RC_NATIVE="$rc_native" RC_CF="$rc_cf" PROFILE="$profile" PMAN="$pman" PATCH="$patchman" python3 - <<'PY'
import hashlib,json,math,os,pathlib,subprocess
import numpy as np
H=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def numeric(p):
 rows=[]
 for raw in pathlib.Path(p).read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s or s.startswith('#'):continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError:continue
  if r and all(math.isfinite(x) for x in r):rows.append(r)
 a=np.asarray(rows,float)
 if a.ndim!=2 or a.shape[0]<3:raise RuntimeError(f'bad table {p}: {a.shape}')
 return a
def one_cl(root,c):
 root=pathlib.Path(root); xs=[]
 for pat in (f'{c}_*_cl.dat',f'{c}_cl.dat'):
  for p in root.glob(pat):
   if p not in xs:xs.append(p)
 if len(xs)!=1:raise RuntimeError(f'cl discovery {root}/{c}: {xs}')
 return xs[0]
def load_diag(p):
 out={};bad=0
 for raw in pathlib.Path(p).read_text(errors='replace').splitlines():
  x=raw.split()
  if len(x)!=15:bad+=1;continue
  try:r=[float(v.replace('D','E').replace('d','e')) for v in x]
  except ValueError:bad+=1;continue
  if not all(math.isfinite(v) for v in r):bad+=1;continue
  key=(int(round(r[2])),int(round(r[0])))
  if key in out:raise RuntimeError(f'duplicate {key} in {p}')
  out[key]=r
 return out,bad
c=os.environ['CID']; pin=os.environ['PIN_ENV']; head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip()
clean=one_cl('clean_output',c); native=one_cl('native_output',c); cfcl=one_cl('cf_output',c)
a=numeric(clean);b=numeric(native)
null_l2=float('inf') if a.shape!=b.shape else float(np.linalg.norm(a-b)/max(float(np.linalg.norm(a)),float(np.linalg.norm(b)),1e-300))
N,bn=load_diag('native.dat'); C,bc=load_diag('cf.dat'); keys=set(N); ckeys=set(C)
shape_clean=(keys==ckeys and len(keys)>0 and {k[0] for k in keys}=={399,400,401} and all(sum(1 for k in keys if k[0]==l)>=20 for l in (399,400,401)))
max_k_rel=float('inf')
if shape_clean:
 max_k_rel=0.0
 for k in keys:
  x=N[k][1];y=C[k][1];max_k_rel=max(max_k_rel,abs(x-y)/max(abs(x),abs(y),1e-300))
ars={r[3] for r in N.values()}; cf_ars={r[3] for r in C.values()}; effs={r[4] for r in C.values()}; th={r[5] for r in N.values()}|{r[5] for r in C.values()}; nflags={int(round(r[14])) for r in N.values()}; cflags={int(round(r[14])) for r in C.values()}
obj={'schema':'KMDSB.W04.M21.CrossCosmologyProviderCase.v0.1','protocol':'protocol/W04_M21_LATE_SOURCE_CROSS_COSMOLOGY_PROVIDER_REGRESSION_v0.1.md','provider_label':os.environ['PROVIDER_LABEL'],'provider_pin':pin,'provider_head':head,'exact_head':head==pin,'cosmology_id':c,'class_rc_clean':int(os.environ['RC_CLEAN']),'class_rc_native':int(os.environ['RC_NATIVE']),'class_rc_cf':int(os.environ['RC_CF']),'only_transfer_source_modified':subprocess.check_output(['git','-C','class','diff','--name-only'],text=True).strip()=='source/transfer.c','clean_cl_sha256':H(clean),'native_cl_sha256':H(native),'cf_cl_sha256':H(cfcl),'patched_native_vs_clean_l2':null_l2,'patched_native_null_le_1e12':null_l2<=1e-12,'diagnostic_native_rows':len(N),'diagnostic_cf_rows':len(C),'diagnostic_native_malformed':bn,'diagnostic_cf_malformed':bc,'shape_clean':shape_clean,'max_native_cf_same_q_k_relative_difference':max_k_rel,'same_q_k_le_1e12':max_k_rel<=1e-12,'native_angular_rescaling_values':sorted(ars),'cf_native_angular_rescaling_values':sorted(cf_ars),'cf_effective_rescaling_values':sorted(effs),'threshold_values':sorted(th),'native_cf_flags':sorted(nflags),'counterfactual_cf_flags':sorted(cflags),'input_manifest_sha256':H(f'cross_cases/{c}_manifest.json'),'profile_sha256':H(os.environ['PROFILE']),'profile_manifest_sha256':H(os.environ['PMAN']),'patch_manifest_sha256':H(os.environ['PATCH']),'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
obj['authority_clean']=all([obj['exact_head'],obj['class_rc_clean']==0,obj['class_rc_native']==0,obj['class_rc_cf']==0,obj['only_transfer_source_modified'],obj['patched_native_null_le_1e12'],bn==0,bc==0,shape_clean,obj['same_q_k_le_1e12'],len(ars)==1,len(cf_ars)==1,ars==cf_ars,effs=={1.0},th=={400.0},nflags=={0},cflags=={1}])
pathlib.Path('case_meta.json').write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n');print(json.dumps(obj,indent=2,sort_keys=True))
PY

if [ "$rc_clean" -ne 0 ] || [ "$rc_native" -ne 0 ] || [ "$rc_cf" -ne 0 ]; then exit 1; fi
python3 -c "import json; assert json.load(open('case_meta.json'))['authority_clean']"
