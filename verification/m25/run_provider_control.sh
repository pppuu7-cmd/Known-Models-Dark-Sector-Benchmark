#!/usr/bin/env bash
set -uo pipefail
PIN=e4486265e8207aa0dd28decc8c8d897266c0a52a
rm -rf provider committed_provider_outfiles generated_provider_outfiles
git clone -q https://github.com/ntveem/sterile-dm.git provider
git -C provider checkout -q --detach "$PIN"
test "$(git -C provider rev-parse HEAD)" = "$PIN" || exit 2
cp -a provider/outfiles committed_provider_outfiles

cd provider
./configure gfortran > ../m25_configure.log 2>&1
cfg=$?
mk=999
if [ "$cfg" -eq 0 ]; then
  make > ../m25_make.log 2>&1
  mk=$?
else
  : > ../m25_make.log
fi
cd ..
if [ "$cfg" -eq 0 ] && [ "$mk" -eq 0 ] && [ -x provider/sterile-nu ]; then build_rc=0; else build_rc=1; fi

run_rc=999
timed_out=false
if [ "$build_rc" -eq 0 ]; then
  rm -rf provider/outfiles
  mkdir -p provider/outfiles
  (cd provider && timeout --signal=TERM 1800s ./sterile-nu params.ini > ../m25_stock_run.log 2>&1)
  run_rc=$?
  if [ "$run_rc" -eq 124 ] || [ "$run_rc" -eq 137 ]; then timed_out=true; fi
else
  : > m25_stock_run.log
fi

if [ -d provider/outfiles ]; then cp -a provider/outfiles generated_provider_outfiles; else mkdir -p generated_provider_outfiles; fi
python3 - "$cfg" "$mk" "$build_rc" "$run_rc" "$timed_out" <<'PY'
import json,sys
cfg,mk,build,run=map(int,sys.argv[1:5])
to=sys.argv[5].lower()=='true'
open('m25_status.json','w').write(json.dumps({'configure_rc':cfg,'make_rc':mk,'build_rc':build,'run_rc':run,'timed_out':to},indent=2,sort_keys=True)+'\n')
PY
cat m25_status.json
exit 0
