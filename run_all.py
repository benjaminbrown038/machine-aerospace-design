"""Run the five built-in cases from any working directory."""
from pathlib import Path
from designlab.runner import run_file


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    for tier in range(1, 6):
        folder = root / "advanced" / ("tier-" + str(tier))
        run_file(folder / "cases" / "baseline.json", folder / "results")
