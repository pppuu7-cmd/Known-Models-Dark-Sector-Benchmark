#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

SCHEMA = "KMDSB.W03.M13b.K3C1IndependentCriticalDensityBackground.v0.1"
PROTOCOL = "protocol/W03_M13B_K3C1_INDEPENDENT_CRITICAL_DENSITY_BACKGROUND_CLOSURE_v0.1.md"
K3C0_PATH = Path("waves/wave_03_expanded_dark_energy/M13B_K3C0_PUBLIC_UNIT_BINDING_AUDIT_RESULT.json")

OMEGA_M0 = 0.3114
OMEGA_R0 = 9.23e-5
S_HAT = 29.0
X_START = 0.92
Y_START = 1.02
N_START = -math.log(6.0)
U_LOW = 1.0e-4
U_HIGH = 2.0
MAX_BISECT = 64
ROOT_E_TOL = 1.0e-11
ROOT_WIDTH_TOL = 1.0e-12
CROSS_THRESHOLD = 1.0e-6
PUBLIC_V0_MP4 = 0.91e-8


def potential(x, u0):
    z = S_HAT * (1.0 - x)
    th = math.tanh(z)
    sech2 = max(0.0, 1.0 - th * th)
    u = u0 * (th + 1.0)
    ux = -u0 * S_HAT * sech2
    return u, ux


def derived(N, state, u0):
    x, p, y, q = state
    a = math.exp(N)
    ux0, ux = potential(x, u0)
    uy0, uy = potential(y, u0)
    D = p*p - q*q
    denom = 1.0 - D/6.0
    B = OMEGA_M0 * a**-3 + OMEGA_R0 * a**-4
    if not math.isfinite(denom) or denom <= 0.0:
        return None
    E2 = (B + ux0 + uy0) / denom
    if not math.isfinite(E2) or E2 <= 0.0:
        return None
    E = math.sqrt(E2)
    dlnE = -0.5 * ((3.0*OMEGA_M0*a**-3 + 4.0*OMEGA_R0*a**-4)/E2 + D)
    values = [E2, E, dlnE, ux0, ux, uy0, uy, D, denom, B]
    if not all(math.isfinite(v) for v in values):
        return None
    return {
        "a": a, "E2": E2, "E": E, "dlnE_dN": dlnE,
        "Ux": ux0, "Ux_x": ux, "Uy": uy0, "Uy_y": uy,
        "D": D, "denom": denom, "B": B,
    }


def rhs(N, state, u0):
    d = derived(N, state, u0)
    if d is None:
        return [float("nan")]*4
    x, p, y, q = state
    E2 = d["E2"]
    fric = 3.0 + d["dlnE_dN"]
    return [
        p,
        -fric*p - 3.0*d["Ux_x"]/E2,
        q,
        -fric*q + 3.0*d["Uy_y"]/E2,
    ]


def add(y, k, fac):
    return [yi + fac*ki for yi, ki in zip(y, k)]


def rk4_step(N, state, h, u0):
    k1 = rhs(N, state, u0)
    k2 = rhs(N + 0.5*h, add(state, k1, 0.5*h), u0)
    k3 = rhs(N + 0.5*h, add(state, k2, 0.5*h), u0)
    k4 = rhs(N + h, add(state, k3, h), u0)
    return [
        yi + h*(a + 2*b + 2*c + d)/6.0
        for yi, a, b, c, d in zip(state, k1, k2, k3, k4)
    ]


def integrate(u0, nsteps, keep_crossing=False):
    state = [X_START, 0.0, Y_START, 0.0]
    N = N_START
    h = -N_START / nsteps
    min_denom = float("inf")
    min_E2 = float("inf")
    finite = True
    min_D = 0.0
    max_D = 0.0
    negative_seen = False
    crossings = []
    prev_D = 0.0
    prev_N = N

    for i in range(nsteps + 1):
        d = derived(N, state, u0)
        if d is None or not all(math.isfinite(v) for v in state):
            finite = False
            break
        D = d["D"]
        min_denom = min(min_denom, d["denom"])
        min_E2 = min(min_E2, d["E2"])
        min_D = min(min_D, D)
        max_D = max(max_D, D)
        if D < -CROSS_THRESHOLD:
            negative_seen = True
        if i > 0 and negative_seen and prev_D < 0.0 <= D:
            frac = (-prev_D)/(D - prev_D) if D != prev_D else 0.0
            Nc = prev_N + frac*(N - prev_N)
            zc = math.exp(-Nc) - 1.0
            crossings.append({"N": Nc, "z": zc})
        if i == nsteps:
            break
        prev_D = D
        prev_N = N
        state = rk4_step(N, state, h, u0)
        N += h

    if not finite:
        return {
            "finite": False,
            "u0": u0,
            "nsteps": nsteps,
            "endpoint": None,
            "crossings": crossings,
            "min_D": min_D,
            "max_D": max_D,
            "min_denom": min_denom,
            "min_E2": min_E2,
        }

    d = derived(N, state, u0)
    omega_de = d["E2"]*d["D"]/6.0 + d["Ux"] + d["Uy"]
    return {
        "finite": True,
        "u0": u0,
        "nsteps": nsteps,
        "endpoint": {
            "N": N, "z": math.exp(-N)-1.0,
            "x": state[0], "p": state[1], "y": state[2], "q": state[3],
            "E": d["E"], "E2": d["E2"], "D": d["D"],
            "Omega_DE": omega_de,
        },
        "crossings": crossings,
        "min_D": min_D,
        "max_D": max_D,
        "min_denom": min_denom,
        "min_E2": min_E2,
    }


