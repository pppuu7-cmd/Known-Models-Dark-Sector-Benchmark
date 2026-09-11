#!/usr/bin/env bash
set -euo pipefail
STAGE="${1:?stage required}"
PREV_TAR="${2:-}"
OUT="$GITHUB_WORKSPACE/m32k0e_stage${STAGE}"
PIN=849ddb716041316d0e223ba22badc0d630b72435
mkdir -p "$OUT"

sudo apt-get update -qq
sudo apt-get install -y -qq gpg-agent wget ca-certificates
wget -qO- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main' | sudo tee /etc/apt/sources.list.d/oneAPI.list >/dev/null
sudo apt-get update -qq
sudo apt-get install -y -qq intel-oneapi-compiler-fortran intel-oneapi-mpi-devel >"$OUT/install_stdout.log" 2>"$OUT/install_stderr.log"
set +u
source /opt/intel/oneapi/setvars.sh --force >/dev/null 2>&1
set -u
ifx --version >"$OUT/ifx_version.txt" 2>&1
mpiifx -v >"$OUT/mpiifx_version.txt" 2>&1 || true

git clone -q https://github.com/nat-woodcock/EFT-Ramses.git "$GITHUB_WORKSPACE/provider_stage${STAGE}"
cd "$GITHUB_WORKSPACE/provider_stage${STAGE}"
git checkout -q --detach "$PIN"
ACTUAL=$(git rev-parse HEAD)
echo "$ACTUAL" >"$OUT/provider_head.txt"
test "$ACTUAL" = "$PIN"
grep -Eqi 'self-accelerating DGP|normal-branch DGP|DGP braneworld' README.md
cd bin
rm -f -- *.o *.mod ramses3d
if [[ -n "$PREV_TAR" && -f "$PREV_TAR" ]]; then
  tar -xf "$PREV_TAR" -C .
fi
find . -maxdepth 1 -type f \( -name '*.o' -o -name '*.mod' -o -name 'ramses3d' \) -printf '%f %s\n' | sort >"$OUT/state_before.txt"

if test -x ramses3d; then
  RC=0
  echo 'previous checkpoint already contains executable' >"$OUT/build_stdout.log"
  : >"$OUT/build_stderr.log"
else
  set +e
  timeout --signal=INT --kill-after=5s 25s make \
    F90='mpiifx' \
    FFLAGS='-O3 -g -mcmodel=large -traceback -fpe0 -ftrapuv -cpp $(DEFINES)' \
    >"$OUT/build_stdout.log" 2>"$OUT/build_stderr.log"
  RC=$?
  set -e
fi

echo "$RC" >"$OUT/build_exit_code.txt"
if test -x ramses3d; then echo 0 >"$OUT/executable_test_exit.txt"; else echo 1 >"$OUT/executable_test_exit.txt"; fi
find . -maxdepth 1 -type f \( -name '*.o' -o -name '*.mod' -o -name 'ramses3d' \) -printf '%f %s\n' | sort >"$OUT/state_after.txt"
tar -cf "$OUT/checkpoint.tar" --ignore-failed-read -- *.o *.mod ramses3d 2>/dev/null || tar -cf "$OUT/checkpoint.tar" --ignore-failed-read -- *.o *.mod 2>/dev/null || true
python3 - "$STAGE" "$RC" "$OUT" <<'PY'
import json, pathlib, sys
stage=int(sys.argv[1]); rc=int(sys.argv[2]); out=pathlib.Path(sys.argv[3])
exe=(out/'executable_test_exit.txt').read_text().strip()=='0'
state={'stage':stage,'build_exit_code':rc,'timed_checkpoint':rc in (124,130),'native_executable_exists':exe,'physical_falsification':False}
(out/'stage_result.json').write_text(json.dumps(state,indent=2,sort_keys=True)+'\n')
print(json.dumps(state,sort_keys=True))
PY
