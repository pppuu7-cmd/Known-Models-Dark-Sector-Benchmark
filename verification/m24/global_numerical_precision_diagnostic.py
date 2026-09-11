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
PREREG = "protocol/W04_M24_GLOBAL_NUMERICAL_PRECISION_DIAGNOSTIC_PREREGISTRATION_v0.1.md"
CASES = {"a18k": 18000.0, "a6k": 6000.0, "a1p8k": 1800.0}
ALLOWED_PROFILES = {"cl_permille", "cl_ref"}


def physical_lines(root: str, case: str) -> list[str]:
    lines = common(root)
    if case == "zero":
        lines += ["a_idm_dr = 0"]
    elif case in CASES:
        lines += [f"a_idm_dr = {CASES[case]:.12e}"]
    elif case != "ref":
        raise ValueError(case)
    return lines


def prepare(out: Path, profile: str) -> None:
    if profile not in ALLOWED_PROFILES:
        raise ValueError(profile)
    out.mkdir(parents=True, exist_ok=True)
    for branch in ["default", "profile"]:
        for case in ["ref", "zero"] + list(CASES):
            root = f"output/{branch}_{case}"
            (out / f"{branch}_{case}.ini").write_text("\n".join(physical_lines(root, case)) + "\n")
    manifest = {
        "schema": "KMDSB.M24.GlobalNumericalPrecisionDiagnostic.Manifest.v1",
        "class_pin": CLASS_PIN,
        "preregistration": PREREG,
        "profile": profile,
        "profile_file": f"{profile}.pre",
        "cases_Mpc^-1": CASES,
        "branches": ["default", "profile"],
        "physical_inputs_identical_between_branches": True,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def branch_metrics(root: Path, branch: str) -> dict:
    ref = tables(root, f"{branch}_ref")
    zero = tables(root, f"{branch}_zero")
    exact = metrics(zero, ref)
    responses = {case: metrics(tables(root, f"{branch}_{case}"), zero) for case in CASES}
    exc = {}
    for ch in ["TT", "EE", "TE"]:
        r6 = responses["a6k"][ch]["R2"]
        denom = max(responses["a18k"][ch]["R2"], responses["a1p8k"][ch]["R2"], 1e-300)
        exc[ch] = float(r6 / denom)
    return {
        "exact_zero_vs_omitted": exact,
        "exact_identity_pass": all(v["R2"] <= 1e-12 for v in exact.values()),
        "responses": responses,
        "excursion_factors": exc,
        "Emax": max(exc.values()),
    }


def analyze(root: Path, status_path: Path, profile: str, out: Path) -> None:
    if profile not in ALLOWED_PROFILES:
        raise ValueError(profile)
    status = json.loads(status_path.read_text())
    res = {
        "schema": "KMDSB.M24.GlobalNumericalPrecisionDiagnostic.v1",
        "class_pin": CLASS_PIN,
        "preregistration": PREREG,
        "precision_profile": profile,
        "status": status,
        "K1_promoted": False,
        "K4_promoted": False,
        "physical_falsification": False,
    }
    if any(v != 0 for v in status.values()):
        res["classification"] = "M24_GLOBAL_PRECISION_PROVIDER_BLOCKED"
        out.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")
        return

    d = branch_metrics(root, "default")
    p = branch_metrics(root, "profile")
    res["default"] = d
    res["profile"] = p
    direct = {}
    ratios = {}
    sensitive_channels = 0
    localized_channels = 0
    for ch in ["TT", "EE", "TE"]:
        direct[ch] = metrics(tables(root, f"profile_a6k"), tables(root, f"default_a6k"))[ch]
        rd = d["responses"]["a6k"][ch]["R2"]
        rp = p["responses"]["a6k"][ch]["R2"]
        ratio = max(rd, rp) / max(min(rd, rp), 1e-300)
        ratios[ch] = float(ratio)
        if rp <= rd / 5.0:
            localized_channels += 1
        if ratio >= 3.0:
            sensitive_channels += 1
    res["direct_profile_vs_default_a6k"] = direct
    res["a6k_response_ratios"] = ratios
    res["localized_channels"] = localized_channels
    res["sensitive_channels"] = sensitive_channels

    if d["Emax"] > 9.0 and p["Emax"] <= 3.0 and localized_channels >= 2:
        cls = "M24_GLOBAL_PRECISION_EXCURSION_LOCALIZED"
    else:
        er = max(d["Emax"], p["Emax"]) / max(min(d["Emax"], p["Emax"]), 1e-300)
        if er >= 3.0 or sensitive_channels >= 2:
            cls = "M24_GLOBAL_PRECISION_EXCURSION_STRONGLY_SENSITIVE"
        else:
            cls = "M24_GLOBAL_PRECISION_EXCURSION_INSENSITIVE"
    res["classification"] = cls
    out.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("prepare")
    p.add_argument("out", type=Path)
    p.add_argument("profile", choices=sorted(ALLOWED_PROFILES))
    a = sp.add_parser("analyze")
    a.add_argument("root", type=Path)
    a.add_argument("status", type=Path)
    a.add_argument("profile", choices=sorted(ALLOWED_PROFILES))
    a.add_argument("out", type=Path)
    args = ap.parse_args()
    if args.cmd == "prepare":
        prepare(args.out, args.profile)
    else:
        analyze(args.root, args.status, args.profile, args.out)