def solve_u0(nsteps):
    lo = integrate(U_LOW, nsteps)
    hi = integrate(U_HIGH, nsteps)
    if not lo["finite"] or not hi["finite"]:
        return {"bracket_ok": False, "lo": lo, "hi": hi, "root": None}
    flo = lo["endpoint"]["E"] - 1.0
    fhi = hi["endpoint"]["E"] - 1.0
    bracket_ok = flo < 0.0 < fhi
    if not bracket_ok:
        return {"bracket_ok": False, "lo": lo, "hi": hi, "root": None}

    left, right = U_LOW, U_HIGH
    fleft = flo
    root_run = None
    iterations = 0
    for iterations in range(1, MAX_BISECT + 1):
        mid = 0.5*(left + right)
        run = integrate(mid, nsteps, keep_crossing=True)
        if not run["finite"]:
            return {"bracket_ok": True, "lo": lo, "hi": hi, "root": None, "nonfinite_mid": mid}
        fm = run["endpoint"]["E"] - 1.0
        root_run = run
        if abs(fm) <= ROOT_E_TOL or (right-left) <= ROOT_WIDTH_TOL:
            break
        if fleft*fm <= 0.0:
            right = mid
        else:
            left = mid
            fleft = fm
    return {
        "bracket_ok": True,
        "lo": lo,
        "hi": hi,
        "root": root_run,
        "iterations": iterations,
        "final_bracket_width": right-left,
    }


def symrel(a, b):
    return abs(a-b)/max(abs(a), abs(b), 1e-12)


