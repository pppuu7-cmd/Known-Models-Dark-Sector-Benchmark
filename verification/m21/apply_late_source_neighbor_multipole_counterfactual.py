#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_CONDITIONAL_LATE_SOURCE_NEIGHBOR_MULTIPOLE_REGRESSION_v0.1.md'
KMIN=0.03030247505892471; KMAX=0.04401375054733766
INCLUDE='#include "parallel.h"\n'
AR='  ptr->angular_rescaling = pth->angular_rescaling;\n'
PRED='  if (l > ppr->transfer_neglect_late_source*ptr->angular_rescaling) {\n'
TAIL='''\n\n  free(radial_function);\n  return _SUCCESS_;\n}\n\n/**\n * This routine computes the transfer functions'''
FILE_LOCAL=r'''

static int kmdsb_m21_neighbor_cf = 0;
static double kmdsb_m21_neighbor_threshold = -1.;
'''
AR_BLOCK=r'''
  {
    const char * e=getenv("KMDSB_M21_NEIGHBOR_CF");
    kmdsb_m21_neighbor_cf=((e!=NULL)&&(e[0]!='\0')&&(pba->sgnK==0))?1:0;
    kmdsb_m21_neighbor_threshold=ppr->transfer_neglect_late_source;
  }
'''
PRED_BLOCK=r'''
  double kmdsb_m21_neighbor_ar=ptr->angular_rescaling;
  if (kmdsb_m21_neighbor_cf==1) kmdsb_m21_neighbor_ar=1.0;
  if (l > ppr->transfer_neglect_late_source*kmdsb_m21_neighbor_ar) {
'''
TAIL_BLOCK=r'''
  {
    const char * path=getenv("KMDSB_M21_NEIGHBOR_DIAG");
    int kmdsb_l=((fabs(l-399.)<1.e-12)||(fabs(l-400.)<1.e-12)||(fabs(l-401.)<1.e-12));
    if ((path!=NULL)&&(path[0]!='\0')&&kmdsb_l&&
        (index_md==ppt->index_md_scalars)&&(index_tt==ptr->index_tt_e)&&
        (k>=0.03030247505892471)&&(k<=0.04401375054733766)) {
      class_test(kmdsb_m21_neighbor_threshold<0.,ptr->error_message,"KMDSB neighbor threshold uninitialized");
      double eff=(kmdsb_m21_neighbor_cf==1)?1.0:ptr->angular_rescaling;
      double rhs=kmdsb_m21_neighbor_threshold*eff;
      int pred=(l>rhs)?1:0;
      FILE * f=fopen(path,"a");
      class_test(f==NULL,ptr->error_message,"KMDSB neighbor diagnostic could not open %s",path);
      fprintf(f,"%d %.17g %.17g %.17g %.17g %.17g %.17g %d %d %d %d %.17g %.17g %.17g %d\n",
              index_q,k,l,ptr->angular_rescaling,eff,kmdsb_m21_neighbor_threshold,rhs,pred,
              (int)ptw->neglect_late_source,index_tau_max_Bessel,index_tau_max,
              tau0_minus_tau[index_tau_max],tau0_minus_tau_min_bessel,*trsf,kmdsb_m21_neighbor_cf);
      fclose(f);
    }
  }
'''
def H(x:bytes)->str:return hashlib.sha256(x).hexdigest()
def main(src:Path,man:Path):
 raw=src.read_bytes(); t=raw.decode()
 for n,a in [('include',INCLUDE),('ar',AR),('pred',PRED),('tail',TAIL)]:
  if t.count(a)!=1: raise RuntimeError(f'{n} anchor count {t.count(a)}')
 if 'KMDSB_M21_NEIGHBOR_CF' in t: raise RuntimeError('already installed')
 n=t.replace(INCLUDE,INCLUDE+FILE_LOCAL,1).replace(AR,AR+AR_BLOCK,1).replace(PRED,PRED_BLOCK,1).replace(TAIL,TAIL_BLOCK+TAIL,1)
 src.write_text(n)
 obj={'schema':'KMDSB.W04.M21.NeighborMultipolePatch.v0.1','protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}','source_path':str(src),'multipoles':[399,400,401],'k_min':KMIN,'k_max':KMAX,'counterfactual_operand':'late_source_predicate_angular_rescaling_only','counterfactual_value':1.0,'mutates_native_angular_rescaling':False,'thread_control':'OMP_NUM_THREADS=1','original_sha256':H(raw),'patched_sha256':H(src.read_bytes())}
 man.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n');print(json.dumps(obj,indent=2,sort_keys=True))
if __name__=='__main__':
 if len(sys.argv)!=3:raise SystemExit('usage: patch TRANSFER_C MANIFEST')
 main(Path(sys.argv[1]),Path(sys.argv[2]))
