#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

CLASS_PIN = "e85808324f51fc694d12e3ed7439552a3c3f9540"
FRACS = [0.10, 0.03, 0.01, 0.003, 0.001]
OMEGA_DM = 0.1200
M_WDM_EV = 3000.0
T_NCDM = 0.71611
PREREG = "protocol/W04_M21_MIXED_COLD_WARM_K1_REFERENCE_PREREGISTRATION_v0.1.md"
OUTPUT_RECOVERY = "protocol/W04_M21_CLASS_OUTPUT_ROOT_NAMING_RECOVERY_v0.1.md"


def common_ini(root: str, omega_cdm: float) -> list[str]:
    return [
        f"root = {root}",
        "output = tCl,pCl,mPk",
        "write background = yes",
        "headers = yes",
        "format = class",
        "lensing = no",
        "non linear = none",
        "modes = s",
        "ic = ad",
        "gauge = synchronous",
        "h = 0.6731",
        "omega_b = 0.02222",
        f"omega_cdm = {omega_cdm:.12g}",
        "N_ur = 3.046",
        "Omega_k = 0",
        "Omega_fld = 0",
        "Omega_scf = 0",
        "YHe = 0.24",
        "T_cmb = 2.725",
        "A_s = 2.196e-9",
        "n_s = 0.9655",
        "k_pivot = 0.05",
        "tau_reio = 0.054",
        "P_k_max_h/Mpc = 20",
        "z_pk = 0",
        "l_max_scalars = 2500",
    ]


