#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

from verification.m25.provider_control import numeric_rows, params_values

PIN = "e4486265e8207aa0dd28decc8c8d897266c0a52a"
PREREG = "protocol/W04_M25_PROVIDER_MOMENTUM_SUPPORT_EXTENSION_PREREGISTRATION_v0.1.md"
MODEL_DIRS = [
    "ms7.115E-03s24.000E-11L2.971E-03",
    "ms7.115E-03s28.000E-12L4.849E-03",
]


def model_metrics(root: Path, name: str) -> dict:
    d = root / name
    pv = params_values(d / "params.dat")
    state = numeric_rows(d / "state.dat")
    snap = numeric_rows(d / "Snapshot100.dat")
    if len(pv) < 6 or not state or len(snap) < 100:
        raise RuntimeError(f"invalid provider output {d}")
    t = float(state[-1][0])
    a = np.asarray([r[:3] for r in snap], dtype=float)
    q = a[:, 0] / t
    f = a[:, 1] + a[:, 2]
    if not (np.all(np.isfinite(q)) and np.all(np.diff(q) > 0) and np.all(q > 0)):
        raise RuntimeError(f"invalid q grid {d}")
    if not (np.all(np.isfinite(f)) and np.all(f >= 0)):
        raise RuntimeError(f"invalid PSD {d}")
    peak = max(float(np.max(f)), 1e-300)
    return {
        "omega_wdm_h2": float(pv[3]),
        "final_T_MeV": t,
        "rows": int(len(q)),
        "q_min": float(q[0]),
        "q_max": float(q[-1]),
        "endpoint_to_peak": float(f[-1] / peak),
        "q": q,
        "f": f,
    }


def main(status_path: Path, generated: Path, stock: Path, profile: str, out: Path) -> None:
    status = json.loads(status_path.read_text())
    result = {
        "schema": "KMDSB.M25.ProviderMomentumSupportExtension.v1",
        "provider_pin": PIN,
        "preregistration": PREREG,
        "profile": profile,
        "status": status,
        "models": {},
        "K1_promoted": False,
        "K4_promoted": False,
        "physical_falsification": False,
    }
    if status.get("build_rc") != 0 or status.get("run_rc") != 0:
        result["classification"] = "M25_PROVIDER_MOMENTUM_SUPPORT_EXTENSION_PROVIDER_BLOCKED"
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return

    ok = True
    for name in MODEL_DIRS:
        try:
            n = model_metrics(generated, name)
            s = model_metrics(stock, name)
            mask = (s["q"] >= n["q"][0]) & (s["q"] <= n["q"][-1])
            qs = s["q"][mask]
            fs = s["f"][mask]
            fn = np.interp(qs, n["q"], n["f"])
            overlap_l2 = float(np.linalg.norm(fn - fs) / max(float(np.linalg.norm(fs)), 1e-300))
            qratio = float(n["q_max"] / s["q_max"])
            closure = abs(n["omega_wdm_h2"] - 0.1188)
            child_ok = bool(
                n["rows"] >= s["rows"] and
                qratio >= 1.25 and
                n["endpoint_to_peak"] < s["endpoint_to_peak"] and
                closure <= 5e-4
            )
            result["models"][name] = {
                "generated": {k:v for k,v in n.items() if k not in {"q","f"}},
                "stock": {k:v for k,v in s.items() if k not in {"q","f"}},
                "qmax_ratio_vs_stock": qratio,
                "closure_target_residual": closure,
                "overlap_shape_normalized_l2": overlap_l2,
                "extension_gate_pass": child_ok,
            }
            ok = ok and child_ok
        except Exception as exc:
            result["models"][name] = {"error": repr(exc), "extension_gate_pass": False}
            ok = False

    result["classification"] = (
        "M25_PROVIDER_MOMENTUM_SUPPORT_EXTENDED_WITH_STABLE_CLOSURE"
        if ok else "M25_PROVIDER_MOMENTUM_SUPPORT_EXTENSION_NOT_ESTABLISHED"
    )
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("status", type=Path)
    ap.add_argument("generated", type=Path)
    ap.add_argument("stock", type=Path)
    ap.add_argument("profile")
    ap.add_argument("out", type=Path)
    a = ap.parse_args()
    main(a.status, a.generated, a.stock, a.profile, a.out)
