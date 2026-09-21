# Tier 3 — Eccentrically loaded bolted mount

## Design problem

Distribute a force applied away from a four-bolt group's centroid. Find the
most heavily loaded bolt and screen nominal bolt shear and plate bearing.
The baseline applies [300, -1000] N at [0.12, 0] m in the plate plane.

## Model and assumptions

The plates are rigid and the bolts have identical shear stiffness. Bolts act in
single shear through their full unthreaded shank area. There is no friction,
preload, clearance/slip, out-of-plane load, prying, or bolt tension. The bearing
calculation uses one plate thickness. The supplied shear and bearing strengths
are illustrative independent input strengths, not tensile yield conversions.
See [shared assumptions](../../docs/units-and-assumptions.md).

## Equations

Let the bolt centroid be C. Coordinates x_i and y_i below are relative to C;
the input coordinates may use any common origin. The input load point is A.

$$
\mathbf{C}=\frac{1}{N}\sum_{i=1}^{N}\mathbf{p}_i,
\qquad
J_g=\sum_{i=1}^{N}(x_i^2+y_i^2).
$$

$$
M_z=M_0+(A_x-C_x)F_y-(A_y-C_y)F_x.
$$

An equal translation shares the direct load equally. A small rigid rotation
displaces each bolt in proportion to [-y_i, x_i]. Equal bolt stiffness therefore
gives tangential forces proportional to radius. Moment balance sets their
coefficient to M_z/J_g:

$$
F_{ix}=\frac{F_x}{N}-\frac{M_zy_i}{J_g},
\qquad
F_{iy}=\frac{F_y}{N}+\frac{M_zx_i}{J_g},
\qquad
R_i=\sqrt{F_{ix}^2+F_{iy}^2}.
$$

$$
\tau_i=\frac{R_i}{\pi d^2/4},
\qquad
\sigma_{\mathrm{bearing},i}=\frac{R_i}{td}.
$$

Each maximum demand is compared with its input strength divided by the design
factor. The tabulated bolt forces are transmitted **demands**, summing to the
applied load. The reactions acting on the loaded plate have opposite signs.
J_g has units m²; it is not a cross-section polar moment with units m⁴.

## Run

From the repository root:

```bash
python3 advanced/tier-3/python/run_case.py
```

Edit the case JSON or pass `--case` and `--output`.

## Outputs

- `results/report.md`: maximum bolt shear and bearing checks.
- `results/result.json`: centroid, moment, forces, and all inputs.
- `results/bolts.csv`: each bolt's force components and stress utilizations.

## CAD and manufacturing exercise

Model the hole pattern with a consistent coordinate origin. Add a mating part
and show the actual load introduction location. Plan holemaking and inspection.
Identify edge distances, thread locations, fit, washer access, and tool access;
these geometric details require checks not included in the current model.

## Experiments

1. Move the load to the centroid and set free moment to zero: loads become equal.
2. Increase eccentricity and locate the new critical bolt.
3. Spread the bolt pattern and compare moment-induced demand.
4. Sum the forces and moments from the output table to recover the applied load.
