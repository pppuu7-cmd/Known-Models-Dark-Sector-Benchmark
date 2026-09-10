# W03 M14 IDECAMB author execution probe preregistration v0.1

Date: 2026-09-10
Scope: provider execution/data-dependency probe only. No K1-K9 promotion.

## Immutable inputs
- IDECAMB `4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- CosmoMC base `eb08c2fe91d9711929802fede310ae58c020fcb4`
- exact committed IDECAMB `test_ide.ini`, unmodified
- exact author overlay rule
- compiler-only compatibility flag `-fallow-argument-mismatch`, already validated in run `34452783661`

## Frozen procedure
1. build the exact overlay with the validated compiler compatibility flag;
2. execute `./cosmomc test_ide.ini` exactly as documented by the IDECAMB README;
3. do not edit `Class_IDE`, likelihood defaults, action, parameters, paths inside the ini, or physics sources;
4. preserve exit code and stdout/stderr tail.

## Classification
- exit 0: `M14_IDECAMB_AUTHOR_EXECUTION_PASS`;
- failure whose first actionable error is absent external likelihood/data product: `M14_IDECAMB_AUTHOR_EXECUTION_BLOCKED_EXTERNAL_DATA`;
- provider/runtime failure after required data are resolved/present: `M14_IDECAMB_AUTHOR_EXECUTION_RUNTIME_BLOCKED`.

Missing external likelihood data is not a physics failure and does not invalidate the successful build control.
