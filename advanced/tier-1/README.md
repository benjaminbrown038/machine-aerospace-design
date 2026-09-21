# Tier 1 — Cantilever equipment support

## Design problem

Size the straight arm of an equipment support for a 200 N transverse tip load.
The baseline arm is 150 mm long, 30 mm wide, and 12 mm high. It must keep tip
deflection below 1 mm and satisfy a nominal bending-strength check with a design
factor of 2. The height is the dimension in the bending direction.

## Model and assumptions

A uniform rectangular beam is perfectly clamped at x = 0 and loaded at x = L.
The material is linear elastic. The calculation omits the actual mount, root
fillet, bolt holes, self-weight, and shear deformation. It screens L/h >= 10 and
absolute deflection/L <= 0.05. See [shared assumptions](../../docs/units-and-assumptions.md).

## Equations

For length L, width b, height h, elastic modulus E, density rho, and tip load F:

$$
I=\frac{bh^3}{12},
\qquad
M_{\mathrm{root}}=FL,
\qquad
\sigma_{\mathrm{max}}=\frac{|F|L(h/2)}{I}.
$$

$$
v(x)=\frac{Fx^2(3L-x)}{6EI},
\qquad
v(L)=\frac{FL^3}{3EI},
\qquad
m=\rho Lbh.
$$

$$
\sigma_{\mathrm{max}}\leq\frac{S_y}{n},
\qquad
|v(L)|\leq v_{\mathrm{allow}}.
$$

The sign of F sets the displacement direction; the stress check uses magnitude.
Theory: [beam stress](../../docs/references.md) and beam displacement references.

## Run

From the repository root:

```bash
python3 advanced/tier-1/python/run_case.py
```

Edit `cases/baseline.json`, or pass `--case` and `--output` as shown in the root
README. Baseline material properties are illustrative.

## Outputs

- `results/report.md`: bending and deflection checks.
- `results/result.json`: complete inputs and outputs in SI units.
- `results/profile.csv`: displacement along the beam.

The baseline nominal stress is approximately **41.67 MPa**, tip displacement
**0.755 mm**, and arm mass **0.1458 kg**.

## CAD and manufacturing exercise

Create the rectangular arm with the baseline dimensions in your CAD system.
Sketch the clamp and applied load separately so the analytical span is clear.
Then develop a practical attachment with a root fillet and fastener access.
Create a drawing with the mounting interface, stock size, and inspection plan.
The detailed attachment requires additional analysis beyond this beam model.

## Experiments

1. Double the load. Predict both stress and deflection before running.
2. Double width and compare with doubling height; explain the different effects.
3. Change E while holding geometry and load fixed. Which result changes?
4. Compare the analytical displacement with a simple cantilever FEA case.
