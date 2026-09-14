#!/usr/bin/env python3
"""Apply the prospectively frozen M13b K3D2-C gauge-mapped z=5 IVP.

Requires the K3D2 adapter + native z=5 interval split + mapping-certified tau
seam to have been applied first.  Only the four direct qcf/qpf perturbation
state entries are assigned at the exact native handoff after vector_init and
before the right-owned evolver starts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--manifest")
    args = ap.parse_args()

    path = Path(args.root) / "source/perturbations.c"
    before = path.read_text()

    required_tokens = [
        "tau_handoff_kmdsb",
        "inserted_handoff_kmdsb",
        "expected_cert_ulps_kmdsb = 12",
        "index_pt_phi_qcf",
        "index_pt_phi_prime_qcf",
        "index_pt_psi_qpf",
        "index_pt_psi_prime_qpf",
        "index_bg_dV_qcf",
        "index_bg_dV_qpf",
    ]
    missing = [x for x in required_tokens if x not in before]
    if missing:
        raise RuntimeError(f"required frozen stack missing tokens: {missing}")

    anchor = '''    class_call(perturbations_vector_init(ppr,
                                         pba,
                                         pth,
                                         ppt,
                                         index_md,
                                         index_ic,
                                         k,
                                         interval_limit[index_interval],
                                         ppw,
                                         previous_approx),
               ppt->error_message,
               ppt->error_message);

    /** - --> (d) integrate the perturbations over the current interval. */
'''
    if before.count(anchor) != 1:
        raise RuntimeError(f"expected exactly one vector-init/evolver anchor, found {before.count(anchor)}")

    insertion = r'''    class_call(perturbations_vector_init(ppr,
                                         pba,
                                         pth,
                                         ppt,
                                         index_md,
                                         index_ic,
                                         k,
                                         interval_limit[index_interval],
                                         ppw,
                                         previous_approx),
               ppt->error_message,
               ppt->error_message);

    /* KMDSB K3D2-C: express the frozen K3C2 Newtonian zero qfield IVP
       in synchronous direct-field coordinates at the exact native z=5
       boundary.  No RHS, stress-energy, Einstein, hierarchy, solver, or
       tolerance equation is changed. */
    if ((inserted_handoff_kmdsb == _TRUE_) &&
        (interval_limit[index_interval] == tau_handoff_kmdsb) &&
        (ppt->has_scalars == _TRUE_) &&
        (index_md == ppt->index_md_scalars) &&
        ((pba->has_qcf == _TRUE_) || (pba->has_qpf == _TRUE_))) {
      const double gauge_ivp_tol_kmdsb = 1.e-12;
      double a_ivp_kmdsb;
      double a2_ivp_kmdsb;
      double aH_ivp_kmdsb;
      double alpha_ivp_kmdsb;
      double alpha_prime_ivp_kmdsb;
      double phi_prime_ivp_kmdsb = 0.;
      double psi_prime_ivp_kmdsb = 0.;
      double Vphi_ivp_kmdsb = 0.;
      double Vpsi_ivp_kmdsb = 0.;
      double dxN_ivp_kmdsb = 0.;
      double rN_ivp_kmdsb = 0.;
      double dyN_ivp_kmdsb = 0.;
      double tN_ivp_kmdsb = 0.;
      double max_residual_ivp_kmdsb = 0.;

      /* Refresh the exact-boundary background and thermodynamics through
         existing CLASS accessors before asking the unmodified Einstein
         constraint code for alpha and alpha'. */
      ppw->last_index_back = 0;
      class_call(background_at_tau(pba,
                                   tau_handoff_kmdsb,
                                   normal_info,
                                   inter_normal,
                                   &(ppw->last_index_back),
                                   ppw->pvecback),
                 pba->error_message,
                 ppt->error_message);
      ppw->last_index_thermo = 0;
      class_call(thermodynamics_at_z(pba,
                                     pth,
                                     1./ppw->pvecback[pba->index_bg_a]-1.,
                                     inter_normal,
                                     &(ppw->last_index_thermo),
                                     ppw->pvecback,
                                     ppw->pvecthermo),
                 pth->error_message,
                 ppt->error_message);
      class_call(perturbations_einstein(ppr,
                                        pba,
                                        pth,
                                        ppt,
                                        index_md,
                                        k,
                                        tau_handoff_kmdsb,
                                        ppw->pv->y,
                                        ppw),
                 ppt->error_message,
                 ppt->error_message);

      a_ivp_kmdsb = ppw->pvecback[pba->index_bg_a];
      a2_ivp_kmdsb = a_ivp_kmdsb*a_ivp_kmdsb;
      aH_ivp_kmdsb = a_ivp_kmdsb*ppw->pvecback[pba->index_bg_H];
      alpha_ivp_kmdsb = ppw->pvecmetric[ppw->index_mt_alpha];
      alpha_prime_ivp_kmdsb = ppw->pvecmetric[ppw->index_mt_alpha_prime];

      if (pba->has_qcf == _TRUE_) {
        phi_prime_ivp_kmdsb = ppw->pvecback[pba->index_bg_phi_prime_qcf];
        Vphi_ivp_kmdsb = ppw->pvecback[pba->index_bg_dV_qcf];
        ppw->pv->y[ppw->pv->index_pt_phi_qcf] = -alpha_ivp_kmdsb*phi_prime_ivp_kmdsb;
        ppw->pv->y[ppw->pv->index_pt_phi_prime_qcf] =
          2.*aH_ivp_kmdsb*alpha_ivp_kmdsb*phi_prime_ivp_kmdsb
          + a2_ivp_kmdsb*Vphi_ivp_kmdsb*alpha_ivp_kmdsb
          - phi_prime_ivp_kmdsb*alpha_prime_ivp_kmdsb;
      }

      if (pba->has_qpf == _TRUE_) {
        psi_prime_ivp_kmdsb = ppw->pvecback[pba->index_bg_psi_prime_qpf];
        Vpsi_ivp_kmdsb = ppw->pvecback[pba->index_bg_dV_qpf];
        ppw->pv->y[ppw->pv->index_pt_psi_qpf] = -alpha_ivp_kmdsb*psi_prime_ivp_kmdsb;
        ppw->pv->y[ppw->pv->index_pt_psi_prime_qpf] =
          2.*aH_ivp_kmdsb*alpha_ivp_kmdsb*psi_prime_ivp_kmdsb
          - a2_ivp_kmdsb*Vpsi_ivp_kmdsb*alpha_ivp_kmdsb
          - psi_prime_ivp_kmdsb*alpha_prime_ivp_kmdsb;
      }

      /* Recompute the unmodified Einstein constraints after the assignment.
         The exact frozen handoff should keep qfield stress perturbations zero
         on the boundary; any material metric feedback fails closed here. */
      class_call(perturbations_einstein(ppr,
                                        pba,
                                        pth,
                                        ppt,
                                        index_md,
                                        k,
                                        tau_handoff_kmdsb,
                                        ppw->pv->y,
                                        ppw),
                 ppt->error_message,
                 ppt->error_message);
      alpha_ivp_kmdsb = ppw->pvecmetric[ppw->index_mt_alpha];
      alpha_prime_ivp_kmdsb = ppw->pvecmetric[ppw->index_mt_alpha_prime];

      if (pba->has_qcf == _TRUE_) {
        dxN_ivp_kmdsb = ppw->pv->y[ppw->pv->index_pt_phi_qcf]
          + alpha_ivp_kmdsb*phi_prime_ivp_kmdsb;
        rN_ivp_kmdsb = (
          ppw->pv->y[ppw->pv->index_pt_phi_prime_qcf]
          - 2.*aH_ivp_kmdsb*alpha_ivp_kmdsb*phi_prime_ivp_kmdsb
          - a2_ivp_kmdsb*Vphi_ivp_kmdsb*alpha_ivp_kmdsb
          + phi_prime_ivp_kmdsb*alpha_prime_ivp_kmdsb
        )/aH_ivp_kmdsb;
      }
      if (pba->has_qpf == _TRUE_) {
        dyN_ivp_kmdsb = ppw->pv->y[ppw->pv->index_pt_psi_qpf]
          + alpha_ivp_kmdsb*psi_prime_ivp_kmdsb;
        tN_ivp_kmdsb = (
          ppw->pv->y[ppw->pv->index_pt_psi_prime_qpf]
          - 2.*aH_ivp_kmdsb*alpha_ivp_kmdsb*psi_prime_ivp_kmdsb
          + a2_ivp_kmdsb*Vpsi_ivp_kmdsb*alpha_ivp_kmdsb
          + psi_prime_ivp_kmdsb*alpha_prime_ivp_kmdsb
        )/aH_ivp_kmdsb;
      }

      max_residual_ivp_kmdsb = fabs(dxN_ivp_kmdsb);
      max_residual_ivp_kmdsb = MAX(max_residual_ivp_kmdsb,fabs(rN_ivp_kmdsb));
      max_residual_ivp_kmdsb = MAX(max_residual_ivp_kmdsb,fabs(dyN_ivp_kmdsb));
      max_residual_ivp_kmdsb = MAX(max_residual_ivp_kmdsb,fabs(tN_ivp_kmdsb));

      if ((index_k == 0) && (index_ic == 0))
        fprintf(stderr,
                "KMDSB_GAUGE_IVP tau=%.17g a=%.17g phip=%.17g psip=%.17g alpha=%.17g alphap=%.17g dxN=%.17g rN=%.17g dyN=%.17g tN=%.17g max=%.17g\n",
                tau_handoff_kmdsb,a_ivp_kmdsb,phi_prime_ivp_kmdsb,psi_prime_ivp_kmdsb,
                alpha_ivp_kmdsb,alpha_prime_ivp_kmdsb,dxN_ivp_kmdsb,rN_ivp_kmdsb,
                dyN_ivp_kmdsb,tN_ivp_kmdsb,max_residual_ivp_kmdsb);

      class_test(max_residual_ivp_kmdsb > gauge_ivp_tol_kmdsb,
                 ppt->error_message,
                 "KMDSB gauge-mapped z=5 IVP identity residual %.17g exceeds frozen %.17g",
                 max_residual_ivp_kmdsb,gauge_ivp_tol_kmdsb);
    }

    /** - --> (d) integrate the perturbations over the current interval. */
'''

    after = before.replace(anchor, insertion, 1)
    if after.count("KMDSB_GAUGE_IVP") != 1:
        raise RuntimeError("gauge-IVP diagnostic insertion failed")
    if after.count("gauge_ivp_tol_kmdsb = 1.e-12") != 1:
        raise RuntimeError("frozen identity tolerance missing")
    if after.count("expected_cert_ulps_kmdsb = 12") != 1:
        raise RuntimeError("certified 12-ULP seam no longer unique")

    path.write_text(after)
    manifest = {
        "schema": "KMDSB.W03.M13b.K3D2CGaugeMappedZ5IVPPatch.v0.1",
        "changed_files": ["source/perturbations.c"],
        "provider_source_sha256_before": digest(before),
        "provider_source_sha256_after": digest(after),
        "exact_native_boundary": True,
        "applied_after_vector_init": True,
        "applied_before_right_owned_evolver": True,
        "inverse_gauge_map": {
            "delta_x_S": "-alpha*phi_prime",
            "delta_x_prime_S": "2*aH*alpha*phi_prime + a^2*V_phi*alpha - phi_prime*alpha_prime",
            "delta_y_S": "-alpha*psi_prime",
            "delta_y_prime_S": "2*aH*alpha*psi_prime - a^2*V_psi*alpha - psi_prime*alpha_prime",
        },
        "identity_raw_tolerance": 1e-12,
        "recomputes_existing_einstein_constraints_after_assignment": True,
        "changes_background_equations": False,
        "changes_qfield_rhs": False,
        "changes_qfield_stress_energy": False,
        "changes_einstein_equations": False,
        "changes_boltzmann_hierarchy": False,
        "changes_thermodynamics": False,
        "changes_solver_family": False,
        "changes_tolerances": False,
        "changes_model_or_cosmology_parameters": False,
        "new_free_parameters": 0,
        "manual_endpoint_sign_flip": False,
    }
    if args.manifest:
        Path(args.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
