#!/usr/bin/env python3
"""W03/M07 common-block theory-response comparator geometry.

Inputs:
  1. M07 strict production result JSON from the frozen W03 precision audit.
  2. DSIR frozen local_response_tangents_v0_1.json from the authority commit
     explicitly cited by the comparison audit.

This script operates only on the common unwhitened 7x5 low-k r_Delta block.
It never promotes a theory-space angle to observational discrimination.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

COMPARATORS = ("C1_smooth_w_nonphantom", "C5_designer_fR_B0")


def geom(a: np.ndarray, b: np.ndarray) -> dict:
    na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
    if na == 0 or nb == 0:
        raise ValueError("zero response vector")
    cos=float(np.dot(a,b)/(na*nb))
    cos=max(-1.0,min(1.0,cos))
    oriented=math.degrees(math.acos(cos))
    acute=math.degrees(math.acos(abs(cos)))
    return {
        "norm_left": na,
        "norm_right": nb,
        "cosine": cos,
        "oriented_angle_deg": oriented,
        "acute_line_angle_deg": acute,
        "best_scalar_projection_residual_fraction": math.sqrt(max(0.0,1.0-cos*cos)),
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("m07_result")
    ap.add_argument("dsir_tangents")
    ap.add_argument("--json", required=True)
    args=ap.parse_args()

    mp=Path(args.m07_result); dp=Path(args.dsir_tangents)
    m=json.loads(mp.read_text()); d=json.loads(dp.read_text())
    if d.get("schema") != "dsir.comparison_readiness.local_structure.v0.1":
        raise ValueError("unexpected DSIR tangent schema")
    z=np.asarray(m["frozen_grid"]["z"],float)
    k=np.asarray(m["frozen_grid"]["k_h_mpc"],float)
    if not np.allclose(z,np.asarray(d["z_nodes"],float),rtol=0,atol=1e-12):
        raise ValueError("z-grid mismatch")
    if not np.allclose(k,np.asarray(d["k_h_mpc"],float),rtol=0,atol=1e-12):
        raise ValueError("k-grid mismatch")

    dvec={x["id"]:np.asarray(x["vector"],float) for x in d["directions"]}
    cmp_by_label={x["label"]:x for x in m["comparisons_to_LCDM"]}
    m07=[]
    for case in m["cases"]:
        if case["label"].startswith("M07_L"):
            rec=cmp_by_label[case["label"]]
            v=np.asarray(rec["response_vector_lnP"],float)
            if len(v) != len(z)*len(k):
                raise ValueError(f"unexpected M07 vector length {case['label']}")
            m07.append((float(case["lambda"]),case["label"],v))
    m07.sort()
    if not m07:
        raise ValueError("no M07 production vectors")

    against=[]
    for lam,label,v in m07:
        for cid in COMPARATORS:
            against.append({
                "m07_label": label,
                "lambda": lam,
                "comparator": cid,
                **geom(v,dvec[cid]),
            })

    # Shape stability of the M07 production ray relative to the smallest lambda.
    lam0,label0,v0=m07[0]
    internal=[]
    for lam,label,v in m07[1:]:
        g=geom(v0,v)
        internal.append({
            "reference_m07_label": label0,
            "reference_lambda": lam0,
            "m07_label": label,
            "lambda": lam,
            "norm_ratio_to_smallest_lambda": g["norm_right"]/g["norm_left"],
            **g,
        })

    out={
        "schema":"KMDSB-W03-M07-comparator-geometry-v0.1",
        "scope":"unwhitened theory-response geometry on common frozen 7x5 low-k r_Delta block; no observational promotion",
        "m07_input_sha256":sha256(mp),
        "dsir_tangent_input_sha256":sha256(dp),
        "z_nodes":z.tolist(),
        "k_h_mpc":k.tolist(),
        "comparators":list(COMPARATORS),
        "m07_vs_comparators":against,
        "m07_internal_shape_stability":internal,
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__ == "__main__":
    main()
