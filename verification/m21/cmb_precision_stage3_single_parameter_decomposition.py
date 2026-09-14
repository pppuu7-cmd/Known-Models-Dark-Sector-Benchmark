#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTOCOL = "protocol/W04_M21_CMB_PRECISION_STAGE3_SINGLE_PARAMETER_DECOMPOSITION_v0.1.md"
PROVIDER = "lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540"
PARENT_EMAX = 534.8355868817356
CHANNELS = ["TT", "EE", "TE"]
PARAMETERS = {
    "G1A": [
        "G1A__recfast_Nz0",
        "G1A__tol_thermo_integration",
        "G1A__recfast_x_He0_trigger_delta",
        "G1A__recfast_x_H0_trigger_delta",
    ],
    "G2B": [
        "G2B__l_logstep",
        "G2B__l_linstep",
        "G2B__hyper_sampling_flat",
        "G2B__hyper_sampling_curved_low_nu",
        "G2B__hyper_sampling_curved_high_nu",
        "G2B__hyper_nu_sampling_step",
        "G2B__hyper_phi_min_abs",
        "G2B__hyper_x_tol",
        "G2B__hyper_flat_approximation_nu",
    ],
}
ALL = [p for xs in PARAMETERS.values() for p in xs]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


INT = load_module("m21_integrator", HERE / "integrator_branch_diagnostic.py")


def parameter_result(root: Path, parameter: str) -> dict:
    meta_path = root / "lane_meta.json"
    meta = json.loads(meta_path.read_text()) if meta_path.is_file() else {}
    expected_subgroup = parameter.split("__", 1)[0]
    evidence_ok = (
        meta.get("parameter") == parameter
        and meta.get("subgroup") == expected_subgroup
        and meta.get("exact_head") is True
        and meta.get("all_cases_rc0") is True
        and meta.get("duplicate_free_serialization") is True
        and meta.get("stage3_assignment_count") == 1
        and meta.get("observed_conflict_keys") == meta.get("expected_conflict_keys")
        and set(meta.get("ini_sha256", {})) == {"ref", "f2", "f3", "f4"}
    )
    profile = None
    try:
        profile = INT.response_profile(root / "output")
    except Exception as exc:
        analysis_error = repr(exc)
    else:
        analysis_error = None
    excursion = profile["excursion_factors"] if profile is not None else {}
    emax = max((float(excursion[ch]) for ch in CHANNELS), default=None)
    if not evidence_ok or profile is None or emax is None:
        classification = "PARAMETER_BLOCKED"
    elif all(float(excursion[ch]) <= 3.0 for ch in CHANNELS):
        classification = "PARAMETER_REMOVES_EXCURSION"
    elif emax <= PARENT_EMAX / 3.0:
        classification = "PARAMETER_REDUCES_EXCURSION"
    else:
        classification = "PARAMETER_INSUFFICIENT"
    return {
        "parameter": parameter,
        "subgroup": expected_subgroup,
        "parameter_key": meta.get("parameter_key"),
        "parameter_value": meta.get("parameter_value"),
        "classification": classification,
        "evidence_ok": evidence_ok,
        "analysis_error": analysis_error,
        "Emax_parameter": emax,
        "excursion_factors": excursion,
        "response_profile": profile,
        "lane_meta": meta,
    }


def main(components: Path, parent_path: Path, out: Path) -> None:
    parent = json.loads(parent_path.read_text())
    parent_valid = (
        parent.get("provider") == PROVIDER
        and parent.get("classification") == "M21_CMB_PRECISION_STAGE2_COMPLETE"
        and parent.get("subgroups", {}).get("G1A", {}).get("classification") == "SUBGROUP_REMOVES_EXCURSION"
        and parent.get("subgroups", {}).get("G2B", {}).get("classification") == "SUBGROUP_REDUCES_EXCURSION"
    )

    dirs = {}
    if components.is_dir():
        for p in components.iterdir():
            if p.is_dir() and p.name.startswith("m21-stage3-"):
                dirs[p.name[len("m21-stage3-"):]] = p
    present = sorted(dirs)
    missing = sorted(set(ALL) - set(present))
    unexpected = sorted(set(present) - set(ALL))

    results = {}
    if parent_valid and not missing and not unexpected:
        for parameter in ALL:
            results[parameter] = parameter_result(dirs[parameter], parameter)

    # Cross-lane identity: physical INI files and common baselines must be identical.
    identity_ok = bool(results)
    for case in ("ref", "f2", "f3", "f4"):
        hashes = {r["lane_meta"].get("ini_sha256", {}).get(case) for r in results.values()}
        identity_ok &= len(hashes) == 1 and None not in hashes
    for key in ("base_cl_permille_sha256", "ncdm_tight_sha256"):
        hashes = {r["lane_meta"].get(key) for r in results.values()}
        identity_ok &= len(hashes) == 1 and None not in hashes

    subgroup_stage3 = {}
    any_blocked = not parent_valid or bool(missing or unexpected) or not identity_ok
    for subgroup, parameters in PARAMETERS.items():
        rs = [results.get(p) for p in parameters]
        blocked = [r["parameter"] for r in rs if r is not None and r["classification"] == "PARAMETER_BLOCKED"]
        sufficient = [
            r["parameter"] for r in rs if r is not None and r["classification"] in {"PARAMETER_REMOVES_EXCURSION", "PARAMETER_REDUCES_EXCURSION"}
        ]
        if any(r is None for r in rs) or blocked:
            cls = f"{subgroup}_STAGE3_BLOCKED"
            any_blocked = True
        elif sufficient:
            cls = f"{subgroup}_STAGE3_SINGLE_PARAMETER_SUFFICIENCY_IDENTIFIED"
        else:
            cls = f"{subgroup}_STAGE3_WITHIN_SUBGROUP_INTERACTION_REQUIRED"
        subgroup_stage3[subgroup] = {
            "classification": cls,
            "required_parameters": parameters,
            "sufficient_parameters": sufficient,
            "blocked_parameters": blocked,
        }

    classification = "M21_CMB_PRECISION_STAGE3_BLOCKED" if any_blocked else "M21_CMB_PRECISION_STAGE3_COMPLETE"
    result = {
        "schema": "KMDSB.W04.M21.CMBPrecisionStage3SingleParameterDecomposition.v0.1",
        "date": "2026-09-14",
        "protocol": PROTOCOL,
        "provider": PROVIDER,
        "parent_valid": parent_valid,
        "parent_classification": parent.get("classification"),
        "Emax_parent_RK": PARENT_EMAX,
        "required_parameters": ALL,
        "missing_parameter_products": missing,
        "unexpected_parameter_products": unexpected,
        "cross_lane_input_identity": identity_ok,
        "parameters": results,
        "subgroup_stage3": subgroup_stage3,
        "classification": classification,
        "K1_promoted": False,
        "physical_falsification": False,
        "interpretation_ceiling": "Single-parameter sufficiency is a scoped numerical localization only. It does not prove a code bug or unique cause, does not authorize tuning, and does not promote K1/K3/K4 or physically falsify mixed dark matter.",
    }
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "classification": classification,
        "cross_lane_input_identity": identity_ok,
        "subgroup_stage3": subgroup_stage3,
        "parameter_classes": {p:r["classification"] for p,r in results.items()},
        "Emax": {p:r["Emax_parameter"] for p,r in results.items()},
    }, indent=2, sort_keys=True))
    if classification == "M21_CMB_PRECISION_STAGE3_BLOCKED":
        raise SystemExit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: cmb_precision_stage3_single_parameter_decomposition.py COMPONENTS PARENT.json OUT.json")
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
