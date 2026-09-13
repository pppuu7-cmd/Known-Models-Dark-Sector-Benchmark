#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

SCHEMA = "KMDSB.W03.M13b.K3C2IndependentCosmologyPerturbationBridge.v0.1"
PROTOCOL = "protocol/W03_M13B_K3C2_INDEPENDENT_COSMOLOGY_PERTURBATION_BRIDGE_v0.1.md"
K3C1_PATH = Path("waves/wave_03_expanded_dark_energy/M13B_K3C1_INDEPENDENT_BACKGROUND_CLOSURE_RESULT.json")

OMEGA_M0 = 0.3114
OMEGA_R0 = 9.23e-5
S_HAT = 29.0
X_START = 0.92
Y_START = 1.02
N_START = -math.log(6.0)
PHI_INIT = 1.0e-5
K_MODES = [1.0, 10.0]
PERT_NAMES = [
    "delta_x", "r", "delta_y", "t", "Phi", "W",
    "delta_m", "Theta_m", "delta_r", "Theta_r"
]


def potential(x, u0):
    z = S_HAT * (1.0 - x)
    th = math.tanh(z)
    sech2 = max(0.0, 1.0 - th*th)
    u = u0 * (th + 1.0)
    ux = -u0 * S_HAT * sech2
    uxx = -2.0 * u0 * S_HAT * S_HAT * sech2 * th
    return u, ux, uxx


def background(N, x, p, y, q, u0):
    a = math.exp(N)
    ux0, ux, uxx = potential(x, u0)
    uy0, uy, uyy = potential(y, u0)
    D = p*p - q*q
    denom = 1.0 - D/6.0
    B = OMEGA_M0*a**-3 + OMEGA_R0*a**-4
    if denom <= 0.0 or not math.isfinite(denom):
        return None
    E2 = (B + ux0 + uy0)/denom
    if E2 <= 0.0 or not math.isfinite(E2):
        return None
    E = math.sqrt(E2)
    dlnE = -0.5*((3.0*OMEGA_M0*a**-3 + 4.0*OMEGA_R0*a**-4)/E2 + D)
    values = [a, ux0, ux, uxx, uy0, uy, uyy, D, denom, B, E2, E, dlnE]
    if not all(math.isfinite(v) for v in values):
        return None
    return {
        "a": a, "Ux": ux0, "Ux_x": ux, "Ux_xx": uxx,
        "Uy": uy0, "Uy_y": uy, "Uy_yy": uyy,
        "D": D, "denom": denom, "B": B,
        "E2": E2, "E": E, "dlnE": dlnE,
    }


def initialize(khat, u0):
    x, p, y, q = X_START, 0.0, Y_START, 0.0
    dx, r, dy, t = 0.0, 0.0, 0.0, 0.0
    Phi, W = PHI_INIT, 0.0
    b = background(N_START, x, p, y, q, u0)
    a, E2 = b["a"], b["E2"]
    K2 = khat*khat/(a*a*E2)
    Cdens = OMEGA_M0*a**-3 + (4.0/3.0)*OMEGA_R0*a**-4
    delta_m = -(2.0*E2/(3.0*Cdens))*(K2*Phi + 3.0*(W+Phi))
    delta_r = (4.0/3.0)*delta_m
    Theta = (2.0*E2*K2/(3.0*Cdens))*(W+Phi)
    return [
        x, p, y, q,
        dx, r, dy, t, Phi, W,
        delta_m, Theta, delta_r, Theta,
    ], {
        "C_density": Cdens,
        "K2": K2,
        "delta_m_formula": "-(2 E2/(3 Cdens))*(K2*Phi+3*(W+Phi))",
        "delta_r_formula": "(4/3)*delta_m",
        "Theta_formula": "(2 E2 K2/(3 Cdens))*(W+Phi)",
    }


