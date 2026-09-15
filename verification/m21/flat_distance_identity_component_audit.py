#!/usr/bin/env python3
from __future__ import annotations
import json,math,pathlib,struct,sys

EXPECTED={'ref':-5,'f2':-4,'f3':1,'f4':-2}
CASES=('ref','f2','f3','f4')
PROTOCOL='protocol/W04_M21_FLAT_DISTANCE_IDENTITY_COMPONENT_AUDIT_v0.1.md'

def ordered_pos_ulp(a,b):
 if a<=0 or b<=0: raise ValueError('positive doubles required')
 ia=struct.unpack('>Q',struct.pack('>d',a))[0]; ib=struct.unpack('>Q',struct.pack('>d',b))[0]
 return int(ia)-int(ib)

def load_row(p):
 rows=[]
 for raw in pathlib.Path(p).read_text(errors='replace').splitlines():
  s=raw.strip()
  if not s: continue
  x=[float(v.replace('D','E').replace('d','e')) for v in s.split()]
  if len(x)==11 and all(math.isfinite(v) for v in x): rows.append(x)
 if len(rows)!=1: raise RuntimeError(f'expected one row in {p}, got {len(rows)}')
 return rows[0]

def find_one(root,pat):
 xs=list(pathlib.Path(root).rglob(pat))
 if len(xs)!=1: raise RuntimeError(f'{pat}: {xs}')
 return xs[0]

def main(root,out):
 root=pathlib.Path(root); results={}; authority=True
 dirs=[d for d in root.iterdir() if d.is_dir()]
 for c in CASES:
  matches=[]
  for d in dirs:
   ms=list(d.rglob('case_meta.json'))
   if len(ms)==1:
    m=json.load(open(ms[0]))
    if m.get('case')==c: matches.append((d,m))
  if len(matches)!=1: raise RuntimeError(f'component {c}: {matches}')
  d,m=matches[0]; authority &= m.get('authority_clean') is True
  r=load_row(find_one(d,f'flat_distance_{c}.dat'))
  sgnK,zrec,taurec,tau0,den,da,ra,absres,relres,ar,ar1=r
  distance_ulp=ordered_pos_ulp(ra,den)
  ar_ulp=ordered_pos_ulp(ar,1.0)
  ratio=ra/den
  ratio_consistent=(ratio==ar)
  results[c]={
   'sgnK':int(round(sgnK)),'z_rec':zrec,'tau_rec':taurec,'conformal_age':tau0,
   'denominator':den,'da_rec':da,'ra_rec':ra,'distance_absolute_residual':absres,'distance_relative_residual':relres,
   'distance_signed_ulp_ra_minus_denominator':distance_ulp,'angular_rescaling':ar,'angular_rescaling_minus_1':ar1,
   'angular_rescaling_signed_ulp_from_1':ar_ulp,'ratio_recomputes_exactly':ratio_consistent,
   'null_cl_l2':m.get('null_cl_l2')}
 pattern={c:results[c]['angular_rescaling_signed_ulp_from_1'] for c in CASES}
 pattern_ok=pattern==EXPECTED
 all_flat=all(results[c]['sgnK']==0 for c in CASES)
 ratio_ok=all(results[c]['ratio_recomputes_exactly'] for c in CASES)
 if authority and all_flat and ratio_ok and pattern_ok:
  cls='M21_FLAT_DISTANCE_INTERPOLATION_RESIDUAL_REPRODUCED_WITH_SCOPE'; rc=0
 elif authority and all_flat and ratio_ok:
  cls='M21_FLAT_DISTANCE_COMPONENT_PATTERN_MISMATCH_BLOCKED'; rc=1
 else:
  cls='M21_FLAT_DISTANCE_COMPONENT_AUDIT_BLOCKED'; rc=1
 obj={'schema':'KMDSB.W04.M21.FlatDistanceIdentityComponentAudit.v0.1','protocol':PROTOCOL,'classification':cls,
      'authority_clean':authority,'all_flat':all_flat,'ratio_consistent':ratio_ok,'expected_angular_rescaling_ulp_pattern':EXPECTED,
      'observed_angular_rescaling_ulp_pattern':pattern,'pattern_reproduced':pattern_ok,'cases':results,
      'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
 pathlib.Path(out).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps(obj,indent=2,sort_keys=True)); return rc

if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: flat_distance_identity_component_audit.py COMPONENTS OUT')
 raise SystemExit(main(sys.argv[1],sys.argv[2]))
