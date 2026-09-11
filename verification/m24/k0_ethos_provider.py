#!/usr/bin/env python3
import json, math
from pathlib import Path

ARMS=['uncoupled_control','ethos_vector','ethos_scalar']
BASE=Path('m24k0')

def read_table(path):
    rows=[]
    if path is None or not path.exists(): return rows
    for line in path.read_text(errors='ignore').splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        try: v=[float(x) for x in s.split()]
        except ValueError: continue
        if v and all(math.isfinite(x) for x in v): rows.append(v)
    return rows

def locate(base,suffix):
    xs=sorted((base/'output').glob(f'*{suffix}'))
    return xs[0] if xs else None

def l2_cmb(pa,pb,col=1):
    a={int(round(r[0])):r[col] for r in read_table(pa) if len(r)>col and r[0]>=2}
    b={int(round(r[0])):r[col] for r in read_table(pb) if len(r)>col and r[0]>=2}
    kk=sorted(set(a)&set(b))
    if not kk: return None
    num=sum((a[k]-b[k])**2 for k in kk)**0.5
    den=max(sum(b[k]**2 for k in kk)**0.5,1e-300)
    return num/den

def interp(pts,x):
    if not pts or x<pts[0][0] or x>pts[-1][0]: return None
    lo,hi=0,len(pts)-1
    while hi-lo>1:
        m=(lo+hi)//2
        if pts[m][0]<=x: lo=m
        else: hi=m
    if pts[lo][0]==x: return pts[lo][1]
    x0,y0=pts[lo]; x1,y1=pts[hi]
    return y0+(y1-y0)*(x-x0)/(x1-x0)

def l2_pk(pa,pb):
    aa=[(r[0],r[1]) for r in read_table(pa) if len(r)>=2 and r[0]>0 and r[1]>0]
    bb=[(r[0],r[1]) for r in read_table(pb) if len(r)>=2 and r[0]>0 and r[1]>0]
    if len(aa)<2 or len(bb)<2: return None
    aa.sort(); bb.sort()
    xs=[x for x,_ in aa if bb[0][0]<=x<=bb[-1][0]]
    av=[]; bv=[]
    amap=dict(aa)
    for x in xs:
        z=interp(bb,x)
        if z is not None:
            av.append(amap[x]); bv.append(z)
    if not av:return None
    num=sum((x-y)**2 for x,y in zip(av,bv))**0.5
    den=max(sum(y*y for y in bv)**0.5,1e-300)
    return num/den

out={'schema':'m24_k0_ethos_provider_v0.1','provider_repository':'lesgourg/class_public',
     'provider_commit':'e85808324f51fc694d12e3ed7439552a3c3f9540','arms':{},
     'physical_falsification':False,'K0_promoted':False}
all_exec=True; all_finite=True
paths={}
for arm in ARMS:
    d=BASE/arm
    ep=d/'exit_code.txt'
    try: rc=int(ep.read_text().strip())
    except Exception: rc=None
    pin=(d/'actual_commit.txt').read_text().strip() if (d/'actual_commit.txt').exists() else None
    cl=locate(d,'_cl.dat'); pk=locate(d,'_pk.dat')
    clr=read_table(cl); pkr=read_table(pk)
    finite=(len(clr)>0 and len(pkr)>0)
    exact=(pin==out['provider_commit'])
    all_exec &= (rc==0 and exact)
    all_finite &= finite
    paths[arm]={'cl':cl,'pk':pk}
    out['arms'][arm]={'exit_code':rc,'exact_pin':exact,'finite_cl':len(clr)>0,'finite_pk':len(pkr)>0,
                      'cl_rows':len(clr),'pk_rows':len(pkr)}
active_all=True
for arm in ['ethos_vector','ethos_scalar']:
    tt=l2_cmb(paths[arm]['cl'],paths['uncoupled_control']['cl']) if all_finite else None
    pk=l2_pk(paths[arm]['pk'],paths['uncoupled_control']['pk']) if all_finite else None
    active=(tt is not None and pk is not None and max(tt,pk)>1e-6)
    active_all &= active
    out['arms'][arm]['active_response']={'TT_normalized_L2':tt,'Pk_normalized_L2':pk,'threshold':1e-6,'pass':active}
out['checks']={'all_execute_exact_pin':all_exec,'all_finite_outputs':all_finite,'both_ethos_arms_active':active_all}
if all_exec and all_finite and active_all:
    cls='M24_K0_PASS_WITH_SCOPE_PINNED_NATIVE_CLASS_ETHOS'; out['K0_promoted']=True
elif not all_exec or not all_finite:
    cls='M24_K0_BLOCKED_IMPLEMENTATION_OR_PROVIDER_EXECUTION'
else:
    cls='M24_K0_NOT_ESTABLISHED_ACTIVE_ETHOS_RESPONSE'
out['classification']=cls
out['scope']='native CLASS ETHOS-parameterized linear executability and active-response K0 only; no claim of complete ETHOS microphysics/nonlinear coverage and no K1-K9 promotion'
Path('waves/wave_04_dark_matter').mkdir(parents=True,exist_ok=True)
p=Path('waves/wave_04_dark_matter/M24_K0_ETHOS_PROVIDER_RESULT.json')
p.write_text(json.dumps(out,indent=2,sort_keys=True,default=str)+'\n')
print(json.dumps(out,indent=2,sort_keys=True,default=str))
