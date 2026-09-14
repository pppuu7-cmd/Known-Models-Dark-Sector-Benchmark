#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path

PROTOCOL='protocol/W04_M21_L400_TRANSFER_VS_HARMONIC_DIAGNOSTIC_v0.1.md'
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
ANCHOR='''    class_call(harmonic_cls(ppr,pba,ppt,ptr,ppm,phr),\n               phr->error_message,\n               phr->error_message);\n'''
BLOCK=r'''

    /* KMDSB M21 output-only l=400 transfer/harmonic diagnostic.
       Runs after harmonic_cls() has completed.  It reads existing transfer,
       primordial and sparse harmonic tables and does not modify CLASS state. */
    {
      const char * kmdsb_diag_path = getenv("KMDSB_M21_L400_TRANSFER_DIAG");
      if ((kmdsb_diag_path != NULL) && (kmdsb_diag_path[0] != '\0')) {
        FILE * kmdsb_diag_file;
        int kmdsb_md;
        int kmdsb_ic;
        int kmdsb_icic;
        int kmdsb_index_l;
        int kmdsb_index_q;
        double * kmdsb_primordial_pk;

        class_test(ppt->has_scalars != _TRUE_,
                   phr->error_message,
                   "KMDSB l400 diagnostic requires scalar mode");

        kmdsb_md = ppt->index_md_scalars;
        class_test(phr->ic_size[kmdsb_md] != 1,
                   phr->error_message,
                   "KMDSB l400 diagnostic requires exactly one scalar initial condition");
        class_test(ppt->has_ad != _TRUE_,
                   phr->error_message,
                   "KMDSB l400 diagnostic requires adiabatic initial conditions");
        class_test(phr->has_ee != _TRUE_,
                   phr->error_message,
                   "KMDSB l400 diagnostic requires EE spectra");

        kmdsb_ic = ppt->index_ic_ad;
        kmdsb_icic = index_symmetric_matrix(kmdsb_ic,kmdsb_ic,phr->ic_size[kmdsb_md]);

        kmdsb_diag_file = fopen(kmdsb_diag_path,"w");
        class_test(kmdsb_diag_file == NULL,
                   phr->error_message,
                   "KMDSB l400 diagnostic could not open output file %s",
                   kmdsb_diag_path);

        class_alloc(kmdsb_primordial_pk,
                    phr->ic_ic_size[kmdsb_md]*sizeof(double),
                    phr->error_message);

        fprintf(kmdsb_diag_file,
                "# l index_l index_q q k Delta_E P_R EE_integrand direct_sparse_Cl_EE\n");

        for (kmdsb_index_l=0;
             kmdsb_index_l<ptr->l_size[kmdsb_md];
             kmdsb_index_l++) {
          int kmdsb_l = ptr->l[kmdsb_index_l];
          if ((kmdsb_l >= 398) && (kmdsb_l <= 402)) {
            double kmdsb_cl_ee =
              phr->cl[kmdsb_md]
              [(kmdsb_index_l*phr->ic_ic_size[kmdsb_md]+kmdsb_icic)*phr->ct_size+phr->index_ct_ee];

            for (kmdsb_index_q=0;
                 kmdsb_index_q<ptr->q_size;
                 kmdsb_index_q++) {
              double kmdsb_k = ptr->k[kmdsb_md][kmdsb_index_q];
              double kmdsb_q = ptr->q[kmdsb_index_q];
              double kmdsb_delta_e;
              double kmdsb_integrand;

              class_call(primordial_spectrum_at_k(ppm,
                                                  kmdsb_md,
                                                  linear,
                                                  kmdsb_k,
                                                  kmdsb_primordial_pk),
                         ppm->error_message,
                         phr->error_message);

              kmdsb_delta_e =
                ptr->transfer[kmdsb_md]
                [((kmdsb_ic*ptr->tt_size[kmdsb_md]+ptr->index_tt_e)
                  *ptr->l_size[kmdsb_md]+kmdsb_index_l)
                 *ptr->q_size+kmdsb_index_q];

              kmdsb_integrand =
                kmdsb_primordial_pk[kmdsb_icic]
                * kmdsb_delta_e
                * kmdsb_delta_e
                * 4. * _PI_ / kmdsb_k;

              fprintf(kmdsb_diag_file,
                      "%d %d %d %.17g %.17g %.17g %.17g %.17g %.17g\n",
                      kmdsb_l,
                      kmdsb_index_l,
                      kmdsb_index_q,
                      kmdsb_q,
                      kmdsb_k,
                      kmdsb_delta_e,
                      kmdsb_primordial_pk[kmdsb_icic],
                      kmdsb_integrand,
                      kmdsb_cl_ee);
            }
          }
        }

        free(kmdsb_primordial_pk);
        fclose(kmdsb_diag_file);
      }
    }
'''

def H_bytes(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def main(src:Path, manifest:Path):
    raw=src.read_bytes(); text=raw.decode('utf-8')
    if text.count(ANCHOR)!=1: raise RuntimeError(f'expected one harmonic_cls anchor, got {text.count(ANCHOR)}')
    if 'KMDSB_M21_L400_TRANSFER_DIAG' in text: raise RuntimeError('diagnostic already present')
    new=text.replace(ANCHOR,ANCHOR+BLOCK,1)
    src.write_text(new)
    m={
      'schema':'KMDSB.W04.M21.L400TransferHarmonicPatch.v0.1',
      'protocol':PROTOCOL,
      'provider':f'lesgourg/class_public@{PIN}',
      'source_path':str(src),
      'anchor_count':1,
      'insertion_after_harmonic_cls':True,
      'environment_gate':'KMDSB_M21_L400_TRANSFER_DIAG',
      'selected_l_closed_interval':[398,402],
      'mutates_class_state':False,
      'original_sha256':H_bytes(raw),
      'patched_sha256':H_bytes(src.read_bytes()),
    }
    manifest.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    print(json.dumps(m,indent=2,sort_keys=True))
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: apply_l400_transfer_harmonic_diag.py HARMONIC_C PATCH_MANIFEST')
    main(Path(sys.argv[1]),Path(sys.argv[2]))
