#!/usr/bin/env python3
import argparse, json, math, pathlib
import numpy as np


def load_table(path):
    rows=[]
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            s=line.strip()
            if not s or s.startswith('#'):
                continue
            try:
                rows.append([float(x) for x in s.split()])
            except ValueError:
                continue
    a=np.asarray(rows,float)
    if a.ndim != 2 or a.shape[0] < 5 or a.shape[1] < 2:
        raise RuntimeError(f'bad table {path}: {getattr(a,"shape",None)}')
    if not np.isfinite(a).all():
        raise RuntimeError(f'nonfinite table {path}')
    return a


def rel_l2(ref, active):
    lo=max(ref[:,0].min(),active[:,0].min()); hi=min(ref[:,0].max(),active[:,0].max())
    mask=(ref[:,0]>=lo)&(ref[:,0]<=hi)
    x=ref[mask,0]; yr=ref[mask,1]
    ya=np.interp(x,active[:,0],active[:,1])
    scale=np.maximum(np.maximum(np.abs(yr),np.abs(ya)),1e-30)
    return float(np.sqrt(np.mean(((yr-ya)/scale)**2)))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--model',required=True)
    p.add_argument('--provider-commit',required=True)
    p.add_argument('--expected-commit',required=True)
    p.add_argument('--reference-cl',required=True)
    p.add_argument('--reference-pk',required=True)
    p.add_argument('--arms-json',required=True,help='JSON list with label,x,cl,pk,exit')
    p.add_argument('--out',required=True)
    p.add_argument('--scope',default='')
    p.add_argument('--k0-provenance-open',action='store_true')
    args=p.parse_args()

    out={'schema':'k1_decoupling_ladder_v0.1','model_id':args.model,
         'provider_commit':args.provider_commit,'expected_commit':args.expected_commit,
         'scope':args.scope,'physical_falsification':False,'K2_K9':'OPEN'}
    try:
        if args.provider_commit != args.expected_commit:
            raise RuntimeError('provider commit mismatch')
        refcl=load_table(args.reference_cl); refpk=load_table(args.reference_pk)
        arms=json.loads(pathlib.Path(args.arms_json).read_text())
        if len(arms) != 4:
            raise RuntimeError(f'expected four active arms, got {len(arms)}')
        metrics=[]
        arm_results=[]
        for arm in arms:
            if int(arm['exit']) != 0:
                raise RuntimeError(f"nonzero exit for {arm['label']}: {arm['exit']}")
            cl=load_table(arm['cl']); pk=load_table(arm['pk'])
            tt=rel_l2(refcl,cl); pkm=rel_l2(refpk,pk); d=max(tt,pkm)
            if not math.isfinite(d) or d <= 0:
                raise RuntimeError(f"invalid response metric for {arm['label']}: {d}")
            metrics.append(d)
            arm_results.append({'label':arm['label'],'x':float(arm['x']),'tt_normalized_l2':tt,'pk_normalized_l2':pkm,'D':d})
        xs=np.asarray([abs(float(a['x'])) for a in arms],float)
        ds=np.asarray(metrics,float)
        if not np.all(xs[:-1] > xs[1:]):
            raise RuntimeError('active ladder must be ordered from largest to smallest |x|')
        adjacent=[bool(ds[i+1] <= 1.20*ds[i]) for i in range(len(ds)-1)]
        reduction=float(ds[-1]/ds[0])
        corr=float(np.corrcoef(np.log10(xs),np.log10(ds))[0,1])
        criteria={
            'finest_less_than_coarsest':bool(ds[-1] < ds[0]),
            'adjacent_within_20pct_nonincrease':all(adjacent),
            'finest_to_coarsest_le_0p25':bool(reduction <= 0.25),
            'loglog_correlation_ge_0p90':bool(math.isfinite(corr) and corr >= 0.90),
        }
        passed=all(criteria.values())
        out.update({'arms':arm_results,'D_finest_over_D_coarsest':reduction,
                    'loglog_pearson':corr,'criteria':criteria,'K1_scoped_pass':passed})
        if passed:
            out['classification']=f'{args.model}_K1_PASS_WITH_SCOPE_DECOUPLING_LADDER'
            out['K1']='PASS_WITH_SCOPE' if not args.k0_provenance_open else 'PARTIAL'
            if args.k0_provenance_open:
                out['provenance_guard']='K0 provenance remains PARTIAL; numerical K1 limit behavior does not upgrade K0.'
        else:
            out['classification']=f'{args.model}_K1_NOT_ESTABLISHED_DECOUPLING_LADDER'
            out['K1']='PARTIAL'
    except Exception as e:
        out['classification']=f'{args.model}_K1_BLOCKED_IMPLEMENTATION_OR_NUMERICAL'
        out['K1']='BLOCKED_IMPLEMENTATION'
        out['K1_scoped_pass']=False
        out['error']=repr(e)
    pathlib.Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
