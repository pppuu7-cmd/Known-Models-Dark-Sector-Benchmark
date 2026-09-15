#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_FLAT_DISTANCE_IDENTITY_COMPONENT_AUDIT_v0.1.md'
ANCHOR='''  pth->angular_rescaling=pth->ra_rec/(pba->conformal_age-pth->tau_rec);\n'''
BLOCK=r'''

  /* KMDSB M21 output-only flat-distance identity component diagnostic. */
  {
    const char * kmdsb_path = getenv("KMDSB_M21_FLAT_DISTANCE_IDENTITY_DIAG");
    if ((kmdsb_path != NULL) && (kmdsb_path[0] != '\0')) {
      double kmdsb_den = pba->conformal_age-pth->tau_rec;
      double kmdsb_abs = pth->ra_rec-kmdsb_den;
      double kmdsb_rel = kmdsb_abs/kmdsb_den;
      FILE * kmdsb_file = fopen(kmdsb_path,"a");
      class_test(kmdsb_file == NULL,
                 pth->error_message,
                 "KMDSB flat-distance identity diagnostic could not open %s",
                 kmdsb_path);
      fprintf(kmdsb_file,
              "%d %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g\n",
              pba->sgnK,
              pth->z_rec,
              pth->tau_rec,
              pba->conformal_age,
              kmdsb_den,
              pth->da_rec,
              pth->ra_rec,
              kmdsb_abs,
              kmdsb_rel,
              pth->angular_rescaling,
              pth->angular_rescaling-1.0);
      fclose(kmdsb_file);
    }
  }
'''

def H(b:bytes)->str: return hashlib.sha256(b).hexdigest()

def main(src:Path,manifest:Path):
 raw=src.read_bytes(); text=raw.decode()
 if text.count(ANCHOR)!=1: raise RuntimeError(f'expected unique angular-rescaling anchor, got {text.count(ANCHOR)}')
 if 'KMDSB_M21_FLAT_DISTANCE_IDENTITY_DIAG' in text: raise RuntimeError('diagnostic already installed')
 new=text.replace(ANCHOR,ANCHOR+BLOCK,1); src.write_text(new)
 obj={
  'schema':'KMDSB.W04.M21.FlatDistanceIdentityComponentPatch.v0.1',
  'protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}',
  'source_path':str(src),'anchor_count':1,
  'environment_gate':'KMDSB_M21_FLAT_DISTANCE_IDENTITY_DIAG',
  'placement':'immediately_after_native_angular_rescaling_assignment',
  'mutates_class_state':False,
  'row_schema':['sgnK','z_rec','tau_rec','conformal_age','conformal_age_minus_tau_rec','da_rec','ra_rec','distance_absolute_residual','distance_relative_residual','angular_rescaling','angular_rescaling_minus_1'],
  'original_sha256':H(raw),'patched_sha256':H(src.read_bytes())}
 manifest.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps(obj,indent=2,sort_keys=True))

if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: apply_flat_distance_identity_component_diag.py THERMODYNAMICS_C PATCH_MANIFEST')
 main(Path(sys.argv[1]),Path(sys.argv[2]))