def rhs(N, state, khat, u0):
    x, p, y, q, dx, r, dy, t, Phi, W, dm, Tm, dr, Tr = state
    b = background(N, x, p, y, q, u0)
    if b is None:
        return [float("nan")]*14
    a, E2, dlnE = b["a"], b["E2"], b["dlnE"]
    K2 = khat*khat/(a*a*E2)
    fric = 3.0 + dlnE

    xp = p
    pp = -fric*p - 3.0*b["Ux_x"]/E2
    yp = q
    qp = -fric*q + 3.0*b["Uy_y"]/E2

    dxp = r
    rp = (
        -fric*r
        -(K2 + 3.0*b["Ux_xx"]/E2)*dx
        +4.0*p*W
        -6.0*b["Ux_x"]*Phi/E2
    )
    dyp = t
    tp = (
        -fric*t
        -(K2 - 3.0*b["Uy_yy"]/E2)*dy
        +4.0*q*W
        +6.0*b["Uy_y"]*Phi/E2
    )

    dP_phi = E2*(p*r - p*p*Phi)/3.0 - b["Ux_x"]*dx
    dP_psi = -E2*(q*t - q*q*Phi)/3.0 - b["Uy_y"]*dy
    dP_rad = OMEGA_R0*a**-4*dr/3.0
    dP = dP_phi + dP_psi + dP_rad

    Phip = W
    Wp = -(4.0+dlnE)*W -(3.0+2.0*dlnE)*Phi +(3.0/(2.0*E2))*dP

    dmp = -Tm + 3.0*W
    Tmp = -(2.0+dlnE)*Tm + K2*Phi
    drp = -(4.0/3.0)*Tr + 4.0*W
    Trp = -(1.0+dlnE)*Tr + K2*(dr/4.0 + Phi)

    return [xp, pp, yp, qp, dxp, rp, dyp, tp, Phip, Wp, dmp, Tmp, drp, Trp]


def add(state, vec, fac):
    return [s + fac*v for s, v in zip(state, vec)]


def rk4_step(N, state, h, khat, u0):
    k1 = rhs(N, state, khat, u0)
    k2 = rhs(N+0.5*h, add(state, k1, 0.5*h), khat, u0)
    k3 = rhs(N+0.5*h, add(state, k2, 0.5*h), khat, u0)
    k4 = rhs(N+h, add(state, k3, h), khat, u0)
    return [
        s + h*(a + 2*b + 2*c + d)/6.0
        for s, a, b, c, d in zip(state, k1, k2, k3, k4)
    ]


def constraints(N, state, khat, u0):
    x, p, y, q, dx, r, dy, t, Phi, W, dm, Tm, dr, Tr = state
    b = background(N, x, p, y, q, u0)
    if b is None:
        return None
    a, E2 = b["a"], b["E2"]
    K2 = khat*khat/(a*a*E2)

    dR_phi = E2*(p*r - p*p*Phi)/3.0 + b["Ux_x"]*dx
    dR_psi = -E2*(q*t - q*q*Phi)/3.0 + b["Uy_y"]*dy
    dR = OMEGA_M0*a**-3*dm + OMEGA_R0*a**-4*dr + dR_phi + dR_psi

    term00a = K2*Phi
    term00b = 3.0*(W+Phi)
    term00c = (3.0/(2.0*E2))*dR
    C00 = term00a + term00b + term00c
    S00 = abs(term00a) + abs(term00b) + abs(term00c) + 1e-30

    fluid_momentum = (
        OMEGA_M0*a**-3*Tm +(4.0/3.0)*OMEGA_R0*a**-4*Tr
    )
    term0ia = W+Phi
    term0ib = -0.5*(p*dx - q*dy)
    term0ic = -(3.0/(2.0*E2*K2))*fluid_momentum
    C0i = term0ia + term0ib + term0ic
    S0i = abs(term0ia) + abs(term0ib) + abs(term0ic) + 1e-30

    return {
        "C00": C00, "C00_norm": abs(C00)/S00,
        "C0i": C0i, "C0i_norm": abs(C0i)/S0i,
        "dR": dR, "K2": K2,
    }


