# Tier 5 — Lightweight equipment-support sizing

## Design problem

Find the lightest rectangular support in a supplied grid of materials, widths,
and heights. The 150 mm span carries a 250 N tip load. The design must meet the
Tier 1 bending and deflection checks and a 0.3 kg mass budget.

## Model and assumptions

Each candidate uses the Tier 1 cantilever model. The baseline grid contains two
illustrative materials, five widths, and six heights: 60 candidates. The result
is the best feasible candidate **within that grid**. It is not a continuous
optimum or a detailed aircraft bracket design. There is no FEA solver here.

## Equations

The variables are material choice, width b, and height h, with fixed span L:

$$
\min_{\mathrm{material},b,h}\ m=\rho Lbh.
$$

Subject to:

$$
\frac{6|F|L}{bh^2}\leq\frac{S_y}{n},
\qquad
\frac{4|F|L^3}{Ebh^3}\leq v_{\mathrm{allow}},
\qquad
m\leq m_{\mathrm{allow}}.
$$

The [Tier 1](../tier-1/README.md) model-screening rules also apply. Every
candidate is evaluated; infeasible candidates remain in the output so the
tradeoffs are visible. If none pass, `best` is JSON `null` and status is FAIL.

## Run

From the repository root:

```bash
python3 advanced/tier-5/python/run_case.py
```

Edit the case JSON or pass `--case` and `--output`.

## Outputs

- `results/report.md`: candidate counts and the lightest feasible choice.
- `results/result.json`: complete design grid, requirements, and evaluations.
- `results/candidates.csv`: every candidate, sorted by mass, with constraint utilizations.

## CAD and manufacturing exercise

Model the selected candidate and one heavier feasible alternative. Compare
available stock, workholding, interface space, stiffness, and machining access.
Develop the actual attachment and recalculate its mass. Document why the final
engineering choice might differ from the lightest idealized beam.

## Experiments

1. Tighten the displacement limit. Observe which dimension or material changes.
2. Add intermediate heights to refine the discrete search.
3. Tighten the mass budget until no feasible candidate remains.
4. Add root geometry and holes in CAD, then use FEA to evaluate the assumptions
   that the simple beam model leaves out.
