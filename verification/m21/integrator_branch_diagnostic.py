#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

PREREG = "protocol/W04_M21_INTEGRATOR_BRANCH_DIAGNOSTIC_PREREGISTRATION_v0.1.md"
CASES = ["f2", "f3", "f4"]
FRACS = {"f2": 0.01, "f3": 0.003, "f4": 0.001}


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
        raise RuntimeError(f"invalid table {path}: shape={a.shape}")
    return a


def nl2(y: np.ndarray, r: np.ndarray) -> float:
    return float(np.linalg.norm(y-r) / max(float(np.linalg.norm(r)), 1e-300))


def cl_metric(a: np.ndarray, r: np.ndarray, col: int) -> dict:
    if a.shape[1] <= col or r.shape[1] <= col:
        raise RuntimeError(f"missing CMB column {col}: {a.shape} {r.shape}")
    if a.shape[0] != r.shape[0] or not np.array_equal(a[:, 0], r[:, 0]):
        raise RuntimeError("CMB ell grids differ")
    return {"R2": nl2(a[:, col], r[:, col]), "n": int(a.shape[0])}


def overlap_metric(a: np.ndarray, r: np.ndarray, xcol: int, ycol: int, logx: bool=False) -> dict:
    x, y = a[:, xcol], a[:, ycol]
    xr, yr = r[:, xcol], r[:, ycol]
    good = np.isfinite(x) & np.isfinite(y)
    goodr = np.isfinite(xr) & np.isfinite(yr)
    if logx:
        good &= x > 0
        goodr &= xr > 0
    x, y = x[good], y[good]
    xr, yr = xr[goodr], yr[goodr]
    ia, ir = np.argsort(x), np.argsort(xr)
    x, y = x[ia], y[ia]
    xr, yr = xr[ir], yr[ir]
    lo, hi = max(float(x.min()), float(xr.min())), min(float(x.max()), float(xr.max()))
    m = (x >= lo) & (x <= hi)
    x, y = x[m], y[m]
    if x.size < 3:
        raise RuntimeError("insufficient overlap")
    if logx:
        rr = np.interp(np.log(x), np.log(xr), yr)
    else:
        rr = np.interp(x, xr, yr)
    return {"R2": nl2(y, rr), "n": int(x.size), "x_min": float(x.min()), "x_max": float(x.max())}


def files(root: Path, case: str) -> dict:
    return {
        "cl": load(root / f"{case}_cl.dat"),
        "pk": load(root / f"{case}_pk.dat"),
        "bg": load(root / f"{case}_background.dat"),
    }


def response_profile(root: Path) -> dict:
    ref = files(root, "ref")
    out = {"points": {}, "excursion_factors": {}}
    for case in CASES:
        x = files(root, case)
        out["points"][case] = {
            "fraction": FRACS[case],
            "TT": cl_metric(x["cl"], ref["cl"], 1),
            "EE": cl_metric(x["cl"], ref["cl"], 2),
            "TE": cl_metric(x["cl"], ref["cl"], 3),
            "Pk": overlap_metric(x["pk"], ref["pk"], 0, 1, logx=True),
            # CLASS background col0 is z and col3 is H [1/Mpc] for the pinned output schema.
            "H": overlap_metric(x["bg"], ref["bg"], 0, 3, logx=False),
        }
    for ch in ["TT", "EE", "TE", "Pk", "H"]:
        vals = [out["points"][c][ch]["R2"] for c in CASES]
        out["excursion_factors"][ch] = float(vals[1] / max(vals[0], vals[2], 1e-300))
    out["max_CMB_excursion_factor"] = max(out["excursion_factors"][x] for x in ["TT", "EE", "TE"])
    return out


def direct_cross_branch(ndf: Path, rk: Path) -> dict:
    out = {}
    for case in ["ref"] + CASES:
        a, b = files(ndf, case), files(rk, case)
        out[case] = {
            "TT": cl_metric(b["cl"], a["cl"], 1),
            "EE": cl_metric(b["cl"], a["cl"], 2),
            "TE": cl_metric(b["cl"], a["cl"], 3),
            "Pk": overlap_metric(b["pk"], a["pk"], 0, 1, logx=True),
        }
    return out


def main(ndf: Path, rk: Path, out: Path) -> None:
    result = {
        "schema": "KMDSB.M21.integratorBranchDiagnostic.v1",
        "preregistration": PREREG,
        "K1_promoted": False,
        "physical_falsification": False,
        "branches": {
            "NDF15_default": response_profile(ndf),
            "RK_evolver0": response_profile(rk),
        },
        "direct_RK_vs_NDF15": direct_cross_branch(ndf, rk),
    }
    e_ndf = result["branches"]["NDF15_default"]["max_CMB_excursion_factor"]
    e_rk = result["branches"]["RK_evolver0"]["max_CMB_excursion_factor"]
    rk_three = result["branches"]["RK_evolver0"]["excursion_factors"]
    ndf_three = result["branches"]["NDF15_default"]["excursion_factors"]
    if all(rk_three[ch] <= 3.0 for ch in ["TT", "EE", "TE"]) and any(ndf_three[ch] > 9.0 for ch in ["TT", "EE", "TE"]):
        classification = "M21_INTEGRATOR_BRANCH_LOCALIZED_TO_NDF15"
    elif e_rk <= e_ndf / 3.0:
        classification = "M21_INTEGRATOR_BRANCH_REDUCES_EXCURSION"
    else:
        classification = "M21_INTEGRATOR_BRANCH_EXCURSION_PERSISTS"
    result["classification"] = classification
    result["Emax_NDF15"] = float(e_ndf)
    result["Emax_RK"] = float(e_rk)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: integrator_branch_diagnostic.py NDF_DIR RK_DIR OUT.json")
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
