"""Wave 02 E1: IDE vs GDM common-block tangent geometry.

Usage:
    python code/w02_e1_pair_angles.py /path/to/local_response_tangents_v0_1.json

The input must be the frozen DSIR artifact
`data/derived/comparison_readiness/local_response_tangents_v0_1.json`
from the authority commit recorded by the Wave-02 audit.

This script measures only unwhitened theory-response geometry on the common
35-node G_lowk r_Delta(k,z) block. It does not make an observational claim.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

PAIR_IDS = [
    ("C2_IDE_alpha_negative", "C3_GDM_cs2"),
    ("C2_IDE_alpha_negative", "C3_GDM_cv2"),
    ("C2_IDE_beta", "C3_GDM_cs2"),
    ("C2_IDE_beta", "C3_GDM_cv2"),
]


def geometry(a: np.ndarray, b: np.ndarray) -> dict:
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na == 0.0 or nb == 0.0:
        raise ValueError("zero tangent vector")
    cos = float(np.dot(a, b) / (na * nb))
    cos = max(-1.0, min(1.0, cos))
    oriented = math.degrees(math.acos(cos))
    acute = math.degrees(math.acos(abs(cos)))
    # Residual fraction after the best one-dimensional scalar projection,
    # expressed relative to a unit-normalized target direction.
    projection_residual = math.sqrt(max(0.0, 1.0 - cos * cos))
    return {
        "cosine": cos,
        "oriented_angle_deg": oriented,
        "acute_line_angle_deg": acute,
        "best_scalar_projection_residual_fraction": projection_residual,
    }


def main(path: str) -> None:
    src = json.loads(Path(path).read_text())
    if src.get("schema") != "dsir.comparison_readiness.local_structure.v0.1":
        raise ValueError("unexpected DSIR tangent schema")
    vectors = {d["id"]: np.asarray(d["vector"], dtype=float) for d in src["directions"]}
    n_expected = len(src["z_nodes"]) * len(src["k_h_mpc"])
    out = []
    for left, right in PAIR_IDS:
        a, b = vectors[left], vectors[right]
        if len(a) != n_expected or len(b) != n_expected:
            raise ValueError(f"unexpected vector length for {left}/{right}")
        out.append({"left": left, "right": right, **geometry(a, b)})
    print(json.dumps({
        "scope": "unwhitened common G_lowk r_Delta(k,z) tangent geometry",
        "z_nodes": src["z_nodes"],
        "k_h_mpc": src["k_h_mpc"],
        "pairs": out,
    }, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: w02_e1_pair_angles.py LOCAL_RESPONSE_TANGENTS.json")
    main(sys.argv[1])
