#!/usr/bin/env python3
"""Enrich exact-pin NDF15/RK failure messages with collapse geometry only.

This diagnostic changes only error-message text at existing minimum-step failure
sites. Numerical branches, tolerances, states, Jacobians, steps, and equations
are unchanged.
"""
from __future__ import annotations
import argparse, hashlib, json, re
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

    # The exact-pin RK site uses tabs in its continuation indentation. Match only
    # whitespace flexibly while keeping the condition and argument sequence exact.
    rk_pattern=re.compile(
        r'(?m)^([ \t]*)class_test\(fabs\(hnext/x1\) <= hmin,\s*\n'
        r'[ \t]*pgi->error_message,\s*\n'
        r'[ \t]*"Step size too small: step:%g, minimum:%g, in interval: \[%g:%g\]",\s*\n'
        r'[ \t]*fabs\(hnext/x1\),\s*\n'
        r'[ \t]*hmin,\s*\n'
        r'[ \t]*x1,\s*\n'
        r'[ \t]*x2\);'
    )
    matches=list(rk_pattern.finditer(r))
    if len(matches)!=1:
        raise RuntimeError(f'expected one RK minimum-step site, found {len(matches)}')
    indent=matches[0].group(1)
    rnew=(indent+'class_test(fabs(hnext/x1) <= hmin,\n'
          +indent+'           pgi->error_message,\n'
          +indent+'           "KMDSB_RK_COLLAPSE x=%.17g step_ratio=%.17g minimum=%.17g hdid=%.17g hnext=%.17g step_index=%d interval=[%.17g:%.17g]",\n'
          +indent+'           x,\n'
          +indent+'           fabs(hnext/x1),\n'
          +indent+'           hmin,\n'
          +indent+'           hdid,\n'
          +indent+'           hnext,\n'
          +indent+'           nstp,\n'
          +indent+'           x1,\n'
          +indent+'           x2);')
    r=rk_pattern.sub(lambda _: rnew,r,count=1)
    ndf.write_text(n); rk.write_text(r)
    manifest={
      'schema':'KMDSB.W03.M13b.K3D2BSolverCollapseGeometryPatch.v0.3',
      'changed_files':['tools/evolver_ndf15.c','tools/dei_rkck.c'],
      'diagnostic_only':True,
      'ndf15_sites_enriched':2,
      'rk_sites_enriched':1,
      'rk_matcher_whitespace_robust':True,
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
