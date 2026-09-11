#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

PREREG = "protocol/W04_M25_NONTHERMAL_PSD_CLASS_BRIDGE_PREREGISTRATION_v0.1.md"
STERILE_PIN = "e4486265e8207aa0dd28decc8c8d897266c0a52a"
CLASS_PIN = "e85808324f51fc694d12e3ed7439552a3c3f9540"
T_LOW_MEV = 10.0
NF = (4.0 / 11.0) ** (1.0 / 3.0)
MODEL_DIRS = [
    "ms7.115E-03s24.000E-11L2.971E-03",
    "ms7.115E-03s28.000E-12L4.849E-03",
]


def numeric_rows(path: Path) -> list[list[float]]:
    rows = []
    for line in path.read_text(errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("!"):
            continue
        vals = []
        for tok in s.split():
            try:
                vals.append(float(tok.replace("D", "E").replace("d", "e")))
            except ValueError:
                break
        if vals and all(math.isfinite(x) for x in vals):
            rows.append(vals)
    return rows


def params_values(path: Path) -> list[float]:
    vals = []
    for line in path.read_text(errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("!"):
            continue
        tok = s.split()[0]
        try:
            vals.append(float(tok.replace("D", "E").replace("d", "e")))
        except ValueError:
            continue
    return vals


def locate_generated(root: Path) -> Path:
    candidates = [p for p in root.rglob("generated_provider_outfiles") if p.is_dir()]
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) == 0 and all((root / x).is_dir() for x in MODEL_DIRS):
        return root
    raise RuntimeError(f"cannot uniquely locate generated_provider_outfiles under {root}: {candidates}")


def transform(upstream: Path, outdir: Path) -> dict:
    generated = locate_generated(upstream)
    outdir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "KMDSB.M25.PSDClassBridge.Transform.v1",
        "preregistration": PREREG,
        "sterile_provider_pin": STERILE_PIN,
        "class_pin": CLASS_PIN,
        "T_ncdm_over_Tcmb": NF,
        "models": {},
    }
    for name in MODEL_DIRS:
        d = generated / name
        pfile, sfile, snapfile = d / "params.dat", d / "state.dat", d / "Snapshot100.dat"
        if not all(x.exists() for x in (pfile, sfile, snapfile)):
            raise RuntimeError(f"missing upstream products for {name}")
        pv = params_values(pfile)
        st = numeric_rows(sfile)
        snap = numeric_rows(snapfile)
        if len(pv) < 6 or not st or len(snap) < 100:
            raise RuntimeError(f"invalid upstream structures for {name}")
        t_final = float(st[-1][0])
        if abs(t_final - T_LOW_MEV) / T_LOW_MEV > 1e-10:
            raise RuntimeError(f"final T mismatch for {name}: {t_final}")
        a = np.asarray([r[:3] for r in snap], dtype=float)
        p, fs, fsbar = a[:, 0], a[:, 1], a[:, 2]
        q = p / t_final
        favg = 0.5 * (fs + fsbar)
        fsum = fs + fsbar
        if not (np.all(np.isfinite(q)) and np.all(np.diff(q) > 0) and np.all(q > 0)):
            raise RuntimeError(f"invalid q for {name}")
        if not (np.all(np.isfinite(favg)) and np.all(favg >= 0) and np.all(np.isfinite(fsum)) and np.all(fsum >= 0)):
            raise RuntimeError(f"invalid f0 for {name}")
        avg_path = outdir / f"{name}_avg_psd.dat"
        sum_path = outdir / f"{name}_sum_psd.dat"
        np.savetxt(avg_path, np.column_stack([q, favg]), fmt="%.17e")
        np.savetxt(sum_path, np.column_stack([q, fsum]), fmt="%.17e")
        manifest["models"][name] = {
            "provider_omega_wdm_h2": float(pv[3]),
            "provider_omega_s_h2": float(pv[4]),
            "provider_omega_sbar_h2": float(pv[5]),
            "final_T_MeV": t_final,
            "q_min": float(q.min()),
            "q_max": float(q.max()),
            "favg_min": float(favg.min()),
            "favg_max": float(favg.max()),
            "rows": int(q.size),
            "avg_psd": str(avg_path.resolve()),
            "sum_psd": str(sum_path.resolve()),
        }
    (outdir / "transform_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def class_omega(psd: str) -> float:
    from classy import Class
    c = Class()
    pars = {
        "h": 0.675,
        "T_cmb": 2.7255,
        "omega_b": 0.0222,
        "omega_cdm": 0.0,
        "N_ur": 3.046,
        "N_ncdm": 1,
        "use_ncdm_psd_files": 1,
        "ncdm_psd_filenames": psd,
        "m_ncdm": 7115.0,
        "T_ncdm": NF,
        "deg_ncdm": 1.0,
    }
    c.set(pars)
    c.compute(["background"])
    omega = float(c.Omega_nu) * float(c.h) ** 2
    c.struct_cleanup()
    c.empty()
    return omega


def run(upstream: Path, work: Path, out: Path) -> None:
    result = {
        "schema": "KMDSB.M25.PSDClassBridge.v1",
        "preregistration": PREREG,
        "sterile_provider_pin": STERILE_PIN,
        "class_pin": CLASS_PIN,
        "K1_promoted": False,
        "physical_falsification": False,
        "classification": None,
        "models": {},
    }
    try:
        manifest = transform(upstream, work)
    except Exception as e:
        result["classification"] = "M25_CLASS_BRIDGE_TRANSFORM_INVALID"
        result["error"] = repr(e)
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return

    try:
        for name, m in manifest["models"].items():
            oa = class_omega(m["avg_psd"])
            os = class_omega(m["sum_psd"])
            target = float(m["provider_omega_wdm_h2"])
            rel = abs(oa - target) / target
            ratio = os / oa
            result["models"][name] = {
                "provider_omega_wdm_h2": target,
                "class_omega_avg_h2": oa,
                "class_omega_sum_h2": os,
                "relative_density_error_avg": rel,
                "sum_to_avg_ratio": ratio,
                "density_gate": bool(rel <= 0.01),
                "factor_two_negative_control": bool(1.98 <= ratio <= 2.02),
                "final_T_MeV": m["final_T_MeV"],
                "q_min": m["q_min"],
                "q_max": m["q_max"],
                "rows": m["rows"],
            }
    except Exception as e:
        result["classification"] = "M25_CLASS_BRIDGE_BLOCKED_CLASS_PROVIDER"
        result["error"] = repr(e)
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return

    ok = len(result["models"]) == 2 and all(
        m["density_gate"] and m["factor_two_negative_control"] for m in result["models"].values()
    )
    result["classification"] = "M25_CLASS_BRIDGE_DENSITY_VALIDATED" if ok else "M25_CLASS_BRIDGE_DENSITY_NOT_VALIDATED"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("upstream", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    run(args.upstream, args.work, args.out)
