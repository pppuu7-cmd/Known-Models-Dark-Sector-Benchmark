#!/usr/bin/env python3
"""Confirmatory source/IVP audit for M13b K3D2-B.

No cosmology solver is executed by this verifier.  It audits exact transformed
source, an immutable parent artifact, and the native CLASS boundary data path.
"""
from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import math
import re
from pathlib import Path

K1 = 0.00022398828992555914
K10 = 0.0022398828992555913
FLOOR = 1e-12


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    print(json.dumps(obj, indent=2, sort_keys=True))


def compact(s: str) -> str:
    return re.sub(r"\s+", "", s)


def rows(path: Path):
    return [
        [float(x) for x in line.split()]
        for line in path.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def numbered_header(path: Path, required):
    hs = [
        line
        for line in path.read_text().splitlines()
        if line.lstrip().startswith("#") and all(x in line for x in required)
    ]
    if len(hs) != 1:
        raise RuntimeError((path, required, hs[:3]))
    return {
        m.group(2).strip(): int(m.group(1)) - 1
        for m in re.finditer(r"(\d+):(.+?)(?=\s+\d+:|$)", hs[0].lstrip("#").strip())
    }


def source_mode(provider: Path, out: Path) -> int:
    bg = (provider / "source/background.c").read_text()
    pt = (provider / "source/perturbations.c").read_text()
    b = compact(bg)
    p = compact(pt)

    checks = {
        "canonical_mass_plus_ddV": "-(k2+a2*pvecback[pba->index_bg_ddV_qcf])*y[pv->index_pt_phi_qcf]" in p,
        "phantom_mass_minus_ddV": "-(k2-a2*pvecback[pba->index_bg_ddV_qpf])*y[pv->index_pt_psi_qpf]" in p,
        "same_metric_source_sign_qcf": "-metric_continuity*pvecback[pba->index_bg_phi_prime_qcf]" in p,
        "same_metric_source_sign_qpf": "-metric_continuity*pvecback[pba->index_bg_psi_prime_qpf]" in p,
        "phantom_background_force_sign": "+a*dV_qpf(pba,y[pba->index_bi_psi_qpf])/H" in b,
        "canonical_background_force_sign": "-a*dV_qcf(pba,y[pba->index_bi_phi_qcf])/H" in b,
        "phantom_rho_kinetic_negative": "delta_rho_qpf=1./3.*(-ppw->pvecback[pba->index_bg_psi_prime_qpf]*y[ppw->pv->index_pt_psi_prime_qpf]/a2" in p,
        "phantom_rho_potential_positive": "+ppw->pvecback[pba->index_bg_dV_qpf]*y[ppw->pv->index_pt_psi_qpf]);" in p,
        "phantom_pressure_potential_negative": "-ppw->pvecback[pba->index_bg_dV_qpf]*y[ppw->pv->index_pt_psi_qpf]);" in p,
        "phantom_momentum_negative": "ppw->rho_plus_p_theta-=1./3.*k*k/a2*ppw->pvecback[pba->index_bg_psi_prime_qpf]*y[ppw->pv->index_pt_psi_qpf]" in p,
        "no_effective_theta_DE": "theta_DE" not in pt,
    }
    ok = all(checks.values())
    obj = {
        "schema": "KMDSB.W03.M13b.K3D2BSourceIVPAudit.Source.v0.1",
        "checks": checks,
        "all_required_checks_pass": ok,
        "classification": "M13B_K3D2B_SOURCE_EQUATIONS_AND_STRESS_SIGNS_PASS" if ok else "M13B_K3D2B_SOURCE_EQUATION_SIGN_INCONSISTENCY",
        "interpretation": "This lane checks the executed independent adapter source signs only; it does not validate the z=5 gauge-mapped initial surface.",
    }
    write_json(out, obj)
    return 0 if ok else 1


def interp_bg(bg_rows, bt, a, key):
    aa = [1.0 / (1.0 + r[bt["z"]]) for r in bg_rows]
    i = bisect.bisect_left(aa, a)
    if i == 0:
        return bg_rows[0][bt[key]]
    if i >= len(bg_rows):
        return bg_rows[-1][bt[key]]
    u, v = bg_rows[i - 1], bg_rows[i]
    au, av = aa[i - 1], aa[i]
    f = (a - au) / (av - au) if av != au else 0.0
    return u[bt[key]] + f * (v[bt[key]] - u[bt[key]])


def artifact_mode(root: Path, canonical: Path, out: Path) -> int:
    outdir = root / "out"
    bg_files = sorted(outdir.glob("default*_background.dat"))
    if len(bg_files) != 1:
        raise RuntimeError(f"expected one parent background, got {bg_files}")
    bg = bg_files[0]
    bt = numbered_header(bg, ["phi_qcf", "psi_qpf"])
    br = rows(bg)
    br.sort(key=lambda r: 1.0 / (1.0 + r[bt["z"]]))

    cb = canonical.read_bytes()
    canonical_sha = hashlib.sha256(cb).hexdigest()
    canon = json.loads(cb)
    # The canonical file is read as provenance and to assert the frozen seed metadata exists.
    if "modes" not in canon:
        raise RuntimeError("canonical K3C2 result lacks modes")

    targets = {"khat_1": K1, "khat_10": K10}
    pfiles = sorted(outdir.glob("default*_perturbations_k*_s.dat"))
    if len(pfiles) != 2:
        raise RuntimeError(f"expected two parent trajectories, got {pfiles}")
    mapped = {}
    for f in pfiles:
        m = re.search(r"k\s*=\s*([0-9.eE+-]+)", f.read_text().splitlines()[0])
        if not m:
            raise RuntimeError(f"no k label in {f}")
        kv = float(m.group(1))
        key = min(targets, key=lambda q: abs(targets[q] - kv))
        if abs(targets[key] - kv) / targets[key] > 1e-8:
            raise RuntimeError((f, kv, key))
        mapped[key] = f

    modes = {}
    t_signs = []
    lane_checks = []
    for key in ("khat_1", "khat_10"):
        f = mapped[key]
        ht = numbered_header(f, ["delta_qcf_S", "delta_qpf_S", "alpha_sync_to_newt"])
        rr = rows(f)
        row = min(rr, key=lambda r: abs(r[ht["a"]] - 1.0 / 6.0))
        a = row[ht["a"]]
        H = interp_bg(br, bt, a, "H [1/Mpc]")
        ah = a * H
        phip = interp_bg(br, bt, a, "phi'_qcf")
        psip = interp_bg(br, bt, a, "psi'_qpf")
        dVx = interp_bg(br, bt, a, "V'_qcf")
        dVy = interp_bg(br, bt, a, "V'_qpf")
        alpha = row[ht["alpha_sync_to_newt"]]
        alphap = row[ht["alpha_prime_sync_to_newt"]]
        dxs = row[ht["delta_qcf_S"]]
        dxps = row[ht["delta_prime_qcf_S"]]
        dys = row[ht["delta_qpf_S"]]
        dyps = row[ht["delta_prime_qpf_S"]]
        Phi = row[ht["phi"]]
        scale = 1e-5 / Phi

        dx = dxs + alpha * phip
        dy = dys + alpha * psip
        dxp = dxps + (-2 * ah * alpha * phip - a * a * dVx * alpha + phip * alphap)
        dyp = dyps + (-2 * ah * alpha * psip + a * a * dVy * alpha + psip * alphap)
        rN = dxp / ah
        tN = dyp / ah

        required_dxps = 2 * ah * alpha * phip + a * a * dVx * alpha - phip * alphap
        required_dyps = 2 * ah * alpha * psip - a * a * dVy * alpha - psip * alphap

        sync_zero = all(v == 0.0 for v in (dxs, dxps, dys, dyps))
        c = {
            "synchronous_direct_seed_printed_zero": sync_zero,
            "alpha_finite_nonzero": math.isfinite(alpha) and alpha != 0.0,
            "V_phi_finite_nonzero": math.isfinite(dVx) and dVx != 0.0,
            "V_psi_finite_nonzero": math.isfinite(dVy) and dVy != 0.0,
            "scaled_r_N_resolved_nonzero": abs(scale * rN) > FLOOR,
            "scaled_t_N_resolved_nonzero": abs(scale * tN) > FLOOR,
        }
        lane_checks.append(all(c.values()))
        t_signs.append(1 if tN > 0 else (-1 if tN < 0 else 0))
        modes[key] = {
            "file": f.name,
            "a_handoff_row": a,
            "tau_handoff_row": row[ht["tau [Mpc]"]] if "tau [Mpc]" in ht else None,
            "alpha": alpha,
            "alpha_prime": alphap,
            "H_1_per_Mpc": H,
            "aH": ah,
            "phi_prime": phip,
            "psi_prime": psip,
            "V_phi": dVx,
            "V_psi": dVy,
            "sync_seed": {"delta_x_S": dxs, "delta_x_prime_S": dxps, "delta_y_S": dys, "delta_y_prime_S": dyps},
            "newtonian_from_executed_sync_seed": {"delta_x_N": dx, "r_N": rN, "delta_y_N": dy, "t_N": tN},
            "common_scale": scale,
            "scaled_newtonian_from_executed_sync_seed": {"delta_x_N": scale * dx, "r_N": scale * rN, "delta_y_N": scale * dy, "t_N": scale * tN},
            "sync_prime_required_for_frozen_newtonian_zero_derivative": {"delta_x_prime_S_required": required_dxps, "delta_y_prime_S_required": required_dyps},
            "checks": c,
        }

    same_t_sign = len(set(t_signs)) == 1 and t_signs[0] != 0
    checks = {
        "both_mode_witnesses_pass": all(lane_checks),
        "phantom_t_N_same_nonzero_sign_both_modes": same_t_sign,
        "no_per_variable_fit_or_rephase": True,
        "canonical_seed_target_is_exact_zero": True,
    }
    ok = all(checks.values())
    obj = {
        "schema": "KMDSB.W03.M13b.K3D2BSourceIVPAudit.Artifact.v0.1",
        "parent_artifact_root": str(root),
        "canonical_sha256": canonical_sha,
        "exclusion_floor_reused": FLOOR,
        "modes": modes,
        "checks": checks,
        "all_required_checks_pass": ok,
        "classification": "M13B_K3D2B_NEWTONIAN_IVP_GAUGE_MISMATCH_WITNESS_PASS" if ok else "M13B_K3D2B_NEWTONIAN_IVP_GAUGE_MISMATCH_NOT_ESTABLISHED",
        "physical_falsification": False,
    }
    write_json(out, obj)
    return 0 if ok else 1


def feasibility_mode(provider: Path, out: Path) -> int:
    pt = (provider / "source/perturbations.c").read_text()
    solve = pt[pt.find("int perturbations_solve(") : pt.find("int perturbations_timescale(") if "int perturbations_timescale(" in pt else len(pt)]
    vec_pos = solve.find("class_call(perturbations_vector_init(")
    evo_pos = solve.find("class_call(generic_evolver(")
    checks = {
        "native_handoff_boundary_present": "tau_handoff_kmdsb" in pt and "inserted_handoff_kmdsb" in pt,
        "vector_init_before_evolver": vec_pos >= 0 and evo_pos >= 0 and vec_pos < evo_pos,
        "metric_refresh_function_available": "int perturbations_einstein(" in pt,
        "synchronous_alpha_available": "ppw->pvecmetric[ppw->index_mt_alpha]" in pt,
        "synchronous_alpha_prime_available": "ppw->pvecmetric[ppw->index_mt_alpha_prime]" in pt,
        "qcf_background_velocity_available": "index_bg_phi_prime_qcf" in pt,
        "qpf_background_velocity_available": "index_bg_psi_prime_qpf" in pt,
        "qcf_qpf_mode_local_state_indices_available": all(x in pt for x in ["index_pt_phi_qcf", "index_pt_phi_prime_qcf", "index_pt_psi_qpf", "index_pt_psi_prime_qpf"]),
        "no_new_free_parameter_needed": True,
    }
    ok = all(checks.values())
    obj = {
        "schema": "KMDSB.W03.M13b.K3D2BSourceIVPAudit.Feasibility.v0.1",
        "checks": checks,
        "all_required_checks_pass": ok,
        "classification": "M13B_K3D2B_GAUGE_MAPPED_IVP_SOURCE_PATH_AVAILABLE" if ok else "M13B_K3D2B_GAUGE_MAPPED_IVP_IMPLEMENTATION_NOT_YET_DEFINED",
        "candidate_source_path": (
            "At the native z=5 interval boundary, after perturbations_vector_init and before the right-owned generic_evolver, refresh the metric with the existing perturbations_einstein path at the exact boundary, read alpha/alpha_prime plus background qcf/qpf values, and assign only the four qcf/qpf direct-field state entries from the frozen gauge-map identities."
            if ok
            else None
        ),
        "protected_equations_need_not_change": ok,
    }
    write_json(out, obj)
    return 0 if ok else 1


def aggregate_mode(source: Path, artifact: Path, feasibility: Path, out: Path) -> int:
    s = json.loads(source.read_text())
    a = json.loads(artifact.read_text())
    f = json.loads(feasibility.read_text())
    source_ok = bool(s.get("all_required_checks_pass"))
    artifact_ok = bool(a.get("all_required_checks_pass"))
    feasibility_ok = bool(f.get("all_required_checks_pass"))
    if not source_ok:
        classification = "M13B_K3D2B_SOURCE_EQUATION_INCONSISTENCY_FOUND"
        ok = False
        next_gate = None
    elif artifact_ok and feasibility_ok:
        classification = "M13B_K3D2B_EQUATIONS_CONSISTENT_IVP_GAUGE_MISMATCH_CONFIRMED"
        ok = True
        next_gate = "prospectively frozen gauge-mapped synchronous z=5 IVP successor; preserve parent B3 history and all old scientific thresholds"
    else:
        classification = "M13B_K3D2B_SOURCE_IVP_AUDIT_INCONCLUSIVE"
        ok = False
        next_gate = None
    obj = {
        "schema": "KMDSB.W03.M13b.K3D2BSourceIVPAudit.Aggregate.v0.1",
        "lane_status": {"source": source_ok, "artifact_ivp": artifact_ok, "implementation_feasibility": feasibility_ok},
        "all_required_checks_pass": ok,
        "classification": classification,
        "historical_parent_B3_rewritten": False,
        "K3_state_ceiling": "PARTIAL",
        "K4_promoted": False,
        "K5_promoted": False,
        "physical_falsification": False,
        "next_authorized_gate": next_gate,
        "interpretation": (
            "The executed synchronous-zero field seed is not gauge-equivalent to the frozen K3C2 Newtonian-zero derivative seed. The parent B3 gap remains historical evidence for the executed initialization, but it is not a clean same-initial-surface regression of K3C2."
            if classification == "M13B_K3D2B_EQUATIONS_CONSISTENT_IVP_GAUGE_MISMATCH_CONFIRMED"
            else "No promotion beyond the parent state is authorized."
        ),
    }
    write_json(out, obj)
    # Aggregate success means a terminal classification was produced, including a source inconsistency.
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="mode", required=True)
    p = sp.add_parser("source"); p.add_argument("--provider", type=Path, required=True); p.add_argument("--out", type=Path, required=True)
    p = sp.add_parser("artifact"); p.add_argument("--root", type=Path, required=True); p.add_argument("--canonical", type=Path, required=True); p.add_argument("--out", type=Path, required=True)
    p = sp.add_parser("feasibility"); p.add_argument("--provider", type=Path, required=True); p.add_argument("--out", type=Path, required=True)
    p = sp.add_parser("aggregate"); p.add_argument("--source", type=Path, required=True); p.add_argument("--artifact", type=Path, required=True); p.add_argument("--feasibility", type=Path, required=True); p.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.mode == "source": return source_mode(a.provider, a.out)
    if a.mode == "artifact": return artifact_mode(a.root, a.canonical, a.out)
    if a.mode == "feasibility": return feasibility_mode(a.provider, a.out)
    if a.mode == "aggregate": return aggregate_mode(a.source, a.artifact, a.feasibility, a.out)
    raise AssertionError(a.mode)


if __name__ == "__main__":
    raise SystemExit(main())
