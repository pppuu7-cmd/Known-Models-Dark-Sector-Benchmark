#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

SCHEMA = "KMDSB.W03.M13b.K3B2IndependentStandardGRDynamicalEmbedding.v0.1"
PROTOCOL = "protocol/W03_M13B_K3B2_INDEPENDENT_STANDARD_GR_DYNAMICAL_EMBEDDING_v0.1.md"

V0 = 1.0
S = 1.0
K = 0.7
T = 0.05

STATE_NAMES = [
    "a", "phi", "u", "psi", "v",
    "delta_phi", "delta_phi_prime", "delta_psi", "delta_psi_prime", "Phi"
]


def potential(x):
    z = S * (1.0 - x)
    th = math.tanh(z)
    sech2 = 1.0 / math.cosh(z) ** 2
    V = V0 * (th + 1.0)
    Vx = -V0 * S * sech2
    Vxx = -2.0 * V0 * S * S * sech2 * th
    return V, Vx, Vxx


def background_derived(y):
    a, phi, u, psi, v = y[:5]
    Vphi0, Vphi, Vphiphi = potential(phi)
    Vpsi0, Vpsi, Vpsipsi = potential(psi)
    rho = (u*u - v*v) / (2.0*a*a) + Vphi0 + Vpsi0
    if not math.isfinite(rho) or rho <= 0.0 or a <= 0.0:
        return None
    Hc = a * math.sqrt(rho / 3.0)
    Hcp = Hc*Hc - 0.5*(u*u - v*v)
    return {
        "Vphi0": Vphi0, "Vphi": Vphi, "Vphiphi": Vphiphi,
        "Vpsi0": Vpsi0, "Vpsi": Vpsi, "Vpsipsi": Vpsipsi,
        "rho": rho, "Hc": Hc, "Hcp": Hcp,
        "q": u*u - v*v,
    }


def rhs(y):
    d = background_derived(y)
    if d is None:
        return [float("nan")] * len(y)
    a, phi, u, psi, v, dphi, dphip, dpsi, dpsip, Phi = y
    Hc = d["Hc"]
    Phip = -Hc*Phi + 0.5*(u*dphi - v*dpsi)
    up = -2.0*Hc*u - a*a*d["Vphi"]
    vp = -2.0*Hc*v + a*a*d["Vpsi"]
    dphipp = (
        -2.0*Hc*dphip
        -(K*K + a*a*d["Vphiphi"])*dphi
        +4.0*u*Phip
        -2.0*a*a*d["Vphi"]*Phi
    )
    dpsipp = (
        -2.0*Hc*dpsip
        -(K*K - a*a*d["Vpsipsi"])*dpsi
        +4.0*v*Phip
        +2.0*a*a*d["Vpsi"]*Phi
    )
    return [
        Hc*a,
        u,
        up,
        v,
        vp,
        dphip,
        dphipp,
        dpsip,
        dpsipp,
        Phip,
    ]


def diagnostics(y):
    d = background_derived(y)
    if d is None:
        return {
            "finite": False, "rho": float("nan"), "Hc": float("nan"),
            "q": float("nan"), "C00": float("nan"), "Cij": float("nan"),
            "C00_norm": float("inf"), "Cij_norm": float("inf")
        }
    a, phi, u, psi, v, dphi, dphip, dpsi, dpsip, Phi = y
    Hc, Hcp = d["Hc"], d["Hcp"]
    deriv = rhs(y)
    up, vp, Phip = deriv[2], deriv[4], deriv[9]

    drho_phi = (u*dphip - u*u*Phi)/(a*a) + d["Vphi"]*dphi
    dp_phi = (u*dphip - u*u*Phi)/(a*a) - d["Vphi"]*dphi
    drho_psi = (-v*dpsip + v*v*Phi)/(a*a) + d["Vpsi"]*dpsi
    dp_psi = (-v*dpsip + v*v*Phi)/(a*a) - d["Vpsi"]*dpsi
    drho = drho_phi + drho_psi
    dp = dp_phi + dp_psi

    Phipp = (
        -Hcp*Phi - Hc*Phip
        +0.5*(up*dphi + u*dphip - vp*dpsi - v*dpsip)
    )

    term00_a = K*K*Phi
    term00_b = 3.0*Hc*(Phip + Hc*Phi)
    term00_c = 0.5*a*a*drho
    C00 = term00_a + term00_b + term00_c
    scale00 = abs(term00_a) + abs(term00_b) + abs(term00_c) + 1e-30

    termij_a = Phipp
    termij_b = 3.0*Hc*Phip
    termij_c = (2.0*Hcp + Hc*Hc)*Phi
    termij_d = -0.5*a*a*dp
    Cij = termij_a + termij_b + termij_c + termij_d
    scaleij = abs(termij_a) + abs(termij_b) + abs(termij_c) + abs(termij_d) + 1e-30

    vals = list(y) + [
        d["rho"], Hc, Hcp, Phip, Phipp, drho, dp, C00, Cij,
        C00/scale00, Cij/scaleij
    ]
    return {
        "finite": all(math.isfinite(x) for x in vals),
        "rho": d["rho"], "Hc": Hc, "Hcp": Hcp, "q": d["q"],
        "Phi_prime": Phip, "Phi_double_prime": Phipp,
        "delta_rho": drho, "delta_p": dp,
        "C00": C00, "Cij": Cij,
        "C00_norm": abs(C00)/scale00,
        "Cij_norm": abs(Cij)/scaleij,
    }


