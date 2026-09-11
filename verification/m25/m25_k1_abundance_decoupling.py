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

from verification.m25.m25_class_bridge import locate_generated, numeric_rows, params_values
from verification.m21.mixed_cold_warm_k1_reference import load_table, metric, resolve_output

CLASS_PIN = "e85808324f51fc694d12e3ed7439552a3c3f9540"
STERILE_PIN = "e4486265e8207aa0dd28decc8c8d897266c0a52a"
PREREG = "protocol/W04_M25_RESONANT_STERILE_K1_ABUNDANCE_DECOUPLING_PREREGISTRATION_v0.1.md"
NF = (4.0 / 11.0) ** (1.0 / 3.0)
ETAS = [0.10, 0.03, 0.01, 0.003, 0.001]
OMEGA_DM = 0.1188
MASS_EV = 7115.0
MODEL_DIRS = [
    "ms7.115E-03s24.000E-11L2.971E-03",
    "ms7.115E-03s28.000E-12L4.849E-03",
]
BASE_CLASS_OMEGA = {
    MODEL_DIRS[0]: 0.1188179433088504,
    MODEL_DIRS[1]: 0.11893069791315644,
}


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
        "h = 0.675",
        "omega_b = 0.0222",
        f"omega_cdm = {omega_cdm:.17g}",
        "N_ur = 3.046",
        "Omega_k = 0",
        "Omega_fld = 0",
        "Omega_scf = 0",
        "YHe = 0.24",
        "T_cmb = 2.7255",
        "A_s = 2.1e-9",
        "n_s = 0.965",
        "k_pivot = 0.05",
        "tau_reio = 0.054",
        "P_k_max_h/Mpc = 20",
        "z_pk = 0",
        "l_max_scalars = 2500",
    ]


def prepare(upstream: Path, out: Path) -> None:
    generated = locate_generated(upstream)
    out.mkdir(parents=True, exist_ok=True)
    psddir = out / "psd"
    psddir.mkdir(parents=True, exist_ok=True)

    ref = common_ini("output/ref_", OMEGA_DM) + ["N_ncdm = 0"]
    (out / "ref.ini").write_text("\n".join(ref) + "\n")
    manifest = {
        "schema": "KMDSB.M25.K1AbundanceDecoupling.Manifest.v1",
        "class_pin": CLASS_PIN,
        "sterile_provider_pin": STERILE_PIN,
        "preregistration": PREREG,
        "etas": ETAS,
        "omega_dm_ref": OMEGA_DM,
        "models": {},
    }

    for mi, name in enumerate(MODEL_DIRS):
        d = generated / name
        pfile, sfile, snapfile = d / "params.dat", d / "state.dat", d / "Snapshot100.dat"
        pv = params_values(pfile)
        st = numeric_rows(sfile)
        snap = numeric_rows(snapfile)
        if len(pv) < 6 or not st or len(snap) < 100:
            raise RuntimeError(f"invalid upstream products for {name}")
        tfinal = float(st[-1][0])
        if abs(tfinal - 10.0) / 10.0 > 1e-10:
            raise RuntimeError(f"final T mismatch for {name}: {tfinal}")
        a = np.asarray([r[:3] for r in snap], dtype=float)
        q = a[:, 0] / tfinal
        fbase = (a[:, 1] + a[:, 2]) / (2.0 * math.pi) ** 3
        if not (np.all(np.isfinite(q)) and np.all(q > 0) and np.all(np.diff(q) > 0)):
            raise RuntimeError(f"invalid q for {name}")
        if not (np.all(np.isfinite(fbase)) and np.all(fbase >= 0)):
            raise RuntimeError(f"invalid fbase for {name}")
        mkey = f"m{mi}"
        manifest["models"][mkey] = {
            "provider_directory": name,
            "provider_omega_wdm_h2": float(pv[3]),
            "base_class_omega_h2": BASE_CLASS_OMEGA[name],
            "final_T_MeV": tfinal,
            "q_min": float(q.min()),
            "q_max": float(q.max()),
            "cases": {},
        }
        for i, eta in enumerate(ETAS):
            f = eta * fbase
            psd = psddir / f"{mkey}_e{i}.dat"
            np.savetxt(psd, np.column_stack([q, f]), fmt="%.17e")
            omega_cdm = OMEGA_DM - eta * BASE_CLASS_OMEGA[name]
            if omega_cdm <= 0:
                raise RuntimeError(f"non-positive omega_cdm for {name}, eta={eta}")
            lines = common_ini(f"output/{mkey}_e{i}_", omega_cdm) + [
                "N_ncdm = 1",
                "use_ncdm_psd_files = 1",
                f"ncdm_psd_filenames = ../m25_k1_cases/psd/{mkey}_e{i}.dat",
                f"m_ncdm = {MASS_EV:.17g}",
                f"T_ncdm = {NF:.17g}",
                "deg_ncdm = 1",
            ]
            (out / f"{mkey}_e{i}.ini").write_text("\n".join(lines) + "\n")
            manifest["models"][mkey]["cases"][f"e{i}"] = {
                "eta": eta,
                "omega_cdm": omega_cdm,
                "expected_ncdm_h2": eta * BASE_CLASS_OMEGA[name],
                "expected_total_dm_h2": OMEGA_DM,
            }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def channel(a: np.ndarray, col: int) -> np.ndarray:
    if col >= a.shape[1]:
        raise RuntimeError(f"missing channel {col} in {a.shape}")
    return a[:, [0, col]]


