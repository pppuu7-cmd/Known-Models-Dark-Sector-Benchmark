#!/usr/bin/env python3
"""Enrich exact-pin NDF15/RK failure messages with collapse geometry only.

This diagnostic changes only error-message text at existing minimum-step failure
sites. Numerical branches, tolerances, states, Jacobians, steps, and equations
are unchanged.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--manifest'); args=ap.parse_args()
    root=Path(args.root)
    ndf=root/'tools/evolver_ndf15.c'; rk=root/'tools/dei_rkck.c'
    n0=ndf.read_text(); r0=rk.read_text(); n=n0; r=r0
    old_newton='''            class_test(absh <= hmin, error_message,
                       "Step size too small: step:%g, minimum:%g, in interval: [%g:%g]\\n",
                       absh,hmin,t0,tfinal);'''
    old_error='''          class_test(absh <= hmin, error_message,
                     "Step size too small: step:%g, minimum:%g, in interval: [%g:%g]\\n",
                     absh,hmin,t0,tfinal);'''
    if n.count(old_newton)!=1:
        raise RuntimeError(f'expected one NDF15 Newton minimum-step site, found {n.count(old_newton)}')
    if n.count(old_error)!=1:
        raise RuntimeError(f'expected one NDF15 error-control minimum-step site, found {n.count(old_error)}')
    new_newton='''            class_test(absh <= hmin, error_message,
                       "KMDSB_NDF15_COLLAPSE reason=newton t=%.17g step=%.17g minimum=%.17g order=%d successful=%d failed=%d fevals=%d jacobians=%d lus=%d linsolves=%d interval=[%.17g:%.17g]\\n",
                       t,absh,hmin,k,stepstat[0],stepstat[1],stepstat[2],stepstat[3],stepstat[4],stepstat[5],t0,tfinal);'''
    new_error='''          class_test(absh <= hmin, error_message,
                     "KMDSB_NDF15_COLLAPSE reason=error_control t=%.17g step=%.17g minimum=%.17g order=%d err=%.17g rtol=%.17g successful=%d failed=%d fevals=%d jacobians=%d lus=%d linsolves=%d interval=[%.17g:%.17g]\\n",
                     t,absh,hmin,k,err,rtol,stepstat[0],stepstat[1],stepstat[2],stepstat[3],stepstat[4],stepstat[5],t0,tfinal);'''
    n=n.replace(old_newton,new_newton,1)
    n=n.replace(old_error,new_error,1)

    rold='''    class_test(fabs(hnext/x1) <= hmin,
               pgi->error_message,
               "Step size too small: step:%g, minimum:%g, in interval: [%g:%g]",
               fabs(hnext/x1),
               hmin,
               x1,
               x2);'''
    if r.count(rold)!=1:
        raise RuntimeError(f'expected one RK minimum-step site, found {r.count(rold)}')
    rnew='''    class_test(fabs(hnext/x1) <= hmin,
               pgi->error_message,
               "KMDSB_RK_COLLAPSE x=%.17g step_ratio=%.17g minimum=%.17g hdid=%.17g hnext=%.17g step_index=%d interval=[%.17g:%.17g]",
               x,
               fabs(hnext/x1),
               hmin,
               hdid,
               hnext,
               nstp,
               x1,
               x2);'''
    r=r.replace(rold,rnew,1)
    ndf.write_text(n); rk.write_text(r)
    manifest={
      'schema':'KMDSB.W03.M13b.K3D2BSolverCollapseGeometryPatch.v0.2',
      'changed_files':['tools/evolver_ndf15.c','tools/dei_rkck.c'],
      'diagnostic_only':True,
      'ndf15_sites_enriched':2,
      'rk_sites_enriched':1,
      'changes_error_text_only':True,
      'changes_equations':False,
      'changes_tolerances':False,
      'changes_solver_logic':False,
      'changes_state_vector':False,
      'ndf15_sha256_before':sha(n0),'ndf15_sha256_after':sha(n),
      'rk_sha256_before':sha(r0),'rk_sha256_after':sha(r),
    }
    if args.manifest: Path(args.manifest).write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps(manifest,indent=2,sort_keys=True)); return 0

if __name__=='__main__': raise SystemExit(main())
