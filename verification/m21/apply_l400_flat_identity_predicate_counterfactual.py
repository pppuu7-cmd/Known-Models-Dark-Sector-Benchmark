#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_L400_CONDITIONAL_FLAT_IDENTITY_PREDICATE_COUNTERFACTUAL_v0.1.md'
KMIN=0.03030247505892471
KMAX=0.04401375054733766
INCLUDE_ANCHOR='#include "parallel.h"\n'
AR_ANCHOR='''  ptr->angular_rescaling = pth->angular_rescaling;\n'''
PRED_ANCHOR='''  if (l > ppr->transfer_neglect_late_source*ptr->angular_rescaling) {\n'''
TAIL_ANCHOR='''\n\n  free(radial_function);\n  return _SUCCESS_;\n}\n\n/**\n * This routine computes the transfer functions'''
FILE_LOCAL=r'''

/* KMDSB M21 conditional flat-identity predicate counterfactual.
 * These file-local values are set before the q-parallel region.
 * Native CLASS state never reads them except for the explicitly gated
 * counterfactual operand in transfer_late_source_can_be_neglected(). */
static int kmdsb_m21_flat_identity_predicate_cf = 0;
static double kmdsb_m21_transfer_neglect_late_source_cf = -1.;
'''
AR_BLOCK=r'''

  /* KMDSB M21 counterfactual plumbing. The gate may activate only in
     exactly flat provider geometry; angular_rescaling itself is never modified. */
  {
    const char * kmdsb_cf = getenv("KMDSB_M21_FLAT_IDENTITY_PREDICATE_CF");
    kmdsb_m21_flat_identity_predicate_cf =
      ((kmdsb_cf != NULL) && (kmdsb_cf[0] != '\0') && (pba->sgnK == 0)) ? 1 : 0;
    kmdsb_m21_transfer_neglect_late_source_cf = ppr->transfer_neglect_late_source;
  }
'''
PRED_BLOCK=r'''
  double kmdsb_m21_predicate_rescaling = ptr->angular_rescaling;
  if (kmdsb_m21_flat_identity_predicate_cf == 1)
    kmdsb_m21_predicate_rescaling = 1.0;

  if (l > ppr->transfer_neglect_late_source*kmdsb_m21_predicate_rescaling) {
'''
TAIL_BLOCK=r'''

  /* KMDSB M21 native/counterfactual l=400 endpoint diagnostic. */
  {
    const char * kmdsb_path = getenv("KMDSB_M21_FLAT_IDENTITY_DIAG");
    if ((kmdsb_path != NULL) && (kmdsb_path[0] != '\0') &&
        (index_md == ppt->index_md_scalars) &&
        (index_tt == ptr->index_tt_e) &&
        (fabs(l-400.) < 1.e-12) &&
        (k >= 0.03030247505892471) &&
        (k <= 0.04401375054733766)) {
      class_test(kmdsb_m21_transfer_neglect_late_source_cf < 0.,
                 ptr->error_message,
                 "KMDSB flat-identity counterfactual threshold was not initialized");
      double kmdsb_eff_ar =
        (kmdsb_m21_flat_identity_predicate_cf == 1) ? 1.0 : ptr->angular_rescaling;
      double kmdsb_rhs = kmdsb_m21_transfer_neglect_late_source_cf*kmdsb_eff_ar;
      int kmdsb_predicate = (l > kmdsb_rhs) ? 1 : 0;
      FILE * kmdsb_file = fopen(kmdsb_path,"a");
      class_test(kmdsb_file == NULL,
                 ptr->error_message,
                 "KMDSB flat-identity diagnostic could not open %s",
                 kmdsb_path);
      fprintf(kmdsb_file,
              "%d %.17g %.17g %.17g %.17g %.17g %.17g %d %d %d %d %d %.17g %.17g %.17g %.17g %d\n",
              index_q,
              k,
              l,
              ptr->angular_rescaling,
              kmdsb_eff_ar,
              kmdsb_m21_transfer_neglect_late_source_cf,
              kmdsb_rhs,
              kmdsb_predicate,
              (int)ptw->neglect_late_source,
              ptw->tau_size,
              index_tau_max_Bessel,
              index_tau_max,
              ptw->tau0_minus_tau_cut,
              tau0_minus_tau[index_tau_max],
              tau0_minus_tau_min_bessel,
              *trsf,
              kmdsb_m21_flat_identity_predicate_cf);
      fclose(kmdsb_file);
    }
  }
'''

def H(b:bytes)->str: return hashlib.sha256(b).hexdigest()

def main(src:Path,manifest:Path):
 raw=src.read_bytes(); text=raw.decode()
 for name,anchor in [('include',INCLUDE_ANCHOR),('angular_rescaling_copy',AR_ANCHOR),('predicate',PRED_ANCHOR),('transfer_integrate_tail',TAIL_ANCHOR)]:
  if text.count(anchor)!=1: raise RuntimeError(f'expected unique {name} anchor, got {text.count(anchor)}')
 if 'KMDSB_M21_FLAT_IDENTITY_PREDICATE_CF' in text: raise RuntimeError('counterfactual already installed')
 new=text.replace(INCLUDE_ANCHOR,INCLUDE_ANCHOR+FILE_LOCAL,1)
 new=new.replace(AR_ANCHOR,AR_ANCHOR+AR_BLOCK,1)
 new=new.replace(PRED_ANCHOR,PRED_BLOCK,1)
 new=new.replace(TAIL_ANCHOR,TAIL_BLOCK+TAIL_ANCHOR,1)
 src.write_text(new)
 obj={
  'schema':'KMDSB.W04.M21.FlatIdentityPredicateCounterfactualPatch.v0.1',
  'protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}',
  'source_path':str(src),'anchor_count':4,
  'counterfactual_gate':'KMDSB_M21_FLAT_IDENTITY_PREDICATE_CF',
  'diagnostic_gate':'KMDSB_M21_FLAT_IDENTITY_DIAG',
  'counterfactual_operand':'late_source_predicate_angular_rescaling_only',
  'counterfactual_value':1.0,'requires_flat_sgnK':0,
  'native_angular_rescaling_mutated':False,'provider_precision_mutated':False,
  'mode':'scalar','transfer_type':'E','l':400,'k_min':KMIN,'k_max':KMAX,
  'requires_single_task_system_worker':True,'thread_control':'OMP_NUM_THREADS=1',
  'row_schema':['index_q','k','l','native_angular_rescaling','effective_predicate_angular_rescaling','transfer_neglect_late_source','predicate_rhs','predicate','actual_neglect_late_source','tau_size','index_tau_max_Bessel','index_tau_max','tau0_minus_tau_cut','u_final','u_min_bessel','transfer_final','counterfactual_enabled'],
  'original_sha256':H(raw),'patched_sha256':H(src.read_bytes())}
 manifest.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps(obj,indent=2,sort_keys=True))

if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: apply_l400_flat_identity_predicate_counterfactual.py TRANSFER_C PATCH_MANIFEST')
 main(Path(sys.argv[1]),Path(sys.argv[2]))
