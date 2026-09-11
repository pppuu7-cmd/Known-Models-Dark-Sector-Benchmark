#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

PROVIDER_PIN = "7c4b26e50d240f1f45f120b623aab2dba13094fd"
PREREG = "protocol/W04_M26_PBH_ENERGY_INJECTION_PROVIDER_CONTROL_PREREGISTRATION_v0.1.md"
CHILDREN = {"evaporation", "spherical", "disk"}


def common_ini(root: str) -> list[str]:
    return [
        f"root = {root}",
        "output = tCl,pCl,mPk",
        "write background = yes",
        "write thermodynamics = yes",
        "headers = yes",
        "format = class",
        "lensing = no",
        "non linear = none",
        "omega_b = 0.02218",
        "omega_cdm = 0.1205",
        "100*theta_s = 1.04069",
        "z_reio = 8.24",
        "ln10^{10}A_s = 3.056",
        "n_s = 0.9619",
        "on the spot = no",
        "energy_deposition_function = DarkAges",
        "DarkAges_mode = built_in",
        "energy_repartition_coefficient = no_factorization",
        "recombination = recfast",
        "reio_stars_and_dark_matter = yes",
        "P_k_max_h/Mpc = 5",
        "z_pk = 0",
        "l_max_scalars = 1200",
    ]


def child_lines(child: str, fraction: float) -> list[str]:
    lines = [f"PBH_fraction = {fraction:.17g}"]
    if child == "evaporation":
        lines += ["PBH_evaporating_mass = 1e15"]
    elif child == "spherical":
        lines += [
            "PBH_accreting_mass = 1e3",
            "PBH_accretion_recipe = spherical_accretion",
        ]
    elif child == "disk":
        lines += [
            "PBH_accreting_mass = 1e3",
            "PBH_accretion_recipe = disk_accretion",
        ]
    else:
        raise ValueError(child)
    return lines


