#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_L400_SOURCE_FACTORIZATION_v0.1.md'
KMIN=0.03030247505892471
KMAX=0.04401375054733766
ANCHOR='      _set_source_(ppt->index_tp_p) = sqrt(6.) * g * P;\n'
BLOCK=r'''

      /* KMDSB M21 output-only scalar-E source factorization diagnostic. */
      {
        const char * kmdsb_path = getenv("KMDSB_M21_L400_SOURCE_DIAG");
        if ((kmdsb_path != NULL) && (kmdsb_path[0] != '\0') &&
            (k >= 0.03030247505892471) &&
            (k <= 0.04401375054733766)) {
          int kmdsb_rsa_on = (ppw->approx[ppw->index_ap_rsa] == (int)rsa_on);
          int kmdsb_tca_on = (ppw->approx[ppw->index_ap_tca] == (int)tca_on);
          int kmdsb_shear_valid = 0;
          int kmdsb_pol_valid = 0;
          double kmdsb_shear = 0.;
          double kmdsb_pol0 = 0.;
          double kmdsb_pol2 = 0.;

          if (!kmdsb_rsa_on) {
            if (kmdsb_tca_on) {
              kmdsb_shear = ppw->tca_shear_g;
              kmdsb_shear_valid = 1;
            }
            else {
              kmdsb_shear = y[ppw->pv->index_pt_shear_g];
              kmdsb_pol0 = y[ppw->pv->index_pt_pol0_g];
              kmdsb_pol2 = y[ppw->pv->index_pt_pol2_g];
              kmdsb_shear_valid = 1;
              kmdsb_pol_valid = 1;
            }
          }

          FILE * kmdsb_file = fopen(kmdsb_path,"a");
          class_test(kmdsb_file == NULL,
                     error_message,
                     "KMDSB l400 source diagnostic could not open %s",
                     kmdsb_path);
          fprintf(kmdsb_file,
                  "%d %d %.17g %.17g %.17g %.17g %.17g %d %d %.17g %d %.17g %d %.17g %.17g\n",
                  index_k,
                  index_tau,
                  k,
                  tau,
                  g,
                  P,
                  _set_source_(ppt->index_tp_p),
                  kmdsb_rsa_on,
                  kmdsb_tca_on,
                  ppw->s_l[2],
                  kmdsb_shear_valid,
                  kmdsb_shear,
                  kmdsb_pol_valid,
                  kmdsb_pol0,
                  kmdsb_pol2);
          fclose(kmdsb_file);
        }
      }
'''

def H(b:bytes)->str: return hashlib.sha256(b).hexdigest()

def main(src:Path,manifest:Path):
 raw=src.read_bytes(); text=raw.decode()
 if text.count(ANCHOR)!=1: raise RuntimeError(f'expected one scalar-E anchor, got {text.count(ANCHOR)}')
 if 'KMDSB_M21_L400_SOURCE_DIAG' in text: raise RuntimeError('source diagnostic already installed')
 new=text.replace(ANCHOR,ANCHOR+BLOCK,1); src.write_text(new)
 obj={'schema':'KMDSB.W04.M21.L400SourceFactorizationPatch.v0.1','protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}','source_path':str(src),'anchor_count':1,'environment_gate':'KMDSB_M21_L400_SOURCE_DIAG','k_min':KMIN,'k_max':KMAX,'placement':'immediately_after_native_scalar_E_source_assignment','mutates_class_state':False,'requires_single_task_system_worker':True,'thread_control':'OMP_NUM_THREADS=1','row_schema':['index_k','index_tau','k','tau','g','P','source','rsa_on','tca_on','s_l2','shear_valid','shear','pol_valid','pol0','pol2'],'original_sha256':H(raw),'patched_sha256':H(src.read_bytes())}
 manifest.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps(obj,indent=2,sort_keys=True))

if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: apply_l400_source_factorization_diag.py PERTURBATIONS_C PATCH_MANIFEST')
 main(Path(sys.argv[1]),Path(sys.argv[2]))
