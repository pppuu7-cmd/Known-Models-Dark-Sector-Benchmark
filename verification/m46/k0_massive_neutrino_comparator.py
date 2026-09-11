#!/usr/bin/env python3
import json, math
from pathlib import Path
ARMS=['massless_control','massive_nu_006']; BASE=Path('m46k0')

def read(path):
    out=[]
    if path is None or not path.exists(): return out
    for line in path.read_text(errors='ignore').splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        try:v=[float(x) for x in s.split()]
        except ValueError:continue
        if v and all(math.isfinite(x) for x in v):out.append(v)
    return out

def loc(base,suf):
    xs=sorted((base/'output').glob(f'*{suf}')); return xs[0] if xs else None

def l2_table(pa,pb,xi=0,yi=1):
    a=read(pa); b=read(pb)
    if not a or not b:return None
    bd={r[xi]:r[yi] for r in b if len(r)>max(xi,yi)}
    av=[]; bv=[]
    for r in a:
        if len(r)>max(xi,yi) and r[xi] in bd:
            av.append(r[yi]); bv.append(bd[r[xi]])
    if not av:return None
    num=math.sqrt(sum((x-y)**2 for x,y in zip(av,bv))); den=max(math.sqrt(sum(y*y for y in bv)),1e-300)
    return num/den
out={'schema':'m46_k0_massive_neutrino_comparator_v0.1','provider_repository':'lesgourg/class_public','provider_commit':'e85808324f51fc694d12e3ed7439552a3c3f9540','arms':{},'checks':{},'K0_promoted':False,'physical_falsification':False}
paths={}; ok=True; finite=True
for arm in ARMS:
    d=BASE/arm
    try:rc=int((d/'exit_code.txt').read_text().strip())
    except Exception:rc=None
    pin=(d/'actual_commit.txt').read_text().strip() if (d/'actual_commit.txt').exists() else None
    cl=loc(d,'_cl.dat'); pk=loc(d,'_pk.dat'); cr=read(cl); pr=read(pk)
    exact=(pin==out['provider_commit']); f=(len(cr)>0 and len(pr)>0)
    ok &= rc==0 and exact; finite &= f; paths[arm]=(cl,pk)
    out['arms'][arm]={'exit_code':rc,'exact_pin':exact,'finite_cl':len(cr)>0,'finite_pk':len(pr)>0,'cl_rows':len(cr),'pk_rows':len(pr)}
tt=l2_table(paths['massive_nu_006'][0],paths['massless_control'][0]) if finite else None
pk=l2_table(paths['massive_nu_006'][1],paths['massless_control'][1]) if finite else None
# Preregistration says active response in at least one of TT or P(k).
active=((tt is not None and tt>1e-6) or (pk is not None and pk>1e-6))
out['arms']['massive_nu_006']['active_response']={'TT_normalized_L2':tt,'Pk_normalized_L2':pk,'threshold':1e-6,'criterion':'TT OR P(k)','pass':active}
out['checks']={'both_execute_exact_pin':ok,'finite_outputs':finite,'active_comparator_response':active}
if ok and finite and active:
    out['classification']='M46_K0_PASS_WITH_SCOPE_PINNED_CLASS_MASSIVE_NEUTRINO_COMPARATOR'; out['K0_promoted']=True
elif not ok or not finite:out['classification']='M46_K0_BLOCKED_IMPLEMENTATION_OR_PROVIDER_EXECUTION'
else:out['classification']='M46_K0_NOT_ESTABLISHED_ACTIVE_COMPARATOR_RESPONSE'
out['scope']='known-sector massive-neutrino comparator K0 only; no mass constraint and no K1-K9 promotion'
Path('waves/wave_04_dark_matter').mkdir(parents=True,exist_ok=True)
p=Path('waves/wave_04_dark_matter/M46_K0_MASSIVE_NEUTRINO_COMPARATOR_RESULT.json'); p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
