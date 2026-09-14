#!/usr/bin/env python3
"""Apply frozen undamped self-consistent z=5 gauge-IVP recovery.

Requires the K3D2 qfield adapter, native z=5 perturbation interval split, and
mapping-certified 12-ULP tau seam.  At the exact native boundary this inserts
only a pure Picard iteration between the copied perturbation state and the
unchanged CLASS Einstein constraints.  No physical RHS or tolerance is edited.
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
    if "KMDSB_GAUGE_IVP" in before:
        raise RuntimeError("another gauge-IVP recovery is already present")

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
        raise RuntimeError(f"expected one vector-init/evolver anchor, found {before.count(anchor)}")

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

    /* KMDSB K3D2-C self-consistent recovery: solve only the already-frozen
       inverse gauge-map boundary identity against the unchanged CLASS Einstein
       constraints with a pure undamped Picard iteration. */
    if ((inserted_handoff_kmdsb == _TRUE_) &&
        (interval_limit[index_interval] == tau_handoff_kmdsb) &&
        (ppt->has_scalars == _TRUE_) &&
        (index_md == ppt->index_md_scalars) &&
        ((pba->has_qcf == _TRUE_) || (pba->has_qpf == _TRUE_))) {
      const double gauge_ivp_tol_kmdsb = 1.e-12;
      const int gauge_ivp_max_iterations_kmdsb = 16;
      int gauge_ivp_iter_kmdsb;
      int gauge_ivp_converged_kmdsb = _FALSE_;
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

      a_ivp_kmdsb = ppw->pvecback[pba->index_bg_a];
      a2_ivp_kmdsb = a_ivp_kmdsb*a_ivp_kmdsb;
      aH_ivp_kmdsb = a_ivp_kmdsb*ppw->pvecback[pba->index_bg_H];
      if (pba->has_qcf == _TRUE_) {
        phi_prime_ivp_kmdsb = ppw->pvecback[pba->index_bg_phi_prime_qcf];
        Vphi_ivp_kmdsb = ppw->pvecback[pba->index_bg_dV_qcf];
      }
      if (pba->has_qpf == _TRUE_) {
        psi_prime_ivp_kmdsb = ppw->pvecback[pba->index_bg_psi_prime_qpf];
        Vpsi_ivp_kmdsb = ppw->pvecback[pba->index_bg_dV_qpf];
      }

      class_test((isfinite(a_ivp_kmdsb) == 0) ||
                 (isfinite(aH_ivp_kmdsb) == 0) ||
                 (aH_ivp_kmdsb == 0.) ||
                 (isfinite(phi_prime_ivp_kmdsb) == 0) ||
                 (isfinite(psi_prime_ivp_kmdsb) == 0) ||
                 (isfinite(Vphi_ivp_kmdsb) == 0) ||
                 (isfinite(Vpsi_ivp_kmdsb) == 0),
                 ppt->error_message,
                 "KMDSB non-finite/zero background input in frozen gauge-IVP fixed point");

      /* Seed alpha and alpha' from the copied exact-boundary state. */
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

      for (gauge_ivp_iter_kmdsb=1;
           gauge_ivp_iter_kmdsb<=gauge_ivp_max_iterations_kmdsb;
           gauge_ivp_iter_kmdsb++) {

        alpha_ivp_kmdsb = ppw->pvecmetric[ppw->index_mt_alpha];
        alpha_prime_ivp_kmdsb = ppw->pvecmetric[ppw->index_mt_alpha_prime];

        class_test((isfinite(alpha_ivp_kmdsb) == 0) ||
                   (isfinite(alpha_prime_ivp_kmdsb) == 0),
                   ppt->error_message,
                   "KMDSB non-finite metric input in gauge-IVP fixed point at iteration %d",
                   gauge_ivp_iter_kmdsb);

        /* Exact inverse of the frozen K3D2-B Newtonian transform.  This is a
           full overwrite, not a relaxed/damped update. */
        if (pba->has_qcf == _TRUE_) {
          ppw->pv->y[ppw->pv->index_pt_phi_qcf] =
            -alpha_ivp_kmdsb*phi_prime_ivp_kmdsb;
          ppw->pv->y[ppw->pv->index_pt_phi_prime_qcf] =
            2.*aH_ivp_kmdsb*alpha_ivp_kmdsb*phi_prime_ivp_kmdsb
            + a2_ivp_kmdsb*Vphi_ivp_kmdsb*alpha_ivp_kmdsb
            - phi_prime_ivp_kmdsb*alpha_prime_ivp_kmdsb;
        }
        if (pba->has_qpf == _TRUE_) {
          ppw->pv->y[ppw->pv->index_pt_psi_qpf] =
            -alpha_ivp_kmdsb*psi_prime_ivp_kmdsb;
          ppw->pv->y[ppw->pv->index_pt_psi_prime_qpf] =
            2.*aH_ivp_kmdsb*alpha_ivp_kmdsb*psi_prime_ivp_kmdsb
            - a2_ivp_kmdsb*Vpsi_ivp_kmdsb*alpha_ivp_kmdsb
            - psi_prime_ivp_kmdsb*alpha_prime_ivp_kmdsb;
        }

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
        dxN_ivp_kmdsb = 0.;
        rN_ivp_kmdsb = 0.;
        dyN_ivp_kmdsb = 0.;
        tN_ivp_kmdsb = 0.;

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

        class_test((isfinite(alpha_ivp_kmdsb) == 0) ||
                   (isfinite(alpha_prime_ivp_kmdsb) == 0) ||
                   (isfinite(dxN_ivp_kmdsb) == 0) ||
                   (isfinite(rN_ivp_kmdsb) == 0) ||
                   (isfinite(dyN_ivp_kmdsb) == 0) ||
                   (isfinite(tN_ivp_kmdsb) == 0) ||
                   (isfinite(max_residual_ivp_kmdsb) == 0),
                   ppt->error_message,
                   "KMDSB non-finite residual in gauge-IVP fixed point at iteration %d",
                   gauge_ivp_iter_kmdsb);

        if ((index_k == 0) && (index_ic == 0))
          fprintf(stderr,
                  "KMDSB_GAUGE_IVP_FIXED iter=%d tau=%.17g a=%.17g phip=%.17g psip=%.17g alpha=%.17g alphap=%.17g dxN=%.17g rN=%.17g dyN=%.17g tN=%.17g max=%.17g\n",
                  gauge_ivp_iter_kmdsb,tau_handoff_kmdsb,a_ivp_kmdsb,
                  phi_prime_ivp_kmdsb,psi_prime_ivp_kmdsb,
                  alpha_ivp_kmdsb,alpha_prime_ivp_kmdsb,
                  dxN_ivp_kmdsb,rN_ivp_kmdsb,dyN_ivp_kmdsb,tN_ivp_kmdsb,
                  max_residual_ivp_kmdsb);

        if (max_residual_ivp_kmdsb <= gauge_ivp_tol_kmdsb) {
          gauge_ivp_converged_kmdsb = _TRUE_;
          break;
        }
      }

      if ((index_k == 0) && (index_ic == 0))
        fprintf(stderr,
                "KMDSB_GAUGE_IVP_FIXED_FINAL converged=%d iterations=%d max=%.17g tol=%.17g\n",
                gauge_ivp_converged_kmdsb,
                gauge_ivp_iter_kmdsb <= gauge_ivp_max_iterations_kmdsb ? gauge_ivp_iter_kmdsb : gauge_ivp_max_iterations_kmdsb,
                max_residual_ivp_kmdsb,gauge_ivp_tol_kmdsb);

      class_test(gauge_ivp_converged_kmdsb == _FALSE_,
                 ppt->error_message,
                 "KMDSB self-consistent gauge-IVP fixed point did not reach %.17g within %d undamped iterations; final residual %.17g",
                 gauge_ivp_tol_kmdsb,gauge_ivp_max_iterations_kmdsb,max_residual_ivp_kmdsb);
    }

    /** - --> (d) integrate the perturbations over the current interval. */
'''

    after = before.replace(anchor, insertion, 1)
    guards = {
        "iterative_diagnostic_unique": after.count("KMDSB_GAUGE_IVP_FIXED iter=") == 1,
        "final_diagnostic_unique": after.count("KMDSB_GAUGE_IVP_FIXED_FINAL") == 1,
        "tolerance_unique": after.count("gauge_ivp_tol_kmdsb = 1.e-12") == 1,
        "iteration_cap_unique": after.count("gauge_ivp_max_iterations_kmdsb = 16") == 1,
        "certified_seam_unique": after.count("expected_cert_ulps_kmdsb = 12") == 1,
    }
    if not all(guards.values()):
        raise RuntimeError(f"post-transform guards failed: {guards}")

    path.write_text(after)
    manifest = {
        "schema": "KMDSB.W03.M13b.K3D2CSelfConsistentGaugeIVPPatch.v0.1",
        "changed_files": ["source/perturbations.c"],
        "provider_source_sha256_before": digest(before),
        "provider_source_sha256_after": digest(after),
        "algorithm": "pure_undamped_picard",
        "max_iterations": 16,
        "identity_raw_tolerance": 1e-12,
        "full_overwrite_each_iteration": True,
        "damping": False,
        "relaxation_coefficient": None,
        "line_search": False,
        "newton_or_jacobian_fit": False,
        "endpoint_data_used": False,
        "per_mode_fitted_parameters": False,
        "inverse_gauge_map": {
            "delta_x_S": "-alpha*phi_prime",
            "delta_x_prime_S": "2*aH*alpha*phi_prime + a^2*V_phi*alpha - phi_prime*alpha_prime",
            "delta_y_S": "-alpha*psi_prime",
            "delta_y_prime_S": "2*aH*alpha*psi_prime - a^2*V_psi*alpha - psi_prime*alpha_prime",
        },
        "recomputes_existing_einstein_constraints_each_iteration": True,
        "changes_background_equations": False,
        "changes_qfield_rhs": False,
        "changes_qfield_stress_energy": False,
        "changes_einstein_equations": False,
        "changes_boltzmann_hierarchy": False,
        "changes_thermodynamics": False,
        "changes_solver_family": False,
        "changes_integration_tolerances": False,
        "changes_model_or_cosmology_parameters": False,
        "new_free_parameters": 0,
        "manual_endpoint_sign_flip": False,
        "guards": guards,
    }
    if args.manifest:
        Path(args.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
