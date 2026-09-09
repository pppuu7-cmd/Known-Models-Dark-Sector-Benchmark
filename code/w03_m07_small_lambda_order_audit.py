#!/usr/bin/env python3
"""Preregistered M07 small-lambda response-order audit."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import numpy as np

LAMBDAS=[0.005,0.010,0.020,0.040]
LABELS={0.005:'M07_L0005',0.010:'M07_L0010',0.020:'M07_L0020',0.040:'M07_L0040'}
P_MIN=1.8
P_MAX=2.2
FLOOR_FACTOR=100.0


def angle(a,b):
    c=float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))
    c=max(-1.0,min(1.0,c))
    return math.degrees(math.acos(c))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('input_json')
    ap.add_argument('--json',required=True)
    args=ap.parse_args()
    src=json.loads(Path(args.input_json).read_text())
    cmp={x['label']:x for x in src['comparisons_to_LCDM']}

    ref=np.asarray(cmp['SCF_SPLIT_L0']['response_vector_lnP'],float)
    floor=float(np.linalg.norm(ref))
    vecs={lam:np.asarray(cmp[LABELS[lam]]['response_vector_lnP'],float) for lam in LAMBDAS}
    norms={lam:float(np.linalg.norm(vecs[lam])) for lam in LAMBDAS}
    floor_ratios={lam:norms[lam]/max(floor,1e-300) for lam in LAMBDAS}
    floor_pass=all(x>=FLOOR_FACTOR for x in floor_ratios.values())

    x=np.log(np.asarray(LAMBDAS,float))
    y=np.log(np.asarray([norms[l] for l in LAMBDAS],float))
    p,a=np.polyfit(x,y,1)
    p=float(p); a=float(a)
    order_pass=(P_MIN<=p<=P_MAX)

    q={lam:vecs[lam]/(lam*lam) for lam in LAMBDAS}
    # list from large -> small adjacent pairs
    pairs=[(0.040,0.020),(0.020,0.010),(0.010,0.005)]
    conv=[]
    for large,small in pairs:
        ang=angle(q[large],q[small])
        rel=float(np.linalg.norm(q[large]-q[small])/np.linalg.norm(q[small]))
        conv.append({'large_lambda':large,'small_lambda':small,'angle_deg':ang,'relative_difference':rel})
    angles=[r['angle_deg'] for r in conv]
    rels=[r['relative_difference'] for r in conv]
    convergence_pass=(angles[2] <= angles[1] <= angles[0] and rels[2] <= rels[1] <= rels[0])

    if not floor_pass:
        verdict='BLOCKED_NUMERICAL'
    elif not order_pass:
        verdict='QUADRATIC_ORDER_REJECTED'
    elif not convergence_pass:
        verdict='INCONCLUSIVE'
    else:
        verdict='PASS_WITH_SCOPE'

    out={
        'schema':'KMDSB-W03-M07-small-lambda-order-v0.1',
        'scope':'strict-shooting quotient representative lambda>=0; unwhitened 7x5 low-k local geometry; not B8',
        'lambda_grid':LAMBDAS,
        'reference_floor_norm':floor,
        'response_norms':{str(k):v for k,v in norms.items()},
        'floor_ratios':{str(k):v for k,v in floor_ratios.items()},
        'preregistered_floor_factor_min':FLOOR_FACTOR,
        'floor_gate_pass':bool(floor_pass),
        'fitted_power_p':p,
        'log_intercept':a,
        'preregistered_p_interval':[P_MIN,P_MAX],
        'quadratic_order_gate_pass':bool(order_pass),
        'q_lambda_squared_norms':{str(k):float(np.linalg.norm(q[k])) for k in LAMBDAS},
        'adjacent_q_convergence_large_to_small':conv,
        'monotone_convergence_gate_pass':bool(convergence_pass),
        'verdict':verdict
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    if verdict=='BLOCKED_NUMERICAL':
        raise SystemExit('small-lambda signal not sufficiently above reference floor')
    if verdict=='QUADRATIC_ORDER_REJECTED':
        raise SystemExit(f'fitted p={p} outside preregistered [{P_MIN},{P_MAX}]')
    if verdict=='INCONCLUSIVE':
        raise SystemExit('quadratic fitted order passes but q convergence is not monotone')

if __name__=='__main__':
    main()
