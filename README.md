# Machine & Aerospace Design

A practical learning repository for turning a mechanical requirement into a sized
component, a CAD concept, a manufacturing plan, and a verification record.

Start with machine components, then use the same design process for aircraft
equipment supports and mechanisms. The initial aerospace scope is **components
and mechanisms**, rather than whole-aircraft configuration or flight performance.

## Start here

Python 3.9 or newer. The five implemented cases use only the standard library;
no package installation or virtual environment is required.

From the extracted repository folder:

```bash
python3 run_all.py
python3 advanced/tier-1/python/run_case.py
python3 -m unittest discover -s tests -v
```

Read `advanced/tier-1/results/report.md` after the first run. Change a dimension
in its case JSON, rerun, and explain how the result changed.

## Five runnable tiers

| Tier | Design project | Calculations implemented | Design decision |
|---|---|---|---|
| [1](advanced/tier-1/README.md) | Cantilever equipment support | Bending stress, deflection, mass | How thick should the support be? |
| [2](advanced/tier-2/README.md) | Drive shaft | Bending plus torsion, von Mises stress, twist | What diameter meets strength and twist requirements? |
| [3](advanced/tier-3/README.md) | Bolted equipment mount | Eccentric bolt-group loading, nominal shear and bearing | Which bolt sees the highest load? |
| [4](advanced/tier-4/README.md) | Actuated access-door arm | Link length, stroke, moment arm, actuator force | Where should the actuator attach? |
| [5](advanced/tier-5/README.md) | Lightweight support | Discrete material and dimension search | Which candidate has the least mass while meeting the checks? |

All five tiers contain working code and baseline inputs. CAD modeling, drawings,
physical tests, and FEA comparisons are guided exercises; native CAD files and
FEA/CFD solvers are not included in this first version.

## Repository map

| Location | Contents |
|---|---|
| `advanced/tier-N/README.md` | Problem, assumptions, equations, run instructions, design exercise |
| `advanced/tier-N/cases/baseline.json` | Editable geometry, loads, properties, requirements |
| `advanced/tier-N/python/run_case.py` | Runnable tier entry point |
| `advanced/tier-N/results/` | Generated reports, inputs snapshot, and numerical tables |
| `designlab/models.py` | Shared analytical calculations |
| `designlab/runner.py` | Input loading and output generation |
| `docs/design-workflow.md` | Requirements through verification and revision |
| `docs/units-and-assumptions.md` | Units, factors, material provenance, model limits |
| `docs/roadmap.md` | Future machine and aerospace projects |
| `docs/references.md` | Mechanics reference links |
| `templates/design-review.md` | Reusable project record |
| `tests/` | Hand-calculation, scaling, equilibrium, and edge-case checks |

## Run a modified design

Copy a baseline before editing it. A separate output directory keeps the two
results available for comparison:

```bash
cp advanced/tier-1/cases/baseline.json advanced/tier-1/cases/my-support.json
python3 advanced/tier-1/python/run_case.py \
  --case advanced/tier-1/cases/my-support.json \
  --output advanced/tier-1/results/my-support
```

Named output files are replaced when the same output directory is reused.
CSV files can be opened in a spreadsheet or plotted with a tool of your choice.
`result.json` preserves the inputs alongside the results. A calculation that
executes successfully can still report `FAIL`: model execution and design
acceptance are different outcomes. Invalid inputs exit with an error.

## How this connects to FEA and CFD

Use this repository to define geometry, loads, requirements, and design choices.
Use an FEA project to investigate stress and displacement in more detailed
geometry. Use a CFD project when pressure, fluid drag, or thermal conditions
must supply the design loads. These links are a workflow for future projects;
there is no automated coupling in this version.

The baseline numbers are invented teaching cases and the material properties
are illustrative. A `PASS` applies only to the equations and checks implemented
in the selected tier; it is not an aircraft qualification or release decision.

## Put the project on GitHub

The downloadable archive contains source files, without Git history or a remote.
Create an empty repository named `machine-aerospace-design` in your account,
then run these commands from this folder. Replace `YOUR_USERNAME` first:

```bash
git init -b main
git add .
git commit -m "Add five machine and aerospace design learning cases"
git remote add origin https://github.com/YOUR_USERNAME/machine-aerospace-design.git
git push -u origin main
```

Choose an empty GitHub repository so there is no separate initial README to
merge. Use your usual GitHub authentication method. No open-source license is
selected in this starter; choose one before inviting reuse or contributions.
