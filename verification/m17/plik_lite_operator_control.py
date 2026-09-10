#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, sys
from pathlib import Path
import numpy as np
import scipy.linalg
from scipy.io import FortranFile

PIN='2c0d0f67e59ce781654cf62dd7fb10757b0e60be'
EXPECTED=-291.33481235418026
TOL=1e-9
FILES=[
 'planck_lite_py.py',
 'data/planck2018_plik_lite/c_matrix_plik_v22.dat',
 'data/planck2018_plik_lite/cl_cmb_plik_v22.dat',
 'data/planck2018_plik_lite/blmin.dat',
 'data/planck2018_plik_lite/blmax.dat',
 'data/planck2018_plik_lite/bweight.dat',
]

def sha256(p:Path):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()

def load_module(root:Path):
 spec=importlib.util.spec_from_file_location('planck_lite_py',root/'planck_lite_py.py')
 mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod); return mod

def main(root:Path,out:Path):
 res={'schema':'KMDSB.M17.PlikLiteOperatorControl.v1','operator_pin':PIN,'expected_loglike':EXPECTED,'tolerance':TOL,'preregistration':'protocol/W03_M17_PLANCK2018_PLIK_LITE_OPERATOR_CONTROL_PREREGISTRATION_v0.1.md','physical_falsification':False,'scientific_promotion':False}
 try:
  res['sha256']={x:sha256(root/x) for x in FILES}
  mod=load_module(root)
  like=mod.PlanckLitePy(data_directory=str(root/'data'),year=2018,spectra='TTTEEE',use_low_ell_bins=False)
  checks={
   'nbintt_hi':int(like.nbintt_hi), 'nbinte':int(like.nbinte), 'nbinee':int(like.nbinee), 'nbin_hi':int(like.nbin_hi),
   'plmin':int(like.plmin), 'plmax':int(like.plmax)
  }
  checks['bin_counts_pass']=(checks['nbintt_hi'],checks['nbinte'],checks['nbinee'],checks['nbin_hi'])==(215,199,199,613)
  covfile=root/'data/planck2018_plik_lite/c_matrix_plik_v22.dat'
  f=FortranFile(covfile,'r'); cov=f.read_reals(dtype=float).reshape((613,613)); f.close()
  for i in range(613):
   for j in range(i,613): cov[i,j]=cov[j,i]
  checks['cov_shape']=list(cov.shape); checks['cov_finite']=bool(np.isfinite(cov).all())
  checks['cov_sym_max_abs']=float(np.max(np.abs(cov-cov.T)))
  try:
   scipy.linalg.cholesky(cov,lower=True,check_finite=True); checks['cov_cholesky_pass']=True
  except Exception as e:
   checks['cov_cholesky_pass']=False; checks['cov_cholesky_error']=repr(e)
  blmin=np.loadtxt(root/'data/planck2018_plik_lite/blmin.dat')
  blmax=np.loadtxt(root/'data/planck2018_plik_lite/blmax.dat')
  bw=np.loadtxt(root/'data/planck2018_plik_lite/bweight.dat')
  checks['bin_arrays_finite']=bool(np.isfinite(blmin).all() and np.isfinite(blmax).all() and np.isfinite(bw).all())
  checks['bin_boundaries_integer']=bool(np.all(blmin==blmin.astype(int)) and np.all(blmax==blmax.astype(int)))
  checks['bin_weight_count']=int(bw.size)
  ls,Dltt,Dlte,Dlee=np.genfromtxt(root/'data/Dl_planck2015fit.dat',unpack=True)
  measured=float(like.loglike(Dltt,Dlte,Dlee,int(ls[0])))
  checks['selftest_measured']=measured; checks['selftest_abs_error']=abs(measured-EXPECTED); checks['selftest_pass']=abs(measured-EXPECTED)<=TOL
  res['checks']=checks
  structure=checks['bin_counts_pass'] and checks['cov_shape']==[613,613] and checks['cov_finite'] and checks['cov_sym_max_abs']<=1e-14 and checks['cov_cholesky_pass'] and checks['bin_arrays_finite'] and checks['bin_boundaries_integer']
  if not structure: cls='M17_PLIK_LITE_OPERATOR_STRUCTURE_FAIL'
  elif not checks['selftest_pass']: cls='M17_PLIK_LITE_OPERATOR_NUMERICAL_FAIL'
  else: cls='M17_PLIK_LITE_OPERATOR_CONTROL_PASS'
 except FileNotFoundError as e:
  cls='M17_PLIK_LITE_OPERATOR_PROVENANCE_BLOCKED'; res['error']=repr(e)
 except Exception as e:
  cls='M17_PLIK_LITE_OPERATOR_STRUCTURE_FAIL'; res['error']=repr(e)
 res['classification']=cls
 out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
 print(json.dumps(res,indent=2,sort_keys=True))

if __name__=='__main__':
 ap=argparse.ArgumentParser(); ap.add_argument('root',type=Path); ap.add_argument('out',type=Path); ns=ap.parse_args(); main(ns.root,ns.out)
