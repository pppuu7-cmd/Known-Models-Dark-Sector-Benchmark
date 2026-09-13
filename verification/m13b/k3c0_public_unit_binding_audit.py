#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

SCHEMA = "KMDSB.W03.M13b.K3C0PublicUnitBindingAudit.v0.1"
PROTOCOL = "protocol/W03_M13B_K3C0_PUBLIC_UNIT_BINDING_AUDIT_v0.1.md"

# Frozen constants.
C = 299792458.0
G = 6.67430e-11
HBAR = 1.054571817e-34
MPC = 3.0856775814913673e22

# Frozen public benchmark.
H0_KM_S_MPC = 67.15
OMEGA_M0 = 0.3114
OMEGA_R0 = 9.23e-5
ZSTAR = 5.0
V0 = 0.91e-8
S = 29.0
PHI_INI = 0.92
PSI_INI = 1.02
DOTPHI_INI = 1.0e-5
DOTPSI_INI = 1.0e-5
THRESHOLD = 1.0e50


def main(output):
    h0_si = H0_KM_S_MPC * 1000.0 / MPC
    mp_mass = math.sqrt(HBAR * C / (8.0 * math.pi * G))
    mp_energy = mp_mass * C * C
    h_planck = HBAR * h0_si / mp_energy

    rho_crit0 = 3.0 * h_planck * h_planck
    omega_de_ref = 1.0 - OMEGA_M0 - OMEGA_R0
    rho_de_ref = 3.0 * omega_de_ref * h_planck * h_planck
    zp1 = 1.0 + ZSTAR
    rho_mr_z5 = 3.0 * h_planck * h_planck * (
        OMEGA_M0 * zp1**3 + OMEGA_R0 * zp1**4
    )

    arg_phi = S * (1.0 - PHI_INI)
    arg_psi = S * (1.0 - PSI_INI)
    factor_phi = math.tanh(arg_phi) + 1.0
    factor_psi = math.tanh(arg_psi) + 1.0
    v_phi = V0 * factor_phi
    v_psi = V0 * factor_psi
    v_literal = v_phi + v_psi

    kinetic_canonical = 0.5 * DOTPHI_INI**2
    kinetic_phantom = -0.5 * DOTPSI_INI**2
    kinetic_total = kinetic_canonical + kinetic_phantom

    r5 = v_literal / rho_mr_z5
    r0 = v_literal / rho_de_ref
    s5 = rho_mr_z5 / v_literal
    s0 = rho_de_ref / v_literal

    finite_positive_values = [
        h0_si, mp_mass, mp_energy, h_planck, rho_crit0,
        omega_de_ref, rho_de_ref, rho_mr_z5,
        factor_phi, factor_psi, v_phi, v_psi, v_literal,
        r5, r0, s5, s0,
    ]
    checks = {
        "all_expected_quantities_finite_positive": all(
            math.isfinite(x) and x > 0.0 for x in finite_positive_values
        ),
        "initial_canonical_phantom_kinetic_cancel_exactly": kinetic_total == 0.0,
        "literal_tanh_potential_sum_positive": v_literal > 0.0,
        "R5_above_frozen_normalization_threshold": r5 > THRESHOLD,
        "R0_above_frozen_normalization_threshold": r0 > THRESHOLD,
        "missing_scale_factors_report_only_not_adopted": s5 > 0.0 and s0 > 0.0,
        "no_physical_falsification_or_promotion": True,
    }
    passed = all(bool(v) for v in checks.values())
    classification = (
        "M13B_K3C0_PUBLIC_UNIT_BINDING_NOT_ESTABLISHED_LITERAL_PLANCK_READING_INCONSISTENT"
        if passed
        else "M13B_K3C0_PUBLIC_UNIT_BINDING_AUDIT_NOT_ESTABLISHED"
    )

    result = {
        "schema": SCHEMA,
        "model_id": "M13b",
        "family_id": "F13",
        "gate": "K3C0",
        "protocol": PROTOCOL,
        "classification": classification,
        "all_required_checks_pass": passed,
        "checks": checks,
        "public_anchor": {
            "H0_km_s_Mpc": H0_KM_S_MPC,
            "Omega_m0": OMEGA_M0,
            "Omega_r0": OMEGA_R0,
            "z_compare": ZSTAR,
            "V0_Mp4": V0,
            "s_Mp_inverse": S,
            "phi_ini_Mp": PHI_INI,
            "psi_ini_Mp": PSI_INI,
            "dotphi_ini_Mp2": DOTPHI_INI,
            "dotpsi_ini_Mp2": DOTPSI_INI,
        },
        "frozen_constants_SI": {
            "c_m_s": C,
            "G_m3_kg_s2": G,
            "hbar_J_s": HBAR,
            "Mpc_m": MPC,
        },
        "conversion": {
            "H0_s_inverse": h0_si,
            "reduced_Planck_mass_kg": mp_mass,
            "reduced_Planck_energy_J": mp_energy,
            "H0_over_reduced_Planck_energy_natural_units": h_planck,
            "rho_crit0_over_Mp4": rho_crit0,
            "Omega_DE_flat_reference": omega_de_ref,
            "rho_DE_reference_over_Mp4": rho_de_ref,
            "rho_matter_plus_radiation_z5_over_Mp4": rho_mr_z5,
        },
        "literal_tanh_evaluation": {
            "argument_phi": arg_phi,
            "argument_psi": arg_psi,
            "factor_phi": factor_phi,
            "factor_psi": factor_psi,
            "V_phi_over_Mp4": v_phi,
            "V_psi_over_Mp4": v_psi,
            "V_total_over_Mp4": v_literal,
            "initial_kinetic_canonical_over_Mp4": kinetic_canonical,
            "initial_kinetic_phantom_over_Mp4": kinetic_phantom,
            "initial_kinetic_total_over_Mp4": kinetic_total,
        },
        "normalization_diagnostic": {
            "threshold_ratio": THRESHOLD,
            "R5_Vliteral_over_rho_mr_z5": r5,
            "R0_Vliteral_over_rho_DE_reference": r0,
            "S5_rho_mr_z5_over_Vliteral_report_only": s5,
            "S0_rho_DE_reference_over_Vliteral_report_only": s0,
            "log10_R5": math.log10(r5),
            "log10_R0": math.log10(r0),
            "interpretation": (
                "The public Planck-unit labels cannot be inserted literally into an ordinary physical cosmology with the simultaneously quoted H0/Omega values and frozen-through-z~5 behavior. A normalization/rescaling convention or correction not established by the public numerical labels is required. The reported S factors are diagnostic magnitudes only and are not adopted model parameters."
                if passed else
                "The preregistered literal-unit inconsistency criterion was not established."
            ),
        },
        "original_provider_reproduced": False,
        "K3_state_ceiling": "PARTIAL",
        "K4_promoted": False,
        "K5_promoted": False,
        "physical_falsification": False,
        "guessed_rescale_adopted": False,
        "next_authorized_gate": (
            "AUTHOR_OR_SOURCE_NORMALIZATION_MAP_SEARCH_OR_INDEPENDENT_DIMENSIONLESS_COSMOLOGY_PREREGISTRATION"
            if passed else "REVIEW_PUBLIC_UNIT_AUDIT"
        ),
    }

    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    main(args.output)
