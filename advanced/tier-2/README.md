# Tier 2 — Drive shaft under combined loading

## Design problem

Check a 25 mm diameter solid shaft carrying a 60 N m bending moment and 50 N m
torque. The torsion span is 400 mm. The baseline twist limit is 1 degree and the
strength design factor is 2.

## Model and assumptions

The prescribed bending moment represents the critical section from a separate
load analysis. The torque is constant over the torsion span. This model computes
nominal elastic surface stress and total twist; it does not solve bearing
reactions, bending displacement, keyway stresses, or rotating fatigue.
See [shared assumptions](../../docs/units-and-assumptions.md).

## Equations

For solid shaft diameter d, torque T, bending moment M, and shear modulus G:

$$
J=\frac{\pi d^4}{32},
\qquad
\sigma_b=\frac{32|M|}{\pi d^3},
\qquad
\tau_t=\frac{16|T|}{\pi d^3}.
$$

$$
\sigma_{\mathrm{VM}}=\sqrt{\sigma_b^2+3\tau_t^2},
\qquad
\theta=\frac{TL}{GJ},
\qquad
m=\rho\frac{\pi d^2}{4}L.
$$

$$
\sigma_{\mathrm{VM}}\leq\frac{S_y}{n},
\qquad
|\theta|\leq\theta_{\mathrm{allow}}.
$$

The combined stress is evaluated at a bending-extreme surface point. E is retained
in the material record but the twist calculation uses G. Theory: [torsion and
yielding references](../../docs/references.md).

## Run

From the repository root:

```bash
python3 advanced/tier-2/python/run_case.py
```

Edit the case JSON or pass `--case` and `--output`.

## Outputs

- `results/report.md`: strength and twist checks.
- `results/result.json`: normal stress, shear stress, equivalent stress, twist, and mass.

## CAD and manufacturing exercise

Model the plain shaft, then sketch a bearing-and-drive arrangement. Identify
which locations need shoulders, retention, bearing fits, or a torque-transmitting
feature. Prepare a turning sequence and identify inspection datums. Treat each
geometric discontinuity as a reason to extend the nominal-stress calculation.

## Experiments

1. Increase diameter by 10 percent; compare stress, twist, and mass.
2. Set torque to zero and confirm the result becomes pure bending.
3. Set bending moment to zero and study pure torsion.
4. Double span while holding the prescribed moments fixed; explain why twist
   changes while the nominal stresses do not.