def prepare(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    manifest = {
        "class_pin": CLASS_PIN,
        "fractions": FRACS,
        "omega_dm": OMEGA_DM,
        "m_wdm_eV": M_WDM_EV,
        "T_ncdm": T_NCDM,
        "cases": {},
    }

    ref = common_ini("output/ref_", OMEGA_DM)
    ref += ["N_ncdm = 0"]
    (out / "ref.ini").write_text("\n".join(ref) + "\n")
    manifest["cases"]["ref"] = {"fraction": 0.0, "omega_cdm": OMEGA_DM, "omega_ncdm": 0.0, "N_ncdm": 0}

    for i, f in enumerate(FRACS):
        oc = OMEGA_DM * (1.0 - f)
        ow = OMEGA_DM * f
        lines = common_ini(f"output/f{i}_", oc)
        lines += [
            "N_ncdm = 1",
            "use_ncdm_psd_files = 0",
            f"m_ncdm = {M_WDM_EV:.12g}",
            f"T_ncdm = {T_NCDM:.12g}",
            f"omega_ncdm = {ow:.12g}",
        ]
        (out / f"f{i}.ini").write_text("\n".join(lines) + "\n")
        manifest["cases"][f"f{i}"] = {"fraction": f, "omega_cdm": oc, "omega_ncdm": ow, "N_ncdm": 1}

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def resolve_output(root: Path, prefix: str, suffix: str) -> Path:
    outdir = root / "output"
    candidates = []
    exact = outdir / f"{prefix}_{suffix}.dat"
    if exact.exists():
        candidates.append(exact)
    for p in sorted(outdir.glob(f"{prefix}_*_{suffix}.dat")):
        if p not in candidates:
            candidates.append(p)
    if len(candidates) != 1:
        raise RuntimeError(f"output discovery {prefix}/{suffix}: {[str(p) for p in candidates]}")
    return candidates[0]


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


def metric(model: np.ndarray, ref: np.ndarray) -> dict:
    x = model[:, 0]
    xr = ref[:, 0]
    lo, hi = max(x.min(), xr.min()), min(x.max(), xr.max())
    mask = (x >= lo) & (x <= hi)
    x = x[mask]
    ym = model[mask, 1:]
    if x.size < 3:
        raise RuntimeError("insufficient overlap")
    if model.shape[1] != ref.shape[1]:
        raise RuntimeError(f"column mismatch model={model.shape[1]} ref={ref.shape[1]}")
    yr = np.column_stack([np.interp(x, xr, ref[:, j]) for j in range(1, ref.shape[1])])
    scale = max(float(np.max(np.abs(ym))), float(np.max(np.abs(yr))), 1e-300)
    floor = 1e-12 * scale
    r = 2.0 * (ym - yr) / (np.abs(ym) + np.abs(yr) + floor)
    vals = np.abs(r).ravel()
    return {
        "median_abs": float(np.median(vals)),
        "rms": float(np.sqrt(np.mean(r * r))),
        "p95_abs": float(np.percentile(vals, 95)),
        "n": int(vals.size),
        "floor": float(floor),
    }


def fit_exp(r95: list[float]) -> dict:
    f = np.asarray(FRACS[-3:], dtype=float)
    r = np.asarray(r95[-3:], dtype=float)
    if np.any(r <= 0):
        return {"valid": False, "p": None}
    p, logA = np.polyfit(np.log(f), np.log(r), 1)
    return {"valid": True, "p": float(p), "logA": float(logA)}


def judge(points: list[dict]) -> dict:
    r95 = [p["p95_abs"] for p in points]
    monotonic = all(r95[i + 1] <= r95[i] * 1.02 for i in range(len(r95) - 1))
    decreased = r95[-1] < r95[0]
    fit = fit_exp(r95)
    exponent = bool(fit["valid"] and fit["p"] is not None and fit["p"] > 0.5)
    return {
        "points": points,
        "r95": r95,
        "monotonic_with_2pct_slack": monotonic,
        "smallest_lower_than_largest": decreased,
        "fit_smallest3": fit,
        "pass": bool(monotonic and decreased and exponent),
    }


def channel(a: np.ndarray, col: int) -> np.ndarray:
    if col >= a.shape[1]:
        raise RuntimeError(f"missing channel col={col} shape={a.shape}")
    return a[:, [0, col]]


def analyze(root: Path, status_path: Path, out: Path):
    status = json.loads(status_path.read_text())
    result = {
        "schema": "KMDSB.M21.mixedColdWarm.K1Reference.v1",
        "class_pin": CLASS_PIN,
        "preregistration": PREREG,
        "output_naming_recovery": OUTPUT_RECOVERY,
        "fractions": FRACS,
        "omega_dm": OMEGA_DM,
        "m_wdm_eV": M_WDM_EV,
        "T_ncdm": T_NCDM,
        "status": status,
        "K0_provenance": "PASS_WITH_SCOPE_PINNED_CLASS_NCDM",
        "K1_reference_limit": "NOT_PROMOTED",
        "K2_physical_geometry": "ONE_SIDED_F_W_GE_0_NO_SIGN_QUOTIENT",
        "K4_promoted": False,
        "physical_falsification": False,
        "blocks": {},
    }
    if any(status.get(k) != 0 for k in ["build", "ref"] + [f"f{i}" for i in range(5)]):
        result["classification"] = "M21_K1_PROVIDER_EXECUTION_BLOCKED"
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return

    ref_cl = load_table(resolve_output(root, "ref", "cl"))
    ref_pk = load_table(resolve_output(root, "ref", "pk"))
    ref_bg_raw = load_table(resolve_output(root, "ref", "background"))
    if ref_cl.shape[1] < 4:
        raise RuntimeError(f"unexpected Cl schema {ref_cl.shape}")
    if ref_bg_raw.shape[1] < 4:
        raise RuntimeError(f"unexpected background schema {ref_bg_raw.shape}")
    ref_bg = ref_bg_raw[:, [0, 3]]

    finite = []
    for i in range(5):
        cl = load_table(resolve_output(root, f"f{i}", "cl"))
        pk = load_table(resolve_output(root, f"f{i}", "pk"))
        bg_raw = load_table(resolve_output(root, f"f{i}", "background"))
        if cl.shape[1] != ref_cl.shape[1]:
            raise RuntimeError(f"Cl schema mismatch f{i}: {cl.shape} ref={ref_cl.shape}")
        finite.append({"cl": cl, "pk": pk, "bg": bg_raw[:, [0, 3]]})

    specs = {
        "H": ([x["bg"] for x in finite], ref_bg),
        "Pk": ([x["pk"] for x in finite], ref_pk),
        "CMB_TT": ([channel(x["cl"], 1) for x in finite], channel(ref_cl, 1)),
        "CMB_EE": ([channel(x["cl"], 2) for x in finite], channel(ref_cl, 2)),
        "CMB_TE": ([channel(x["cl"], 3) for x in finite], channel(ref_cl, 3)),
    }

    all_pass = True
    for name, (models, ref) in specs.items():
        pts = []
        for f, m in zip(FRACS, models):
            q = metric(m, ref)
            q["fraction"] = f
            pts.append(q)
        result["blocks"][name] = judge(pts)
        all_pass = all_pass and result["blocks"][name]["pass"]

    result["failing_blocks"] = [k for k, v in result["blocks"].items() if not v["pass"]]
    if all_pass:
        result["classification"] = "M21_K1_REFERENCE_LIMIT_PASS_WITH_SCOPE"
        result["K1_reference_limit"] = "PASS_WITH_SCOPE_SAME_SOLVER_ZERO_FRACTION_LIMIT"
    else:
        result["classification"] = "M21_K1_REFERENCE_LIMIT_NOT_ESTABLISHED"
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
