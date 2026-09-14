#!/usr/bin/env python3
from __future__ import annotations
import json,tempfile
from pathlib import Path
import importlib.util
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('selector',HERE/'select_k1v2_numerical_reference.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
TAIL='M21_G2B_L_SAMPLING_TAIL_CONTRACTION_SUPPORTED_WITH_SCOPE'
def run(tc,lc=TAIL,ti=True,li=True):
 with tempfile.TemporaryDirectory() as td:
  td=Path(td); t=td/'t.json'; l=td/'l.json'; o=td/'o.json'
  t.write_text(json.dumps({'classification':tc,'cross_lane_input_identity':ti})); l.write_text(json.dumps({'classification':lc,'cross_lane_input_identity':li}))
  mod.main(t,l,o); return json.loads(o.read_text())
def main():
 a=run('M21_THERMO_NDF15_SPECIFIC_SENSITIVITY_SUPPORTED'); assert a['authorized'] is True and a['thermo_evolver']=='rk' and a['thermo_evolver_serialized']=='0'
 b=run('M21_THERMO_SOLVER_INDEPENDENT_TIGHT_LIMIT_SUPPORTED_WITH_SCOPE'); assert b['authorized'] is True and b['thermo_evolver']=='ndf15' and b['thermo_evolver_serialized']=='1'
 for bad in ('M21_THERMO_EVOLVER_DEPENDENCE_MIXED','M21_THERMO_TOLERANCE_EFFECT_NOT_SUPPORTED_AT_TIGHT_LIMIT','M21_THERMO_EVOLVER_CROSSCHECK_BLOCKED'):
  x=run(bad); assert x['authorized'] is False and x['thermo_evolver'] is None
 assert run('M21_THERMO_NDF15_SPECIFIC_SENSITIVITY_SUPPORTED','M21_G2B_L_SAMPLING_TAIL_REMOVAL_STABLE_DISTANCE_NONMONOTONE')['authorized'] is False
 assert run('M21_THERMO_NDF15_SPECIFIC_SENSITIVITY_SUPPORTED',ti=False)['authorized'] is False
 assert run('M21_THERMO_NDF15_SPECIFIC_SENSITIVITY_SUPPORTED',li=False)['authorized'] is False
 print('M21 K1-v2 selector synthetic tests PASS')
if __name__=='__main__': main()
