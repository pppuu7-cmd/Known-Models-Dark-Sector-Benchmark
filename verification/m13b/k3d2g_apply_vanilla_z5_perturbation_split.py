#!/usr/bin/env python3
"""Insert a diagnostic-only native CLASS perturbation interval split at z=5.

This transformer is intentionally independent of qcf/qpf and is used only by
K3D2-G to test whether hard interval re-entry alone reproduces the RK blocker.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--manifest")
    a = ap.parse_args()
    p = Path(a.root) / "source/perturbations.c"
    before = p.read_text()
    s = before

    anchor = "  free(interval_number_of);\n\n  /** - fill the structure containing all fixed parameters, indices"
    if s.count(anchor) != 1:
        raise RuntimeError("unique interval-construction anchor not found")

    block = '''  free(interval_number_of);

  /* KMDSB K3D2-G: diagnostic-only vanilla CLASS perturbation split at z=5.
     Duplicate the native approximation row across the inserted boundary. */
  double tau_split_kmdsb = -1.;
  int inserted_split_kmdsb = _FALSE_;
  {
    int old_interval_number_kmdsb = interval_number;
    int insert_index_kmdsb = -1;
    int ii_kmdsb, jj_kmdsb;
    double * new_interval_limit_kmdsb;
    int ** new_interval_approx_kmdsb;

    class_call(background_tau_of_z(pba,5.,&tau_split_kmdsb),
               pba->error_message,
               ppt->error_message);
    for (ii_kmdsb=0; ii_kmdsb<old_interval_number_kmdsb; ii_kmdsb++) {
      if ((interval_limit[ii_kmdsb] < tau_split_kmdsb) &&
          (tau_split_kmdsb < interval_limit[ii_kmdsb+1])) {
        insert_index_kmdsb = ii_kmdsb;
        break;
      }
    }

    if (insert_index_kmdsb >= 0) {
      class_alloc(new_interval_limit_kmdsb,(old_interval_number_kmdsb+2)*sizeof(double),ppt->error_message);
      class_alloc(new_interval_approx_kmdsb,(old_interval_number_kmdsb+1)*sizeof(int*),ppt->error_message);
      for (ii_kmdsb=0; ii_kmdsb<old_interval_number_kmdsb+1; ii_kmdsb++)
        class_alloc(new_interval_approx_kmdsb[ii_kmdsb],ppw->ap_size*sizeof(int),ppt->error_message);

      for (ii_kmdsb=0; ii_kmdsb<=insert_index_kmdsb; ii_kmdsb++)
        new_interval_limit_kmdsb[ii_kmdsb] = interval_limit[ii_kmdsb];
      new_interval_limit_kmdsb[insert_index_kmdsb+1] = tau_split_kmdsb;
      for (ii_kmdsb=insert_index_kmdsb+1; ii_kmdsb<=old_interval_number_kmdsb; ii_kmdsb++)
        new_interval_limit_kmdsb[ii_kmdsb+1] = interval_limit[ii_kmdsb];

      for (ii_kmdsb=0; ii_kmdsb<old_interval_number_kmdsb+1; ii_kmdsb++) {
        int src_interval_kmdsb = ii_kmdsb;
        if (ii_kmdsb > insert_index_kmdsb+1)
          src_interval_kmdsb = ii_kmdsb-1;
        else if (ii_kmdsb == insert_index_kmdsb+1)
          src_interval_kmdsb = insert_index_kmdsb;
        for (jj_kmdsb=0; jj_kmdsb<ppw->ap_size; jj_kmdsb++)
          new_interval_approx_kmdsb[ii_kmdsb][jj_kmdsb] = interval_approx[src_interval_kmdsb][jj_kmdsb];
      }

      for (ii_kmdsb=0; ii_kmdsb<old_interval_number_kmdsb; ii_kmdsb++)
        free(interval_approx[ii_kmdsb]);
      free(interval_approx);
      free(interval_limit);
      interval_limit = new_interval_limit_kmdsb;
      interval_approx = new_interval_approx_kmdsb;
      interval_number = old_interval_number_kmdsb+1;
      inserted_split_kmdsb = _TRUE_;
    }
  }

  /** - fill the structure containing all fixed parameters, indices'''
    s = s.replace(anchor, block)

    anchor2 = '''    class_call(generic_evolver(perturbations_derivs,
                               interval_limit[index_interval],
                               interval_limit[index_interval+1],'''
    if s.count(anchor2) != 1:
        raise RuntimeError("unique perturbation evolver call not found")
    repl2 = '''    double interval_start_kmdsb = interval_limit[index_interval];
    if ((inserted_split_kmdsb == _TRUE_) &&
        (interval_limit[index_interval] == tau_split_kmdsb))
      interval_start_kmdsb = nextafter(tau_split_kmdsb,interval_limit[index_interval+1]);

    class_call(generic_evolver(perturbations_derivs,
                               interval_start_kmdsb,
                               interval_limit[index_interval+1],'''
    s = s.replace(anchor2, repl2)

    if s.count("background_tau_of_z(pba,5.,&tau_split_kmdsb)") != 1:
        raise RuntimeError("z=5 tau map missing")
    if s.count("inserted_split_kmdsb") < 3:
        raise RuntimeError("split guard transform incomplete")

    p.write_text(s)
    manifest = {
        "schema": "KMDSB.W03.M13B.K3D2G.VanillaZ5PerturbationSplitPatch.v0.1",
        "changed_files": ["source/perturbations.c"],
        "z_split": 5.0,
        "tau_from_background_z5": True,
        "restart_start": "nextafter(tau_z5, interval_end)",
        "duplicates_native_approximation_row": True,
        "requires_qfields": False,
        "state_vector_unchanged": True,
        "changes_initial_conditions": False,
        "changes_tolerances": False,
        "changes_solver_family": False,
        "changes_boltzmann_hierarchy_equations": False,
        "changes_einstein_sources": False,
        "sha256_before": sha(before),
        "sha256_after": sha(s),
    }
    if a.manifest:
        Path(a.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
