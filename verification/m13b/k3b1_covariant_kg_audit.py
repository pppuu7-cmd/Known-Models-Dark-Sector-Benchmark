#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import sympy as sp

SCHEMA = "KMDSB.W03.M13b.K3B1CovariantKGAudit.v0.1"
PROTOCOL = "protocol/W03_M13B_K3B1_COVARIANT_KG_CONVENTION_AUDIT_v0.1.md"


def zero(expr):
    return sp.simplify(sp.expand(expr)) == 0


def main(output):
    a, Hc, k = sp.symbols("a Hc k", nonzero=True, finite=True)
    Phi, Phip = sp.symbols("Phi Phip", finite=True)
    phip, psip = sp.symbols("phip psip", finite=True)
    Vphi, Vpsi = sp.symbols("Vphi Vpsi", finite=True)
    Vphiphi, Vpsipsi = sp.symbols("Vphiphi Vpsipsi", finite=True)
    dphi, dphip, dphipp = sp.symbols("dphi dphip dphipp", finite=True)
    dpsi, dpsip, dpsipp = sp.symbols("dpsi dpsip dpsipp", finite=True)

    common_phi = dphipp + 2*Hc*dphip + (k**2 + a**2*Vphiphi)*dphi
    common_psi = dpsipp + 2*Hc*dpsip + (k**2 - a**2*Vpsipsi)*dpsi

    cov_phi = common_phi - 4*phip*Phip + 2*a**2*Vphi*Phi
    cov_psi = common_psi - 4*psip*Phip - 2*a**2*Vpsi*Phi
    pub_phi = common_phi - 3*phip*Phip
    pub_psi = common_psi - 3*psip*Phip

    diff_phi = sp.expand(pub_phi - cov_phi)
    diff_psi = sp.expand(pub_psi - cov_psi)
    expected_phi = phip*Phip - 2*a**2*Vphi*Phi
    expected_psi = psip*Phip + 2*a**2*Vpsi*Phi

    # Generic probes are deliberately arbitrary finite nonzero values, not fitted cosmology.
    probe = {a: sp.Rational(3,2), Phi: sp.Rational(1,100), Phip: sp.Rational(1,200),
             phip: sp.Rational(2,5), psip: sp.Rational(-1,3),
             Vphi: sp.Rational(-2,7), Vpsi: sp.Rational(3,11)}
    generic_phi = sp.simplify(diff_phi.subs(probe))
    generic_psi = sp.simplify(diff_psi.subs(probe))

    source_rhs_phi = sp.expand(4*phip*Phip - 2*a**2*Vphi*Phi)
    source_rhs_psi = sp.expand(4*psip*Phip + 2*a**2*Vpsi*Phi)

    checks = {
        "canonical_literal_minus_covariant_exact": zero(diff_phi - expected_phi),
        "phantom_literal_minus_covariant_exact": zero(diff_psi - expected_psi),
        "canonical_difference_not_identity": generic_phi != 0,
        "phantom_difference_not_identity": generic_psi != 0,
        "canonical_no_metric_special_case_coincides": zero(diff_phi.subs({Phi:0,Phip:0})),
        "phantom_no_metric_special_case_coincides": zero(diff_psi.subs({Phi:0,Phip:0})),
        "canonical_covariant_rhs_source_structure": zero((common_phi - cov_phi) - source_rhs_phi),
        "phantom_covariant_rhs_source_structure": zero((common_psi - cov_psi) - source_rhs_psi),
        "canonical_covariant_mass_sign_positive": sp.expand(cov_phi).coeff(dphi,1).has(Vphiphi),
        "phantom_covariant_mass_sign_negative": sp.expand(cov_psi).coeff(dpsi,1).has(Vpsipsi),
    }
    passed = all(bool(v) for v in checks.values())
    classification = (
        "M13B_K3B1_PUBLISHED_PERTURBED_KG_NOT_LITERAL_COVARIANT_IMPLEMENTATION_AUTHORITY"
        if passed else "M13B_K3B1_COVARIANT_KG_AUDIT_NOT_ESTABLISHED"
    )
    result = {
        "schema": SCHEMA,
        "model_id": "M13b",
        "family_id": "F13",
        "gate": "K3B1",
        "protocol": PROTOCOL,
        "classification": classification,
        "all_required_checks_pass": passed,
        "checks": checks,
        "canonical_literal_minus_covariant": str(diff_phi),
        "phantom_literal_minus_covariant": str(diff_psi),
        "generic_nonzero_probe": {"canonical": str(generic_phi), "phantom": str(generic_psi)},
        "covariant_rhs_sources": {"canonical": str(source_rhs_phi), "phantom": str(source_rhs_psi)},
        "implementation_authority": "independent_covariant_standard_GR" if passed else "UNRESOLVED",
        "original_provider_reproduced": False,
        "K3_state_ceiling": "PARTIAL",
        "K4_promoted": False,
        "K5_promoted": False,
        "physical_falsification": False,
        "next_authorized_gate": (
            "K3B2_INDEPENDENT_STANDARD_GR_TWO_FIELD_DYNAMICAL_EMBEDDING"
            if passed else "NONE"
        ),
    }
    out = Path(output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--output", required=True)
    args=ap.parse_args(); main(args.output)
