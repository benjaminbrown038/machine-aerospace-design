"""Run this tier's baseline, or supply --case and --output."""
from pathlib import Path
import sys

TIER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TIER.parents[1]))
from designlab.runner import main

if __name__ == "__main__":
    main(TIER / "cases" / "baseline.json", TIER / "results")
