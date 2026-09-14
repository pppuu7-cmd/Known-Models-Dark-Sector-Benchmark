#!/usr/bin/env python3
"""Enrich the already-authorized RK failure diagnostics with component attribution.

Requires the K3D2-B collapse-geometry patch and direct-mode failure trace to be
applied first.  Only diagnostic workspace fields, duplicate error-ratio scans,
and error-message text are added.  Solver branches, states, tolerances and
physical equations are unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--manifest")
    args = ap.parse_args()
    root = Path(args.root)
    header = root / "include/dei_rkck.h"
    rk = root / "tools/dei_rkck.c"
    pt = root / "source/perturbations.c"
    h0 = header.read_text()
    r0 = rk.read_text()
    p0 = pt.read_text()

    # Diagnostic-only fields in the generic RK workspace.
    h_anchor = """  double stepmin;\n\n  /**\n    * zone for writing error messages\n    */\n"""
    if h0.count(h_anchor) != 1:
        raise RuntimeError("unique dei_rkck workspace anchor not found")
    h_insert = """  double stepmin;\n\n  /* KMDSB diagnostic-only RK error-control attribution. */\n  int kmdsb_rk_attempts;\n  int kmdsb_first_max_index;\n  int kmdsb_final_max_index;\n  double kmdsb_first_raw_ratio;\n  double kmdsb_first_errmax;\n  double kmdsb_final_raw_ratio;\n  double kmdsb_final_errmax;\n\n  /**\n    * zone for writing error messages\n    */\n"""
    h = h0.replace(h_anchor, h_insert, 1)

    # Reset diagnostics at each rkqs call without changing any numerical input.
    r_anchor = """  int i;\n  double errmax,h,htemp,xnew;\n\n  h=htry;\n  for (;;) {\n    class_call(rkck(*x,h,derivs,parameters_and_workspace_for_derivs,pgi),\n"""
    if r0.count(r_anchor) != 1:
        raise RuntimeError("unique rkqs declaration anchor not found")
    r_insert = """  int i;\n  double errmax,h,htemp,xnew;\n\n  pgi->kmdsb_rk_attempts=0;\n  pgi->kmdsb_first_max_index=-1;\n  pgi->kmdsb_final_max_index=-1;\n  pgi->kmdsb_first_raw_ratio=0.;\n  pgi->kmdsb_first_errmax=0.;\n  pgi->kmdsb_final_raw_ratio=0.;\n  pgi->kmdsb_final_errmax=0.;\n\n  h=htry;\n  for (;;) {\n    pgi->kmdsb_rk_attempts++;\n    class_call(rkck(*x,h,derivs,parameters_and_workspace_for_derivs,pgi),\n"""
    r = r0.replace(r_anchor, r_insert, 1)

    # Preserve the original errmax calculation exactly, then duplicate the scan
    # diagnostically to identify its maximizing component.
    err_anchor = """    errmax=0.0;\n    for (i=0;i<pgi->n;i++) errmax=MAX(errmax,fabs(pgi->yerr[i]/pgi->yscal[i]));\n    errmax /= eps;\n    if (errmax <= 1.0) break;\n"""
    if r.count(err_anchor) != 1:
        raise RuntimeError("unique rkqs errmax anchor not found")
    err_insert = """    errmax=0.0;\n    for (i=0;i<pgi->n;i++) errmax=MAX(errmax,fabs(pgi->yerr[i]/pgi->yscal[i]));\n    {\n      int kmdsb_max_index=0;\n      double kmdsb_max_ratio=0.;\n      double kmdsb_ratio;\n      for (i=0;i<pgi->n;i++) {\n        kmdsb_ratio=fabs(pgi->yerr[i]/pgi->yscal[i]);\n        if (kmdsb_ratio > kmdsb_max_ratio) {\n          kmdsb_max_ratio=kmdsb_ratio;\n          kmdsb_max_index=i;\n        }\n      }\n      if (pgi->kmdsb_rk_attempts == 1) {\n        pgi->kmdsb_first_max_index=kmdsb_max_index;\n        pgi->kmdsb_first_raw_ratio=kmdsb_max_ratio;\n      }\n      pgi->kmdsb_final_max_index=kmdsb_max_index;\n      pgi->kmdsb_final_raw_ratio=kmdsb_max_ratio;\n    }\n    errmax /= eps;\n    if (pgi->kmdsb_rk_attempts == 1) pgi->kmdsb_first_errmax=errmax;\n    pgi->kmdsb_final_errmax=errmax;\n    if (errmax <= 1.0) break;\n"""
    r = r.replace(err_anchor, err_insert, 1)

    # Enrich the already-authorized failure text with the first/final error-control
    # decomposition. The class_test condition and all solver variables are intact.
    fail_anchor = """    class_test(fabs(hnext/x1) <= hmin,\n\t       pgi->error_message,\n\t       \"KMDSB_RK_COLLAPSE x=%.17g step_ratio=%.17g minimum=%.17g hdid=%.17g hnext=%.17g step_index=%d interval=[%.17g:%.17g]\",\n\t       x,\n\t       fabs(hnext/x1),\n\t       hmin,\n\t       hdid,\n\t       hnext,\n\t       nstp,\n\t       x1,\n\t       x2);\n"""
    if r.count(fail_anchor) != 1:
        raise RuntimeError("authorized RK collapse text anchor not found")
    fail_insert = """    class_test(fabs(hnext/x1) <= hmin,\n\t       pgi->error_message,\n\t       \"KMDSB_RK_COLLAPSE x=%.17g step_ratio=%.17g minimum=%.17g hdid=%.17g hnext=%.17g step_index=%d interval=[%.17g:%.17g] attempts=%d first_max_index=%d first_raw_ratio=%.17g first_errmax=%.17g final_max_index=%d final_raw_ratio=%.17g final_errmax=%.17g final_yerr=%.17g final_yscal=%.17g final_y=%.17g final_start_dydx=%.17g\",\n\t       x,\n\t       fabs(hnext/x1),\n\t       hmin,\n\t       hdid,\n\t       hnext,\n\t       nstp,\n\t       x1,\n\t       x2,\n               pgi->kmdsb_rk_attempts,\n               pgi->kmdsb_first_max_index,\n               pgi->kmdsb_first_raw_ratio,\n               pgi->kmdsb_first_errmax,\n               pgi->kmdsb_final_max_index,\n               pgi->kmdsb_final_raw_ratio,\n               pgi->kmdsb_final_errmax,\n               pgi->yerr[pgi->kmdsb_final_max_index],\n               pgi->yscal[pgi->kmdsb_final_max_index],\n               pgi->y[pgi->kmdsb_final_max_index],\n               pgi->dydx[pgi->kmdsb_final_max_index]);\n"""
    r = r.replace(fail_anchor, fail_insert, 1)

    # Append only integer index metadata to the existing mode failure line.
    p_anchor = """      fprintf(stderr,\"KMDSB_MODE_FAIL index_md=%d index_ic=%d index_k=%d k=%.17g interval_start=%.17g evolver_start=%.17g interval_end=%.17g error=%s\\n\",\n              index_md,index_ic,index_k,k,\n              interval_limit[index_interval],interval_start_kmdsb,\n              interval_limit[index_interval+1],kmdsb_error_flat);\n"""
    if p0.count(p_anchor) != 1:
        raise RuntimeError("direct mode failure wrapper anchor not found")
    p_insert = """      fprintf(stderr,\"KMDSB_MODE_FAIL index_md=%d index_ic=%d index_k=%d k=%.17g interval_start=%.17g evolver_start=%.17g interval_end=%.17g pt_size=%d eta_i=%d dg_i=%d tg_i=%d sg_i=%d l3g_i=%d lmax_g=%d pol0g_i=%d lmax_pol_g=%d db_i=%d tb_i=%d dcdm_i=%d tcdm_i=%d dur_i=%d tur_i=%d sur_i=%d l3ur_i=%d lmax_ur=%d qcf_i=%d qcfp_i=%d qpf_i=%d qpfp_i=%d error=%s\\n\",\n              index_md,index_ic,index_k,k,\n              interval_limit[index_interval],interval_start_kmdsb,\n              interval_limit[index_interval+1],\n              ppw->pv->pt_size,ppw->pv->index_pt_eta,\n              ppw->pv->index_pt_delta_g,ppw->pv->index_pt_theta_g,ppw->pv->index_pt_shear_g,ppw->pv->index_pt_l3_g,ppw->pv->l_max_g,\n              ppw->pv->index_pt_pol0_g,ppw->pv->l_max_pol_g,\n              ppw->pv->index_pt_delta_b,ppw->pv->index_pt_theta_b,\n              ppw->pv->index_pt_delta_cdm,ppw->pv->index_pt_theta_cdm,\n              ppw->pv->index_pt_delta_ur,ppw->pv->index_pt_theta_ur,ppw->pv->index_pt_shear_ur,ppw->pv->index_pt_l3_ur,ppw->pv->l_max_ur,\n              ppw->pv->index_pt_phi_qcf,ppw->pv->index_pt_phi_prime_qcf,\n              ppw->pv->index_pt_psi_qpf,ppw->pv->index_pt_psi_prime_qpf,\n              kmdsb_error_flat);\n"""
    p = p0.replace(p_anchor, p_insert, 1)

    header.write_text(h)
    rk.write_text(r)
    pt.write_text(p)
    manifest = {
        "schema": "KMDSB.W03.M13b.K3D2ERKErrorComponentProbePatch.v0.1",
        "changed_files": ["include/dei_rkck.h", "tools/dei_rkck.c", "source/perturbations.c"],
        "diagnostic_only": True,
        "preserves_original_errmax_calculation": True,
        "duplicate_component_scan_only": True,
        "records_first_attempt_component": True,
        "records_final_accepted_component": True,
        "records_attempt_count": True,
        "records_runtime_perturbation_index_map": True,
        "changes_equations": False,
        "changes_state_vector": False,
        "changes_tolerances": False,
        "changes_minimum_variation": False,
        "changes_solver_logic": False,
        "changes_solver_family": False,
        "header_sha256_before": sha(h0),
        "header_sha256_after": sha(h),
        "rk_sha256_before": sha(r0),
        "rk_sha256_after": sha(r),
        "perturbations_sha256_before": sha(p0),
        "perturbations_sha256_after": sha(p),
    }
    if args.manifest:
        Path(args.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
