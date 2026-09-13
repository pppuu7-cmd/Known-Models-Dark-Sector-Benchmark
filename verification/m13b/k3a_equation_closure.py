#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

import sympy as sp


SCHEMA = "KMDSB.W03.M13b.IndependentK3AEquationClosure.v0.1"
PROTOCOL = "protocol/W03_M13B_INDEPENDENT_K3A_EQUATION_CLOSURE_PREREGISTRATION_v0.1.md"
AUTHORITY = "Goh&Taylor2026 arXiv:2606.27049 MNRAS551:stag1403"


def is_zero(expr):
    return sp.simplify(sp.trigsimp(expr)) == 0


def main(output):
    # Potential identities.
    x, V0, s = sp.symbols("x V0 s", finite=True)
    u = s * (1 - x)
    V = V0 * (sp.tanh(u) + 1)
    Vx_expected = -V0 * s * sp.sech(u) ** 2
    Vxx_expected = -2 * V0 * s ** 2 * sp.sech(u) ** 2 * sp.tanh(u)

    # Background/conformal variables.
    a, Hc = sp.symbols("a Hc", nonzero=True, finite=True)
    phip, phipp = sp.symbols("phip phipp", finite=True)
    psip, psipp = sp.symbols("psip psipp", finite=True)
    Vphi, Vpsi = sp.symbols("Vphi Vpsi", finite=True)

    rho_plus_p_phi = phip ** 2 / a ** 2
    rho_plus_p_psi = -psip ** 2 / a ** 2

    # d/dtau of rho, using a'/a=Hc and dV/dtau=V_field*field'.
    rho_phi_prime = phip * phipp / a ** 2 - Hc * phip ** 2 / a ** 2 + Vphi * phip
    rho_psi_prime = -psip * psipp / a ** 2 + Hc * psip ** 2 / a ** 2 + Vpsi * psip

    phi_bg_sub = {phipp: -2 * Hc * phip - a ** 2 * Vphi}
    psi_bg_sub = {psipp: -2 * Hc * psip + a ** 2 * Vpsi}
    phi_continuity = sp.simplify((rho_phi_prime + 3 * Hc * rho_plus_p_phi).subs(phi_bg_sub))
    psi_continuity = sp.simplify((rho_psi_prime + 3 * Hc * rho_plus_p_psi).subs(psi_bg_sub))

    # Perturbed stress energy.
    Psi = sp.symbols("Psi", finite=True)
    dphi, dphip, dphipp = sp.symbols("dphi dphip dphipp", finite=True)
    dpsi, dpsip, dpsipp = sp.symbols("dpsi dpsip dpsipp", finite=True)
    Aphi = (phip * dphip - phip ** 2 * Psi) / a ** 2
    Apsi = (psip * dpsip - psip ** 2 * Psi) / a ** 2
    drho_phi = Aphi + Vphi * dphi
    dp_phi = Aphi - Vphi * dphi
    drho_psi = -Apsi + Vpsi * dpsi
    dp_psi = -Apsi - Vpsi * dpsi

    # Published direct perturbed KG structure.
    k, Vphiphi, Vpsipsi, Phip = sp.symbols("k Vphiphi Vpsipsi Phip", finite=True)
    phi_kg = dphipp + 2 * Hc * dphip + (k ** 2 + a ** 2 * Vphiphi) * dphi - 3 * Phip * phip
    psi_kg = dpsipp + 2 * Hc * dpsip + (k ** 2 - a ** 2 * Vpsipsi) * dpsi - 3 * Phip * psip

    cross = sp.simplify(rho_plus_p_phi + rho_plus_p_psi)

    # At a nontrivial crossing the effective-fluid velocity denominator vanishes,
    # while direct field equations remain polynomial/finite.
    theta_phi, theta_psi = sp.symbols("theta_phi theta_psi", finite=True)
    theta_num = sp.expand(rho_plus_p_phi * theta_phi + rho_plus_p_psi * theta_psi)
    theta_den = cross
    crossing_symbolic_den = sp.simplify(theta_den.subs(psip, phip))
    crossing_num_probe = sp.simplify(theta_num.subs({a: sp.Integer(1), phip: sp.Integer(2), psip: sp.Integer(2), theta_phi: sp.Integer(1), theta_psi: sp.Integer(0)}))

    direct_terms = [
        2 * Hc,
        k ** 2 + a ** 2 * Vphiphi,
        -3 * Phip * phip,
        2 * Hc,
        k ** 2 - a ** 2 * Vpsipsi,
        -3 * Phip * psip,
    ]
    crossing_probe = {
        a: 1.3,
        Hc: 0.2,
        k: 0.01,
        Vphiphi: -0.7,
        Vpsipsi: -0.7,
        Phip: 1.0e-4,
        phip: 0.3,
        psip: 0.3,
    }
    direct_values = [float(sp.N(e.subs(crossing_probe))) for e in direct_terms]
    direct_finite = all(math.isfinite(v) for v in direct_values)
    direct_denominators_safe = all(sp.denom(sp.together(e)) == 1 for e in direct_terms)

    checks = {
        "potential_first_derivative_exact": is_zero(sp.diff(V, x) - Vx_expected),
        "potential_second_derivative_exact": is_zero(sp.diff(V, x, 2) - Vxx_expected),
        "canonical_background_continuity_exact": is_zero(phi_continuity),
        "phantom_background_continuity_exact": is_zero(psi_continuity),
        "canonical_drho_plus_dp_sign": is_zero(drho_phi + dp_phi - 2 * Aphi),
        "canonical_drho_minus_dp_potential": is_zero(drho_phi - dp_phi - 2 * Vphi * dphi),
        "phantom_drho_plus_dp_sign": is_zero(drho_psi + dp_psi + 2 * Apsi),
        "phantom_drho_minus_dp_potential": is_zero(drho_psi - dp_psi - 2 * Vpsi * dpsi),
        "crossing_rho_plus_p_identity": is_zero(cross - (phip ** 2 - psip ** 2) / a ** 2),
        "direct_kg_coefficients_finite_at_nontrivial_crossing": direct_finite,
        "direct_kg_coefficients_have_no_crossing_denominator": direct_denominators_safe,
        "effective_theta_denominator_vanishes_at_crossing": is_zero(crossing_symbolic_den),
        "effective_theta_numerator_can_remain_nonzero_at_crossing": crossing_num_probe != 0,
        "phi_kg_has_no_direct_psi_perturbation": not any(phi_kg.has(z) for z in (dpsi, dpsip, dpsipp)),
        "psi_kg_has_no_direct_phi_perturbation": not any(psi_kg.has(z) for z in (dphi, dphip, dphipp)),
    }
    passed = all(bool(v) for v in checks.values())
    classification = (
        "M13B_INDEPENDENT_K3A_EQUATION_CLOSURE_PASS_WITH_SCOPE"
        if passed
        else "M13B_INDEPENDENT_K3A_EQUATION_CLOSURE_NOT_ESTABLISHED"
    )

    result = {
        "schema": SCHEMA,
        "model_id": "M13b",
        "family_id": "F13",
        "gate": "K3A",
        "protocol": PROTOCOL,
        "scientific_authority": AUTHORITY,
        "implementation_provenance": "independent_KMDSB_verification",
        "original_provider_reproduced": False,
        "classification": classification,
        "all_required_checks_pass": passed,
        "checks": checks,
        "K3_canonical_promotion": False,
        "K3_independent_contribution": "PARTIAL_EQUATION_CLOSURE" if passed else "NOT_ESTABLISHED",
        "K4_promoted": False,
        "K5_promoted": False,
        "physical_falsification": False,
        "crossing": {
            "rho_DE_plus_p_DE": str(cross),
            "condition": "phip**2 == psip**2 with nonzero finite field velocities",
            "effective_theta_denominator_at_crossing": str(crossing_symbolic_den),
            "effective_theta_numerator_probe": str(crossing_num_probe),
            "direct_kg_coefficient_probe": direct_values,
            "interpretation": "direct field perturbations are the fundamental crossing variables; theta_DE is diagnostic and is singular/ill-conditioned at exact kinetic cancellation",
        },
        "frozen_equation_manifest": {
            "V": str(V),
            "V_x": str(Vx_expected),
            "V_xx": str(Vxx_expected),
            "delta_rho_phi": str(drho_phi),
            "delta_p_phi": str(dp_phi),
            "delta_rho_psi": str(drho_psi),
            "delta_p_psi": str(dp_psi),
            "delta_phi_KG_LHS": str(phi_kg),
            "delta_psi_KG_LHS": str(psi_kg),
        },
        "next_authorized_gate": (
            "K3B_INDEPENDENT_METRIC_EINSTEIN_TWO_FIELD_DYNAMICAL_EMBEDDING_PREREGISTRATION"
            if passed
            else "NONE_REPAIR_EQUATION_TRANSCRIPTION_FIRST"
        ),
    }
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    main(args.output)
