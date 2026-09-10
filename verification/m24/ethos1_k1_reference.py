#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

CLASS_PIN = "e85808324f51fc694d12e3ed7439552a3c3f9540"
PREREG = "protocol/W04_M24_ETHOS1_K1_REFERENCE_PREREGISTRATION_v0.1.md"
A4 = [6.0e4, 1.8e4, 6.0e3, 1.8e3, 6.0e2]


def common(root: str) -> list[str]:
    return [
        f"root = {root}",
        "overwrite_root = yes",
        "output = tCl,pCl,mPk",
        "lensing = no",
        "non linear = none",
        "modes = s",
        "ic = ad",
        "gauge = synchronous",
        "h = 0.675",
        "omega_b = 0.0222",
        "omega_cdm = 0.1197",
        "N_ur = 3.046",
        "A_s = 2.196e-9",
        "n_s = 0.9655",
        "tau_reio = 0.06",
        "f_idm = 1",
        "xi_idr = 0.5",
        "stat_f_idr = 0.875",
        "nindex_idm_dr = 4",
        "idr_nature = free_streaming",
        "alpha_idm_dr = 1.5",
        "b_idr = 0",
        "P_k_max_h/Mpc = 50",
        "z_pk = 0",
        "l_max_scalars = 2500",
    ]


