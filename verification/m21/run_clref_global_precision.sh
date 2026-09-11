#!/usr/bin/env bash
set -uo pipefail
PIN=e85808324f51fc694d12e3ed7439552a3c3f9540
rm -rf class m21_clref_cases m21_clref_output
git clone -q https://github.com/lesgourg/class_public.git class
git -C class checkout -q --detach "$PIN"
test "$(git -C class rev-parse HEAD)" = "$PIN" || exit 2
test "$(git -C class hash-object cl_ref.pre)" = 'ccb86d11f72d9fa754b18dca40d23378b90c0699' || exit 3
make -C class -j2 > m21_clref_build.log 2>&1 || exit 4
python3 verification/m21/mixed_cold_warm_k1_reference.py prepare m21_clref_cases || exit 5
rm -rf class/output; mkdir -p class/output
: > m21_clref_status.tsv
for c in ref f2 f3 f4; do
  (cd class && ./class ../m21_clref_cases/${c}.ini cl_ref.pre > ../m21_clref_${c}.log 2>&1)
  rc=$?
  printf '%s\t%d\n' "$c" "$rc" >> m21_clref_status.tsv
done
cp -a class/output m21_clref_output
python3 - <<'PY'
import json
d={}
for line in open('m21_clref_status.tsv'):
    k,v=line.rstrip().split('\t'); d[k]=int(v)
open('m21_clref_status.json','w').write(json.dumps(d,indent=2,sort_keys=True)+'\n')
PY
cat m21_clref_status.json
exit 0
