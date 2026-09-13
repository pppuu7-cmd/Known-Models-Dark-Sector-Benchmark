#!/usr/bin/env python3
"""Insert the frozen z=5 qfield seam into CLASS native perturbation intervals."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--a-ulps',type=int,choices=(0,1,2),default=0); ap.add_argument('--manifest'); a=ap.parse_args()
    p=Path(a.root)/'source/perturbations.c'; before=p.read_text()
    if 'has_qcf' not in before or 'has_qpf' not in before:
        raise RuntimeError('K3D2 qfield adapter must be applied first')

    n=before.count('a < 1./6.')
    if n != 2:
        raise RuntimeError(f'expected exactly two perturbation handoff guards, found {n}')
    s=before.replace('a < 1./6.','a <= exp(log(1./6.))')

    anchor='  free(interval_number_of);\n\n  /** - fill the structure containing all fixed parameters, indices'
    if s.count(anchor)!=1:
        raise RuntimeError('unique interval-construction anchor not found')
    advance=''.join('    a_post_handoff_kmdsb = nextafter(a_post_handoff_kmdsb,1.);\n' for _ in range(a.a_ulps))
    post_map = ''
    if a.a_ulps:
        post_map = f'''    double a_post_handoff_kmdsb = exp(log(1./6.));
{advance}    double z_post_handoff_kmdsb = 1./a_post_handoff_kmdsb-1.;
    class_call(background_tau_of_z(pba,z_post_handoff_kmdsb,&tau_post_handoff_kmdsb),
               pba->error_message,
               ppt->error_message);
'''
    block=f'''  free(interval_number_of);

  /* KMDSB K3D2-B: insert the frozen z=5 qfield seam as a native CLASS
     perturbation interval without changing any approximation flags. */
  double tau_handoff_kmdsb = -1.;
  double tau_post_handoff_kmdsb = -1.;
  int inserted_handoff_kmdsb = _FALSE_;
  if ((pba->has_qcf == _TRUE_) || (pba->has_qpf == _TRUE_)) {{
    int old_interval_number_kmdsb = interval_number;
    int insert_index_kmdsb = -1;
    int ii_kmdsb, jj_kmdsb;
    double * new_interval_limit_kmdsb;
    int ** new_interval_approx_kmdsb;

    class_call(background_tau_of_z(pba,5.,&tau_handoff_kmdsb),
               pba->error_message,
               ppt->error_message);
{post_map}
    for (ii_kmdsb=0; ii_kmdsb<old_interval_number_kmdsb; ii_kmdsb++) {{
      if ((interval_limit[ii_kmdsb] < tau_handoff_kmdsb) &&
          (tau_handoff_kmdsb < interval_limit[ii_kmdsb+1])) {{
        insert_index_kmdsb = ii_kmdsb;
        break;
      }}
    }}

    if (insert_index_kmdsb >= 0) {{
      class_alloc(new_interval_limit_kmdsb,(old_interval_number_kmdsb+2)*sizeof(double),ppt->error_message);
      class_alloc(new_interval_approx_kmdsb,(old_interval_number_kmdsb+1)*sizeof(int*),ppt->error_message);
      for (ii_kmdsb=0; ii_kmdsb<old_interval_number_kmdsb+1; ii_kmdsb++)
        class_alloc(new_interval_approx_kmdsb[ii_kmdsb],ppw->ap_size*sizeof(int),ppt->error_message);

      for (ii_kmdsb=0; ii_kmdsb<=insert_index_kmdsb; ii_kmdsb++)
        new_interval_limit_kmdsb[ii_kmdsb] = interval_limit[ii_kmdsb];
      new_interval_limit_kmdsb[insert_index_kmdsb+1] = tau_handoff_kmdsb;
      for (ii_kmdsb=insert_index_kmdsb+1; ii_kmdsb<=old_interval_number_kmdsb; ii_kmdsb++)
        new_interval_limit_kmdsb[ii_kmdsb+1] = interval_limit[ii_kmdsb];

      for (ii_kmdsb=0; ii_kmdsb<old_interval_number_kmdsb+1; ii_kmdsb++) {{
        int src_interval_kmdsb = ii_kmdsb;
        if (ii_kmdsb > insert_index_kmdsb+1)
          src_interval_kmdsb = ii_kmdsb-1;
        else if (ii_kmdsb == insert_index_kmdsb+1)
          src_interval_kmdsb = insert_index_kmdsb;
        for (jj_kmdsb=0; jj_kmdsb<ppw->ap_size; jj_kmdsb++)
          new_interval_approx_kmdsb[ii_kmdsb][jj_kmdsb] = interval_approx[src_interval_kmdsb][jj_kmdsb];
      }}

      for (ii_kmdsb=0; ii_kmdsb<old_interval_number_kmdsb; ii_kmdsb++)
        free(interval_approx[ii_kmdsb]);
      free(interval_approx);
      free(interval_limit);
      interval_limit = new_interval_limit_kmdsb;
      interval_approx = new_interval_approx_kmdsb;
      interval_number = old_interval_number_kmdsb+1;
      inserted_handoff_kmdsb = _TRUE_;
    }}
  }}

  /** - fill the structure containing all fixed parameters, indices'''
    s=s.replace(anchor,block)

    anchor2='''    class_call(generic_evolver(perturbations_derivs,
                               interval_limit[index_interval],
                               interval_limit[index_interval+1],'''
    if s.count(anchor2)!=1:
        raise RuntimeError('unique perturbation evolver call not found')
    if a.a_ulps:
        seam='tau_post_handoff_kmdsb'
    else:
        seam='nextafter(tau_handoff_kmdsb,interval_limit[index_interval+1])'
    repl2=f'''    double interval_start_kmdsb = interval_limit[index_interval];
    if ((inserted_handoff_kmdsb == _TRUE_) &&
        (interval_limit[index_interval] == tau_handoff_kmdsb))
      interval_start_kmdsb = {seam};

    class_call(generic_evolver(perturbations_derivs,
                               interval_start_kmdsb,
                               interval_limit[index_interval+1],'''
    s=s.replace(anchor2,repl2)

    if s.count('a <= exp(log(1./6.))') != 2: raise RuntimeError('boundary guard transform failed')
    if s.count('background_tau_of_z(pba,5.,&tau_handoff_kmdsb)') != 1: raise RuntimeError('tau map missing')
    if a.a_ulps and s.count('background_tau_of_z(pba,z_post_handoff_kmdsb,&tau_post_handoff_kmdsb)') != 1: raise RuntimeError('post-handoff a-map missing')
    p.write_text(s)
    manifest={'schema':'KMDSB.W03.M13b.K3D2BPerturbationNativeIntervalSplitPatch.v0.2','changed_files':['source/perturbations.c'],'conditional_qfields':True,'tau_from_background_z5':True,'post_handoff_a_ulps':a.a_ulps,'post_handoff_tau_from_background_inverse_map':bool(a.a_ulps),'duplicates_native_approximation_row':True,'state_vector_unchanged':True,'vector_init_at_exact_boundary':True,'perturbation_boundary_guard_replacements':2,'changes_tolerances':False,'changes_solver_family':False,'changes_boltzmann_hierarchy_equations':False,'changes_einstein_sources':False,'sha256_before':sha(before),'sha256_after':sha(s)}
    if a.manifest: Path(a.manifest).write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps(manifest,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
