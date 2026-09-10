#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

CLASS_PIN = "e85808324f51fc694d12e3ed7439552a3c3f9540"
PREREG = "protocol/W04_M24_DARK_TCA_THRESHOLD_DIAGNOSTIC_PREREGISTRATION_v0.1.md"
PROFILES = ["D_DEFAULT", "E_EARLY_OFF", "O_TCA_OFF"]
CASES = {"a18k": 18000.0, "a6k": 6000.0, "a1p8k": 1800.0}


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


def prepare(out: Path, pres: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    pres.mkdir(parents=True, exist_ok=True)
    (out / "ref.ini").write_text("\n".join(common("output/ref")) + "\n")
    (out / "zero.ini").write_text("\n".join(common("output/zero") + ["a_idm_dr = 0"]) + "\n")
    for name, a in CASES.items():
        (out / f"{name}.ini").write_text("\n".join(common(f"output/{name}") + [f"a_idm_dr = {a:.12e}"]) + "\n")
    (pres / "E_EARLY_OFF.pre").write_text(
        "idm_dr_tight_coupling_trigger_tau_c_over_tau_k = 0.003\n"
        "idm_dr_tight_coupling_trigger_tau_c_over_tau_h = 0.0045\n"
    )
    (pres / "O_TCA_OFF.pre").write_text(
        "idm_dr_tight_coupling_trigger_tau_c_over_tau_k = 0\n"
        "idm_dr_tight_coupling_trigger_tau_c_over_tau_h = 0\n"
    )
    manifest = {
        "schema": "KMDSB.M24.DarkTCAThresholdDiagnostic.Manifest.v1",
        "class_pin": CLASS_PIN,
        "preregistration": PREREG,
        "cases_Mpc^-1": CASES,
        "profiles": {
            "D_DEFAULT": {"tau_k": 0.01, "tau_h": 0.015, "provider_default": True},
            "E_EARLY_OFF": {"tau_k": 0.003, "tau_h": 0.0045},
            "O_TCA_OFF": {"tau_k": 0.0, "tau_h": 0.0},
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
    if a.shape[0] != r.shape[0] or not np.array_equal(a[:, 0], r[:, 0]):
        raise RuntimeError("CMB ell grid mismatch")
    return {"R2": nl2(a[:, col], r[:, col]), "n": int(a.shape[0])}


def pk_metric(a: np.ndarray, r: np.ndarray) -> dict:
    x, y = a[:, 0], a[:, 1]
    xr, yr = r[:, 0], r[:, 1]
    ma = (x > 0) & np.isfinite(x) & np.isfinite(y)
    mr = (xr > 0) & np.isfinite(xr) & np.isfinite(yr)
    x, y = x[ma], y[ma]
    xr, yr = xr[mr], yr[mr]
    ia, ir = np.argsort(x), np.argsort(xr)
    x, y, xr, yr = x[ia], y[ia], xr[ir], yr[ir]
    lo, hi = max(float(x.min()), float(xr.min())), min(float(x.max()), float(xr.max()))
    keep = (x >= lo) & (x <= hi)
    x, y = x[keep], y[keep]
    rr = np.interp(np.log(x), np.log(xr), yr)
    return {"R2": nl2(y, rr), "n": int(x.size), "k_min": float(x.min()), "k_max": float(x.max())}


def tables(root: Path, case: str) -> tuple[np.ndarray, np.ndarray]:
    return load(root / f"{case}_cl.dat"), load(root / f"{case}_pk.dat")


def metrics(a: tuple[np.ndarray, np.ndarray], r: tuple[np.ndarray, np.ndarray]) -> dict:
    ac, ap = a; rc, rp = r
    return {
        "TT": cl_metric(ac, rc, 1),
        "EE": cl_metric(ac, rc, 2),
        "TE": cl_metric(ac, rc, 3),
        "Pk": pk_metric(ap, rp),
    }


def analyze(results: Path, status_path: Path, out: Path) -> None:
    status = json.loads(status_path.read_text())
    res = {
        "schema": "KMDSB.M24.DarkTCAThresholdDiagnostic.v1",
        "class_pin": CLASS_PIN,
        "preregistration": PREREG,
        "K1_promoted": False,
        "physical_falsification": False,
        "status": status,
        "profiles": {},
        "direct_profile_vs_default": {},
    }
    if any(v != 0 for v in status.values()):
        res["classification"] = "M24_DARK_TCA_DIAGNOSTIC_PROVIDER_BLOCKED"
        out.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")
        return

    for profile in PROFILES:
        root = results / profile
        ref = tables(root, "ref")
        zero = tables(root, "zero")
        exact = metrics(zero, ref)
        responses = {case: metrics(tables(root, case), zero) for case in CASES}
        exc = {}
        for ch in ["TT", "EE", "TE"]:
            r6 = responses["a6k"][ch]["R2"]
            denom = max(responses["a18k"][ch]["R2"], responses["a1p8k"][ch]["R2"], 1e-300)
            exc[ch] = float(r6 / denom)
        res["profiles"][profile] = {
            "exact_zero_vs_omitted": exact,
            "exact_identity_pass": all(v["R2"] <= 1e-12 for v in exact.values()),
            "responses": responses,
            "excursion_factors": exc,
            "Emax": max(exc.values()),
        }

    droot = results / "D_DEFAULT"
    for profile in ["E_EARLY_OFF", "O_TCA_OFF"]:
        proot = results / profile
        res["direct_profile_vs_default"][profile] = {}
        for case in ["ref", "zero"] + list(CASES):
            res["direct_profile_vs_default"][profile][case] = metrics(tables(proot, case), tables(droot, case))

    d = res["profiles"]["D_DEFAULT"]
    o = res["profiles"]["O_TCA_OFF"]
    localized_channels = 0
    sensitive_channels = 0
    for ch in ["TT", "EE", "TE"]:
        rd = d["responses"]["a6k"][ch]["R2"]
        ro = o["responses"]["a6k"][ch]["R2"]
        ratio = max(rd, ro) / max(min(rd, ro), 1e-300)
        if ro <= rd / 5.0:
            localized_channels += 1
        if ratio >= 3.0:
            sensitive_channels += 1
    if d["Emax"] > 9.0 and o["Emax"] <= 3.0 and localized_channels >= 2:
        cls = "M24_DARK_TCA_EXCURSION_LOCALIZED"
    else:
        e_ratio = max(d["Emax"], o["Emax"]) / max(min(d["Emax"], o["Emax"]), 1e-300)
        if e_ratio >= 3.0 or sensitive_channels >= 2:
            cls = "M24_DARK_TCA_EXCURSION_STRONGLY_SENSITIVE"
        else:
            cls = "M24_DARK_TCA_EXCURSION_INSENSITIVE"
    res["classification"] = cls
    res["localized_channels"] = localized_channels
    res["sensitive_channels"] = sensitive_channels
    out.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("prepare"); p.add_argument("cases", type=Path); p.add_argument("profiles", type=Path)
    a = sp.add_parser("analyze"); a.add_argument("results", type=Path); a.add_argument("status", type=Path); a.add_argument("out", type=Path)
    args = ap.parse_args()
    if args.cmd == "prepare": prepare(args.cases, args.profiles)
    else: analyze(args.results, args.status, args.out)
