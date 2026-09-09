#!/usr/bin/env python3
"""M07 +/-lambda parity and near-reference coordinate audit.

Consumes a W03 probe-style result JSON containing matched +lambda and -lambda
cases at the same |lambda|. Tests whether the observable response is even in
lambda within a preregistered numerical tolerance, and reports the q=lambda^2
scaled response convergence descriptively.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

PAIRS = [
    (0.025, "M07_P0025", "M07_M0025"),
    (0.075, "M07_P0075", "M07_M0075"),
]
ODD_FRACTION_MAX = 1.0e-3


def angle(a: np.ndarray, b: np.ndarray) -> float:
    c=float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))
    c=max(-1.0,min(1.0,c))
    return math.degrees(math.acos(c))


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("input_json")
    ap.add_argument("--json", required=True)
    args=ap.parse_args()

    src=json.loads(Path(args.input_json).read_text())
    cmp={x["label"]:x for x in src["comparisons_to_LCDM"]}
    cases={x["label"]:x for x in src["cases"]}

    out_pairs=[]
    q_vectors=[]
    all_pass=True
    for abs_lam,plab,mlab in PAIRS:
        vp=np.asarray(cmp[plab]["response_vector_lnP"],float)
        vm=np.asarray(cmp[mlab]["response_vector_lnP"],float)
        hp=np.asarray(cmp[plab]["response_lnH"],float)
        hm=np.asarray(cmp[mlab]["response_lnH"],float)
        even=0.5*(vp+vm); odd=0.5*(vp-vm)
        even_h=0.5*(hp+hm); odd_h=0.5*(hp-hm)
        odd_frac=float(np.linalg.norm(odd)/np.linalg.norm(even))
        odd_frac_h=float(np.linalg.norm(odd_h)/np.linalg.norm(even_h))
        omega_p=float(cases[plab]["background"]["Omega_scf_today"])
        omega_m=float(cases[mlab]["background"]["Omega_scf_today"])
        passed=odd_frac <= ODD_FRACTION_MAX
        all_pass &= passed
        qvec=even/(abs_lam*abs_lam)
        q_vectors.append((abs_lam,qvec))
        out_pairs.append({
            "abs_lambda":abs_lam,
            "plus_label":plab,
            "minus_label":mlab,
            "omega_scf_plus":omega_p,
            "omega_scf_minus":omega_m,
            "lnP_plus_minus_angle_deg":angle(vp,vm),
            "lnP_even_norm":float(np.linalg.norm(even)),
            "lnP_odd_norm":float(np.linalg.norm(odd)),
            "lnP_odd_fraction":odd_frac,
            "lnH_odd_fraction":odd_frac_h,
            "parity_gate": "PASS" if passed else "FAIL",
            "q_scaled_lnP_norm":float(np.linalg.norm(qvec)),
        })

    q1=q_vectors[0][1]; q2=q_vectors[1][1]
    q_rel=float(np.linalg.norm(q2-q1)/np.linalg.norm(q2))
    q_angle=angle(q1,q2)

    out={
        "schema":"KMDSB-W03-M07-parity-coordinate-v0.1",
        "scope":"strict-shooting unwhitened 7x5 low-k response; parity hard-gate only; q convergence descriptive",
        "preregistered_odd_fraction_max":ODD_FRACTION_MAX,
        "pairs":out_pairs,
        "all_parity_gates_pass":bool(all_pass),
        "q_lambda_squared_diagnostic":{
            "relative_difference_between_abs_lambda_0p025_and_0p075":q_rel,
            "angle_deg":q_angle,
            "interpretation":"descriptive only; no preregistered convergence threshold"
        }
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    if not all_pass:
        raise SystemExit("preregistered lambda-parity gate failed")


if __name__ == "__main__":
    main()
