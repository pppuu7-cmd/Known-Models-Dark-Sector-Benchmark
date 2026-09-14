#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import OrderedDict
from pathlib import Path

PIN = "e85808324f51fc694d12e3ed7439552a3c3f9540"
RECOVERY = "protocol/W04_M21_CMB_PRECISION_COMPONENT_SERIALIZATION_RECOVERY_v0.2.md"

GROUPS = {
    "G1": [
        ("recfast_Nz0", "100000"),
        ("tol_thermo_integration", "1.e-5"),
        ("recfast_x_He0_trigger_delta", "0.01"),
        ("recfast_x_H0_trigger_delta", "0.01"),
        ("start_small_k_at_tau_c_over_tau_h", "0.0004"),
        ("start_large_k_at_tau_h_over_tau_k", "0.05"),
        ("tight_coupling_trigger_tau_c_over_tau_h", "0.005"),
        ("tight_coupling_trigger_tau_c_over_tau_k", "0.008"),
        ("start_sources_at_tau_c_over_tau_h", "0.006"),
        ("l_max_g", "50"),
        ("l_max_pol_g", "25"),
        ("l_max_ur", "50"),
        ("tol_perturbations_integration", "1.e-6"),
        ("perturbations_sampling_stepsize", "0.01"),
        ("radiation_streaming_approximation", "2"),
        ("radiation_streaming_trigger_tau_over_tau_k", "240."),
        ("radiation_streaming_trigger_tau_c_over_tau", "100."),
        ("ur_fluid_approximation", "2"),
        ("ur_fluid_trigger_tau_over_tau_k", "50."),
    ],
    "G2": [
        ("k_min_tau0", "0.002"),
        ("k_max_tau0_over_l_max", "3."),
        ("k_step_sub", "0.015"),
        ("k_step_super", "0.0001"),
        ("k_step_super_reduction", "0.1"),
        ("l_logstep", "1.026"),
        ("l_linstep", "25"),
        ("hyper_sampling_flat", "12."),
        ("hyper_sampling_curved_low_nu", "10."),
        ("hyper_sampling_curved_high_nu", "10."),
        ("hyper_nu_sampling_step", "10."),
        ("hyper_phi_min_abs", "1.e-10"),
        ("hyper_x_tol", "1.e-4"),
        ("hyper_flat_approximation_nu", "1.e6"),
        ("q_linstep", "0.20"),
        ("q_logstep_spline", "20."),
        ("q_logstep_trapzd", "0.5"),
        ("q_numstep_transition", "250"),
    ],
    "G3": [
        ("transfer_neglect_delta_k_S_t0", "100."),
        ("transfer_neglect_delta_k_S_t1", "100."),
        ("transfer_neglect_delta_k_S_t2", "100."),
        ("transfer_neglect_delta_k_S_e", "100."),
        ("neglect_CMB_sources_below_visibility", "1.e-30"),
        ("transfer_neglect_late_source", "3000."),
    ],
}

EXPECTED_CONFLICTS = {
    "G1": {"tol_perturbations_integration", "perturbations_sampling_stepsize"},
    "G2": {"hyper_flat_approximation_nu"},
    "G3": {
        "transfer_neglect_delta_k_S_t0",
        "transfer_neglect_delta_k_S_t1",
        "transfer_neglect_delta_k_S_t2",
        "transfer_neglect_delta_k_S_e",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse(path: Path) -> list[tuple[str, str]]:
    out = []
    for raw in path.read_text(errors="replace").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if "=" not in line:
            raise RuntimeError(f"unparsed non-comment line in {path}: {raw!r}")
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if not key or not value:
            raise RuntimeError(f"invalid assignment in {path}: {raw!r}")
        out.append((key, value))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("group", choices=sorted(GROUPS))
    ap.add_argument("cl_permille", type=Path)
    ap.add_argument("ncdm_tight", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("manifest", type=Path)
    args = ap.parse_args()

    values: OrderedDict[str, str] = OrderedDict()
    origin: dict[str, str] = {}
    conflicts = []

    def apply(source: str, items: list[tuple[str, str]]) -> None:
        for key, value in items:
            if key in values:
                conflicts.append({
                    "key": key,
                    "previous_value": values[key],
                    "previous_source": origin[key],
                    "final_value": value,
                    "final_source": source,
                })
            values[key] = value
            origin[key] = source

    apply("cl_permille.pre", parse(args.cl_permille))
    apply("m21_ncdm_tight.pre", parse(args.ncdm_tight))
    apply("frozen_common_control", [("evolver", "0")])
    apply(args.group, GROUPS[args.group])

    conflict_keys = {x["key"] for x in conflicts}
    expected = EXPECTED_CONFLICTS[args.group]
    if conflict_keys != expected:
        raise RuntimeError(f"{args.group}: conflict keys {sorted(conflict_keys)} != frozen expected {sorted(expected)}")

    if args.group == "G1":
        for x in conflicts:
            if x["key"] in expected and x["previous_value"] != x["final_value"]:
                raise RuntimeError(f"G1 identical-value deduplication changed value: {x}")
    if args.group == "G2":
        x = {z["key"]: z for z in conflicts}["hyper_flat_approximation_nu"]
        if x["previous_value"] != "7000." or x["final_value"] != "1.e6":
            raise RuntimeError(f"unexpected G2 override {x}")
    if args.group == "G3":
        expected_old = {
            "transfer_neglect_delta_k_S_t0": "0.17",
            "transfer_neglect_delta_k_S_t1": "0.05",
            "transfer_neglect_delta_k_S_t2": "0.17",
            "transfer_neglect_delta_k_S_e": "0.13",
        }
        for x in conflicts:
            if x["previous_value"] != expected_old[x["key"]] or x["final_value"] != "100.":
                raise RuntimeError(f"unexpected G3 override {x}")

    lines = [
        "# KMDSB M21 deterministic unique-key precision profile",
        f"# recovery: {RECOVERY}",
        f"# provider: lesgourg/class_public@{PIN}",
        f"# group: {args.group}",
    ]
    lines += [f"{k} = {v}" for k, v in values.items()]
    args.output.write_text("\n".join(lines) + "\n")

    reparsed = parse(args.output)
    keys = [k for k, _ in reparsed]
    if len(keys) != len(set(keys)):
        raise RuntimeError("serialized recovery profile still has duplicate keys")

    manifest = {
        "schema": "KMDSB.W04.M21.ComponentPrecisionProfileMerge.v0.2",
        "provider": f"lesgourg/class_public@{PIN}",
        "recovery_protocol": RECOVERY,
        "group": args.group,
        "cl_permille_sha256": sha256(args.cl_permille),
        "ncdm_tight_sha256": sha256(args.ncdm_tight),
        "output_sha256": sha256(args.output),
        "final_assignment_count": len(values),
        "duplicate_free_serialization": True,
        "expected_conflict_keys": sorted(expected),
        "observed_conflicts": conflicts,
        "final_assignments": dict(values),
    }
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "group": args.group,
        "final_assignment_count": len(values),
        "conflicts": conflicts,
        "output_sha256": manifest["output_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
