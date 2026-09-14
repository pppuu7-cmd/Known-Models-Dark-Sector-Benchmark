#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTOCOL = "protocol/W04_M21_CONDITIONAL_CMB_PRECISION_STAGE2_SUBGROUP_DECOMPOSITION_v0.1.md"
PROVIDER = "lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540"
PARENT_EMAX = 534.8355868817356
SUFFICIENT_PARENT = {"GROUP_REMOVES_EXCURSION", "GROUP_REDUCES_EXCURSION"}
PARENT_TO_SUBGROUPS = {
    "G1": ["G1A", "G1B", "G1C"],
    "G2": ["G2A", "G2B", "G2C"],
    "G3": ["G3A", "G3B"],
}
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


def read_meta(meta_root: Path, subgroup: str) -> dict:
    out = {}
    d = meta_root / subgroup.lower()
    for case in CASES:
        p = d / f"{case}.json"
        if p.is_file():
            out[case] = json.loads(p.read_text())
    return out


def subgroup_result(root: Path, meta_root: Path, subgroup: str) -> dict:
    meta = read_meta(meta_root, subgroup)
    expected_parent = subgroup[:2]
    evidence_ok = (
        set(meta) == set(CASES)
        and all(x.get("subgroup") == subgroup for x in meta.values())
        and all(x.get("parent_group") == expected_parent for x in meta.values())
        and all(x.get("provider_rc") == 0 and x.get("exact_head") is True for x in meta.values())
        and all(x.get("duplicate_free_serialization") is True for x in meta.values())
        and all(x.get("observed_conflict_keys") == x.get("expected_conflict_keys") for x in meta.values())
        and len({x.get("stage2_pre_sha256") for x in meta.values()}) == 1
        and len({x.get("merge_manifest_sha256") for x in meta.values()}) == 1
        and len({x.get("base_cl_permille_sha256") for x in meta.values()}) == 1
        and len({x.get("ncdm_tight_sha256") for x in meta.values()}) == 1
    )

    finite_outputs = True
    profile = None
    try:
        for case in CASES:
            INT.files(root, case)
        profile = INT.response_profile(root)
    except Exception as exc:
        finite_outputs = False
        analysis_error = repr(exc)
    else:
        analysis_error = None

    excursion = profile["excursion_factors"] if profile is not None else {}
    emax = max((float(excursion[ch]) for ch in CHANNELS), default=None)

    if not evidence_ok or not finite_outputs or emax is None:
        classification = "SUBGROUP_BLOCKED"
    elif all(float(excursion[ch]) <= 3.0 for ch in CHANNELS):
        classification = "SUBGROUP_REMOVES_EXCURSION"
    elif emax <= PARENT_EMAX / 3.0:
        classification = "SUBGROUP_REDUCES_EXCURSION"
    else:
        classification = "SUBGROUP_INSUFFICIENT"

    return {
        "subgroup": subgroup,
        "parent_group": expected_parent,
        "classification": classification,
        "evidence_ok": evidence_ok,
        "finite_outputs": finite_outputs,
        "analysis_error": analysis_error,
        "Emax_subgroup": emax,
        "excursion_factors": excursion,
        "response_profile": profile,
        "lane_meta": meta,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("products_root", type=Path)
    ap.add_argument("meta_root", type=Path)
    ap.add_argument("parent_aggregate", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()

    parent = json.loads(args.parent_aggregate.read_text())
    parent_groups = parent.get("groups", {})
    parent_valid = (
        parent.get("provider") == PROVIDER
        and parent.get("classification") == "M21_CMB_REFERENCE_PRECISION_COMPONENT_SUFFICIENCY_IDENTIFIED"
        and isinstance(parent_groups, dict)
    )

    activated_parents = [
        g for g in ("G1", "G2", "G3")
        if parent_groups.get(g, {}).get("classification") in SUFFICIENT_PARENT
    ]
    activated_subgroups = [sg for g in activated_parents for sg in PARENT_TO_SUBGROUPS[g]]

    present_dirs = {
        p.name.upper() for p in args.products_root.iterdir() if p.is_dir()
    } if args.products_root.is_dir() else set()
    unexpected = sorted(present_dirs - set(activated_subgroups))
    missing = sorted(set(activated_subgroups) - present_dirs)

    results = {}
    if parent_valid and not unexpected and not missing:
        for subgroup in activated_subgroups:
            results[subgroup] = subgroup_result(
                args.products_root / subgroup.lower(), args.meta_root, subgroup
            )

    parent_stage2 = {}
    any_blocked = False
    for group in activated_parents:
        expected = PARENT_TO_SUBGROUPS[group]
        group_results = [results.get(sg) for sg in expected]
        if any(x is None for x in group_results):
            cls = f"{group}_STAGE2_BLOCKED"
            sufficient = []
        else:
            blocked = [x["subgroup"] for x in group_results if x["classification"] == "SUBGROUP_BLOCKED"]
            sufficient = [
                x["subgroup"] for x in group_results
                if x["classification"] in {"SUBGROUP_REMOVES_EXCURSION", "SUBGROUP_REDUCES_EXCURSION"}
            ]
            if blocked:
                cls = f"{group}_STAGE2_BLOCKED"
            elif sufficient:
                cls = f"{group}_STAGE2_SUBGROUP_SUFFICIENCY_IDENTIFIED"
            else:
                cls = f"{group}_STAGE2_WITHIN_GROUP_INTERACTION_REQUIRED"
        any_blocked |= cls.endswith("_BLOCKED")
        parent_stage2[group] = {
            "classification": cls,
            "sufficient_subgroups": sufficient,
            "required_subgroups": expected,
        }

    if not parent_valid:
        classification = "M21_CMB_PRECISION_STAGE2_NOT_AUTHORIZED"
    elif unexpected or missing or any_blocked:
        classification = "M21_CMB_PRECISION_STAGE2_BLOCKED"
    else:
        classification = "M21_CMB_PRECISION_STAGE2_COMPLETE"

    result = {
        "schema": "KMDSB.W04.M21.CMBPrecisionStage2SubgroupDecomposition.v0.1",
        "date": "2026-09-14",
        "protocol": PROTOCOL,
        "provider": PROVIDER,
        "parent_aggregate_classification": parent.get("classification"),
        "parent_valid": parent_valid,
        "activated_parents": activated_parents,
        "activated_subgroups": activated_subgroups,
        "unexpected_subgroup_products": unexpected,
        "missing_subgroup_products": missing,
        "Emax_parent_RK": PARENT_EMAX,
        "subgroups": results,
        "parent_stage2": parent_stage2,
        "classification": classification,
        "K1_promoted": False,
        "physical_falsification": False,
        "interpretation_ceiling": "Stage-2 subgroup sufficiency narrows a numerical module family only. It does not prove a unique bug, does not authorize single-parameter tuning, and does not promote K1/K3/K4.",
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "classification": classification,
        "activated_parents": activated_parents,
        "parent_stage2": parent_stage2,
        "subgroup_classes": {k: v["classification"] for k, v in results.items()},
        "Emax": {k: v["Emax_subgroup"] for k, v in results.items()},
    }, indent=2, sort_keys=True))

    if classification in {"M21_CMB_PRECISION_STAGE2_NOT_AUTHORIZED", "M21_CMB_PRECISION_STAGE2_BLOCKED"}:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
