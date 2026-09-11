#!/usr/bin/env python3
import json, math
from pathlib import Path

ARMS=['zero_control','evaporation','accretion_disk']
BASE=Path('m26k0')

def read(path):
    out=[]
    if path is None or not path.exists(): return out
    for line in path.read_text(errors='ignore').splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        try: v=[float(x) for x in s.split()]
        except ValueError: continue
        if v and all(math.isfinite(x) for x in v): out.append(v)
    return out

def locate(base,suffix):
    xs=sorted((base/'output').glob(f'*{suffix}'))
    return xs[0] if xs else None

def tt_l2(pa,pb):
    a={int(round(r[0])):r[1] for r in read(pa) if len(r)>=2 and r[0]>=2}
    b={int(round(r[0])):r[1] for r in read(pb) if len(r)>=2 and r[0]>=2}
    kk=sorted(set(a)&set(b))
    if not kk:return None
    num=math.sqrt(sum((a[k]-b[k])**2 for k in kk))
    den=max(math.sqrt(sum(b[k]**2 for k in kk)),1e-300)
    return num/den

out={'schema':'m26_k0_pbh_provider_v0.1','provider_repository':'lesgourg/class_public',
     'provider_commit':'e85808324f51fc694d12e3ed7439552a3c3f9540','arms':{},'checks':{},
     'K0_promoted':False,'physical_falsification':False}
paths={}; all_exec=True; all_finite=True
for arm in ARMS:
    d=BASE/arm
    try: rc=int((d/'exit_code.txt').read_text().strip())
    except Exception: rc=None
    pin=(d/'actual_commit.txt').read_text().strip() if (d/'actual_commit.txt').exists() else None
    cl=locate(d,'_cl.dat'); pk=locate(d,'_pk.dat'); clr=read(cl); pkr=read(pk)
    exact=(pin==out['provider_commit']); finite=(len(clr)>0 and len(pkr)>0)
    all_exec &= (rc==0 and exact); all_finite &= finite
    paths[arm]=cl
    out['arms'][arm]={'exit_code':rc,'exact_pin':exact,'finite_cl':len(clr)>0,'finite_pk':len(pkr)>0,'cl_rows':len(clr),'pk_rows':len(pkr)}
active_all=True
for arm in ['evaporation','accretion_disk']:
    val=tt_l2(paths[arm],paths['zero_control']) if all_finite else None
    active=(val is not None and val>1e-6); active_all &= active
    out['arms'][arm]['active_response']={'TT_normalized_L2':val,'threshold':1e-6,'pass':active}
out['checks']={'all_execute_exact_pin':all_exec,'all_finite_outputs':all_finite,'both_pbh_channels_active':active_all}
if all_exec and all_finite and active_all:
    out['classification']='M26_K0_PASS_WITH_SCOPE_NATIVE_CLASS_PBH_ENERGY_INJECTION'; out['K0_promoted']=True
elif not all_exec or not all_finite:
    out['classification']='M26_K0_BLOCKED_IMPLEMENTATION_OR_PROVIDER_EXECUTION'
else:
    out['classification']='M26_K0_NOT_ESTABLISHED_ACTIVE_PBH_RESPONSE'
out['scope']='native CLASS PBH evaporation/accretion energy-injection K0 only; PBH discreteness/Poisson/isocurvature and K1-K9 remain open'
Path('waves/wave_04_dark_matter').mkdir(parents=True,exist_ok=True)
p=Path('waves/wave_04_dark_matter/M26_K0_PBH_PROVIDER_RESULT.json')
p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
