#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

CLASS_PIN = "e85808324f51fc694d12e3ed7439552a3c3f9540"
PREREG = "protocol/W04_M22_ANNIHILATING_DM_K1_REFERENCE_PREREGISTRATION_v0.1.md"
PANN = [1.11e-22, 3.33e-23, 1.11e-23, 3.33e-24, 1.11e-24]


def common_ini(root: str) -> list[str]:
    return [
        f"root = {root}",
        "overwrite_root = yes",
        "output = tCl,pCl,mPk",
        "lensing = no",
        "non linear = none",
        "recombination = HyRec",
        "omega_b = 2.255065e-2",
        "omega_cdm = 1.193524e-1",
        "H0 = 67.76953",
        "A_s = 2.123257e-9",
        "n_s = 0.9686025",
        "z_reio = 8.227371",
        "P_k_max_1/Mpc = 3.0",
        "l_max_scalars = 2500",
    ]


def prepare(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    cases: dict[str, dict] = {}

    ref = common_ini("output/ref")
    (out / "ref.ini").write_text("\n".join(ref) + "\n")
    cases["ref"] = {"p_ann": None, "kind": "omitted_reference"}

    zero = common_ini("output/zero") + ["DM_annihilation_efficiency = 0"]
    (out / "zero.ini").write_text("\n".join(zero) + "\n")
    cases["zero"] = {"p_ann": 0.0, "kind": "explicit_zero"}

    for i, p in enumerate(PANN):
        lines = common_ini(f"output/p{i}") + [f"DM_annihilation_efficiency = {p:.12e}"]
        (out / f"p{i}.ini").write_text("\n".join(lines) + "\n")
        cases[f"p{i}"] = {"p_ann": p, "kind": "finite"}

    manifest = {
        "schema": "KMDSB.M22.annihilatingDM.K1Manifest.v1",
        "class_pin": CLASS_PIN,
        "preregistration": PREREG,
        "p_ann_m3_s_J": PANN,
        "cases": cases,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def load_table(path: Path) -> np.ndarray:
    rows: list[list[float]] = []
    for line in path.read_text(errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        try:
            row = [float(x.replace("D", "E").replace("d", "e")) for x in s.split()]
        except ValueError:
            continue
        if row and all(math.isfinite(v) for v in row):
            rows.append(row)
    arr = np.asarray(rows, dtype=float)
    if arr.ndim != 2 or arr.shape[0] < 3 or arr.shape[1] < 2:
        raise RuntimeError(f"invalid table {path}: shape={arr.shape}")
    return arr


def normalized_l2(y: np.ndarray, yr: np.ndarray) -> float:
    den = max(float(np.linalg.norm(yr)), 1e-300)
    return float(np.linalg.norm(y - yr) / den)


def cl_metric(model: np.ndarray, ref: np.ndarray, col: int) -> dict:
    if model.shape[1] <= col or ref.shape[1] <= col:
        raise RuntimeError(f"missing CMB column {col}: model={model.shape}, ref={ref.shape}")
    if model.shape[0] != ref.shape[0] or not np.array_equal(model[:, 0], ref[:, 0]):
        raise RuntimeError("CMB ell grids differ")
    return {"R2": normalized_l2(model[:, col], ref[:, col]), "n": int(model.shape[0])}


def pk_metric(model: np.ndarray, ref: np.ndarray) -> dict:
    xm, ym = model[:, 0], model[:, 1]
    xr, yr = ref[:, 0], ref[:, 1]
    good_m = (xm > 0) & np.isfinite(xm) & np.isfinite(ym)
    good_r = (xr > 0) & np.isfinite(xr) & np.isfinite(yr)
    xm, ym = xm[good_m], ym[good_m]
    xr, yr = xr[good_r], yr[good_r]
    im, ir = np.argsort(xm), np.argsort(xr)
    xm, ym = xm[im], ym[im]
    xr, yr = xr[ir], yr[ir]
    lo, hi = max(float(xm.min()), float(xr.min())), min(float(xm.max()), float(xr.max()))
    mask = (xm >= lo) & (xm <= hi)
    x = xm[mask]
    y = ym[mask]
    if x.size < 3:
        raise RuntimeError("insufficient P(k) overlap")
    yref = np.interp(np.log(x), np.log(xr), yr)
    return {"R2": normalized_l2(y, yref), "n": int(x.size)}


def fit_tail(residuals: list[float]) -> dict:
    x = np.asarray(PANN[-3:], dtype=float)
    y = np.asarray(residuals[-3:], dtype=float)
    if np.any(y <= 0) or np.any(~np.isfinite(y)):
        return {"valid": False, "p": None}
    p, logA = np.polyfit(np.log(x), np.log(y), 1)
    return {"valid": True, "p": float(p), "logA": float(logA)}


def judge_positive(points: list[dict]) -> dict:
    r = [float(p["R2"]) for p in points]
    monotonic = all(r[i + 1] <= 1.02 * r[i] for i in range(len(r) - 1))
    response = r[0] > 1e-8
    contracted = r[-1] <= 0.25 * r[0]
    fit = fit_tail(r)
    positive_tail = bool(fit["valid"] and fit["p"] is not None and fit["p"] > 0.20)
    return {
        "points": points,
        "R2_sequence": r,
        "monotonic_with_2pct_slack": monotonic,
        "largest_response_gt_1e-8": response,
        "smallest_le_quarter_largest": contracted,
        "fit_smallest3": fit,
        "pass": bool(monotonic and response and contracted and positive_tail),
    }


def analyze(root: Path, status_path: Path, out: Path) -> None:
    status = json.loads(status_path.read_text())
    keys = ["build", "ref", "zero"] + [f"p{i}" for i in range(len(PANN))]
    result = {
        "schema": "KMDSB.M22.annihilatingDM.K1Reference.v1",
        "class_pin": CLASS_PIN,
        "preregistration": PREREG,
        "p_ann_m3_s_J": PANN,
        "status": status,
        "K0_provenance": "PASS_WITH_SCOPE_PINNED_NATIVE_CLASS_ENERGY_INJECTION",
        "K1_reference_limit": "NOT_PROMOTED",
        "K2_physical_geometry": "ONE_SIDED_PANN_GE_0_NO_SIGN_QUOTIENT",
        "K4_promoted": False,
        "physical_falsification": False,
    }
    if any(status.get(k) != 0 for k in keys):
        result["classification"] = "M22_K1_PROVIDER_EXECUTION_BLOCKED"
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return

    ref_cl = load_table(root / "output/ref_cl.dat")
    zero_cl = load_table(root / "output/zero_cl.dat")
    ref_pk = load_table(root / "output/ref_pk.dat")
    zero_pk = load_table(root / "output/zero_pk.dat")

    zero_identity = {
        "TT": cl_metric(zero_cl, ref_cl, 1),
        "EE": cl_metric(zero_cl, ref_cl, 2),
        "TE": cl_metric(zero_cl, ref_cl, 3),
        "Pk": pk_metric(zero_pk, ref_pk),
    }
    zero_identity_pass = all(v["R2"] <= 1e-12 for v in zero_identity.values())
    result["exact_zero_vs_omitted"] = zero_identity
    result["exact_zero_identity_pass"] = bool(zero_identity_pass)

    finite_cls = [load_table(root / f"output/p{i}_cl.dat") for i in range(len(PANN))]
    finite_pks = [load_table(root / f"output/p{i}_pk.dat") for i in range(len(PANN))]

    blocks = {}
    for name, col in [("TT", 1), ("EE", 2), ("TE", 3)]:
        pts = []
        for p, cl in zip(PANN, finite_cls):
            q = cl_metric(cl, zero_cl, col)
            q["p_ann"] = p
            pts.append(q)
        blocks[name] = judge_positive(pts)

    pk_points = []
    for p, pk in zip(PANN, finite_pks):
        q = pk_metric(pk, zero_pk)
        q["p_ann"] = p
        pk_points.append(q)
    pk_max = max(float(q["R2"]) for q in pk_points)
    blocks["Pk_negative_control"] = {
        "points": pk_points,
        "max_R2": pk_max,
        "threshold": 1e-4,
        "pass": bool(pk_max <= 1e-4),
    }
    result["blocks"] = blocks
    result["TE_diagnostic_pass"] = bool(blocks["TE"]["pass"])

    required = zero_identity_pass and blocks["TT"]["pass"] and blocks["EE"]["pass"] and blocks["Pk_negative_control"]["pass"]
    if required:
        result["classification"] = "M22_K1_REFERENCE_LIMIT_PASS_WITH_SCOPE_NATIVE_ENERGY_INJECTION"
        result["K1_reference_limit"] = "PASS_WITH_SCOPE_NATIVE_ENERGY_INJECTION_EXACT_ZERO"
    else:
        result["classification"] = "M22_K1_REFERENCE_LIMIT_NOT_ESTABLISHED"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("prepare")
    p.add_argument("out", type=Path)
    a = sp.add_parser("analyze")
    a.add_argument("root", type=Path)
    a.add_argument("status", type=Path)
    a.add_argument("out", type=Path)
    args = ap.parse_args()
    if args.cmd == "prepare":
        prepare(args.out)
    else:
        analyze(args.root, args.status, args.out)
