#!/usr/bin/env python3
import json, math, os, sys
from pathlib import Path


def numeric_rows(path):
    rows=[]
    with open(path,'r',encoding='utf-8',errors='ignore') as f:
        for line in f:
            s=line.strip()
            if not s or s.startswith('#'):
                continue
            vals=[]
            ok=True
            for x in s.split():
                try:
                    v=float(x)
                except ValueError:
                    ok=False; break
                if not math.isfinite(v):
                    ok=False; break
                vals.append(v)
            if ok and vals:
                rows.append(vals)
    return rows


def find_one(root, suffix):
    xs=sorted(Path(root).glob(f'*{suffix}'))
    return str(xs[0]) if xs else None


def max_rel(a,b,col=1,floor=1e-30):
    n=min(len(a),len(b))
    if n==0: return None
    vals=[]
    for i in range(n):
        if len(a[i])<=col or len(b[i])<=col: continue
        x,y=a[i][col],b[i][col]
        vals.append(abs(x-y)/max(abs(y),floor))
    return max(vals) if vals else None

base=Path(sys.argv[1] if len(sys.argv)>1 else 'probe')
pin=os.environ.get('PINNED_HICLASS_COMMIT','')
actual=os.environ.get('ACTUAL_HICLASS_COMMIT','')
exits={}
for arm in ('bd_author','lcdm_control'):
    p=base/arm/'exit_code.txt'
    exits[arm]=int(p.read_text().strip()) if p.exists() else None

files={}
rows={}
for arm in ('bd_author','lcdm_control'):
    d=base/arm/'output'
    cl=find_one(d,'_cl.dat')
    pk=find_one(d,'_pk.dat')
    bg=find_one(d,'_background.dat')
    files[arm]={'cl':cl,'pk':pk,'background':bg}
    rows[arm]={}
    for k,p in files[arm].items():
        rows[arm][k]=numeric_rows(p) if p and Path(p).exists() else []

cldiff=max_rel(rows['bd_author']['cl'],rows['lcdm_control']['cl'],1)
pkdiff=max_rel(rows['bd_author']['pk'],rows['lcdm_control']['pk'],1)
distinct=max(x for x in (cldiff,pkdiff) if x is not None) if any(x is not None for x in (cldiff,pkdiff)) else None

checks={
  'pin_exact': bool(pin) and actual==pin,
  'both_exit_zero': all(exits[a]==0 for a in exits),
  'bd_cl_finite_nonempty': len(rows['bd_author']['cl'])>0,
  'bd_pk_finite_nonempty': len(rows['bd_author']['pk'])>0,
  'bd_background_finite_nonempty': len(rows['bd_author']['background'])>0,
  'lcdm_cl_finite_nonempty': len(rows['lcdm_control']['cl'])>0,
  'lcdm_pk_finite_nonempty': len(rows['lcdm_control']['pk'])>0,
  'branch_distinct_gt_1e6': distinct is not None and distinct>1e-6,
}
passed=all(checks.values())
if passed:
    classification='M29_K0_PASS_WITH_SCOPE_PINNED_HICLASS_BRANS_DICKE_PROVIDER'
elif actual!=pin:
    classification='M29_K0_PROVENANCE_FAIL'
elif any(exits[a] not in (0,None) for a in exits):
    classification='M29_K0_BLOCKED_IMPLEMENTATION'
else:
    classification='M29_K0_INFRASTRUCTURE_OR_OUTPUT_BLOCKED'

out={
 'schema':'m29_k0_hiclass_provider_probe_v0.1',
 'pinned_commit':pin,'actual_commit':actual,'exit_codes':exits,
 'files':files,
 'row_counts':{a:{k:len(v) for k,v in rows[a].items()} for a in rows},
 'max_rel_diff':{'cmb_col1':cldiff,'pk_col1':pkdiff,'max':distinct},
 'checks':checks,'all_pass':passed,'classification':classification,
 'K0_promoted':passed,'K1_promoted':False,'physical_falsification':False,
 'scope':'provider/provenance executability only; no GR-limit or physical-family conclusion'
}
Path('waves/wave_05_modified_gravity').mkdir(parents=True,exist_ok=True)
Path('waves/wave_05_modified_gravity/M29_K0_HICLASS_PROVIDER_RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
