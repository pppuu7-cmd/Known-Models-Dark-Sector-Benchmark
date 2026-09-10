# W03 M14 LisaGoh/CDE provider-control preregistration v0.1

Date: 2026-09-10
Target: F14/M14 coupled quintessence / conformal scalar-DM coupling
Purpose: establish whether the exact public paper-linked `LisaGoh/CDE` source builds and executes its committed author workload before any KMDSB parameter modification.

## Frozen provider

- repository: `LisaGoh/CDE`
- commit: `b85a675af7544a5183e402964550811aa805b698`
- source root: `class_CDE/`
- author workload: `class_CDE/CDE.ini`

No source or INI physics edit is authorized in this control.

## Provenance/family facts frozen before execution

Repository README identifies this as the modified CLASS used for Goh et al. arXiv:2211.13588, extending earlier constant-coupling CDE implementations.

Source audit already found active:

- coupled CDM background conservation with `beta rho_c phi'` exchange;
- compensating scalar-field source;
- coupled CDM density and velocity perturbation equations;
- coupled scalar perturbation equation including beta/beta-prime sources;
- scalar perturbation contribution to Einstein sources.

Thus execution is scientifically worth testing as an independent M14 source-complete perturbation candidate.

## Frozen execution

1. clone the exact repository and checkout the exact commit;
2. enter `class_CDE`;
3. record compiler/Python/runtime information;
4. compile the source with its committed Makefile (`make clean`, then `make -j2`);
5. execute exactly `./class CDE.ini`;
6. do not alter the author INI, coupling amplitudes, ICs, precision files, nonlinear switch, output list or source code;
7. inventory files created/modified by the run.

## Provider-control PASS rule

`M14_LISAGOH_CDE_PROVIDER_CONTROL_PASS` requires:

- compilation exit code 0;
- author workload exit code 0;
- at least one fresh background product;
- at least one fresh linear matter-power product;
- at least one fresh CMB Cl product;
- at least one fresh transfer product;
- all discovered required output files nonempty.

If build/run fails, classify `BLOCKED_IMPLEMENTATION_OR_RUNTIME` and preserve logs. That is not a physical failure of M14.

## Scientific scope

Provider-control PASS establishes executable K0 infrastructure only. It does not itself promote K1, K3, K4 or K5, even though source audit indicates active perturbation coupling. K1 must be separately preregistered after the exact author workload is shown executable.
