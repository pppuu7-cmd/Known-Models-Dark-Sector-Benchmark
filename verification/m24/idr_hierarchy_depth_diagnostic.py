#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verification.m24.dark_tca_threshold_diagnostic import common, metrics, tables

CLASS_PIN = "e85808324f51fc694d12e3ed7439552a3c3f9540"
PREREG = "protocol/W04_M24_IDR_HIERARCHY_DEPTH_DIAGNOSTIC_PREREGISTRATION_v0.1.md"
PROFILES = ["D_L17", "L35", "L70"]
CASES = {"a18k": 18000.0, "a6k": 6000.0, "a1p8k": 1800.0}


def prepare(out: Path, pres: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    pres.mkdir(parents=True, exist_ok=True)
    (out / "ref.ini").write_text("\n".join(common("output/ref")) + "\n")
    (out / "zero.ini").write_text("\n".join(common("output/zero") + ["a_idm_dr = 0"]) + "\n")
    for name, a in CASES.items():
        (out / f"{name}.ini").write_text("\n".join(common(f"output/{name}") + [f"a_idm_dr = {a:.12e}"]) + "\n")
    (pres / "L35.pre").write_text("l_max_idr = 35\n")
    (pres / "L70.pre").write_text("l_max_idr = 70\n")
    manifest = {
        "schema": "KMDSB.M24.IDRHierarchyDepthDiagnostic.Manifest.v1",
        "class_pin": CLASS_PIN,
        "preregistration": PREREG,
        "cases_Mpc^-1": CASES,
        "profiles": {
            "D_L17": {"l_max_idr": 17, "provider_default": True},
            "L35": {"l_max_idr": 35},
            "L70": {"l_max_idr": 70},
        },
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def analyze(results: Path, status_path: Path, out: Path) -> None:
    status = json.loads(status_path.read_text())
    res = {
        "schema": "KMDSB.M24.IDRHierarchyDepthDiagnostic.v1",
        "class_pin": CLASS_PIN,
        "preregistration": PREREG,
        "K1_promoted": False,
        "physical_falsification": False,
        "status": status,
        "profiles": {},
        "direct_profile_vs_default": {},
    }
    if any(v != 0 for v in status.values()):
        res["classification"] = "M24_IDR_HIERARCHY_DIAGNOSTIC_PROVIDER_BLOCKED"
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

    droot = results / "D_L17"
    for profile in ["L35", "L70"]:
        proot = results / profile
        res["direct_profile_vs_default"][profile] = {}
        for case in ["ref", "zero"] + list(CASES):
            res["direct_profile_vs_default"][profile][case] = metrics(tables(proot, case), tables(droot, case))

    d = res["profiles"]["D_L17"]
    hi = res["profiles"]["L70"]
    localized_channels = 0
    sensitive_channels = 0
    ratios = {}
    for ch in ["TT", "EE", "TE"]:
        rd = d["responses"]["a6k"][ch]["R2"]
        rh = hi["responses"]["a6k"][ch]["R2"]
        ratio = max(rd, rh) / max(min(rd, rh), 1e-300)
        ratios[ch] = float(ratio)
        if rh <= rd / 5.0:
            localized_channels += 1
        if ratio >= 3.0:
            sensitive_channels += 1

    if d["Emax"] > 9.0 and hi["Emax"] <= 3.0 and localized_channels >= 2:
        cls = "M24_IDR_HIERARCHY_EXCURSION_LOCALIZED"
    else:
        e_ratio = max(d["Emax"], hi["Emax"]) / max(min(d["Emax"], hi["Emax"]), 1e-300)
        if e_ratio >= 3.0 or sensitive_channels >= 2:
            cls = "M24_IDR_HIERARCHY_EXCURSION_STRONGLY_SENSITIVE"
        else:
            cls = "M24_IDR_HIERARCHY_EXCURSION_INSENSITIVE"
    res["classification"] = cls
    res["localized_channels"] = localized_channels
    res["sensitive_channels"] = sensitive_channels
    res["a6k_L70_vs_L17_response_ratios"] = ratios
    out.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("prepare"); p.add_argument("cases", type=Path); p.add_argument("profiles", type=Path)
    a = sp.add_parser("analyze"); a.add_argument("results", type=Path); a.add_argument("status", type=Path); a.add_argument("out", type=Path)
    args = ap.parse_args()
    if args.cmd == "prepare":
        prepare(args.cases, args.profiles)
    else:
        analyze(args.results, args.status, args.out)