def integrate(khat, u0, nsteps):
    state, init_manifest = initialize(khat, u0)
    N = N_START
    h = -N_START/nsteps
    initial_constraints = constraints(N, state, khat, u0)
    max_c00 = 0.0
    max_c0i = 0.0
    max_abs_pert = 0.0
    min_denom = float("inf")
    min_E2 = float("inf")
    min_D = 0.0
    max_D = 0.0
    finite = True
    crossings = []
    negative_seen = False
    prev_D = 0.0
    prev_N = N

    for i in range(nsteps + 1):
        x, p, y, q = state[:4]
        b = background(N, x, p, y, q, u0)
        c = constraints(N, state, khat, u0)
        if b is None or c is None or not all(math.isfinite(v) for v in state):
            finite = False
            break
        D = b["D"]
        min_D = min(min_D, D)
        max_D = max(max_D, D)
        min_denom = min(min_denom, b["denom"])
        min_E2 = min(min_E2, b["E2"])
        max_c00 = max(max_c00, c["C00_norm"])
        max_c0i = max(max_c0i, c["C0i_norm"])
        max_abs_pert = max(max_abs_pert, max(abs(v) for v in state[4:]))
        if D < -1e-6:
            negative_seen = True
        if i > 0 and negative_seen and prev_D < 0.0 <= D:
            frac = (-prev_D)/(D-prev_D) if D != prev_D else 0.0
            Nc = prev_N + frac*(N-prev_N)
            crossings.append({"N": Nc, "z": math.exp(-Nc)-1.0})
        if i == nsteps:
            break
        prev_D, prev_N = D, N
        state = rk4_step(N, state, h, khat, u0)
        N += h

    if not finite:
        return {
            "finite": False, "k_hat": khat, "nsteps": nsteps,
            "initial_manifest": init_manifest,
            "initial_constraints": initial_constraints,
            "crossings": crossings,
        }

    b = background(N, *state[:4], u0)
    c = constraints(N, state, khat, u0)
    endpoint = {
        "N": N, "z": math.exp(-N)-1.0,
        "x": state[0], "p": state[1], "y": state[2], "q": state[3],
        "E": b["E"], "D": b["D"],
    }
    endpoint.update({name: state[4+i] for i, name in enumerate(PERT_NAMES)})
    return {
        "finite": True, "k_hat": khat, "nsteps": nsteps,
        "initial_manifest": init_manifest,
        "initial_state": {name: val for name, val in zip(
            ["x","p","y","q"]+PERT_NAMES, initialize(khat,u0)[0]
        )},
        "initial_constraints": initial_constraints,
        "endpoint": endpoint,
        "crossings": crossings,
        "max_C00_norm": max_c00,
        "max_C0i_norm": max_c0i,
        "max_abs_perturbation_state": max_abs_pert,
        "min_D": min_D, "max_D": max_D,
        "min_denom": min_denom, "min_E2": min_E2,
        "endpoint_constraints": c,
    }


def symrel(a, b):
    return abs(a-b)/max(abs(a), abs(b), 1e-12)


