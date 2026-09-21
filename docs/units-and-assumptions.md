# Units and assumptions

## Units

| Quantity | Input/output unit | Conversion example |
|---|---|---|
| Length | m | 12 mm = 0.012 m |
| Force | N | 1 kN = 1000 N |
| Moment/torque | N m | 50 N m = 50 in a `_Nm` field |
| Stress/modulus | Pa | 69 GPa = 69000000000 Pa |
| Density | kg/m³ | 2700 kg/m³ = 2700 |
| Mass | kg | 0.15 kg = 150 g |
| Shaft twist | rad | 1 degree = 0.017453292519943295 rad |
| Mechanism input angle | degrees | 90 means a quarter turn |

Every numerical input field carries its unit in the name where applicable.
Loads may be signed. Dimensions, capacities, and material properties must be
positive and finite. Stress checks use magnitudes. The code does not infer units.

## Design factors and acceptance

For the stress checks, the entered strength is divided by a teaching design
factor. Baseline applied loads are unfactored. The deflection and twist limits
are checked directly at those loads.

$$
S_{\mathrm{allow}}=\frac{S}{n},
\qquad
U=\frac{S_{\mathrm{demand}}}{S_{\mathrm{allow}}},
\qquad
MS=\frac{S_{\mathrm{allow}}}{S_{\mathrm{demand}}}-1.
$$

A check passes when utilization is at most 1. Zero demand has utilization 0;
the undefined/infinite margin is written as JSON `null`. Tier 4 instead multiplies
the required actuator force by the design factor before comparing with capacity.
Do not additionally factor the same loads unless you intentionally redefine the
case. These factors do not implement an aerospace limit/ultimate load framework.

## Material data

The bundled aluminum-like and steel-like properties are **illustrative inputs**,
not certified allowables for named grades. No supplier material is implied.
For a specific material, record its specification, temper or condition, product
form, direction, temperature, source, and applicable statistical basis before
using its properties for a hardware decision. The shaft's illustrative E and G
correspond to a Poisson ratio of approximately 0.299.

## Model coverage

| Model | Included | Outside the implemented calculation |
|---|---|---|
| Cantilever | Uniform rectangular section, transverse tip force, linear bending | Root fillets, hole stresses, transverse shear, local connection compliance, fatigue |
| Shaft | Solid circular section, prescribed bending moment and constant torque | Bearing reactions/selection, shoulders, keyways, rotating fatigue, critical speed |
| Bolt group | Rigid plates, identical bolt shear stiffness, single shear, in-plane force/moment | Preload, friction, clearance/slip, bolt tension, prying, edge tear-out, net-section failure |
| Actuator | Rigid planar geometry, static constant resisting moment, equal push/pull capacity | Friction, inertia, buckling, pins, joints, actuator mounting length limits, interference |
| Sizing search | Tier 1 checks plus a mass limit over supplied candidates | Continuous/global optimization, full bracket detail, manufacturing cost, joints |

Beam cases also require L/h >= 10 and absolute tip displacement/L <= 0.05 as
explicit model-screening rules. These are teaching thresholds, not universal
proof that a beam idealization is appropriate. Cases outside them return FAIL.

Tier 4 reports force extrema from the evaluated positions; increase angular
resolution until the peak force converges. It inserts all exact collinear
positions in the requested range so a dead center cannot hide between samples.
A singular position returns `null` for force and makes the case fail.