def main(output):
    prior = json.loads(K3C0_PATH.read_text(encoding="utf-8"))
    assert prior["classification"] == "M13B_K3C0_PUBLIC_UNIT_BINDING_NOT_ESTABLISHED_LITERAL_PLANCK_READING_INCONSISTENT"
    rho_crit_mp4 = prior["conversion"]["rho_crit0_over_Mp4"]

    lanes = {"coarse": solve_u0(4000), "fine": solve_u0(8000)}
    roots_ok = all(lanes[k]["root"] is not None for k in lanes)

    checks = {
        "coarse_bracket_straddles": lanes["coarse"]["bracket_ok"],
        "fine_bracket_straddles": lanes["fine"]["bracket_ok"],
    }

    if roots_ok:
        cr = lanes["coarse"]["root"]
        fr = lanes["fine"]["root"]
        ce = cr["endpoint"]
        fe = fr["endpoint"]
        omega_target = 1.0 - OMEGA_M0 - OMEGA_R0
        coarse_cross = cr["crossings"]
        fine_cross = fr["crossings"]
        u_rel = symrel(cr["u0"], fr["u0"])
        endpoint_rel = {
            key: symrel(ce[key], fe[key]) for key in ("x", "p", "y", "q", "E")
        }
        max_endpoint_rel = max(endpoint_rel.values())
        crossing_converged = len(coarse_cross) == 1 and len(fine_cross) == 1
        z_cross_diff = (
            abs(coarse_cross[0]["z"] - fine_cross[0]["z"])
            if crossing_converged else float("inf")
        )
        checks.update({
            "coarse_root_closure": abs(ce["E"]-1.0) <= 1e-10,
            "fine_root_closure": abs(fe["E"]-1.0) <= 1e-10,
            "coarse_flat_scalar_closure": abs(ce["Omega_DE"]-omega_target) <= 2e-10,
            "fine_flat_scalar_closure": abs(fe["Omega_DE"]-omega_target) <= 2e-10,
            "coarse_finite_positive_background": cr["finite"] and cr["min_E2"] > 0.0 and cr["min_denom"] > 0.5,
            "fine_finite_positive_background": fr["finite"] and fr["min_E2"] > 0.0 and fr["min_denom"] > 0.5,
            "fine_phantom_phase_develops": fr["min_D"] < -1e-6,
            "fine_exactly_one_later_crossing": len(fine_cross) == 1 and 0.0 < fine_cross[0]["z"] < 5.0,
            "fine_quintessence_phase_survives_today": fe["D"] > 1e-4,
            "amplitude_coarse_fine_converged": u_rel <= 1e-6,
            "crossing_redshift_coarse_fine_converged": z_cross_diff <= 1e-3,
            "endpoint_coarse_fine_converged": max_endpoint_rel <= 1e-6,
            "no_author_amplitude_reassignment": True,
            "no_promotion_leakage": True,
        })

        fine_u0 = fr["u0"]
        implied_v0_mp4 = rho_crit_mp4 * fine_u0
        public_ratio = implied_v0_mp4 / PUBLIC_V0_MP4
        numerics = {
            "coarse_U0": cr["u0"],
            "fine_U0": fine_u0,
            "U0_symmetric_relative_difference": u_rel,
            "coarse_E0": ce["E"],
            "fine_E0": fe["E"],
            "target_Omega_DE0": omega_target,
            "coarse_Omega_DE0": ce["Omega_DE"],
            "fine_Omega_DE0": fe["Omega_DE"],
            "coarse_crossings": coarse_cross,
            "fine_crossings": fine_cross,
            "crossing_redshift_absolute_difference": z_cross_diff,
            "endpoint_symmetric_relative_differences": endpoint_rel,
            "max_endpoint_symmetric_relative_difference": max_endpoint_rel,
            "fine_min_D": fr["min_D"],
            "fine_final_D": fe["D"],
            "fine_min_1_minus_D_over_6": fr["min_denom"],
            "fine_min_E2": fr["min_E2"],
            "fine_endpoint": fe,
            "implied_independent_V0_over_Mp4": implied_v0_mp4,
            "implied_to_public_V0_label_ratio_report_only": public_ratio,
        }
    else:
        numerics = {"roots_ok": False}
        checks.update({
            "coarse_root_closure": False,
            "fine_root_closure": False,
            "no_author_amplitude_reassignment": True,
            "no_promotion_leakage": True,
        })

    passed = roots_ok and all(bool(v) for v in checks.values())
    classification = (
        "M13B_K3C1_INDEPENDENT_CRITICAL_DENSITY_BACKGROUND_CLOSURE_PASS_WITH_SCOPE"
        if passed else
        ("M13B_K3C1_INDEPENDENT_BACKGROUND_IMPLEMENTATION_BLOCKED"
         if not roots_ok or not checks["coarse_bracket_straddles"] or not checks["fine_bracket_straddles"]
         else "M13B_K3C1_INDEPENDENT_BACKGROUND_CLOSURE_NOT_ESTABLISHED")
    )

    result = {
        "schema": SCHEMA,
        "model_id": "M13b",
        "family_id": "F13",
        "gate": "K3C1",
        "protocol": PROTOCOL,
        "classification": classification,
        "all_required_checks_pass": passed,
        "checks": checks,
        "implementation_provenance": "independent_KMDSB_critical_density_normalized_background",
        "public_shape_seed_only": {
            "z_start": 5.0,
            "x_start_phi_over_Mp": X_START,
            "y_start_psi_over_Mp": Y_START,
            "s_hat": S_HAT,
            "p_start": 0.0,
            "q_start": 0.0,
        },
        "amplitude_boundary_condition": {
            "U_definition": "V/rho_crit0",
            "U0_frozen_bracket": [U_LOW, U_HIGH],
            "target": "E(N=0)=H/H0=1",
            "varied_quantities": ["U0 only"],
            "observational_likelihood_fit": False,
        },
        "lanes": lanes,
        "numerics": numerics,
        "author_normalization_map_claimed": False,
        "published_V0_reproduced": False,
        "original_provider_reproduced": False,
        "K3_state_ceiling": "PARTIAL",
        "K4_promoted": False,
        "K5_promoted": False,
        "physical_falsification": False,
        "next_authorized_gate": (
            "K3C2_INDEPENDENT_COSMOLOGY_SCALE_PERTURBATION_BRIDGE_PREREGISTRATION"
            if passed else "NONE_REVIEW_K3C1_BACKGROUND"
        ),
    }
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    main(args.output)
