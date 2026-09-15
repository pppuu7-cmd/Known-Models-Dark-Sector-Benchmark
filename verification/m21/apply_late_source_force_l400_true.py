#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
PROTOCOL='protocol/W04_M21_LATE_SOURCE_BRANCH_TOPOLOGY_INTERACTION_v0.1.md'
PINS={'e85808324f51fc694d12e3ed7439552a3c3f9540','64bbab707faf4de4779a9e04edd180fef18d98fa'}
INCLUDE='#include "parallel.h"\n'; AR='  ptr->angular_rescaling = pth->angular_rescaling;\n'; PRED='  if (l > ppr->transfer_neglect_late_source*ptr->angular_rescaling) {\n'
TAIL='''\n\n  free(radial_function);\n  return _SUCCESS_;\n}\n\n/**\n * This routine computes the transfer functions'''
FILE='''\n\nstatic int kmdsb_force_l400_true = 0;\nstatic double kmdsb_branch_threshold = -1.;\n'''
ARB='''\n  {\n    const char * e=getenv("KMDSB_M21_FORCE_L400_TRUE");\n    kmdsb_force_l400_true=((e!=NULL)&&(e[0]!='\\0')&&(pba->sgnK==0))?1:0;\n    kmdsb_branch_threshold=ppr->transfer_neglect_late_source;\n  }\n'''
PREDB='''\n  int kmdsb_native_pred=(l > ppr->transfer_neglect_late_source*ptr->angular_rescaling);\n  int kmdsb_effective_pred=kmdsb_native_pred;\n  if ((kmdsb_force_l400_true==1)&&(fabs(l-400.)<1.e-12)) kmdsb_effective_pred=1;\n  if (kmdsb_effective_pred) {\n'''
TAILB='''\n  {\n    const char * path=getenv("KMDSB_M21_BRANCH_DIAG");\n    int wanted_l=((fabs(l-399.)<1.e-12)||(fabs(l-400.)<1.e-12)||(fabs(l-401.)<1.e-12));\n    if ((path!=NULL)&&(path[0]!='\\0')&&wanted_l&&\n        (index_md==ppt->index_md_scalars)&&(index_tt==ptr->index_tt_e)&&\n        (k>=0.02)&&(k<=0.06)) {\n      class_test(kmdsb_branch_threshold<0.,ptr->error_message,"KMDSB branch threshold uninitialized");\n      int native_pred=(l > kmdsb_branch_threshold*ptr->angular_rescaling)?1:0;\n      int effective_pred=native_pred;\n      if ((kmdsb_force_l400_true==1)&&(fabs(l-400.)<1.e-12)) effective_pred=1;\n      FILE * f=fopen(path,"a");\n      class_test(f==NULL,ptr->error_message,"KMDSB branch diagnostic could not open %s",path);\n      fprintf(f,"%d %.17g %.17g %.17g %.17g %.17g %d %d %d %d %.17g %.17g %.17g %d\\n",\n              index_q,k,l,ptr->angular_rescaling,kmdsb_branch_threshold,\n              kmdsb_branch_threshold*ptr->angular_rescaling,native_pred,effective_pred,\n              index_tau_max_Bessel,index_tau_max,tau0_minus_tau[index_tau_max],\n              tau0_minus_tau_min_bessel,*trsf,kmdsb_force_l400_true);\n      fclose(f);\n    }\n  }\n'''
def H(b):return hashlib.sha256(b).hexdigest()
def main(src,man,pin):
 if pin not in PINS:raise RuntimeError(f'unauthorized pin {pin}')
 raw=src.read_bytes();t=raw.decode()
 for n,a in [('include',INCLUDE),('angular_rescaling',AR),('predicate',PRED),('tail',TAIL)]:
  if t.count(a)!=1:raise RuntimeError(f'{n} anchor count {t.count(a)}')
 if 'KMDSB_M21_FORCE_L400_TRUE' in t:raise RuntimeError('already installed')
 n=t.replace(INCLUDE,INCLUDE+FILE,1).replace(AR,AR+ARB,1).replace(PRED,PREDB,1).replace(TAIL,TAILB+TAIL,1);src.write_text(n)
 o={'schema':'KMDSB.W04.M21.ForceL400TruePatch.v0.1','protocol':PROTOCOL,'provider_pin':pin,'authorized_pins':sorted(PINS),'multipoles':[399,400,401],'k_min':0.02,'k_max':0.06,'intervention':'force_l400_late_source_predicate_true_only','mutates_angular_rescaling':False,'mutates_threshold':False,'thread_control':'OMP_NUM_THREADS=1','original_sha256':H(raw),'patched_sha256':H(src.read_bytes())}
 man.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':
 if len(sys.argv)!=4:raise SystemExit('usage: patch TRANSFER_C MANIFEST PIN')
 main(Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3])
