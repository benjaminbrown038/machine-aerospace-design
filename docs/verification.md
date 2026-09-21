# Starter verification record

Verified with Python 3.12.14 using the bundled cases. The source uses Python 3.9
compatible syntax; Python 3.9 itself was not available in the build environment.

## Baseline results

| Tier | Selected result | Implemented checks |
|---|---|---|
| 1 | 41.667 MPa nominal bending stress; 0.754831 mm tip displacement; 0.1458 kg | Pass |
| 2 | Combined nominal stress and twist within case limits | Pass |
| 3 | Bolt forces recover 300 N in x, -1000 N in y, and -120 N m about the centroid | Pass |
| 4 | 1805.933 N sampled required capacity including design factor; 61.258 mm stroke | Pass |
| 5 | 11 of 60 candidates feasible; lightest is illustrative aluminum, 20 mm wide and 14 mm high, 0.1134 kg | Pass |

These are reproducibility values for the supplied analytical models, not
physical validation of hardware. Changing an input changes the reference case.

## Automated checks

All 12 tests passed. They cover a numerical hand result, clamp displacement,
dimension scaling, zero/reversed loading, pure stress modes, bolt force/moment
balance, coordinate translation invariance, equal load sharing, actuator moment
balance, a dead center hidden between samples, infeasible sizing, invalid inputs,
and JSON output of singular conditions.

```bash
python3 -m unittest discover -s tests -v
```

The singular-mechanism test deliberately prints a design FAIL. The test succeeds
when that invalid design is detected. A test pass does not mean every possible
design passes.

All five baseline entry points were executed. Local Markdown links and paired
display-math delimiters were checked. Native CAD, FEA, physical testing, and
aircraft compliance have not been performed.
