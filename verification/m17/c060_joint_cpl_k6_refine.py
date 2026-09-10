#!/usr/bin/env python3
"""Execute the mechanically preregistered M17 c=0.6 K6 joint-CPL refinement."""
from __future__ import annotations
import argparse,json,math,re
from pathlib import Path
W0C=-1.299870066355541; WAC=0.9082964747357177
DW0=[-0.10,-0.05,0.0,0.05,0.10]; DWA=[-0.20,-0.10,0.0,0.10,0.20]
LIKES=['DEFAULT(batch3/plik_rd12_HM_v22_TTTEEE.ini)','DEFAULT(batch3/lowl.ini)','DEFAULT(batch3/lowE.ini)','DEFAULT(batch3/lensing.ini)','DEFAULT(batch3/BAO.ini)','DEFAULT(batch3/Pantheon18.ini)']
def ro(s,o,n):
 c=s.count(o)
 if c!=1: raise RuntimeError(f'anchor {o!r} count={c}')
 return s.replace(o,n,1)
def rk(s,k,v):
 p=re.compile(rf'(?m)^(\s*{re.escape(k)}\s*=).*?$'); m=list(p.finditer(s))
 if len(m)!=1: raise RuntimeError(f'{k}: active count={len(m)}')
 return p.sub(lambda x:f'{x.group(1)} {v}',s,count=1)
def allcases():
 d={'r0':{'kind':'cpl','w0':-1.,'w1':0.},'h06':{'kind':'hde','c':0.6}}
 for i,x in enumerate(DW0):
  for j,y in enumerate(DWA): d[f'r{i}{j}']={'kind':'cpl','w0':W0C+x,'w1':WAC+y,'dw0':x,'dwa':y}
 return d
CASES=allcases()
def prepare(base,outdir):
 s=base.read_text()
 for x in LIKES:s=ro(s,x,'#'+x)
 s=ro(s,'DEFAULT(batch3/common.ini)','DEFAULT(batch3/common.ini)\nuse_nonlinear_lensing = F')
 s=ro(s,'#Use_PPF = F','Use_PPF = T'); s=ro(s,'test_check_compare = 1820.775','#test_check_compare = 1820.775'); s=ro(s,'#test_output_root = output_ide','test_output_root = PLACEHOLDER')
 outdir.mkdir(parents=True,exist_ok=True)
 for n,c in CASES.items():
  t=s.replace('test_output_root = PLACEHOLDER',f'test_output_root = m17k6r_{n}'); t=rk(t,'param[beta_cf]','0')
  if c['kind']=='hde': t=rk(t,'WForm_CF','2'); t=rk(t,'param[c_hde]',repr(c['c']))
  else: t=rk(t,'WForm_CF','1'); t=rk(t,'param[w0]',repr(c['w0'])); t=rk(t,'param[w1]',repr(c['w1']))
  (outdir/f'{n}.ini').write_text(t)
 (outdir/'manifest.json').write_text(json.dumps(CASES,indent=2,sort_keys=True)+'\n')
def nums(s):return [float(x.replace('D','E').replace('d','e')) for x in s.split()]
def theory(p):
 z=[]
 for line in p.read_text(errors='replace').splitlines():
  s=line.strip()
  if not s or s.startswith('#'):continue
  try:r=nums(s)
  except ValueError:continue
  if len(r)!=4 or not all(math.isfinite(x) for x in r):raise RuntimeError(f'bad theory row {p}')
  z.append(r)
 if len(z)<2000:raise RuntimeError(f'{p}: rows={len(z)}')
 return z
def quant(p):
 z=[]
 for line in p.read_text(errors='replace').splitlines():
  s=line.strip()
  if not s or s.startswith('#'):continue
  try:r=nums(s)
  except ValueError:continue
  if len(r)!=11 or not all(math.isfinite(x) for x in r[:7]):raise RuntimeError(f'bad quantity row {p}')
  z.append(r[:7])
 if len(z)!=2000:raise RuntimeError(f'{p}: rows={len(z)}')
 return z