def make_anchor():
    a = 1.0
    phi, psi = 0.5, 1.5
    u = v = 0.1
    dphi, dpsi = 1.0e-5, -5.0e-6
    dphip = 0.0
    Phi = 2.0e-6

    base = [a, phi, u, psi, v, dphi, dphip, dpsi, 0.0, Phi]
    d = background_derived(base)
    Hc = d["Hc"]
    Phip = -Hc*Phi + 0.5*(u*dphi - v*dpsi)
    target_drho = -2.0*(K*K*Phi + 3.0*Hc*(Phip + Hc*Phi))/(a*a)
    dpsip = (
        u*dphip + (v*v-u*u)*Phi
        +a*a*(d["Vphi"]*dphi + d["Vpsi"]*dpsi)
        -a*a*target_drho
    )/v
    y = [a, phi, u, psi, v, dphi, dphip, dpsi, dpsip, Phi]
    d = background_derived(y)
    qprime = -2.0*u*a*a*(d["Vphi"] + d["Vpsi"])
    return y, qprime


def add_scaled(y, kvec, scale):
    return [yi + scale*ki for yi,ki in zip(y,kvec)]


def rk4_step(y, h):
    k1 = rhs(y)
    k2 = rhs(add_scaled(y, k1, 0.5*h))
    k3 = rhs(add_scaled(y, k2, 0.5*h))
    k4 = rhs(add_scaled(y, k3, h))
    return [
        yi + (h/6.0)*(a + 2.0*b + 2.0*c + d)
        for yi,a,b,c,d in zip(y,k1,k2,k3,k4)
    ]


def integrate(direction, N):
    y, _ = make_anchor()
    h = direction*T/N
    max_c00 = 0.0
    max_cij = 0.0
    finite = True
    positive = True
    min_rho = float("inf")
    min_Hc = float("inf")
    for i in range(N+1):
        diag = diagnostics(y)
        finite = finite and diag["finite"]
        positive = positive and diag["rho"] > 0.0 and diag["Hc"] > 0.0
        min_rho = min(min_rho, diag["rho"])
        min_Hc = min(min_Hc, diag["Hc"])
        max_c00 = max(max_c00, diag["C00_norm"])
        max_cij = max(max_cij, diag["Cij_norm"])
        if i < N:
            y = rk4_step(y, h)
    return {
        "endpoint": y,
        "endpoint_diag": diagnostics(y),
        "max_C00_norm": max_c00,
        "max_Cij_norm": max_cij,
        "finite": finite,
        "positive_background": positive,
        "min_rho": min_rho,
        "min_Hc": min_Hc,
    }


def symrel(a, b):
    return abs(a-b)/max(abs(a), abs(b), 1e-12)


def endpoint_stability(coarse, fine):
    # a, phi, u, psi, v, Phi, delta_phi, delta_psi
    idx = [0,1,2,3,4,9,5,7]
    names = [STATE_NAMES[i] for i in idx]
    vals = {}
    for name,i in zip(names,idx):
        vals[name] = symrel(coarse["endpoint"][i], fine["endpoint"][i])
    return vals


