#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import sympy as sp


SCHEMA = "KMDSB.W03.M13b.K3B0EinsteinTraceAudit.v0.1"
PROTOCOL = "protocol/W03_M13B_K3B0_EINSTEIN_TRACE_CONVENTION_AUDIT_v0.1.md"


def main(output):
    tau = sp.symbols("tau", positive=True, finite=True)
    Phi = sp.symbols("Phi", nonzero=True, finite=True)
    G, a, dp = sp.symbols("G a dp", finite=True)

    Hc = sp.Rational(2, 1) / tau
    Hcp = -sp.Rational(2, 1) / tau**2

    standard_coeff = sp.simplify(2 * Hcp + Hc**2)
    published_literal_coeff = sp.simplify(2 * Hcp - Hc**2)

    # Matter-era growing mode: Phi is constant and delta_p=0.
    standard_matter_residual = sp.simplify(standard_coeff * Phi)
    published_literal_matter_residual = sp.simplify(published_literal_coeff * Phi)

    standard_rhs_prefactor = 4 * sp.pi * G * a**2
    published_literal_rhs_prefactor = sp.Rational(4, 3) * sp.pi * G * a**2
    rhs_ratio = sp.simplify(published_literal_rhs_prefactor / standard_rhs_prefactor)

    checks = {
        "matter_background_Hc": sp.simplify(Hc - 2 / tau) == 0,
        "matter_background_Hc_prime": sp.simplify(Hcp + 2 / tau**2) == 0,
        "standard_trace_coefficient_vanishes": standard_coeff == 0,
        "standard_constant_Phi_matter_residual_zero": standard_matter_residual == 0,
        "published_literal_trace_coefficient_is_minus_8_over_tau2": sp.simplify(published_literal_coeff + 8 / tau**2) == 0,
        "published_literal_constant_Phi_matter_residual_nonzero": published_literal_matter_residual != 0,
        "published_literal_rhs_is_one_third_standard_pressure_prefactor": rhs_ratio == sp.Rational(1, 3),
    }
    all_pass = all(bool(x) for x in checks.values())
    classification = (
        "M13B_K3B0_PUBLISHED_EINSTEIN_TRACE_FORM_NOT_LITERAL_IMPLEMENTATION_AUTHORITY"
        if all_pass
        else "M13B_K3B0_TRACE_AUDIT_NOT_ESTABLISHED"
    )

    result = {
        "schema": SCHEMA,
        "model_id": "M13b",
        "family_id": "F13",
        "gate": "K3B0",
        "protocol": PROTOCOL,
        "classification": classification,
        "all_required_checks_pass": all_pass,
        "checks": checks,
        "matter_era_probe": {
            "Hc": str(Hc),
            "Hc_prime": str(Hcp),
            "standard_trace_coefficient": str(standard_coeff),
            "published_literal_trace_coefficient": str(published_literal_coeff),
            "standard_constant_Phi_residual": str(standard_matter_residual),
            "published_literal_constant_Phi_residual": str(published_literal_matter_residual),
            "published_to_standard_delta_p_prefactor_ratio": str(rhs_ratio),
        },
        "interpretation": (
            "The literal printed trace equation cannot be used as independent numerical authority under the stated physical-pressure interpretation because it fails the pressureless matter-era constant-potential limit. This establishes a reproduction/convention ambiguity only; it does not establish a physical failure and does not determine what the nonpublic author code implemented."
            if all_pass
            else "The preregistered trace-convention distinction was not reproduced; no K3B1 authorization follows."
        ),
        "original_provider_reproduced": False,
        "K3_state_ceiling": "PARTIAL",
        "K4_promoted": False,
        "K5_promoted": False,
        "physical_falsification": False,
        "next_authorized_gate": (
            "K3B1_INDEPENDENT_STANDARD_GR_TWO_FIELD_DYNAMICAL_EMBEDDING"
            if all_pass
            else "NONE"
        ),
    }
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    args = p.parse_args()
    main(args.output)