def norm(v):return math.sqrt(sum(x*x for x in v))
def analyze(work,statusp,out):
 st=json.loads(statusp.read_text()); th={};qu={};problems=[];iso={}
 for n in CASES:
  txt=(work.parent/f'm17k6r_{n}.log').read_text(errors='replace') if (work.parent/f'm17k6r_{n}.log').exists() else ''
  iso[n]='Doing non-linear lensing: F' in txt
  if int(st.get(n,999))!=0:problems.append(f'{n}:exit={st.get(n)}')
  if not iso[n]:problems.append(f'{n}:nonlinear-lensing-isolation-missing')
  try:th[n]=theory(work/f'm17k6r_{n}.theory_cl')
  except Exception as e:problems.append(f'{n}:theory:{e}')
  try:qu[n]=quant(work/f'm17k6r_{n}.quantity')
  except Exception as e:problems.append(f'{n}:quantity:{e}')
 if not problems:
  ell=[int(round(r[0])) for r in th['r0']]; aa=[r[0] for r in qu['r0']]
  for n in CASES:
   if [int(round(r[0])) for r in th[n]]!=ell:problems.append(f'{n}:ell-grid')
   aq=[r[0] for r in qu[n]]
   if len(aq)!=len(aa) or max(abs(x-y) for x,y in zip(aq,aa))>1e-14:problems.append(f'{n}:a-grid')
 res={'schema':'KMDSB.M17.c060.jointCPLK6.refinement.v1','provider':{'cosmomc':'eb08c2fe91d9711929802fede310ae58c020fcb4','idecamb':'4f1093d9efe46f28cf7e2acb4d07ae116ad5e075'},'grid':{'center':{'w0':W0C,'wa':WAC},'delta_w0':DW0,'delta_wa':DWA,'n':25},'status':st,'linear_isolation_flags':iso,'physical_falsification':False,'observational_significance_claim':False,'activation':'protocol/W03_M17_C060_JOINT_CPL_K6_REFINEMENT_EXECUTION_v0.1.md'}
 if problems:
  res['classification']='M17_C060_K6_REFINEMENT_OUTPUT_BLOCKED';res['problems']=problems;out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n');return
 blocks={'H':([r[4] for r in qu['h06']],[r[4] for r in qu['r0']]),'TT':([r[1] for r in th['h06']],[r[1] for r in th['r0']]),'TE':([r[2] for r in th['h06']],[r[2] for r in th['r0']]),'EE':([r[3] for r in th['h06']],[r[3] for r in th['r0']])}
 tn={b:norm([x-y for x,y in zip(h,r)]) for b,(h,r) in blocks.items()};res['target_response_norms']=tn
 cand=[]
 for n,c in CASES.items():
  if not n.startswith('r') or n=='r0':continue
  rb={}
  for b in ('H','TT','TE','EE'):
   if tn[b]<=1e-20:continue
   p=[r[4] for r in qu[n]] if b=='H' else [r[{'TT':1,'TE':2,'EE':3}[b]] for r in th[n]]
   rb[b]=norm([x-y for x,y in zip(blocks[b][0],p)])/tn[b]
  vals=list(rb.values());rj=math.sqrt(sum(x*x for x in vals)/len(vals));rm=max(vals)
  cand.append({'case':n,'w0':c['w0'],'wa':c['w1'],'delta_w0':c['dw0'],'delta_wa':c['dwa'],'R_blocks':rb,'R_joint':rj,'R_max':rm})
 cand.sort(key=lambda x:(x['R_joint'],x['R_max'],x['case']));best=cand[0]
 if best['R_joint']<=0.10 and best['R_max']<=0.20:cl='M17_C060_K6_REFINEMENT_STRONG_ABSORPTION'
 elif best['R_joint']<=0.30 and best['R_max']<=0.50:cl='M17_C060_K6_REFINEMENT_PARTIAL_ABSORPTION'
 else:cl='M17_C060_K6_REFINEMENT_SURVIVOR'
 res['classification']=cl;res['best']=best;res['ties_within_1e-12']=[x for x in cand if abs(x['R_joint']-best['R_joint'])<=1e-12];res['candidates']=cand;res['next']='if survivor, freeze K6 status and design K7 covariance/observation-space profiling; if absorbed, retain comparator absorption result'
 out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':
 a=argparse.ArgumentParser();s=a.add_subparsers(dest='cmd',required=True);p=s.add_parser('prepare');p.add_argument('base',type=Path);p.add_argument('outdir',type=Path);q=s.add_parser('analyze');q.add_argument('work',type=Path);q.add_argument('status',type=Path);q.add_argument('out',type=Path);n=a.parse_args();prepare(n.base,n.outdir) if n.cmd=='prepare' else analyze(n.work,n.status,n.out)
