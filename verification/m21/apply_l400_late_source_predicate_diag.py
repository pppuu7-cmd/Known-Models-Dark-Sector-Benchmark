#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_L400_LATE_SOURCE_PREDICATE_ULP_AUDIT_v0.1.md'
KMIN=0.03030247505892471
KMAX=0.04401375054733766
ANCHOR='''\n\n  free(radial_function);\n  return _SUCCESS_;\n}\n\n/**\n * This routine computes the transfer functions'''
BLOCK=r'''

  /* KMDSB M21 output-only l=400 late-source predicate diagnostic. */
  {
    const char * kmdsb_path = getenv("KMDSB_M21_L400_LATE_SOURCE_DIAG");
    if ((kmdsb_path != NULL) && (kmdsb_path[0] != '\0') &&
        (index_md == ppt->index_md_scalars) &&
        (index_tt == ptr->index_tt_e) &&
        (fabs(l-400.) < 1.e-12) &&
        (k >= 0.03030247505892471) &&
        (k <= 0.04401375054733766)) {
      double kmdsb_rhs = ppr->transfer_neglect_late_source*ptr->angular_rescaling;
      int kmdsb_predicate = (l > kmdsb_rhs) ? 1 : 0;
      FILE * kmdsb_file = fopen(kmdsb_path,"a");
      class_test(kmdsb_file == NULL,
                 ptr->error_message,
                 "KMDSB l400 late-source diagnostic could not open %s",
                 kmdsb_path);
      fprintf(kmdsb_file,
              "%d %.17g %.17g %.17g %.17g %.17g %d %d %d %d %d %.17g %.17g %.17g %.17g\n",
              index_q,
              k,
              l,
              ptr->angular_rescaling,
              ppr->transfer_neglect_late_source,
              kmdsb_rhs,
              kmdsb_predicate,
              (int)ptw->neglect_late_source,
              ptw->tau_size,
              index_tau_max_Bessel,
              index_tau_max,
              ptw->tau0_minus_tau_cut,
              tau0_minus_tau[index_tau_max],
              tau0_minus_tau_min_bessel,
              *trsf);
      fclose(kmdsb_file);
    }
  }
'''

def H(b:bytes)->str: return hashlib.sha256(b).hexdigest()

def main(src:Path,manifest:Path):
 raw=src.read_bytes(); text=raw.decode()
 if text.count(ANCHOR)!=1: raise RuntimeError(f'expected unique transfer_integrate tail anchor, got {text.count(ANCHOR)}')
 if 'KMDSB_M21_L400_LATE_SOURCE_DIAG' in text: raise RuntimeError('diagnostic already installed')
 new=text.replace(ANCHOR,BLOCK+ANCHOR,1); src.write_text(new)
 obj={'schema':'KMDSB.W04.M21.L400LateSourcePredicatePatch.v0.1','protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}','source_path':str(src),'anchor_count':1,'environment_gate':'KMDSB_M21_L400_LATE_SOURCE_DIAG','mode':'scalar','transfer_type':'E','l':400,'k_min':KMIN,'k_max':KMAX,'placement':'after_native_transfer_integral_before_radial_free','mutates_class_state':False,'requires_single_task_system_worker':True,'thread_control':'OMP_NUM_THREADS=1','row_schema':['index_q','k','l','angular_rescaling','transfer_neglect_late_source','predicate_rhs','predicate','actual_neglect_late_source','tau_size','index_tau_max_Bessel','index_tau_max','tau0_minus_tau_cut','u_final','u_min_bessel','transfer_final'],'original_sha256':H(raw),'patched_sha256':H(src.read_bytes())}
 manifest.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps(obj,indent=2,sort_keys=True))

if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: apply_l400_late_source_predicate_diag.py TRANSFER_C PATCH_MANIFEST')
 main(Path(sys.argv[1]),Path(sys.argv[2]))