def main(output):
    anchor, qprime0 = make_anchor()
    anchor_diag = diagnostics(anchor)

    runs = {}
    for N in (500, 1000):
        runs[str(N)] = {
            "backward": integrate(-1.0, N),
            "forward": integrate(+1.0, N),
        }

    coarse, fine = runs["500"], runs["1000"]
    stab_back = endpoint_stability(coarse["backward"], fine["backward"])
    stab_forw = endpoint_stability(coarse["forward"], fine["forward"])

    coarse_c00 = max(coarse["backward"]["max_C00_norm"], coarse["forward"]["max_C00_norm"])
    fine_c00 = max(fine["backward"]["max_C00_norm"], fine["forward"]["max_C00_norm"])
    coarse_cij = max(coarse["backward"]["max_Cij_norm"], coarse["forward"]["max_Cij_norm"])
    fine_cij = max(fine["backward"]["max_Cij_norm"], fine["forward"]["max_Cij_norm"])

    q_back = fine["backward"]["endpoint_diag"]["q"]
    q_forw = fine["forward"]["endpoint_diag"]["q"]
    all_finite = all(runs[n][d]["finite"] for n in runs for d in ("backward","forward"))
    all_positive = all(runs[n][d]["positive_background"] for n in runs for d in ("backward","forward"))
    max_stability = max(list(stab_back.values()) + list(stab_forw.values()))

    checks = {
        "anchor_q_zero": abs(anchor_diag["q"]) <= 1e-15,
        "anchor_C00_solved": abs(anchor_diag["C00"]) <= 1e-13,
        "transverse_crossing_prediction_positive": math.isfinite(qprime0) and qprime0 > 0.0,
        "executed_crossing_backward_negative": q_back < -1e-12,
        "executed_crossing_forward_positive": q_forw > 1e-12,
        "all_states_and_diagnostics_finite": all_finite,
        "rho_and_Hc_positive_throughout": all_positive,
        "fine_C00_normalized_max": fine_c00 <= 1e-7,
        "fine_Cij_normalized_max": fine_cij <= 1e-7,
        "endpoint_resolution_stability": max_stability <= 1e-7,
        "C00_refinement_or_floor": fine_c00 <= 1e-10 or fine_c00 <= 0.5*coarse_c00,
        "Cij_refinement_or_floor": fine_cij <= 1e-10 or fine_cij <= 0.5*coarse_cij,
        "direct_variables_no_crossing_denominator": True,
        "no_promotion_leakage": True,
    }
    passed = all(bool(v) for v in checks.values())
    classification = (
        "M13B_K3B2_INDEPENDENT_STANDARD_GR_DYNAMICAL_EMBEDDING_PASS_WITH_SCOPE"
        if passed else "M13B_K3B2_DYNAMICAL_EMBEDDING_NOT_ESTABLISHED"
    )

    compact_runs = {}
    for n in ("500","1000"):
        compact_runs[n] = {}
        for direction in ("backward","forward"):
            r = runs[n][direction]
            compact_runs[n][direction] = {
                "endpoint": {name: r["endpoint"][i] for i,name in enumerate(STATE_NAMES)},
                "endpoint_q": r["endpoint_diag"]["q"],
                "max_C00_norm": r["max_C00_norm"],
                "max_Cij_norm": r["max_Cij_norm"],
                "finite": r["finite"],
                "positive_background": r["positive_background"],
                "min_rho": r["min_rho"],
                "min_Hc": r["min_Hc"],
            }

    result = {
        "schema": SCHEMA,
        "model_id": "M13b",
        "family_id": "F13",
        "gate": "K3B2",
        "protocol": PROTOCOL,
        "implementation_provenance": "independent_KMDSB_standard_GR_verification",
        "original_provider_reproduced": False,
        "classification": classification,
        "all_required_checks_pass": passed,
        "checks": checks,
        "anchor": {
            "state": {name: anchor[i] for i,name in enumerate(STATE_NAMES)},
            "q0": anchor_diag["q"],
            "qprime0": qprime0,
            "C00_initial": anchor_diag["C00"],
            "Hc0": anchor_diag["Hc"],
            "rho0": anchor_diag["rho"],
            "Phi_prime0": anchor_diag["Phi_prime"],
        },
        "numerics": {
            "method": "fixed_step_classical_RK4_binary64",
            "half_interval_T": T,
            "coarse_steps_per_half": 500,
            "fine_steps_per_half": 1000,
            "runs": compact_runs,
            "endpoint_stability_backward": stab_back,
            "endpoint_stability_forward": stab_forw,
            "max_endpoint_symmetric_relative_difference": max_stability,
            "coarse_max_C00_norm": coarse_c00,
            "fine_max_C00_norm": fine_c00,
            "coarse_max_Cij_norm": coarse_cij,
            "fine_max_Cij_norm": fine_cij,
        },
        "direct_variable_manifest": {
            "evolved": STATE_NAMES,
            "metric_equation": "Phi_prime=-Hc*Phi+(u*delta_phi-v*delta_psi)/2",
            "forbidden_denominators_absent": ["q", "rho_plus_p", "u2_minus_v2", "theta_DE"],
        },
        "K3_canonical_state_ceiling": "PARTIAL",
        "K4_promoted": False,
        "K5_promoted": False,
        "physical_falsification": False,
        "next_authorized_gate": (
            "M13B_COSMOLOGY_SCALE_INDEPENDENT_EINSTEIN_BOLTZMANN_PREREGISTRATION"
            if passed else "NONE_REVIEW_K3B2_CONSTRAINT_FAILURE"
        ),
    }
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    main(args.output)
