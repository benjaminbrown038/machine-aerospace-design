# From a requirement to a design

## 1. Define the job

Write what the component supports or moves, its interfaces, available space,
loads, allowed displacement, environment, and mass target. Separate known facts
from assumptions. Start from the tier case JSON, then record the reasoning in
the [design review template](../templates/design-review.md).

## 2. Draw the load path

Create a free-body diagram. Show where forces enter, where the structure is
restrained, and how reactions reach the parent assembly. Keep coordinates and
signs consistent with the selected calculation.

## 3. Make a first estimate

Use the analytical code to size dimensions and identify the governing check.
Calculate one value by hand. Compare changes in force, span, section dimensions,
and material properties before choosing a candidate.

## 4. Build CAD and plan fabrication

Model the candidate in the CAD system you use. Add actual interfaces, fillets,
fastener clearances, tool access, and assembly space. Document which changes
invalidate the simple analytical assumptions. Prepare the needed drawings and
choose tolerances from function and process capability.

For machined supports, consider stock size, milling access, tool diameter,
workholding, setup count, inspection access, and deburring. For a shaft, consider
turning operations, bearing seats, shoulders, retention, and assembly order.

## 5. Verify the detailed design

Compare an appropriately restrained FEA model with the analytical case before
adding geometric complexity. Check force balance, displacement direction,
mesh convergence, and the effect of the load application area. Distinguish a
local peak at a modeling singularity from a meaningful stress measure.

For a mechanism, also check its swept envelope, end stops, interference,
manufacturing tolerances, and assembly access across the full motion range.

## 6. Record and revise

Keep a requirement-to-evidence table, dimensions, assumptions, CAD revision,
case inputs, result summary, and the reason for choosing the design. State
unverified items explicitly. Revise the record whenever a load, material,
interface, or geometry changes.
