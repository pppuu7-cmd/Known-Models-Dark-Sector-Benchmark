#!/usr/bin/env python3
"""KMDSB W02-E4: common temporal-centroid comparator.

Inputs are frozen DSIR JSON products:
  1. local_response_tangents_v0_1.json
  2. experiment_053a_dcdm_withheld_temporal_localization_v0_1_summary.json

For every 7x5 low-k tangent vector r(k,z), compute the same amplitude-invariant
response-power temporal centroid used by Exp053A:

  q_z(z) = sum_k r(k,z)^2 / sum_{z,k} r(k,z)^2
  z_R    = exp(sum_z q_z ln(1+z)) - 1

This script is a theory-response comparator only. It does not define an
observational discrimination threshold and must not be used to claim B5/B6
observation-space separation without a pinned operator/covariance.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def temporal_centroid(vector, z_nodes, nk):
    if len(vector) != len(z_nodes) * nk:
        raise ValueError("vector length incompatible with frozen z/k grid")
    power = []
    for iz in range(len(z_nodes)):
        row = vector[iz * nk:(iz + 1) * nk]
        power.append(sum(float(x) ** 2 for x in row))
    total = sum(power)
    if not math.isfinite(total) or total <= 0:
        raise ValueError("non-finite or zero response power")
    q = [p / total for p in power]
    zr = math.exp(sum(qi * math.log1p(float(z)) for qi, z in zip(q, z_nodes))) - 1.0
    return zr, q


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tangents", required=True)
    ap.add_argument("--dcdm-summary", required=True)
    ap.add_argument("--json", required=True)
    args = ap.parse_args()

    tangents = json.loads(Path(args.tangents).read_text())
    dcdm = json.loads(Path(args.dcdm_summary).read_text())

    z = tangents["z_nodes"]
    k = tangents["k_h_mpc"]
    if z != dcdm["frozen_z_nodes"] or k != dcdm["frozen_k_h_mpc"]:
        raise ValueError("DCDM and tangent products do not use the same frozen 7x5 grid")

    alternatives = []
    for d in tangents["directions"]:
        zr, q = temporal_centroid(d["vector"], z, len(k))
        alternatives.append({
            "id": d["id"],
            "family": d["family"],
            "z_R": zr,
            "q_z": q,
        })

    dseq = [float(x) for x in dcdm["z_R_sequence"]]
    nearest = []
    for dz in dseq:
        best = min(alternatives, key=lambda a: abs(a["z_R"] - dz))
        nearest.append({
            "dcdm_z_R": dz,
            "alternative": best["id"],
            "alternative_z_R": best["z_R"],
            "absolute_delta": abs(best["z_R"] - dz),
        })

    out = {
        "schema_version": "KMDSB-W02-E4-temporal-centroid-v0.1",
        "coordinate": "z_R=exp(sum_z q_z ln(1+z))-1; q_z=sum_k r^2/sum_zk r^2",
        "z_nodes": z,
        "k_h_mpc": k,
        "alternative_centroids": alternatives,
        "dcdm_z_R_sequence": dseq,
        "nearest_by_scalar_z_R": nearest,
        "interpretation": "Common coordinate exists, but no frozen scalar-distance threshold exists; z_R alone is not promoted to a mechanism discriminator.",
    }
    Path(args.json).write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
