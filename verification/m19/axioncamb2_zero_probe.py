#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,re
from pathlib import Path
CASES={'r0f':{'use_axfrac':'T','omdah2':'0.1200','axfrac':'0.0'},'r0d':{'use_axfrac':'F','omch2':'0.1200','omaxh2':'0.0'},'p1':{'use_axfrac':'T','omdah2':'0.1200','axfrac':'0.10'}}
FILES=['scalCls.dat','matterpower.dat','transfer_out.dat']; TOL=1e-10

def repl(s,k,v):
 p=re.compile(rf'(?m)^(\s*{re.escape(k)}\s*=).*?$'); m=list(p.finditer(s))
 if len(m)!=1: raise RuntimeError(f'{k}: active-count={len(m)}')
 return p.sub(lambda x:f'{x.group(1)} {v}',s,count=1)
def prep(base,outdir):
 s=base.read_text(); outdir.mkdir(parents=True,exist_ok=True)
 common={'get_scalar_cls':'T','get_tensor_cls':'F','get_vector_cls':'F','get_transfer':'T','do_lensing':'F','do_nonlinear':'0','m_ax':'1.e-27','axion_isocurvature':'F'}
 for n,c in CASES.items():
  t=s
  for k,v in common.items(): t=repl(t,k,v)
  # axionCAMB appends its own underscore to output_root; use bare case name here.
  t=repl(t,'output_root',n)
  for k,v in c.items(): t=repl(t,k,v)
  (outdir/f'{n}.ini').write_text(t)
def rows(p):
 out=[]
 for line in p.read_text(errors='replace').splitlines():
  s=line.strip()
  if not s or s.startswith('#'): continue
  try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
  except ValueError: continue
  if r:
   if not all(math.isfinite(x) for x in r): raise RuntimeError('nonfinite')
   out.append(r)
 if not out: raise RuntimeError('empty')
 if any(len(r)!=len(out[0]) for r in out): raise RuntimeError('ragged')
 return out
def cmp(a,b):
 if len(a)!=len(b) or len(a[0])!=len(b[0]): return {'pass':False,'shape_match':False}
 ma=1e-30; md=0.; ss=0.; n=0
 for x,y in zip(a,b):
  for u,v in zip(x,y): md=max(md,abs(u-v)); ma=max(ma,abs(u),abs(v)); ss+=(u-v)**2;n+=1
 d=md/ma; return {'pass':d<=TOL,'shape_match':True,'D_inf':d,'rms_normalized':math.sqrt(ss/n)/ma,'max_abs_difference':md,'scale':ma,'rows':len(a),'cols':len(a[0]),'tolerance':TOL}
def analyze(work,status,out):
 st=json.loads(status.read_text()); result={'schema':'KMDSB.M19.axionCAMB2.zeroProbe.v1','provider_pin':'891e779cc0bd422e49f97533e6c2fc761149737d','status':st,'cases':{},'comparisons':{},'physical_falsification':False}
 if st.get('build_exit')!=0: result['classification']='M19_AXIONCAMB2_BUILD_BLOCKED'; out.write_text(json.dumps(result,indent=2)+'\n');return
 contract={}
 for c in CASES:
  contract[c]=True; result['cases'][c]={'exit':st.get(c)}
  for f in FILES:
   p=work/(c+'_'+f)
   try:r=rows(p); result['cases'][c][f]={'rows':len(r),'cols':len(r[0]),'finite':True};
   except Exception as e: result['cases'][c][f]={'finite':False,'error':str(e)}; contract[c]=False
  contract[c]=contract[c] and st.get(c)==0
 if not contract['p1']: cls='M19_AXIONCAMB2_FINITE_CONTROL_BLOCKED'
 elif not contract['r0f'] or not contract['r0d']: cls='M19_AXIONCAMB2_ZERO_REFERENCE_BLOCKED'
 else:
  ok=True
  for f in FILES:
   q=cmp(rows(work/('r0f_'+f)),rows(work/('r0d_'+f)));result['comparisons'][f]=q;ok=ok and q['pass']
  cls='M19_AXIONCAMB2_K1_ZERO_REFERENCE_PASS_WITH_SCOPE' if ok else 'M19_AXIONCAMB2_ZERO_IDENTITY_FAIL'
 result['classification']=cls; out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':
 a=argparse.ArgumentParser();s=a.add_subparsers(dest='cmd',required=True);p=s.add_parser('prepare');p.add_argument('base',type=Path);p.add_argument('outdir',type=Path);q=s.add_parser('analyze');q.add_argument('work',type=Path);q.add_argument('status',type=Path);q.add_argument('out',type=Path);n=a.parse_args(); prep(n.base,n.outdir) if n.cmd=='prepare' else analyze(n.work,n.status,n.out)
