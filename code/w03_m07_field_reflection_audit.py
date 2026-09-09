#!/usr/bin/env python3
"""Quotient-aware M07 field-reflection audit.

Tests the physical field-redefinition pair
  (+lambda, +phi_ini, +delta_phi orientation)
  (-lambda, -phi_ini, reflected scalar-field orientation)
through solver outputs. For matched scalar density and zero initial field
velocity, metric/matter observables should coincide if the field reflection is
an exact redundancy of the frozen pure-exponential branch.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

PAIRS=[
    (0.025,"M07_QP0025","M07_QM0025"),
    (0.075,"M07_QP0075","M07_QM0075"),
]
ODD_MAX=1e-4


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input_json")
    ap.add_argument("--json",required=True)
    args=ap.parse_args()
    src=json.loads(Path(args.input_json).read_text())
    cmp={x['label']:x for x in src['comparisons_to_LCDM']}
    cases={x['label']:x for x in src['cases']}
    rows=[]; all_pass=True
    for lam,plab,mlab in PAIRS:
        vp=np.asarray(cmp[plab]['response_vector_lnP'],float)
        vm=np.asarray(cmp[mlab]['response_vector_lnP'],float)
        hp=np.asarray(cmp[plab]['response_lnH'],float)
        hm=np.asarray(cmp[mlab]['response_lnH'],float)
        pe=0.5*(vp+vm); po=0.5*(vp-vm)
        he=0.5*(hp+hm); ho=0.5*(hp-hm)
        pf=float(np.linalg.norm(po)/max(np.linalg.norm(pe),1e-300))
        hf=float(np.linalg.norm(ho)/max(np.linalg.norm(he),1e-300))
        maxdp=float(np.max(np.abs(vp-vm)))
        maxdh=float(np.max(np.abs(hp-hm)))
        passed=(pf<=ODD_MAX and hf<=ODD_MAX)
        all_pass &= passed
        rows.append({
            'abs_lambda':lam,
            'plus_label':plab,
            'minus_label':mlab,
            'omega_plus':float(cases[plab]['background']['Omega_scf_today']),
            'omega_minus':float(cases[mlab]['background']['Omega_scf_today']),
            'lnP_odd_fraction':pf,
            'lnH_odd_fraction':hf,
            'max_abs_lnP_difference':maxdp,
            'max_abs_lnH_difference':maxdh,
            'gate':'PASS' if passed else 'FAIL'
        })
    out={
        'schema':'KMDSB-W03-M07-field-reflection-v0.1',
        'scope':'strict-shooting quotient-aware field-reflection test on frozen 7x5 low-k response',
        'preregistered_odd_fraction_max':ODD_MAX,
        'pairs':rows,
        'all_field_reflection_gates_pass':bool(all_pass)
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    if not all_pass:
        raise SystemExit('field-reflection quotient gate failed')

if __name__=='__main__':
    main()
