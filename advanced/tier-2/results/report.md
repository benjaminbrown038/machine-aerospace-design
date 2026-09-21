# Drive shaft under bending and torsion

Educational analytical screening result.

Status: **PASS** for the implemented checks.

- `model`: shaft
- `J_m4`: 3.8349519697141036e-08
- `bending_stress_Pa`: 39113918.81426419
- `torsional_shear_Pa`: 16297466.17261008
- `von_mises_Pa`: 48236094.94922821
- `twist_rad`: 0.006772972954850943
- `twist_deg`: 0.3880627650692093
- `mass_kg`: 1.5413438956674925
- `passes`: True

| Check | Demand | Allowable | Utilization | Pass |
|---|---:|---:|---:|---|
| von_mises_Pa | 4.82361e+07 | 1.75e+08 | 0.2756 | True |
| twist_rad | 0.00677297 | 0.0174533 | 0.3881 | True |

Inputs and full results: `result.json`. Units follow the field suffixes.
Read the tier README for omitted failure modes and model limits.
