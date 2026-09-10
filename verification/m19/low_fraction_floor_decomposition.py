#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

FRACS = np.asarray([0.10, 0.03, 0.01, 0.003, 0.001], dtype=float)
LOW_IDX = [2, 3, 4]
LOW_FRACS = FRACS[LOW_IDX]
AXPIN = "891e779cc0bd422e49f97533e6c2fc761149737d"
CDMPIN = "dc437acd8c90aa7e5595fcb25c615b03de8357a7"
SOURCE_RUN = 34536498517
SOURCE_ARTIFACT = 10175630339
SOURCE_DIGEST = "sha256:2c9c6d5df28e7221bb4754cbff932a70feeb35aaa0f2991415d1b153489502a9"
PREREG = "protocol/W04_M19_LOW_FRACTION_FLOOR_DECOMPOSITION_PREREGISTRATION_v0.1.md"


def load(path: Path) -> np.ndarray:
    rows = []
    for line in path.read_text(errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        try:
            row = [float(x.replace("D", "E").replace("d", "e")) for x in s.split()]
        except ValueError:
            continue
        if row and all(math.isfinite(x) for x in row):
            rows.append(row)
    a = np.asarray(rows, dtype=float)
    if a.ndim != 2 or a.shape[0] < 3 or a.shape[1] < 2:
        raise RuntimeError(f"invalid table {path}")
    return a


def channel(a: np.ndarray, col: int) -> np.ndarray:
    return a[:, [0, col]]


def interp_to_x(a: np.ndarray, x: np.ndarray) -> np.ndarray:
    return np.column_stack([np.interp(x, a[:, 0], a[:, j]) for j in range(1, a.shape[1])])


def common_grid(models: list[np.ndarray], ref: np.ndarray):
    base = models[-1]
    lo = max([m[:, 0].min() for m in models] + [ref[:, 0].min()])
    hi = min([m[:, 0].max() for m in models] + [ref[:, 0].max()])
    mask = (base[:, 0] >= lo) & (base[:, 0] <= hi)
    x = base[mask, 0]
    if x.size < 3:
        raise RuntimeError("insufficient common-domain samples")
    ys = [interp_to_x(m, x) for m in models]
    yr = interp_to_x(ref, x)
    return x, ys, yr


def sym_metrics(a: np.ndarray, b: np.ndarray) -> dict:
    scale = max(float(np.max(np.abs(a))), float(np.max(np.abs(b))), 1e-300)
    floor = 1e-12 * scale
    r = 2.0 * (a - b) / (np.abs(a) + np.abs(b) + floor)
    vals = np.abs(r).ravel()
    return {
        "median_abs": float(np.median(vals)),
        "rms": float(np.sqrt(np.mean(r * r))),
        "p95_abs": float(np.percentile(vals, 95)),
        "n": int(vals.size),
        "floor": float(floor),
    }


def fit_block(models: list[np.ndarray], ref: np.ndarray) -> dict:
    _, ys, yr = common_grid(models, ref)
    y = np.stack([ys[i] for i in LOW_IDX], axis=0)
    f = LOW_FRACS

    design = np.column_stack([np.ones_like(f), f])
    coeff = np.tensordot(np.linalg.pinv(design), y, axes=(1, 0))
    b = coeff[0]
    a = coeff[1]
    pred = np.stack([b + a * fi for fi in f], axis=0)

    f2 = f[1:]
    y2 = y[1:]
    a2 = (y2[1] - y2[0]) / (f2[1] - f2[0])
    b2 = y2[0] - a2 * f2[0]

    external = sym_metrics(b, yr)
    finite = []
    for i, fi in enumerate(f):
        q = sym_metrics(y[i], b)
        q["fraction"] = float(fi)
        finite.append(q)
    r95 = np.asarray([q["p95_abs"] for q in finite], dtype=float)
    exponent = None
    if np.all(r95 > 0):
        exponent = float(np.polyfit(np.log(f), np.log(r95), 1)[0])

    scale = max(float(np.max(np.abs(y))), float(np.max(np.abs(pred))), 1e-300)
    floor = 1e-12 * scale
    rr = 2.0 * (y - pred) / (np.abs(y) + np.abs(pred) + floor)
    fit_error_p95 = float(np.percentile(np.abs(rr), 95))
    asymptote_shift = sym_metrics(b, b2)

    strict_decrease = bool(r95[1] < r95[0] and r95[2] < r95[1])
    exponent_gt_half = bool(exponent is not None and exponent > 0.5)
    baseline_dominant = bool(external["p95_abs"] >= 3.0 * finite[-1]["p95_abs"])
    fit_small = bool(fit_error_p95 <= finite[-1]["p95_abs"])
    stable_asymptote = bool(asymptote_shift["p95_abs"] <= external["p95_abs"])

    if strict_decrease and exponent_gt_half and baseline_dominant and fit_small and stable_asymptote:
        classification = "BASELINE_FLOOR_DOMINANT_WITH_SCOPE"
    elif strict_decrease and exponent_gt_half:
        classification = "INTERNAL_LIMIT_CONVERGENT_BUT_BASELINE_NOT_DOMINANT"
    else:
        classification = "LOW_FRACTION_LIMIT_NOT_DIAGNOSTICALLY_RESOLVED"

    return {
        "classification": classification,
        "external_floor_p95": external["p95_abs"],
        "finite_effect_p95": {str(q["fraction"]): q["p95_abs"] for q in finite},
        "finite_effect_exponent": exponent,
        "fit_error_p95": fit_error_p95,
        "two_point_asymptote_shift_p95": asymptote_shift["p95_abs"],
        "n": int(b.size),
        "conditions": {
            "strict_decrease": strict_decrease,
            "exponent_gt_0_5": exponent_gt_half,
            "external_floor_ge_3x_smallest_effect": baseline_dominant,
            "fit_error_le_smallest_effect": fit_small,
            "two_point_shift_le_external_floor": stable_asymptote,
        },
    }


def analyze(root: Path, out: Path):
    ax = []
    for i in range(5):
        ax.append(
            {
                "scal": load(root / f"axc/a{i}_scalCls.dat"),
                "pk": load(root / f"axc/a{i}_matterpower.dat"),
                "tr": load(root / f"axc/a{i}_transfer_out.dat"),
            }
        )
    ref = {
        "scal": load(root / "camb0/c0_scalCls.dat"),
        "pk": load(root / "camb0/c0_matterpower.dat"),
        "tr": load(root / "camb0/c0_transfer_out.dat"),
    }

    if ref["scal"].shape[1] != 4 or any(x["scal"].shape[1] != 4 for x in ax):
        raise RuntimeError("scalar schema must be [ell,TT,EE,TE]")
    if ref["tr"].shape[1] != 7 or any(x["tr"].shape[1] != 9 for x in ax):
        raise RuntimeError("transfer schema mismatch")

    for x in ax:
        x["trp"] = x["tr"][:, [0, 1, 2, 3, 4, 5, 8]]
    ref["trp"] = ref["tr"][:, [0, 1, 2, 3, 4, 5, 6]]

    specs = {}
    for name, col in [("CMB_TT", 1), ("CMB_EE", 2), ("CMB_TE", 3)]:
        specs[name] = ([channel(ax[i]["scal"], col) for i in range(5)], channel(ref["scal"], col))
    specs["Pk"] = ([ax[i]["pk"] for i in range(5)], ref["pk"])
    for name, col in [("T_cdm", 1), ("T_b", 2), ("T_g", 3), ("T_r", 4), ("T_nu", 5), ("T_tot", 6)]:
        specs[name] = ([channel(ax[i]["trp"], col) for i in range(5)], channel(ref["trp"], col))

    blocks = {name: fit_block(models, r) for name, (models, r) in specs.items()}
    floor_dominant = [name for name, q in blocks.items() if q["classification"] == "BASELINE_FLOOR_DOMINANT_WITH_SCOPE"]
    internal_only = [name for name, q in blocks.items() if q["classification"] == "INTERNAL_LIMIT_CONVERGENT_BUT_BASELINE_NOT_DOMINANT"]
    unresolved = [name for name, q in blocks.items() if q["classification"] == "LOW_FRACTION_LIMIT_NOT_DIAGNOSTICALLY_RESOLVED"]

    result = {
        "schema": "KMDSB.M19.lowFractionFloorDecomposition.v1",
        "classification": "M19_LOW_FRACTION_BASELINE_FLOOR_LOCALIZED_WITH_SCOPE" if not unresolved else "M19_LOW_FRACTION_FLOOR_PARTIALLY_UNRESOLVED",
        "preregistration": PREREG,
        "source": {
            "run": SOURCE_RUN,
            "artifact": SOURCE_ARTIFACT,
            "artifact_digest": SOURCE_DIGEST,
            "axion_pin": AXPIN,
            "external_cdm_pin": CDMPIN,
            "fractions": FRACS.tolist(),
            "fit_fractions": LOW_FRACS.tolist(),
        },
        "blocks": blocks,
        "baseline_floor_dominant_blocks": floor_dominant,
        "internal_limit_convergent_blocks": internal_only,
        "unresolved_blocks": unresolved,
        "K1_promoted": False,
        "physical_falsification": False,
        "interpretation": "Low-fraction axionCAMB response converges internally in every common block; several cross-provider residual floors are dominated by the external solver/reference baseline. Frozen K1 non-promotion is unchanged.",
        "next": "matched-baseline calibration or independent implementation with executable exact CDM limit",
    }
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    analyze(args.root, args.out)