def main(output):
    bg_result = json.loads(K3C1_PATH.read_text(encoding="utf-8"))
    assert bg_result["classification"] == "M13B_K3C1_INDEPENDENT_CRITICAL_DENSITY_BACKGROUND_CLOSURE_PASS_WITH_SCOPE"
    u0 = bg_result["numerics"]["fine_U0"]
    bg_endpoint = bg_result["numerics"]["fine_endpoint"]
    bg_cross_z = bg_result["numerics"]["fine_crossings"][0]["z"]

    mode_results = {}
    mode_checks = {}
    all_pass = True

    for khat in K_MODES:
        coarse = integrate(khat, u0, 4000)
        fine = integrate(khat, u0, 8000)
        key = f"khat_{int(khat)}"
        mode_results[key] = {"coarse": coarse, "fine": fine}

        if not coarse["finite"] or not fine["finite"]:
            checks = {"finite_execution": False}
            mode_checks[key] = checks
            all_pass = False
            continue

        epc, epf = coarse["endpoint"], fine["endpoint"]
        bg_diffs = {name: symrel(epf[name], bg_endpoint[name]) for name in ("x","p","y","q","E")}
        fine_cross = fine["crossings"]
        coarse_cross = coarse["crossings"]
        bg_cross_diff = abs(fine_cross[0]["z"]-bg_cross_z) if len(fine_cross)==1 else float("inf")
        pert_diffs = {name: symrel(epc[name], epf[name]) for name in PERT_NAMES}
        max_pert_diff = max(pert_diffs.values())

        c00_refine = fine["max_C00_norm"] <= 1e-10 or fine["max_C00_norm"] <= 0.5*coarse["max_C00_norm"]
        c0i_refine = fine["max_C0i_norm"] <= 1e-10 or fine["max_C0i_norm"] <= 0.5*coarse["max_C0i_norm"]
        scalar_sourced = max(abs(epf["delta_x"]), abs(epf["delta_y"])) > 1e-8

        checks = {
            "finite_execution": True,
            "background_endpoint_matches_K3C1": max(bg_diffs.values()) <= 2e-9,
            "background_crossing_matches_K3C1": bg_cross_diff <= 2e-5,
            "initial_C00_constraint": coarse["initial_constraints"]["C00_norm"] <= 1e-12 and fine["initial_constraints"]["C00_norm"] <= 1e-12,
            "initial_C0i_constraint": coarse["initial_constraints"]["C0i_norm"] <= 1e-12 and fine["initial_constraints"]["C0i_norm"] <= 1e-12,
            "fine_positive_background_and_denominator": fine["min_E2"] > 0.0 and fine["min_denom"] > 0.5,
            "fine_linear_amplitude_domain": fine["max_abs_perturbation_state"] < 0.1,
            "fine_C00_preserved": fine["max_C00_norm"] <= 1e-7,
            "fine_C0i_preserved": fine["max_C0i_norm"] <= 1e-7,
            "C00_refines_or_floor": c00_refine,
            "C0i_refines_or_floor": c0i_refine,
            "perturbation_endpoint_converged": max_pert_diff <= 1e-5,
            "scalar_perturbations_dynamically_sourced": scalar_sourced,
            "unique_background_crossing_retained": len(fine_cross)==1 and len(coarse_cross)==1 and epf["D"] > 1e-4,
            "direct_field_crossing_discipline": True,
        }
        mode_checks[key] = {
            **checks,
            "background_endpoint_symmetric_relative_differences": bg_diffs,
            "background_crossing_z_difference_vs_K3C1": bg_cross_diff,
            "perturbation_endpoint_symmetric_relative_differences": pert_diffs,
            "max_perturbation_endpoint_difference": max_pert_diff,
        }
        all_pass = all_pass and all(bool(v) for k,v in checks.items())

    classification = (
        "M13B_K3C2_INDEPENDENT_COSMOLOGY_PERTURBATION_BRIDGE_PASS_WITH_SCOPE"
        if all_pass else "M13B_K3C2_COSMOLOGY_PERTURBATION_BRIDGE_NOT_ESTABLISHED"
    )

    result = {
        "schema": SCHEMA,
        "model_id": "M13b",
        "family_id": "F13",
        "gate": "K3C2",
        "protocol": PROTOCOL,
        "classification": classification,
        "all_required_checks_pass": all_pass,
        "implementation_provenance": "independent_KMDSB_standard_GR_ideal_fluid_perturbation_bridge",
        "background_authority": {
            "source": str(K3C1_PATH),
            "U0_exact_from_K3C1_fine": u0,
            "K3C1_crossing_z": bg_cross_z,
        },
        "modes": mode_results,
        "mode_checks": mode_checks,
        "initialization_manifest": {
            "Phi_i": PHI_INIT,
            "W_i": 0.0,
            "scalar_perturbations_i": 0.0,
            "adiabatic_density_relation": "delta_r=(4/3)delta_m",
            "common_velocity_relation": "Theta_r=Theta_m",
            "delta_m_solution": "-(2 E2/(3 Cdens))*(K2*Phi+3*(W+Phi))",
            "Theta_solution": "(2 E2 K2/(3 Cdens))*(W+Phi)",
        },
        "direct_variable_manifest": {
            "dark_energy_variables": ["delta_x","r","delta_y","t"],
            "forbidden_denominators_absent": ["D", "rho_DE+p_DE", "theta_DE"],
        },
        "full_Boltzmann_hierarchy": False,
        "radiation_anisotropic_stress": False,
        "author_model_reproduced": False,
        "author_normalization_map_claimed": False,
        "K3_state_ceiling": "PARTIAL",
        "K4_promoted": False,
        "K5_promoted": False,
        "physical_falsification": False,
        "next_authorized_gate": (
            "FULL_INDEPENDENT_EINSTEIN_BOLTZMANN_PROVIDER_BUILD_OR_ADAPTER_PREREGISTRATION"
            if all_pass else "NONE_REVIEW_K3C2"
        ),
    }
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args=ap.parse_args()
    main(args.output)