def judge(points: list[dict]) -> dict:
    r95 = [p["p95_abs"] for p in points]
    monotonic = all(r95[i + 1] <= r95[i] * 1.02 for i in range(len(r95) - 1))
    decreased = r95[-1] < r95[0]
    f = np.asarray(ETAS[-3:], dtype=float)
    r = np.asarray(r95[-3:], dtype=float)
    if np.any(r <= 0):
        fit = {"valid": False, "p": None}
        exponent = False
    else:
        p, logA = np.polyfit(np.log(f), np.log(r), 1)
        fit = {"valid": True, "p": float(p), "logA": float(logA)}
        exponent = bool(p > 0.5)
    return {
        "points": points,
        "r95": r95,
        "monotonic_with_2pct_slack": monotonic,
        "smallest_lower_than_largest": decreased,
        "fit_smallest3": fit,
        "pass": bool(monotonic and decreased and exponent),
    }


def analyze(root: Path, status_path: Path, manifest_path: Path, out: Path) -> None:
    status = json.loads(status_path.read_text())
    manifest = json.loads(manifest_path.read_text())
    result = {
        "schema": "KMDSB.M25.K1AbundanceDecoupling.v1",
        "class_pin": CLASS_PIN,
        "sterile_provider_pin": STERILE_PIN,
        "preregistration": PREREG,
        "etas": ETAS,
        "omega_dm_ref": OMEGA_DM,
        "K1_reference_limit": "NOT_PROMOTED",
        "K2_physical_geometry": "ONE_SIDED_ETA_GE_0",
        "K4_promoted": False,
        "physical_falsification": False,
        "status": status,
        "models": {},
    }
    required = ["build", "ref"] + [f"m{m}_e{i}" for m in range(2) for i in range(len(ETAS))]
    if any(status.get(k) != 0 for k in required):
        result["classification"] = "M25_K1_ABUNDANCE_DECOUPLING_PROVIDER_BLOCKED"
        result["failed_status_keys"] = [k for k in required if status.get(k) != 0]
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return

    ref_cl = load_table(resolve_output(root, "ref", "cl"))
    ref_pk = load_table(resolve_output(root, "ref", "pk"))
    ref_bg_raw = load_table(resolve_output(root, "ref", "background"))
    ref_bg = ref_bg_raw[:, [0, 3]]
    all_pass = True

    for mi in range(2):
        finite = []
        for i in range(len(ETAS)):
            prefix = f"m{mi}_e{i}"
            cl = load_table(resolve_output(root, prefix, "cl"))
            pk = load_table(resolve_output(root, prefix, "pk"))
            bg = load_table(resolve_output(root, prefix, "background"))[:, [0, 3]]
            finite.append({"cl": cl, "pk": pk, "bg": bg})
        specs = {
            "H": ([x["bg"] for x in finite], ref_bg),
            "Pk": ([x["pk"] for x in finite], ref_pk),
            "CMB_TT": ([channel(x["cl"], 1) for x in finite], channel(ref_cl, 1)),
            "CMB_EE": ([channel(x["cl"], 2) for x in finite], channel(ref_cl, 2)),
            "CMB_TE": ([channel(x["cl"], 3) for x in finite], channel(ref_cl, 3)),
        }
        model_result = {
            "provider_directory": manifest["models"][f"m{mi}"]["provider_directory"],
            "blocks": {},
        }
        for block, (models, ref) in specs.items():
            pts = []
            for eta, arr in zip(ETAS, models):
                q = metric(arr, ref)
                q["eta"] = eta
                pts.append(q)
            model_result["blocks"][block] = judge(pts)
            all_pass = all_pass and model_result["blocks"][block]["pass"]
        model_result["failing_blocks"] = [k for k, v in model_result["blocks"].items() if not v["pass"]]
        result["models"][f"m{mi}"] = model_result

    if all_pass:
        result["classification"] = "M25_K1_ABUNDANCE_DECOUPLING_PASS_WITH_SCOPE"
        result["K1_reference_limit"] = "PASS_WITH_SCOPE_ABUNDANCE_TO_ZERO_MIXED_CDM_EMBEDDING"
    else:
        result["classification"] = "M25_K1_ABUNDANCE_DECOUPLING_NOT_ESTABLISHED"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("prepare"); p.add_argument("upstream", type=Path); p.add_argument("out", type=Path)
    a = sp.add_parser("analyze"); a.add_argument("root", type=Path); a.add_argument("status", type=Path); a.add_argument("manifest", type=Path); a.add_argument("out", type=Path)
    args = ap.parse_args()
    if args.cmd == "prepare":
        prepare(args.upstream, args.out)
    else:
        analyze(args.root, args.status, args.manifest, args.out)
