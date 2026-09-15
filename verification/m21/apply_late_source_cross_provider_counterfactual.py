#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
PROTOCOL='protocol/W04_M21_LATE_SOURCE_CROSS_COSMOLOGY_PROVIDER_REGRESSION_v0.1.md'
PINS={'e85808324f51fc694d12e3ed7439552a3c3f9540','64bbab707faf4de4779a9e04edd180fef18d98fa'}
KMIN=0.02;KMAX=0.06
INCLUDE='#include "parallel.h"\n';AR='  ptr->angular_rescaling = pth->angular_rescaling;\n';PRED='  if (l > ppr->transfer_neglect_late_source*ptr->angular_rescaling) {\n'
TAIL='''\n\n  free(radial_function);\n  return _SUCCESS_;\n}\n\n/**\n * This routine computes the transfer functions'''
FILE=r'''

static int kmdsb_cross_cf = 0;
static double kmdsb_cross_threshold = -1.;
'''
ARB=r'''
  {
    const char * e=getenv("KMDSB_M21_CROSS_CF");
    kmdsb_cross_cf=((e!=NULL)&&(e[0]!='\0')&&(pba->sgnK==0))?1:0;
    kmdsb_cross_threshold=ppr->transfer_neglect_late_source;
  }
'''
PREDB=r'''
  double kmdsb_cross_ar=ptr->angular_rescaling;
  if (kmdsb_cross_cf==1) kmdsb_cross_ar=1.0;
  if (l > ppr->transfer_neglect_late_source*kmdsb_cross_ar) {
'''
TAILB=r'''
  {
    const char * path=getenv("KMDSB_M21_CROSS_DIAG");
    int wanted_l=((fabs(l-399.)<1.e-12)||(fabs(l-400.)<1.e-12)||(fabs(l-401.)<1.e-12));
    if ((path!=NULL)&&(path[0]!='\0')&&wanted_l&&
        (index_md==ppt->index_md_scalars)&&(index_tt==ptr->index_tt_e)&&
        (k>=0.02)&&(k<=0.06)) {
      class_test(kmdsb_cross_threshold<0.,ptr->error_message,"KMDSB cross threshold uninitialized");
      double eff=(kmdsb_cross_cf==1)?1.0:ptr->angular_rescaling;
      double rhs=kmdsb_cross_threshold*eff;
      int pred=(l>rhs)?1:0;
      FILE * f=fopen(path,"a");
      class_test(f==NULL,ptr->error_message,"KMDSB cross diagnostic could not open %s",path);
      fprintf(f,"%d %.17g %.17g %.17g %.17g %.17g %.17g %d %d %d %d %.17g %.17g %.17g %d\n",
              index_q,k,l,ptr->angular_rescaling,eff,kmdsb_cross_threshold,rhs,pred,
              (int)ptw->neglect_late_source,index_tau_max_Bessel,index_tau_max,
              tau0_minus_tau[index_tau_max],tau0_minus_tau_min_bessel,*trsf,kmdsb_cross_cf);
      fclose(f);
    }
  }
'''
def H(b):return hashlib.sha256(b).hexdigest()
def main(src,man,pin):
 if pin not in PINS:raise RuntimeError(f'unauthorized pin {pin}')
 raw=src.read_bytes();t=raw.decode()
 for n,a in [('include',INCLUDE),('angular_rescaling',AR),('predicate',PRED),('tail',TAIL)]:
  if t.count(a)!=1:raise RuntimeError(f'{n} anchor count {t.count(a)}')
 if 'KMDSB_M21_CROSS_CF' in t:raise RuntimeError('already installed')
 n=t.replace(INCLUDE,INCLUDE+FILE,1).replace(AR,AR+ARB,1).replace(PRED,PREDB,1).replace(TAIL,TAILB+TAIL,1);src.write_text(n)
 o={'schema':'KMDSB.W04.M21.CrossProviderCounterfactualPatch.v0.1','protocol':PROTOCOL,'provider_pin':pin,'authorized_pins':sorted(PINS),'k_min':KMIN,'k_max':KMAX,'multipoles':[399,400,401],'counterfactual_value':1.0,'counterfactual_operand':'late_source_predicate_angular_rescaling_only','mutates_native_angular_rescaling':False,'thread_control':'OMP_NUM_THREADS=1','original_sha256':H(raw),'patched_sha256':H(src.read_bytes())}
 man.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n');print(json.dumps(o,indent=2,sort_keys=True))
if __name__=='__main__':
 if len(sys.argv)!=4:raise SystemExit('usage: patch TRANSFER_C MANIFEST PIN')
 main(Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3])
