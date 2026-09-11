#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

PREREG = "protocol/W04_M21_CLREF_GLOBAL_PRECISION_DIAGNOSTIC_PREREGISTRATION_v0.1.md"
CASES = ["f2", "f3", "f4"]
FRACS = {"f2": 0.01, "f3": 0.003, "f4": 0.001}
P2_E = {"TT": 67.5202694494654, "EE": 211.58560557338748, "TE": 323.42821108733295}
P2_F3 = {"TT": 6.876596406059055e-05, "EE": 2.7773845469355833e-04, "TE": 5.181261380722199e-04}


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
        raise RuntimeError(f"invalid table {path}: {a.shape}")
    return a


def nl2(y: np.ndarray, r: np.ndarray) -> float:
    return float(np.linalg.norm(y-r) / max(float(np.linalg.norm(r)), 1e-300))


def cl_metric(a: np.ndarray, r: np.ndarray, col: int) -> dict:
    if a.shape[0] != r.shape[0] or not np.array_equal(a[:, 0], r[:, 0]):
        raise RuntimeError("CMB ell grid mismatch")
    return {"R2": nl2(a[:, col], r[:, col]), "n": int(a.shape[0])}


def pk_metric(a: np.ndarray, r: np.ndarray) -> dict:
    x, y = a[:, 0], a[:, 1]
    xr, yr = r[:, 0], r[:, 1]
    ma = (x > 0) & np.isfinite(x) & np.isfinite(y)
    mr = (xr > 0) & np.isfinite(xr) & np.isfinite(yr)
    x, y = x[ma], y[ma]; xr, yr = xr[mr], yr[mr]
    ia, ir = np.argsort(x), np.argsort(xr)
    x, y = x[ia], y[ia]; xr, yr = xr[ir], yr[ir]
    lo, hi = max(float(x.min()), float(xr.min())), min(float(x.max()), float(xr.max()))
    keep = (x >= lo) & (x <= hi)
    x, y = x[keep], y[keep]
    if x.size < 3:
        raise RuntimeError("insufficient P(k) overlap")
    rr = np.interp(np.log(x), np.log(xr), yr)
    return {"R2": nl2(y, rr), "n": int(x.size), "k_min": float(x.min()), "k_max": float(x.max())}


def main(root: Path, status_path: Path, out: Path) -> None:
    status = json.loads(status_path.read_text())
    result = {
        "schema": "KMDSB.M21.CLREFGlobalPrecisionDiagnostic.v1",
        "preregistration": PREREG,
        "K1_promoted": False,
        "physical_falsification": False,
        "status": status,
        "provider_preset": "cl_ref.pre",
        "provider_preset_git_blob": "ccb86d11f72d9fa754b18dca40d23378b90c0699",
        "parent_P2_excursion_factors": P2_E,
        "parent_P2_f3_R2": P2_F3,
    }
    if any(int(v) != 0 for v in status.values()):
        result["classification"] = "M21_CLREF_DIAGNOSTIC_PROVIDER_BLOCKED"
        out.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
        return

    ref_cl = load(root / "ref_cl.dat")
    ref_pk = load(root / "ref_pk.dat")
    points = {}
    for case in CASES:
        cl = load(root / f"{case}_cl.dat")
        pk = load(root / f"{case}_pk.dat")
        points[case] = {
            "fraction": FRACS[case],
            "TT": cl_metric(cl, ref_cl, 1),
            "EE": cl_metric(cl, ref_cl, 2),
            "TE": cl_metric(cl, ref_cl, 3),
            "Pk": pk_metric(pk, ref_pk),
        }
    result["points"] = points

    exc = {}
    for ch in ["TT", "EE", "TE"]:
        exc[ch] = float(points["f3"][ch]["R2"] / max(points["f2"][ch]["R2"], points["f4"][ch]["R2"], 1e-300))
    emax = max(exc.values())
    result["excursion_factors"] = exc
    result["Emax"] = float(emax)
    result["P2_Emax_over_clref_Emax"] = float(max(P2_E.values()) / max(emax, 1e-300))

    f3_reduction = {}
    localized_channels = 0
    strongly_reduced_channels = 0
    for ch in ["TT", "EE", "TE"]:
        new = points["f3"][ch]["R2"]
        ratio = float(P2_F3[ch] / max(new, 1e-300))
        f3_reduction[ch] = ratio
        if ratio >= 5.0: localized_channels += 1
        if ratio >= 3.0: strongly_reduced_channels += 1
    result["P2_to_clref_f3_reduction"] = f3_reduction

    if emax <= 3.0 and localized_channels >= 2:
        cls = "M21_CLREF_EXCURSION_LOCALIZED_TO_LOWER_PRECISION"
    elif result["P2_Emax_over_clref_Emax"] >= 3.0 or strongly_reduced_channels >= 2:
        cls = "M21_CLREF_EXCURSION_STRONGLY_REDUCED"
    else:
        cls = "M21_CLREF_EXCURSION_PERSISTS"
    result["classification"] = cls
    result["localized_channels"] = localized_channels
    result["strongly_reduced_channels"] = strongly_reduced_channels
    out.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: clref_global_precision_diagnostic.py OUTPUT_DIR STATUS.json OUT.json")
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
