#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTOCOL = "protocol/W04_M21_CONDITIONAL_CMB_PRECISION_COMPONENT_DECOMPOSITION_v0.1.md"
PROVIDER = "lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540"
PARENT_EMAX = 534.8355868817356
ALLOWED_ACTIVATION = {
    "M21_FULL_CMB_REFERENCE_PRECISION_REMOVES_EXCURSION",
    "M21_FULL_CMB_REFERENCE_PRECISION_REDUCES_EXCURSION",
}
GROUPS = ["G1", "G2", "G3"]
CASES = ["ref", "f2", "f3", "f4"]
CHANNELS = ["TT", "EE", "TE"]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


INT = load_module("m21_integrator", HERE / "integrator_branch_diagnostic.py")
FULL = load_module("m21_full_reference", HERE / "full_cmb_reference_precision_diagnostic.py")


def read_meta(meta_root: Path, group: str) -> dict:
    out = {}
    d = meta_root / group.lower()
    for case in CASES:
        p = d / f"{case}.json"
        if not p.is_file():
            continue
        obj = json.loads(p.read_text())
        out[case] = obj
    return out


def group_result(root: Path, meta_root: Path, parent_rk: Path, group: str) -> dict:
    meta = read_meta(meta_root, group)
    evidence_ok = (
        set(meta) == set(CASES)
        and all(x.get("group") == group for x in meta.values())
        and all(x.get("provider_rc") == 0 and x.get("exact_head") is True for x in meta.values())
        and len({x.get("component_pre_sha256") for x in meta.values()}) == 1
        and len({x.get("base_cl_permille_sha256") for x in meta.values()}) == 1
        and len({x.get("ncdm_tight_sha256") for x in meta.values()}) == 1
    )

    finite_outputs = True
    profile = None
    ell_bands = None
    direct_parent = None
    try:
        for case in CASES:
            INT.files(root, case)
        profile = INT.response_profile(root)
        ell_bands = FULL.bands(root)
        direct_parent = FULL.direct(root, parent_rk)
    except Exception as exc:
        finite_outputs = False
        analysis_error = repr(exc)
    else:
        analysis_error = None

    excursion = profile["excursion_factors"] if profile is not None else {}
    if profile is not None:
        emax = max(float(excursion[ch]) for ch in CHANNELS)
    else:
        emax = None

    if not evidence_ok or not finite_outputs or emax is None:
        classification = "GROUP_BLOCKED"
    elif all(float(excursion[ch]) <= 3.0 for ch in CHANNELS):
        classification = "GROUP_REMOVES_EXCURSION"
    elif emax <= PARENT_EMAX / 3.0:
        classification = "GROUP_REDUCES_EXCURSION"
    else:
        classification = "GROUP_INSUFFICIENT"

    return {
        "group": group,
        "classification": classification,
        "evidence_ok": evidence_ok,
        "finite_outputs": finite_outputs,
        "analysis_error": analysis_error,
        "Emax_group": emax,
        "excursion_factors": excursion,
        "response_profile": profile,
        "ell_band_localization": ell_bands,
        "direct_group_vs_parent_RK_P2": direct_parent,
        "lane_meta": meta,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("components_root", type=Path)
    ap.add_argument("meta_root", type=Path)
    ap.add_argument("parent_rk", type=Path)
    ap.add_argument("activation_json", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()

    activation = json.loads(args.activation_json.read_text())
    activation_class = activation.get("classification")
    activation_ok = (
        activation_class in ALLOWED_ACTIVATION
        and activation.get("provider") == PROVIDER
        and activation.get("evidence_ok") is True
        and activation.get("finite_outputs") is True
    )

    groups = {
        g: group_result(args.components_root / g.lower(), args.meta_root, args.parent_rk, g)
        for g in GROUPS
    }

    blocked = [g for g, x in groups.items() if x["classification"] == "GROUP_BLOCKED"]
    sufficient = [
        g for g, x in groups.items()
        if x["classification"] in {"GROUP_REMOVES_EXCURSION", "GROUP_REDUCES_EXCURSION"}
    ]
    removes = [g for g, x in groups.items() if x["classification"] == "GROUP_REMOVES_EXCURSION"]
    reduces = [g for g, x in groups.items() if x["classification"] == "GROUP_REDUCES_EXCURSION"]

    if not activation_ok:
        classification = "M21_CMB_PRECISION_COMPONENT_DECOMPOSITION_NOT_AUTHORIZED"
    elif blocked:
        classification = "M21_CMB_REFERENCE_PRECISION_COMPONENT_DECOMPOSITION_BLOCKED"
    elif sufficient:
        classification = "M21_CMB_REFERENCE_PRECISION_COMPONENT_SUFFICIENCY_IDENTIFIED"
    else:
        classification = "M21_CMB_REFERENCE_PRECISION_INTERACTION_REQUIRED"

    result = {
        "schema": "KMDSB.W04.M21.CMBPrecisionComponentDecomposition.v0.1",
        "date": "2026-09-14",
        "protocol": PROTOCOL,
        "provider": PROVIDER,
        "activation_source_run": 34864827822,
        "activation_classification": activation_class,
        "activation_valid": activation_ok,
        "Emax_parent_RK_P2": PARENT_EMAX,
        "groups": groups,
        "blocked_groups": blocked,
        "sufficient_groups": sufficient,
        "groups_removing_excursion": removes,
        "groups_reducing_excursion": reduces,
        "classification": classification,
        "K1_promoted": False,
        "physical_falsification": False,
        "interpretation_ceiling": "Component sufficiency localizes numerical implementation sensitivity only. It does not prove a unique bug and does not promote K1.",
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "activation": activation_class,
        "classification": classification,
        "group_classes": {g: x["classification"] for g, x in groups.items()},
        "Emax": {g: x["Emax_group"] for g, x in groups.items()},
        "sufficient_groups": sufficient,
    }, indent=2, sort_keys=True))

    if classification in {
        "M21_CMB_PRECISION_COMPONENT_DECOMPOSITION_NOT_AUTHORIZED",
        "M21_CMB_REFERENCE_PRECISION_COMPONENT_DECOMPOSITION_BLOCKED",
    }:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
