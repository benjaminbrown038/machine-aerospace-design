# Tier 4 — Actuated access-door arm

## Design problem

An actuator connects a fixed anchor A to a point B on a rotating arm. Determine
the required length range and force to resist a constant 40 N m moment from
10 to 80 degrees. This is an idealized access-door mechanism geometry study.

## Model and assumptions

The arm pivots at O = [0, 0]. Its attachment radius is 60 mm; the fixed anchor
is [-100, 80] mm. Motion is planar and quasi-static. The actuator is a two-force
member with identical push/pull capacity. Friction, inertia, joint strength,
actuator buckling, and interference are not included. Required minimum and
maximum pin-to-pin lengths are reported but not checked against a product.

## Equations

For arm radius r and angle theta measured counterclockwise from positive x:

$$
\mathbf{B}=\begin{bmatrix}r\cos\theta\\r\sin\theta\end{bmatrix},
\qquad
\ell=\|\mathbf{A}-\mathbf{B}\|,
\qquad
\mathbf{u}=\frac{\mathbf{A}-\mathbf{B}}{\ell}.
$$

The signed moment arm and actuator force follow from moment equilibrium:

$$
h=B_xu_y-B_yu_x,
\qquad
F_a=-\frac{M}{h},
\qquad
F_{\mathrm{capacity,required}}=n|F_a|.
$$

$$
s_{\mathrm{required}}=\ell_{\mathrm{max}}-\ell_{\mathrm{min}}.
$$

Positive actuator force is tension pulling B toward A; negative is compression.
At zero moment arm, the mechanism cannot oppose a nonzero applied moment with
a finite actuator force. Collinear positions are inserted into the sampled
angle list and treated as singular, even if the applied moment is zero, because
force is then indeterminate. Force entries become `null` and the case fails.

The reported maximum required force is sampled, not a guaranteed continuous
maximum. Refine the angular spacing and check convergence before choosing a
capacity. Stroke extrema include endpoints and exact collinear positions.
Theory: moment equilibrium in the [mechanics references](../../docs/references.md).

## Run

From the repository root:

```bash
python3 advanced/tier-4/python/run_case.py
```

Edit the case JSON or pass `--case` and `--output`.

## Outputs

- `results/report.md`: stroke, length range, and sampled maximum required capacity.
- `results/result.json`: complete inputs and outputs.
- `results/positions.csv`: length, moment arm, signed force, and singularity status at each angle.

## CAD and manufacturing exercise

Create a planar assembly with a pivot, an arm, and a variable-length actuator.
Check the swept envelope and pin-to-pin lengths. Add actual clevises, pins, stops,
and mounting interfaces as a second stage. Identify interference and side load
before treating the geometry as a practical assembly.

## Experiments

1. Move the anchor and compare peak force with required stroke.
2. Put A on the positive x-axis and span angles across zero to expose dead center.
3. Double the resisting moment and explain the force change.
4. Increase `samples` and determine whether the sampled peak has converged.
