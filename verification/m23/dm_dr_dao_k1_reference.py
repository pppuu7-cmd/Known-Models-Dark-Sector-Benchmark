#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

CLASS_PIN = "e85808324f51fc694d12e3ed7439552a3c3f9540"
PREREG = "protocol/W04_M23_DM_DR_DAO_K1_REFERENCE_PREREGISTRATION_v0.1.md"
GAMMA = [2.371e-8, 7.113e-9, 2.371e-9, 7.113e-10, 2.371e-10]


def common_ini(root: str) -> list[str]:
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
        "N_idr = 0.4290",
        "nindex_idm_dr = 0",
        "idr_nature = fluid",
        "b_idr = 0",
        "P_k_max_h/Mpc = 20",
        "z_pk = 0",
        "l_max_scalars = 2500",
    ]


def prepare(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    ref = common_ini("output/ref")
    (out / "ref.ini").write_text("\n".join(ref) + "\n")
    zero = common_ini("output/zero") + ["Gamma_0_nadm = 0"]
    (out / "zero.ini").write_text("\n".join(zero) + "\n")
    for i, g in enumerate(GAMMA):
        lines = common_ini(f"output/g{i}") + [f"Gamma_0_nadm = {g:.12e}"]
        (out / f"g{i}.ini").write_text("\n".join(lines) + "\n")
    manifest = {
        "schema": "KMDSB.M23.dmDrDao.K1Manifest.v1",
        "class_pin": CLASS_PIN,
        "preregistration": PREREG,
        "Gamma_0_nadm_Mpc^-1": GAMMA,
        "fixed": {"f_idm": 1.0, "N_idr": 0.4290, "nindex_idm_dr": 0, "idr_nature": "fluid", "b_idr": 0.0},
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def load_table(path: Path) -> np.ndarray:
    rows = []
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
    a = np.asarray(rows, dtype=float)
    if a.ndim != 2 or a.shape[0] < 3 or a.shape[1] < 2:
        raise RuntimeError(f"invalid table {path}: shape={a.shape}")
    return a


def r2(y: np.ndarray, yr: np.ndarray) -> float:
    return float(np.linalg.norm(y - yr) / max(float(np.linalg.norm(yr)), 1e-300))


def cl_metric(model: np.ndarray, ref: np.ndarray, col: int) -> dict:
    if model.shape[1] <= col or ref.shape[1] <= col:
        raise RuntimeError(f"missing CMB col={col}: model={model.shape}, ref={ref.shape}")
    if model.shape[0] != ref.shape[0] or not np.array_equal(model[:, 0], ref[:, 0]):
        raise RuntimeError("CMB ell grids differ")
    return {"R2": r2(model[:, col], ref[:, col]), "n": int(model.shape[0])}


def pk_metric(model: np.ndarray, ref: np.ndarray) -> dict:
    xm, ym = model[:, 0], model[:, 1]
    xr, yr = ref[:, 0], ref[:, 1]
    im, ir = np.argsort(xm), np.argsort(xr)
    xm, ym = xm[im], ym[im]
    xr, yr = xr[ir], yr[ir]
    goodm = (xm > 0) & np.isfinite(ym)
    goodr = (xr > 0) & np.isfinite(yr)
    xm, ym = xm[goodm], ym[goodm]
    xr, yr = xr[goodr], yr[goodr]
    lo, hi = max(float(xm.min()), float(xr.min())), min(float(xm.max()), float(xr.max()))
    mask = (xm >= lo) & (xm <= hi)
    x, y = xm[mask], ym[mask]
    if x.size < 3:
        raise RuntimeError("insufficient P(k) overlap")
    yref = np.interp(np.log(x), np.log(xr), yr)
    return {"R2": r2(y, yref), "n": int(x.size), "k_min": float(x.min()), "k_max": float(x.max())}


def fit_tail(seq: list[float]) -> dict:
    x = np.asarray(GAMMA[-3:], dtype=float)
    y = np.asarray(seq[-3:], dtype=float)
    if np.any(y <= 0) or np.any(~np.isfinite(y)):
        return {"valid": False, "p": None}
    p, logA = np.polyfit(np.log(x), np.log(y), 1)
    return {"valid": True, "p": float(p), "logA": float(logA)}


def judge(points: list[dict]) -> dict:
    seq = [float(q["R2"]) for q in points]
    monotonic = all(seq[i + 1] <= 1.02 * seq[i] for i in range(len(seq) - 1))
    response = seq[0] > 1e-8
    contracted = seq[-1] <= 0.25 * seq[0]
    fit = fit_tail(seq)
    positive = bool(fit["valid"] and fit["p"] is not None and fit["p"] > 0.20)
    return {
        "points": points,
        "R2_sequence": seq,
        "monotonic_with_2pct_slack": monotonic,
        "largest_response_gt_1e-8": response,
        "smallest_le_quarter_largest": contracted,
        "fit_smallest3": fit,
        "pass": bool(monotonic and response and contracted and positive),
    }


def analyze(root: Path, status_path: Path, out: Path) -> None:
    status = json.loads(status_path.read_text())
    keys = ["build", "ref", "zero"] + [f"g{i}" for i in range(len(GAMMA))]
    result = {
        "schema": "KMDSB.M23.dmDrDao.K1Reference.v1",
        "class_pin": CLASS_PIN,
        "preregistration": PREREG,
        "Gamma_0_nadm_Mpc^-1": GAMMA,
        "status": status,
        "K0_provenance": "PASS_WITH_SCOPE_PINNED_NATIVE_CLASS_IDM_DR",
        "K1_reference_limit": "NOT_PROMOTED",
        "K2_physical_geometry": "ONE_SIDED_GAMMA_GE_0_NO_SIGN_QUOTIENT",
        "reference_scope": "FIXED_F_IDM_1_N_IDR_0P429_FLUID_DR_NINDEX0_ONLY_COUPLING_REMOVED",
        "K4_promoted": False,
        "physical_falsification": False,
    }
    if any(status.get(k) != 0 for k in keys):
        result["classification"] = "M23_K1_PROVIDER_EXECUTION_BLOCKED"
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return

    ref_cl = load_table(root / "output/ref_cl.dat")
    zero_cl = load_table(root / "output/zero_cl.dat")
    ref_pk = load_table(root / "output/ref_pk.dat")
    zero_pk = load_table(root / "output/zero_pk.dat")
    exact = {
        "TT": cl_metric(zero_cl, ref_cl, 1),
        "EE": cl_metric(zero_cl, ref_cl, 2),
        "TE": cl_metric(zero_cl, ref_cl, 3),
        "Pk": pk_metric(zero_pk, ref_pk),
    }
    exact_pass = all(v["R2"] <= 1e-12 for v in exact.values())
    result["exact_zero_vs_omitted"] = exact
    result["exact_zero_identity_pass"] = bool(exact_pass)

    finite_cl = [load_table(root / f"output/g{i}_cl.dat") for i in range(len(GAMMA))]
    finite_pk = [load_table(root / f"output/g{i}_pk.dat") for i in range(len(GAMMA))]
    blocks = {}
    for name, col in [("TT", 1), ("EE", 2), ("TE", 3)]:
        pts = []
        for g, cl in zip(GAMMA, finite_cl):
            q = cl_metric(cl, zero_cl, col)
            q["Gamma_0_nadm"] = g
            pts.append(q)
        blocks[name] = judge(pts)
    pk_pts = []
    for g, pk in zip(GAMMA, finite_pk):
        q = pk_metric(pk, zero_pk)
        q["Gamma_0_nadm"] = g
        pk_pts.append(q)
    blocks["Pk"] = judge(pk_pts)
    result["blocks"] = blocks
    result["diagnostic_failing_blocks"] = [x for x in ["EE", "TE"] if not blocks[x]["pass"]]

    required = exact_pass and blocks["Pk"]["pass"] and blocks["TT"]["pass"]
    if required:
        result["classification"] = "M23_K1_DECOUPLING_PASS_WITH_SCOPE_FIXED_DM_DR_CONTENT"
        result["K1_reference_limit"] = "PASS_WITH_SCOPE_FIXED_DM_DR_CONTENT_ONLY_COUPLING_TO_ZERO"
    else:
        result["classification"] = "M23_K1_DECOUPLING_NOT_ESTABLISHED"
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
