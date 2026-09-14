#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import OrderedDict
from pathlib import Path

PIN = "e85808324f51fc694d12e3ed7439552a3c3f9540"
PROTOCOL = "protocol/W04_M21_CMB_PRECISION_STAGE3_SINGLE_PARAMETER_DECOMPOSITION_v0.1.md"

PARAMETERS = {
    "G1A__recfast_Nz0": ("G1A", "recfast_Nz0", "100000"),
    "G1A__tol_thermo_integration": ("G1A", "tol_thermo_integration", "1.e-5"),
    "G1A__recfast_x_He0_trigger_delta": ("G1A", "recfast_x_He0_trigger_delta", "0.01"),
    "G1A__recfast_x_H0_trigger_delta": ("G1A", "recfast_x_H0_trigger_delta", "0.01"),
    "G2B__l_logstep": ("G2B", "l_logstep", "1.026"),
    "G2B__l_linstep": ("G2B", "l_linstep", "25"),
    "G2B__hyper_sampling_flat": ("G2B", "hyper_sampling_flat", "12."),
    "G2B__hyper_sampling_curved_low_nu": ("G2B", "hyper_sampling_curved_low_nu", "10."),
    "G2B__hyper_sampling_curved_high_nu": ("G2B", "hyper_sampling_curved_high_nu", "10."),
    "G2B__hyper_nu_sampling_step": ("G2B", "hyper_nu_sampling_step", "10."),
    "G2B__hyper_phi_min_abs": ("G2B", "hyper_phi_min_abs", "1.e-10"),
    "G2B__hyper_x_tol": ("G2B", "hyper_x_tol", "1.e-4"),
    "G2B__hyper_flat_approximation_nu": ("G2B", "hyper_flat_approximation_nu", "1.e6"),
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
    ap.add_argument("parameter", choices=sorted(PARAMETERS))
    ap.add_argument("cl_permille", type=Path)
    ap.add_argument("ncdm_tight", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("manifest", type=Path)
    args = ap.parse_args()

    subgroup, key, value = PARAMETERS[args.parameter]
    values: OrderedDict[str, str] = OrderedDict()
    origin: dict[str, str] = {}
    conflicts = []

    def apply(source: str, items: list[tuple[str, str]]) -> None:
        for k, v in items:
            if k in values:
                conflicts.append({
                    "key": k,
                    "previous_value": values[k],
                    "previous_source": origin[k],
                    "final_value": v,
                    "final_source": source,
                })
            values[k] = v
            origin[k] = source

    apply("cl_permille.pre", parse(args.cl_permille))
    apply("m21_ncdm_tight.pre", parse(args.ncdm_tight))
    apply("frozen_common_control", [("evolver", "0")])
    apply(args.parameter, [(key, value)])

    conflict_keys = {x["key"] for x in conflicts}
    expected = {"hyper_flat_approximation_nu"} if args.parameter == "G2B__hyper_flat_approximation_nu" else set()
    if conflict_keys != expected:
        raise RuntimeError(f"{args.parameter}: conflict keys {sorted(conflict_keys)} != frozen expected {sorted(expected)}")
    if expected:
        x = conflicts[0]
        if x["previous_value"] != "7000." or x["final_value"] != "1.e6":
            raise RuntimeError(f"unexpected hyper_flat override: {x}")

    lines = [
        "# KMDSB M21 stage-3 single-parameter precision profile",
        f"# protocol: {PROTOCOL}",
        f"# provider: lesgourg/class_public@{PIN}",
        f"# parameter: {args.parameter}",
        f"# subgroup: {subgroup}",
    ]
    lines += [f"{k} = {v}" for k, v in values.items()]
    args.output.write_text("\n".join(lines) + "\n")

    reparsed = parse(args.output)
    keys = [k for k, _ in reparsed]
    if len(keys) != len(set(keys)):
        raise RuntimeError("serialized stage-3 profile has duplicate keys")
    if dict(reparsed).get(key) != value:
        raise RuntimeError("frozen stage-3 assignment missing after serialization")

    manifest = {
        "schema": "KMDSB.W04.M21.Stage3SingleParameterProfile.v0.1",
        "provider": f"lesgourg/class_public@{PIN}",
        "protocol": PROTOCOL,
        "parameter": args.parameter,
        "subgroup": subgroup,
        "parameter_key": key,
        "parameter_value": value,
        "cl_permille_sha256": sha256(args.cl_permille),
        "ncdm_tight_sha256": sha256(args.ncdm_tight),
        "output_sha256": sha256(args.output),
        "final_assignment_count": len(values),
        "duplicate_free_serialization": True,
        "expected_conflict_keys": sorted(expected),
        "observed_conflicts": conflicts,
        "stage3_assignment_count": 1,
    }
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "parameter": args.parameter,
        "subgroup": subgroup,
        "parameter_key": key,
        "parameter_value": value,
        "output_sha256": manifest["output_sha256"],
        "expected_conflict_keys": sorted(expected),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