def prepare(child: str, out: Path) -> None:
    if child not in CHILDREN:
        raise ValueError(f"unknown child {child}")
    out.mkdir(parents=True, exist_ok=True)
    cases = {
        "baseline": common_ini(f"output/m26_{child}_baseline_"),
        "zero": common_ini(f"output/m26_{child}_zero_") + child_lines(child, 0.0),
        "finite": common_ini(f"output/m26_{child}_finite_") + child_lines(child, 1e-5),
    }
    for name, lines in cases.items():
        (out / f"{name}.ini").write_text("\n".join(lines) + "\n")
    manifest = {
        "schema": "KMDSB.M26.PBHEnergyInjectionProviderControl.Manifest.v1",
        "provider": "GFAbellan/ExoCLASS",
        "provider_pin": PROVIDER_PIN,
        "preregistration": PREREG,
        "child": child,
        "fraction_zero": 0.0,
        "fraction_finite": 1e-5,
        "mass": {"evaporation_g": 1e15} if child == "evaporation" else {"accretion_Msun": 1e3},
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
        if len(row) >= 2 and all(math.isfinite(v) for v in row):
            rows.append(row)
    a = np.asarray(rows, dtype=float)
    if a.ndim != 2 or a.shape[0] < 3 or a.shape[1] < 2:
        raise RuntimeError(f"invalid table {path}: shape={a.shape}")
    order = np.argsort(a[:, 0])
    return a[order]


def resolve_output(root: Path, prefix: str, suffix: str) -> Path:
    outdir = root / "output"
    candidates: list[Path] = []
    exact = outdir / f"{prefix}_{suffix}.dat"
    if exact.exists():
        candidates.append(exact)
    for p in sorted(outdir.glob(f"{prefix}_*_{suffix}.dat")):
        if p not in candidates:
            candidates.append(p)
    if len(candidates) != 1:
        raise RuntimeError(f"output discovery {prefix}/{suffix}: {[str(p) for p in candidates]}")
    return candidates[0]


def channel(a: np.ndarray, col: int) -> np.ndarray:
    if col >= a.shape[1]:
        raise RuntimeError(f"missing column {col} in shape {a.shape}")
    return a[:, [0, col]]


def metric(model: np.ndarray, ref: np.ndarray) -> dict:
    if model.shape[1] != ref.shape[1]:
        raise RuntimeError(f"column mismatch {model.shape[1]} vs {ref.shape[1]}")
    x = model[:, 0]
    xr = ref[:, 0]
    lo = max(float(x.min()), float(xr.min()))
    hi = min(float(x.max()), float(xr.max()))
    mask = (x >= lo) & (x <= hi)
    xq = x[mask]
    ym = model[mask, 1:]
    if xq.size < 3:
        raise RuntimeError("insufficient support overlap")
    yr = np.column_stack([np.interp(xq, xr, ref[:, j]) for j in range(1, ref.shape[1])])
    scale = max(float(np.max(np.abs(ym))), float(np.max(np.abs(yr))), 1e-300)
    floor = 1e-12 * scale
    r = 2.0 * (ym - yr) / (np.abs(ym) + np.abs(yr) + floor)
    vals = np.abs(r).ravel()
    return {
        "p95_abs": float(np.percentile(vals, 95)),
        "max_abs": float(np.max(vals)),
        "rms": float(np.sqrt(np.mean(r * r))),
        "n": int(vals.size),
        "support": [lo, hi],
        "floor": float(floor),
    }


def analyze(root: Path, status_path: Path, manifest_path: Path, out: Path) -> None:
    status = json.loads(status_path.read_text())
    manifest = json.loads(manifest_path.read_text())
    child = manifest["child"]
    result = {
        "schema": "KMDSB.M26.PBHEnergyInjectionProviderControl.v1",
        "provider": manifest["provider"],
        "provider_pin": manifest["provider_pin"],
        "preregistration": manifest["preregistration"],
        "child": child,
        "K1_promoted": False,
        "K4_promoted": False,
        "physical_falsification": False,
        "status": status,
        "zero_identity_threshold_p95": 1e-8,
        "finite_response_floor_max_abs": 1e-10,
    }
    required = ["build", "baseline", "zero", "finite"]
    bad = [k for k in required if status.get(k) != 0]
    if bad:
        result["classification"] = f"M26_{child.upper()}_PROVIDER_EXECUTION_BLOCKED"
        result["failed_status_keys"] = bad
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return

    data: dict[str, dict[str, np.ndarray]] = {}
    for case in ("baseline", "zero", "finite"):
        prefix = f"m26_{child}_{case}"
        bg = load_table(resolve_output(root, prefix, "background"))
        th = load_table(resolve_output(root, prefix, "thermodynamics"))
        cl = load_table(resolve_output(root, prefix, "cl"))
        pk = load_table(resolve_output(root, prefix, "pk"))
        data[case] = {
            "background": bg,
            "thermodynamics": th,
            "TT": channel(cl, 1),
            "EE": channel(cl, 2),
            "TE": channel(cl, 3),
            "Pk": pk,
        }

    zero = {k: metric(data["zero"][k], data["baseline"][k]) for k in data["baseline"]}
    finite = {k: metric(data["finite"][k], data["baseline"][k]) for k in data["baseline"]}
    result["baseline_vs_explicit_zero"] = zero
    result["baseline_vs_finite"] = finite
    result["zero_identity_pass"] = all(v["p95_abs"] <= 1e-8 for v in zero.values())
    sensitive_blocks = ["thermodynamics", "TT", "EE", "TE"]
    result["finite_response_resolved"] = any(finite[k]["max_abs"] > 1e-10 for k in sensitive_blocks)

    if not result["zero_identity_pass"]:
        cls = f"M26_{child.upper()}_EXPLICIT_ZERO_IDENTITY_NOT_ESTABLISHED"
    elif not result["finite_response_resolved"]:
        cls = f"M26_{child.upper()}_FINITE_RESPONSE_NOT_RESOLVED"
    else:
        cls = f"M26_{child.upper()}_PROVIDER_REFERENCE_CONTROL_PASS_WITH_SCOPE"
    result["classification"] = cls
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("prepare")
    p.add_argument("child", choices=sorted(CHILDREN))
    p.add_argument("out", type=Path)
    a = sp.add_parser("analyze")
    a.add_argument("root", type=Path)
    a.add_argument("status", type=Path)
    a.add_argument("manifest", type=Path)
    a.add_argument("out", type=Path)
    args = ap.parse_args()
    if args.cmd == "prepare":
        prepare(args.child, args.out)
    else:
        analyze(args.root, args.status, args.manifest, args.out)


if __name__ == "__main__":
    main()
