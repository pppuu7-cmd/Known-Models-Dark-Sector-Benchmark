#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('k1v2',HERE/'k1v2_numerically_resolved_reference.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def gate(r,q):
    # floors chosen so R/F=q pointwise
    f=[ri/qi for ri,qi in zip(r,q)]
    return mod.pass_route(r,f)

def main():
    # Route A: all points clearly identified and contract with ~linear f_w.
    a=gate([1.0,0.30,0.10,0.030,0.010],[10,10,10,10,10])
    assert a['pass'] is True and a['route']=='A_IDENTIFIED'

    # Route B valid: identified prefix contracts, then numerical equivalence persists.
    b=gate([1.0,0.30,0.10,0.030,0.010],[10,8,2,1,0.5])
    assert b['pass'] is True and b['route']=='B_NUMERICAL_EQUIVALENCE'

    # Once equivalent, an identified smaller fraction may not re-emerge.
    c=gate([1.0,0.30,0.10,0.030,0.010],[10,2,5,1,0.5])
    assert c['pass'] is False

    # Frozen edge condition: if only f=0.10 is identified then f=0.03 enters
    # equivalence, the 'last identified below f=0.10' condition is NOT met,
    # because the last identified point is f=0.10 itself.
    d=gate([1.0,0.30,0.10,0.030,0.010],[10,2,1,1,0.5])
    assert d['pass'] is False and d.get('first_equivalent_index')==1

    # If even f=0.10 is already numerically equivalent and equivalence persists,
    # no identified-prefix amplitude condition is required.
    e=gate([1.0,0.30,0.10,0.030,0.010],[2,2,2,2,2])
    assert e['pass'] is True and e['route']=='B_NUMERICAL_EQUIVALENCE'

    print('M21 K1-v2 synthetic gate logic PASS')
if __name__=='__main__': main()
