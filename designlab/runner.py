"""Shared command-line runner and plain-text/JSON/CSV outputs."""
import argparse
import csv
import json
from pathlib import Path

from .models import MODELS


def run_file(case_path, output):
    case_path, output = Path(case_path), Path(output)
    with case_path.open(encoding="utf-8") as f:
        case = json.load(f)
    model = case["model"]
    if model not in MODELS:
        raise ValueError("Unknown model: {}".format(model))
    result = MODELS[model](case)
    output.mkdir(parents=True, exist_ok=True)
    envelope = {"case_name": case["name"], "inputs": case, "result": result}
    (output / "result.json").write_text(json.dumps(envelope, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    lines = ["# " + case["name"], "", "Educational analytical screening result.", "",
             "Status: **{}** for the implemented checks.".format("PASS" if result["passes"] else "FAIL"), ""]
    for key, value in result.items():
        if not isinstance(value, (dict, list)):
            lines.append("- `{}`: {}".format(key, value))
    if "checks" in result:
        lines += ["", "| Check | Demand | Allowable | Utilization | Pass |",
                  "|---|---:|---:|---:|---|"]
        for key, item in result["checks"].items():
            lines.append("| {} | {:.6g} | {:.6g} | {:.4f} | {} |".format(
                key, item["demand"], item["allowable"], item["utilization"], item["passes"]))
    if "best" in result:
        lines += ["", "## Lightest feasible candidate in the supplied grid", "",
                  "```json", json.dumps(result["best"], indent=2), "```"]
    for key in ("profile", "bolts", "positions", "candidates"):
        rows = result.get(key)
        if rows:
            with (output / (key + ".csv")).open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
    lines += ["", "Inputs and full results: `result.json`. Units follow the field suffixes.",
              "Read the tier README for omitted failure modes and model limits.", ""]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")
    status = "PASS" if result["passes"] else "FAIL"
    print("{}: {} -> {}".format(case["name"], status, output))
    return result


def main(default_case, default_output):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, default=default_case)
    parser.add_argument("--output", type=Path, default=default_output)
    args = parser.parse_args()
    try:
        run_file(args.case, args.output)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, "Case error: {}\n".format(exc))
