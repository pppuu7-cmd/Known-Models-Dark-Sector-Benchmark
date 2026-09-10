#!/usr/bin/env python3
from pathlib import Path
import sys


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected one anchor, found {n}")
    return text.replace(old, new, 1)


def patch(src: Path) -> None:
    p = src / "recfast_axion.f90"
    s = p.read_text()
    old1 = """        z=1/a-1
        if (z.ge.zrec(1)) then"""
    new1 = """        write(*,'(A,1PE24.16)') 'KMDSB_RECFAST_A=',a
        if (a.ne.a .or. abs(a).gt.huge(a) .or. a.le.0._dl) then
          write(*,*) 'KMDSB_RECFAST_BAD_A'
          stop 91
        endif
        z=1/a-1
        write(*,'(A,1PE24.16)') 'KMDSB_RECFAST_Z=',z
        if (z.ne.z .or. abs(z).gt.huge(z)) then
          write(*,*) 'KMDSB_RECFAST_BAD_Z'
          stop 92
        endif
        if (z.ge.zrec(1)) then"""
    s = replace_once(s, old1, new1, "pre-z instrumentation")
    old2 = """          zst=(zinitial-z)/delta_z
          ihi= int(zst)
          ilo = ihi+1"""
    new2 = """          zst=(zinitial-z)/delta_z
          write(*,'(A,1PE24.16)') 'KMDSB_RECFAST_ZST=',zst
          write(*,'(A,1PE24.16)') 'KMDSB_RECFAST_ZINITIAL=',zinitial
          write(*,'(A,1PE24.16)') 'KMDSB_RECFAST_DELTA_Z=',delta_z
          if (zst.ne.zst .or. abs(zst).gt.huge(zst) .or. zst.lt.0._dl .or. zst.gt.real(nz-1,dl)) then
            write(*,*) 'KMDSB_RECFAST_BAD_ZST'
            stop 93
          endif
          ihi= int(zst)
          ilo = ihi+1"""
    s = replace_once(s, old2, new2, "pre-index instrumentation")
    p.write_text(s)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: axioncamb2_recfast_input_diag.py SOURCE_DIR")
    patch(Path(sys.argv[1]))
