#!/usr/bin/env python3
import json, math, os, re, sys
from pathlib import Path

OMEGAS=['1e2','1e3','1e4','1e5']


def rows(path):
    out=[]
    with open(path,'r',encoding='utf-8',errors='ignore') as f:
        for line in f:
            s=line.strip()
            if not s or s.startswith('#'): continue
            try: vals=[float(x) for x in s.split()]
            except ValueError: continue
            if vals and all(math.isfinite(v) for v in vals): out.append(vals)
    return out


def file_for(arm,suffix):
    xs=sorted((Path('m29k1')/arm/'output').glob(f'*{suffix}'))
    return xs[0] if xs else None


def interp(points,x):
    # points sorted ascending x
    lo,hi=0,len(points)-1
    if not points or x<points[0][0] or x>points[-1][0]: return None
    while hi-lo>1:
        m=(lo+hi)//2
        if points[m][0] <= x: lo=m
        else: hi=m
    if points[lo][0]==x or lo==hi: return points[lo][1]
    x0,y0=points[lo]; x1,y1=points[hi]
    if x1==x0: return y0
    t=(x-x0)/(x1-x0)
    return y0+t*(y1-y0)


def channel(arm,kind):
    if kind=='background': p=file_for(arm,'_background.dat'); xcol,ycol=0,3
    elif kind=='tt': p=file_for(arm,'_cl.dat'); xcol,ycol=0,1
    else: p=file_for(arm,'_pk.dat'); xcol,ycol=0,1
    rr=rows(p) if p else []
    pts=[]
    for r in rr:
        if len(r)>max(xcol,ycol): pts.append((r[xcol],r[ycol]))
    pts.sort(key=lambda q:q[0])
    return p,pts


def compare(model,ref):
    vals=[]
    for x,y in model:
        yr=interp(ref,x)
        if yr is None: continue
        den=abs(y)+abs(yr)+1e-300
        vals.append(2*abs(y-yr)/den)
    if not vals: return {'n':0,'max':None,'rms':None}
    return {'n':len(vals),'max':max(vals),'rms':math.sqrt(sum(v*v for v in vals)/len(vals))}

reference={}
files={}
for kind in ('background','tt','pk'):
    p,pts=channel('lcdm',kind); reference[kind]=pts; files[f'lcdm_{kind}']=str(p) if p else None

metrics={}; exits={}; finite_ok=True
for om in OMEGAS:
    arm='bd_'+om
    ep=Path('m29k1')/arm/'exit_code.txt'
    exits[arm]=int(ep.read_text().strip()) if ep.exists() else None
    metrics[om]={}
    for kind in ('background','tt','pk'):
        p,pts=channel(arm,kind); files[f'{arm}_{kind}']=str(p) if p else None
        m=compare(pts,reference[kind])
        metrics[om][kind]=m
        finite_ok &= (m['n']>0 and m['max'] is not None and m['rms'] is not None and math.isfinite(m['max']) and math.isfinite(m['rms']))

ep=Path('m29k1/lcdm/exit_code.txt'); exits['lcdm']=int(ep.read_text().strip()) if ep.exists() else None
all_exit_zero=all(v==0 for v in exits.values())
strict_contraction={}
final_floor={}
final_threshold={}
for kind in ('background','tt','pk'):
    rms=[metrics[o][kind]['rms'] for o in OMEGAS]
    strict_contraction[kind]=all(rms[i+1] < rms[i] for i in range(2)) if all(v is not None for v in rms[:3]) else False
    final_floor[kind]=(rms[3] <= 1.2*rms[2]) if rms[2] is not None and rms[3] is not None else False
    final_threshold[kind]=(metrics['1e5'][kind]['max'] <= 5e-3 and metrics['1e5'][kind]['rms'] <= 1e-3) if metrics['1e5'][kind]['max'] is not None else False
branch_active=max(metrics['1e2'][k]['max'] or 0 for k in ('background','tt','pk')) > 1e-5
pass_all=all_exit_zero and finite_ok and all(strict_contraction.values()) and all(final_floor.values()) and all(final_threshold.values()) and branch_active
if pass_all:
    classification='M29_K1_PASS_WITH_SCOPE_BRANS_DICKE_GR_LIMIT'
elif all_exit_zero and finite_ok and all(final_threshold.values()) and branch_active and (not all(strict_contraction.values()) or not all(final_floor.values())):
    classification='M29_K1_NOT_ESTABLISHED_NUMERICAL_FLOOR'
elif not all_exit_zero:
    classification='M29_K1_BLOCKED_IMPLEMENTATION'
else:
    classification='M29_K1_NOT_ESTABLISHED'

out={
 'schema':'m29_k1_brans_dicke_gr_limit_v0.1',
 'provider_commit':'0009f51d89e6465c79e570b496c66fc90058fa77',
 'omega_ladder':[1e2,1e3,1e4,1e5], 'metrics':metrics,'exit_codes':exits,
 'checks':{'all_exit_zero':all_exit_zero,'finite_common_support':finite_ok,'strict_contraction_1e2_to_1e4':strict_contraction,'final_1e5_not_above_1e4_by_gt20pct':final_floor,'final_thresholds':final_threshold,'branch_active_at_1e2':branch_active},
 'all_pass':pass_all,'classification':classification,'K0_assumed_prerequisite':True,'K1_promoted':pass_all,'physical_falsification':False,
 'scope':'same-provider GR/reference limit only; no K2-K9 or observational conclusion'
}
Path('waves/wave_05_modified_gravity').mkdir(parents=True,exist_ok=True)
Path('waves/wave_05_modified_gravity/M29_K1_BRANS_DICKE_GR_LIMIT_RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
