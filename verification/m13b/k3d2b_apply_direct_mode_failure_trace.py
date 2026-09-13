#!/usr/bin/env python3
"""Replace the recovered perturbation evolver class_call by a diagnostic wrapper.

The wrapper preserves the exact generic_evolver call and all arguments. On
_FAILURE_ it prints the mode/IC/k identity together with the raw solver error
before returning failure from perturbations_solve. No solver, tolerance,
state, or equation is changed.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--manifest')
    args = ap.parse_args()
    p = Path(args.root) / 'source/perturbations.c'
    before = p.read_text()
    old = '''    class_call(generic_evolver(perturbations_derivs,
                               interval_start_kmdsb,
                               interval_limit[index_interval+1],
                               ppw->pv->y,
                               ppw->pv->used_in_sources,
                               ppw->pv->pt_size,
                               &ppaw,
                               ppr->tol_perturbations_integration,
                               ppr->smallest_allowed_variation,
                               perturbations_timescale,
                               ppr->perturbations_integration_stepsize,
                               ppt->tau_sampling,
                               tau_actual_size,
                               perturbations_sources,
                               perhaps_print_variables,
                               ppt->error_message),
               ppt->error_message,
               ppt->error_message);
'''
    if before.count(old) != 1:
        raise RuntimeError(f'expected one recovered generic_evolver class_call, found {before.count(old)}')
    new = '''    int kmdsb_evolver_status = generic_evolver(perturbations_derivs,
                               interval_start_kmdsb,
                               interval_limit[index_interval+1],
                               ppw->pv->y,
                               ppw->pv->used_in_sources,
                               ppw->pv->pt_size,
                               &ppaw,
                               ppr->tol_perturbations_integration,
                               ppr->smallest_allowed_variation,
                               perturbations_timescale,
                               ppr->perturbations_integration_stepsize,
                               ppt->tau_sampling,
                               tau_actual_size,
                               perturbations_sources,
                               perhaps_print_variables,
                               ppt->error_message);
    if (kmdsb_evolver_status == _FAILURE_) {
      fprintf(stderr,"KMDSB_MODE_FAIL index_md=%d index_ic=%d index_k=%d k=%.17g interval_start=%.17g evolver_start=%.17g interval_end=%.17g error=%s\\n",
              index_md,index_ic,index_k,k,
              interval_limit[index_interval],interval_start_kmdsb,
              interval_limit[index_interval+1],ppt->error_message);
      return _FAILURE_;
    }
'''
    after = before.replace(old, new, 1)
    p.write_text(after)
    manifest = {
        'schema': 'KMDSB.W03.M13b.K3D2BDirectModeFailureTracePatch.v0.1',
        'changed_files': ['source/perturbations.c'],
        'diagnostic_only': True,
        'preserves_generic_evolver_arguments': True,
        'changes_equations': False,
        'changes_tolerances': False,
        'changes_solver_family': False,
        'changes_state_vector': False,
        'sha256_before': sha(before),
        'sha256_after': sha(after),
    }
    if args.manifest:
        Path(args.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
