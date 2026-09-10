#!/usr/bin/env python3
from pathlib import Path
import sys


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected one anchor, found {n}")
    return text.replace(old, new, 1)


def patch(root: Path) -> None:
    # 1) Trace GetTauStart output before thermodynamics begins.
    p = root / "cmbmain.f90"
    s = p.read_text()
    old = """    taumin=GetTauStart(maxq)\n\n    !     Initialize baryon temperature and ionization fractions vs. time."""
    new = """    taumin=GetTauStart(maxq)\n    if (CP%omegaax .eq. 0._dl) then\n       write(*,*) 'M19TRACE GETTAUSTART', CP%tau0, qmax, maxq, taumin, adotrad, nu_masses(1)\n    endif\n\n    !     Initialize baryon temperature and ionization fractions vs. time."""
    p.write_text(replace_once(s, old, new, "cmbmain GetTauStart trace"))

    # 2) Trace state around modified RECFAST and immediately before the first
    #    thermodynamic dtauda call. This is print-only instrumentation.
    p = root / "modules.f90"
    s = p.read_text()
    old = """    call Recombination_Init(CP%Recomb, CP%omegac,CP%omegab,CP%Omegan,&\n         CP%Omegav,CP%h0,CP%tcmb,CP%yhe,CP%omegaax,CP%omegar,&\n         ntable,CP%aeq,CP%a_osc,CP%drefp_hsq,CP%loga_table,&\n         CP%grhoax_table,CP%grhoax_table_buff)"""
    new = """    if (CP%omegaax .eq. 0._dl) then\n       write(*,*) 'M19TRACE PRE_RECFAST', taumin, taumax, adotrad, nu_masses(1), CP%aeq, CP%a_osc, CP%drefp_hsq\n    endif\n    call Recombination_Init(CP%Recomb, CP%omegac,CP%omegab,CP%Omegan,&\n         CP%Omegav,CP%h0,CP%tcmb,CP%yhe,CP%omegaax,CP%omegar,&\n         ntable,CP%aeq,CP%a_osc,CP%drefp_hsq,CP%loga_table,&\n         CP%grhoax_table,CP%grhoax_table_buff)\n    if (CP%omegaax .eq. 0._dl) then\n       write(*,*) 'M19TRACE POST_RECFAST', taumin, taumax, adotrad, nu_masses(1), CP%aeq, CP%a_osc, CP%drefp_hsq\n    endif"""
    s = replace_once(s, old, new, "modules RECFAST trace")
    old = """        adot=1/dtauda(a)\n\n        if (matter_verydom_tau ==0 .and. a > a_verydom) then"""
    new = """        if (CP%omegaax .eq. 0._dl .and. i .le. 4) then\n           write(*,*) 'M19TRACE INITHERMO_A', i, tauminn, a0, dtau, a, adot0, nu_masses(1), a*nu_masses(1)\n        endif\n        adot=1/dtauda(a)\n\n        if (matter_verydom_tau ==0 .and. a > a_verydom) then"""
    s = replace_once(s, old, new, "modules inithermo dtauda trace")
    p.write_text(s)

    # 3) Trace exact argument passed to Nu_rho from background dtauda.
    p = root / "equations_ppf.f90"
    s = p.read_text()
    old = """    integer nu_i\n\n    a2=a**2"""
    new = """    integer nu_i\n    integer, save :: m19_trace_dtauda_count = 0\n\n    a2=a**2"""
    s = replace_once(s, old, new, "dtauda trace counter declaration")
    old = """        do nu_i = 1, CP%nu_mass_eigenstates\n            call Nu_rho(a*nu_masses(nu_i),rhonu)\n            grhoa2=grhoa2+rhonu*grhormass(nu_i)\n        end do"""
    new = """        do nu_i = 1, CP%nu_mass_eigenstates\n            if (CP%omegaax .eq. 0._dl .and. m19_trace_dtauda_count .lt. 16) then\n               write(*,*) 'M19TRACE DTAUDA_NURHO', m19_trace_dtauda_count, a, nu_masses(nu_i), a*nu_masses(nu_i), grhoa2\n            endif\n            m19_trace_dtauda_count = m19_trace_dtauda_count + 1\n            call Nu_rho(a*nu_masses(nu_i),rhonu)\n            grhoa2=grhoa2+rhonu*grhormass(nu_i)\n        end do"""
    p.write_text(replace_once(s, old, new, "dtauda Nu_rho trace"))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: axioncamb2_zero_value_trace.py <axionCAMB source dir>")
    patch(Path(sys.argv[1]))
