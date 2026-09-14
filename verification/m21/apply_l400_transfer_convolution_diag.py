#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_v0.1.md'
KMIN='0.03030247505892471'
KMAX='0.04401375054733766'
ANCHOR='''\n\n  free(radial_function);\n  return _SUCCESS_;\n}\n\n/**\n * This routine computes the transfer functions'''
BLOCK=r'''

  /* KMDSB M21 output-only scalar-E l=400 transfer-convolution diagnostic.
     Executed only after the native convolution and edge correction are final. */
  {
    const char * kmdsb_path = getenv("KMDSB_M21_L400_CONV_DIAG");
    if ((kmdsb_path != NULL) && (kmdsb_path[0] != '\0') &&
        (index_md == ppt->index_md_scalars) &&
        (index_tt == ptr->index_tt_e) &&
        (fabs(l-400.) < 1.e-12) &&
        (k >= 0.03030247505892471) &&
        (k <= 0.04401375054733766)) {
      double kmdsb_edge_correction = 0.;
      int kmdsb_index_tau;

      if ((index_tau_max!=(ptw->tau_size-1)) &&
          (index_tau_max==index_tau_max_Bessel)) {
        kmdsb_edge_correction =
          -0.5*(tau0_minus_tau[index_tau_max+1]-tau0_minus_tau_min_bessel)*
          radial_function[index_tau_max]*sources[index_tau_max];
      }

#pragma omp critical(kmdsb_m21_l400_conv_diag)
      {
        FILE * kmdsb_file = fopen(kmdsb_path,"a");
        class_test(kmdsb_file == NULL,
                   ptr->error_message,
                   "KMDSB l400 convolution diagnostic could not open %s",
                   kmdsb_path);
        for (kmdsb_index_tau=0;
             kmdsb_index_tau<=index_tau_max;
             kmdsb_index_tau++) {
          double kmdsb_contribution =
            sources[kmdsb_index_tau]*
            radial_function[kmdsb_index_tau]*
            w_trapz[kmdsb_index_tau];
          fprintf(kmdsb_file,
                  "%d %.17g %d %.17g %.17g %.17g %.17g %.17g %.17g %.17g %d %.17g\n",
                  index_q,
                  k,
                  kmdsb_index_tau,
                  tau0_minus_tau[kmdsb_index_tau],
                  sources[kmdsb_index_tau],
                  radial_function[kmdsb_index_tau],
                  w_trapz[kmdsb_index_tau],
                  kmdsb_contribution,
                  *trsf,
                  kmdsb_edge_correction,
                  index_tau_max,
                  tau0_minus_tau_min_bessel);
        }
        fclose(kmdsb_file);
      }
    }
  }
'''

def H(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def main(src:Path,manifest:Path):
 raw=src.read_bytes(); text=raw.decode()
 if text.count(ANCHOR)!=1: raise RuntimeError(f'expected unique transfer_integrate tail anchor, got {text.count(ANCHOR)}')
 if 'KMDSB_M21_L400_CONV_DIAG' in text: raise RuntimeError('diagnostic already installed')
 new=text.replace(ANCHOR,BLOCK+ANCHOR,1); src.write_text(new)
 obj={
  'schema':'KMDSB.W04.M21.L400TransferConvolutionPatch.v0.1',
  'protocol':PROTOCOL,
  'provider':f'lesgourg/class_public@{PIN}',
  'source_path':str(src),
  'anchor_count':1,
  'environment_gate':'KMDSB_M21_L400_CONV_DIAG',
  'mode':'scalar','transfer_type':'E','l':400,
  'k_min':float(KMIN),'k_max':float(KMAX),
  'placement':'after_native_convolution_and_bessel_edge_correction_before_radial_free',
  'mutates_class_state':False,
  'openmp_serialized_io':True,
  'original_sha256':H(raw),'patched_sha256':H(src.read_bytes()),
 }
 manifest.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
 print(json.dumps(obj,indent=2,sort_keys=True))
if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: apply_l400_transfer_convolution_diag.py TRANSFER_C PATCH_MANIFEST')
 main(Path(sys.argv[1]),Path(sys.argv[2]))
