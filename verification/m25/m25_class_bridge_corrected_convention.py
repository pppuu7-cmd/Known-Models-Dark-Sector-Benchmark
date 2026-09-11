#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verification.m25.m25_class_bridge import (
    CLASS_PIN,
    MODEL_DIRS,
    NF,
    STERILE_PIN,
    T_LOW_MEV,
    class_omega,
    locate_generated,
    numeric_rows,
    params_values,
)

PREREG = "protocol/W04_M25_CLASS_PSD_CONVENTION_CORRECTION_PREREGISTRATION_v0.1.md"
CONVENTION_FACTOR = (2.0 * math.pi) ** 3 / 2.0


def transform(upstream: Path, outdir: Path) -> dict:
    generated = locate_generated(upstream)
    outdir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "KMDSB.M25.PSDClassBridge.CorrectedConvention.Transform.v1",
        "preregistration": PREREG,
        "sterile_provider_pin": STERILE_PIN,
        "class_pin": CLASS_PIN,
        "T_ncdm_over_Tcmb": NF,
        "analytic_wrong_to_correct_factor": CONVENTION_FACTOR,
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
        fcorrect = (fs + fsbar) / (2.0 * math.pi) ** 3
        f2x = 2.0 * fcorrect
        if not (np.all(np.isfinite(q)) and np.all(np.diff(q) > 0) and np.all(q > 0)):
            raise RuntimeError(f"invalid q for {name}")
        if not (np.all(np.isfinite(fcorrect)) and np.all(fcorrect >= 0)):
            raise RuntimeError(f"invalid corrected f0 for {name}")
        correct_path = outdir / f"{name}_class_convention_psd.dat"
        twice_path = outdir / f"{name}_class_convention_2x_psd.dat"
        np.savetxt(correct_path, np.column_stack([q, fcorrect]), fmt="%.17e")
        np.savetxt(twice_path, np.column_stack([q, f2x]), fmt="%.17e")
        manifest["models"][name] = {
            "provider_omega_wdm_h2": float(pv[3]),
            "provider_omega_s_h2": float(pv[4]),
            "provider_omega_sbar_h2": float(pv[5]),
            "final_T_MeV": t_final,
            "q_min": float(q.min()),
            "q_max": float(q.max()),
            "fcorrect_min": float(fcorrect.min()),
            "fcorrect_max": float(fcorrect.max()),
            "rows": int(q.size),
            "correct_psd": str(correct_path.resolve()),
            "twice_psd": str(twice_path.resolve()),
        }
    (outdir / "transform_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def run(upstream: Path, work: Path, out: Path) -> None:
    result = {
        "schema": "KMDSB.M25.PSDClassBridge.CorrectedConvention.v1",
        "preregistration": PREREG,
        "sterile_provider_pin": STERILE_PIN,
        "class_pin": CLASS_PIN,
        "analytic_wrong_to_correct_factor": CONVENTION_FACTOR,
        "K1_promoted": False,
        "physical_falsification": False,
        "classification": None,
        "models": {},
    }
    try:
        manifest = transform(upstream, work)
        for name, m in manifest["models"].items():
            oc = class_omega(m["correct_psd"])
            o2 = class_omega(m["twice_psd"])
            target = float(m["provider_omega_wdm_h2"])
            rel = abs(oc - target) / target
            ratio = o2 / oc
            result["models"][name] = {
                "provider_omega_wdm_h2": target,
                "class_omega_corrected_h2": oc,
                "class_omega_2x_h2": o2,
                "relative_density_error": rel,
                "two_x_ratio": ratio,
                "density_gate": bool(rel <= 0.01),
                "factor_two_negative_control": bool(1.98 <= ratio <= 2.02),
                "final_T_MeV": m["final_T_MeV"],
                "q_min": m["q_min"],
                "q_max": m["q_max"],
                "rows": m["rows"],
            }
    except Exception as e:
        result["classification"] = "M25_CLASS_CONVENTION_CORRECTED_BLOCKED"
        result["error"] = repr(e)
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return

    ok = len(result["models"]) == 2 and all(
        m["density_gate"] and m["factor_two_negative_control"] for m in result["models"].values()
    )
    result["classification"] = (
        "M25_CLASS_CONVENTION_CORRECTED_DENSITY_VALIDATED"
        if ok
        else "M25_CLASS_CONVENTION_CORRECTED_DENSITY_NOT_VALIDATED"
    )
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("upstream", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    run(args.upstream, args.work, args.out)
