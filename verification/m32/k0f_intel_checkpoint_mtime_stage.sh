#!/usr/bin/env bash
set -euo pipefail
STAGE="${1:?stage required}"
PREV_TAR="${2:?previous checkpoint tar required}"
OUT="$GITHUB_WORKSPACE/m32k0f_stage${STAGE}"
PIN=849ddb716041316d0e223ba22badc0d630b72435
mkdir -p "$OUT"

sudo apt-get update -qq
sudo apt-get install -y -qq gpg-agent wget ca-certificates
a=$(mktemp)
wget -qO "$a" https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
gpg --dearmor <"$a" | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg >/dev/null
rm -f "$a"
echo 'deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main' | sudo tee /etc/apt/sources.list.d/oneAPI.list >/dev/null
sudo apt-get update -qq
sudo apt-get install -y -qq intel-oneapi-compiler-fortran intel-oneapi-mpi-devel >"$OUT/install_stdout.log" 2>"$OUT/install_stderr.log"
set +u
source /opt/intel/oneapi/setvars.sh --force >/dev/null 2>&1
set -u
ifx --version >"$OUT/ifx_version.txt" 2>&1
mpiifx -v >"$OUT/mpiifx_version.txt" 2>&1 || true

git clone -q https://github.com/nat-woodcock/EFT-Ramses.git "$GITHUB_WORKSPACE/provider_k0f_stage${STAGE}"
cd "$GITHUB_WORKSPACE/provider_k0f_stage${STAGE}"
git checkout -q --detach "$PIN"
ACTUAL=$(git rev-parse HEAD)
echo "$ACTUAL" >"$OUT/provider_head.txt"
test "$ACTUAL" = "$PIN"
grep -Eqi 'self-accelerating DGP|normal-branch DGP|DGP braneworld' README.md
cd bin
rm -f -- *.o *.mod ramses3d
tar -xf "$PREV_TAR" -C .

find . -maxdepth 1 -type f \( -name '*.o' -o -name '*.mod' \) -print0 | sort -z | xargs -0 sha256sum >"$OUT/hashes_before_touch.txt"
find . -maxdepth 1 -type f \( -name '*.o' -o -name '*.mod' \) -exec touch {} +
find . -maxdepth 1 -type f \( -name '*.o' -o -name '*.mod' \) -print0 | sort -z | xargs -0 sha256sum >"$OUT/hashes_after_touch.txt"
cmp "$OUT/hashes_before_touch.txt" "$OUT/hashes_after_touch.txt"
echo true >"$OUT/checkpoint_bytes_unchanged.txt"
find . -maxdepth 1 -type f \( -name '*.o' -o -name '*.mod' -o -name 'ramses3d' \) -printf '%f %s %T@\n' | sort >"$OUT/state_before.txt"

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
find . -maxdepth 1 -type f \( -name '*.o' -o -name '*.mod' -o -name 'ramses3d' \) -printf '%f %s %T@\n' | sort >"$OUT/state_after.txt"
tar -cf "$OUT/checkpoint.tar" --ignore-failed-read -- *.o *.mod ramses3d 2>/dev/null || tar -cf "$OUT/checkpoint.tar" --ignore-failed-read -- *.o *.mod 2>/dev/null || true
python3 - "$STAGE" "$RC" "$OUT" <<'PY'
import json, pathlib, sys
stage=int(sys.argv[1]); rc=int(sys.argv[2]); out=pathlib.Path(sys.argv[3])
exe=(out/'executable_test_exit.txt').read_text().strip()=='0'
integ=(out/'checkpoint_bytes_unchanged.txt').read_text().strip()=='true'
state={'stage':stage,'build_exit_code':rc,'timed_checkpoint':rc in (124,130),'native_executable_exists':exe,'checkpoint_bytes_unchanged':integ,'physical_falsification':False}
(out/'stage_result.json').write_text(json.dumps(state,indent=2,sort_keys=True)+'\n')
print(json.dumps(state,sort_keys=True))
PY
