# W05 M32 K0g — umuscl micro-checkpoint preregistration v0.1

Date: 2026-09-12

## Purpose
Test a materially different infrastructure recovery for the pinned EFT-Ramses Intel build after K0f. K0f stage1 produced a valid durable checkpoint but its 25-second compile budget repeatedly stopped while building the single next object `umuscl.o`; later stage2 attempts also suffered external hosted-runner shutdown. This K0g probe compiles exactly that next provider target as its own durable micro-checkpoint.

## Immutable parent
- provider `nat-woodcock/EFT-Ramses@849ddb716041316d0e223ba22badc0d630b72435`;
- parent K0f run `34647841987`;
- parent stage1 artifact `10283774354` (`m32-k0f-stage1`);
- parent checkpoint already contains the earlier exact-pin `.o/.mod` chain and does not contain a completed `umuscl.o`.

## Frozen toolchain and science
Unchanged from K0f: Intel oneAPI `ifx` through Intel MPI `mpiifx`; serial provider-native Makefile target semantics; `F90=mpiifx`; `FFLAGS=-O3 -g -mcmodel=large -traceback -fpe0 -ftrapuv -cpp $(DEFINES)`; exact provider commit; no source, Makefile, preprocessor definition, optimization, DGP parameter, numerical constant, or physics edit.

## Only allowed infrastructure change
Restore the immutable K0f stage1 checkpoint, verify exact provider pin, hash all restored `.o/.mod`, normalize only their mtimes exactly as K0f already authorized, re-hash and require byte equality, then invoke the single explicit provider target `make umuscl.o` with the unchanged compiler and flags. The workflow uses the GitHub job timeout rather than K0f's 25-second shell timeout so one known slow compilation unit can finish. No subsequent object is compiled in this probe.

## Frozen interpretation
- exact pin + checkpoint integrity + `make umuscl.o` rc=0 + nonempty `umuscl.o` -> `M32_K0G_UMUSCL_MICROTARGET_RECOVERED`;
- explicit compiler/linker/source error -> `M32_K0G_UMUSCL_MICROTARGET_COMPILER_BLOCKED`;
- external cancellation/shutdown -> infrastructure blocked, not a compiler/physics failure;
- checkpoint byte mutation during mtime normalization -> integrity failure.

Success authorizes a later prospectively frozen continuation from the new checkpoint. It does not promote K0 and makes no physical claim about DGP.