def prepare(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "ref.ini").write_text("\n".join(common("output/ref")) + "\n")
    (out / "zero.ini").write_text("\n".join(common("output/zero") + ["a_idm_dr = 0"]) + "\n")
    for i, a4 in enumerate(A4):
        (out / f"a{i}.ini").write_text("\n".join(common(f"output/a{i}") + [f"a_idm_dr = {a4:.12e}"]) + "\n")
    manifest = {
        "schema": "KMDSB.M24.ETHOS1.K1Manifest.v1",
        "class_pin": CLASS_PIN,
        "preregistration": PREREG,
        "a4_Mpc^-1": A4,
        "fixed": {
            "f_idm": 1.0, "xi_idr": 0.5, "stat_f_idr": 0.875,
            "nindex_idm_dr": 4, "idr_nature": "free_streaming",
            "alpha_idm_dr": 1.5, "b_idr": 0.0,
        },
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


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
    if a.shape[1] <= col or r.shape[1] <= col:
        raise RuntimeError(f"missing CMB col {col}: {a.shape} {r.shape}")
    if a.shape[0] != r.shape[0] or not np.array_equal(a[:, 0], r[:, 0]):
        raise RuntimeError("CMB ell grid mismatch")
    return {"R2": nl2(a[:, col], r[:, col]), "n": int(a.shape[0])}


def pk_metric(a: np.ndarray, r: np.ndarray) -> dict:
    x, y = a[:, 0], a[:, 1]
    xr, yr = r[:, 0], r[:, 1]
    m = (x > 0) & np.isfinite(x) & np.isfinite(y)
    mr = (xr > 0) & np.isfinite(xr) & np.isfinite(yr)
    x, y = x[m], y[m]
    xr, yr = xr[mr], yr[mr]
    ia, ir = np.argsort(x), np.argsort(xr)
    x, y = x[ia], y[ia]
    xr, yr = xr[ir], yr[ir]
    lo, hi = max(float(x.min()), float(xr.min())), min(float(x.max()), float(xr.max()))
    keep = (x >= lo) & (x <= hi)
    x, y = x[keep], y[keep]
    if x.size < 3:
        raise RuntimeError("insufficient Pk overlap")
    rr = np.interp(np.log(x), np.log(xr), yr)
    return {"R2": nl2(y, rr), "n": int(x.size), "k_min": float(x.min()), "k_max": float(x.max())}


def fit_tail(seq: list[float]) -> dict:
    x = np.asarray(A4[-3:], dtype=float)
    y = np.asarray(seq[-3:], dtype=float)
    if np.any(y <= 0) or np.any(~np.isfinite(y)):
        return {"valid": False, "p": None}
    p, logA = np.polyfit(np.log(x), np.log(y), 1)
    return {"valid": True, "p": float(p), "logA": float(logA)}


def judge(points: list[dict], response_floor: float, subthreshold_ok: bool=False) -> dict:
    seq = [float(q["R2"]) for q in points]
    if seq[0] <= response_floor and subthreshold_ok:
        return {"points": points, "R2_sequence": seq, "status": "SUBTHRESHOLD_RESPONSE", "pass": True}
    monotonic = all(seq[i+1] <= 1.02*seq[i] for i in range(len(seq)-1))
    contracted = seq[-1] <= 0.25*seq[0]
    fit = fit_tail(seq)
    positive = bool(fit["valid"] and fit["p"] is not None and fit["p"] > 0.20)
    passed = bool(seq[0] > response_floor and monotonic and contracted and positive)
    return {
        "points": points, "R2_sequence": seq,
        "largest_response_gt_floor": bool(seq[0] > response_floor),
        "response_floor": response_floor,
        "monotonic_with_2pct_slack": monotonic,
        "smallest_le_quarter_largest": contracted,
        "fit_smallest3": fit,
        "status": "PASS" if passed else "FAIL",
        "pass": passed,
    }


def analyze(root: Path, status_path: Path, out: Path) -> None:
    st = json.loads(status_path.read_text())
    keys = ["build", "ref", "zero"] + [f"a{i}" for i in range(len(A4))]
    res = {
        "schema": "KMDSB.M24.ETHOS1.K1Reference.v1",
        "class_pin": CLASS_PIN,
        "preregistration": PREREG,
        "a4_Mpc^-1": A4,
        "status": st,
        "K0_provenance": "PASS_WITH_SCOPE_PINNED_CLASS_ETHOS1_LITERATURE_ANCHOR",
        "K1_reference_limit": "NOT_PROMOTED",
        "K2_physical_geometry": "ONE_SIDED_A4_GE_0_NO_SIGN_QUOTIENT",
        "representative_scope": "ETHOS1_N4_XI0P5_FREE_STREAMING_ALPHA1P5_B0",
        "K3_promoted": False,
        "K4_promoted": False,
        "physical_falsification": False,
    }
    if any(st.get(k) != 0 for k in keys):
        res["classification"] = "M24_ETHOS1_K1_PROVIDER_EXECUTION_BLOCKED"
        out.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")
        return

    rc, zc = load(root/"output/ref_cl.dat"), load(root/"output/zero_cl.dat")
    rp, zp = load(root/"output/ref_pk.dat"), load(root/"output/zero_pk.dat")
    exact = {
        "TT": cl_metric(zc, rc, 1), "EE": cl_metric(zc, rc, 2),
        "TE": cl_metric(zc, rc, 3), "Pk": pk_metric(zp, rp),
    }
    exact_pass = all(v["R2"] <= 1e-12 for v in exact.values())
    res["exact_zero_vs_omitted"] = exact
    res["exact_zero_identity_pass"] = bool(exact_pass)

    cls = [load(root/f"output/a{i}_cl.dat") for i in range(len(A4))]
    pks = [load(root/f"output/a{i}_pk.dat") for i in range(len(A4))]
    blocks = {}
    pts = []
    for a4, pk in zip(A4, pks):
        q = pk_metric(pk, zp); q["a4"] = a4; pts.append(q)
    blocks["Pk"] = judge(pts, 1e-6, subthreshold_ok=False)
    for name, col in [("TT",1),("EE",2),("TE",3)]:
        pts = []
        for a4, cl in zip(A4, cls):
            q = cl_metric(cl, zc, col); q["a4"] = a4; pts.append(q)
        blocks[name] = judge(pts, 1e-8, subthreshold_ok=True)
    res["blocks"] = blocks
    res["diagnostic_failing_blocks"] = [k for k in ["TT","EE","TE"] if blocks[k]["status"] == "FAIL"]
    if exact_pass and blocks["Pk"]["pass"]:
        res["classification"] = "M24_ETHOS1_K1_DECOUPLING_PASS_WITH_SCOPE_N4_FREE_STREAMING"
        res["K1_reference_limit"] = "PASS_WITH_SCOPE_ETHOS1_FIXED_SPECIES_A4_TO_ZERO"
    else:
        res["classification"] = "M24_ETHOS1_K1_DECOUPLING_NOT_ESTABLISHED"
    out.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("prepare"); p.add_argument("out", type=Path)
    a = sp.add_parser("analyze"); a.add_argument("root", type=Path); a.add_argument("status", type=Path); a.add_argument("out", type=Path)
    args = ap.parse_args(); prepare(args.out) if args.cmd == "prepare" else analyze(args.root, args.status, args.out)
