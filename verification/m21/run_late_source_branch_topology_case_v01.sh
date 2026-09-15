#!/usr/bin/env bash
set -euo pipefail
p="$1"; c="$2"; case "$p" in P0) PIN=e85808324f51fc694d12e3ed7439552a3c3f9540;; P1) PIN=64bbab707faf4de4779a9e04edd180fef18d98fa;; *) exit 2;; esac
case "$c" in base|h105) ;; *) exit 2;; esac
python3 -m pip install --disable-pip-version-check --no-input -q numpy==2.2.6
git clone -q https://github.com/lesgourg/class_public.git class; git -C class checkout -q --detach "$PIN"; test "$(git -C class rev-parse HEAD)" = "$PIN"
python3 verification/m21/build_late_source_cross_cosmology_case.py "$c" cross_cases
python3 verification/m21/build_l_grid_phase_profile.py P400_ON_TAIL_OFF class/cl_permille.pre verification/m21/m21_ncdm_tight.pre profile.pre profile_manifest.json
mkdir -p clean_output native_output force_output
make -C class -j2 > build_clean.log 2>&1
set +e; timeout 2700 ./class/class "cross_cases/${c}_clean_native.ini" profile.pre > run_clean.log 2>&1; r0=$?; set -e
python3 verification/m21/apply_late_source_force_l400_true.py class/source/transfer.c patch_manifest.json "$PIN"; test "$(git -C class diff --name-only)" = source/transfer.c; git -C class diff --check; make -C class -j2 > build_patch.log 2>&1
set +e
OMP_NUM_THREADS=1 KMDSB_M21_BRANCH_DIAG="$(pwd)/native.dat" timeout 2700 ./class/class "cross_cases/${c}_patched_native.ini" profile.pre > run_native.log 2>&1; r1=$?
OMP_NUM_THREADS=1 KMDSB_M21_FORCE_L400_TRUE=1 KMDSB_M21_BRANCH_DIAG="$(pwd)/force.dat" timeout 2700 ./class/class "cross_cases/${c}_patched_native.ini" profile.pre > run_force.log 2>&1; r2=$?
set -e
P="$p" C="$c" PIN="$PIN" R0="$r0" R1="$r1" R2="$r2" python3 - <<'PY'
import json,math,os,pathlib,subprocess,numpy as np
def table(p):
 a=[]
 for s in pathlib.Path(p).read_text(errors='replace').splitlines():
  if not s.strip() or s.lstrip().startswith('#'):continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except:continue
  if r and all(math.isfinite(x) for x in r):a.append(r)
 return np.asarray(a,float)
def cl(root):
 x=list(pathlib.Path(root).glob('*_cl.dat')); assert len(x)==1,(root,x); return table(x[0])
def diag(p):
 d={}
 for s in pathlib.Path(p).read_text().splitlines():
  r=[float(x) for x in s.split()]; assert len(r)==14
  k=(int(round(r[2])),int(round(r[0]))); assert k not in d; d[k]=r
 return d
A=cl('clean_output');B=cl('native_output');F=cl('force_output')
l2=lambda x,y: float(np.linalg.norm(x-y)/max(float(np.linalg.norm(x)),float(np.linalg.norm(y)),1e-300)) if x.shape==y.shape else float('inf')
N=diag('native.dat');T=diag('force.dat'); keys=set(N); shape=(keys==set(T) and {k[0] for k in keys}=={399,400,401} and all(sum(k[0]==l for k in keys)>=20 for l in (399,400,401)))
ar={r[3] for r in N.values()}; th={r[4] for r in N.values()}|{r[4] for r in T.values()}; neigh=True; changed=False
for k in keys:
 n,t=N[k],T[k]; l=k[0]
 if l in (399,401): neigh &= (int(round(n[7]))==int(round(t[7])) and int(round(n[8]))==int(round(t[8])))
 if l==400: changed |= int(round(n[8]))!=int(round(t[8]))
native_l400=all(int(round(r[6]))==0 and int(round(r[7]))==0 for k,r in N.items() if k[0]==400)
force_l400=all(int(round(r[6]))==0 and int(round(r[7]))==1 for k,r in T.items() if k[0]==400)
null=l2(A,B); effect=l2(B,F); head=subprocess.check_output(['git','-C','class','rev-parse','HEAD'],text=True).strip()
o={'schema':'KMDSB.W04.M21.BranchTopologyCase.v0.1','protocol':'protocol/W04_M21_LATE_SOURCE_BRANCH_TOPOLOGY_INTERACTION_v0.1.md','provider_label':os.environ['P'],'provider_pin':os.environ['PIN'],'cosmology_id':os.environ['C'],'exact_head':head==os.environ['PIN'],'rc':[int(os.environ[x]) for x in ('R0','R1','R2')],'only_transfer_source_modified':subprocess.check_output(['git','-C','class','diff','--name-only'],text=True).strip()=='source/transfer.c','native_clean_l2':null,'force_effect_l2':effect,'cl_changed':effect>1e-12,'shape_clean':shape,'angular_rescaling_values':sorted(ar),'threshold_values':sorted(th),'native_l400_false':native_l400,'forced_l400_true':force_l400,'neighbors_invariant':neigh,'l400_count_changed':changed,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
o['authority_clean']=all([o['exact_head'],o['rc']==[0,0,0],o['only_transfer_source_modified'],null<=1e-12,shape,len(ar)==1,next(iter(ar))>1.0,th=={400.0},native_l400,force_l400,neigh])
pathlib.Path('case_meta.json').write_text(json.dumps(o,indent=2,sort_keys=True)+'\n'); print(json.dumps(o,indent=2,sort_keys=True))
PY
python3 -c "import json; assert json.load(open('case_meta.json'))['authority_clean']"
