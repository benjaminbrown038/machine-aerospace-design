"""Check independent balances, hand results, physical scaling, and boundary cases."""
import json
import math
from pathlib import Path
import tempfile
import unittest

from designlab.models import cantilever, shaft, bolt_group, actuator, optimize_bracket
from designlab.runner import run_file

ROOT = Path(__file__).resolve().parents[1]


def case(tier):
    return json.loads((ROOT / "advanced" / ("tier-" + str(tier)) / "cases" / "baseline.json").read_text())


class MechanicsChecks(unittest.TestCase):
    def test_beam_hand_result_and_clamp_conditions(self):
        r = cantilever(case(1))
        self.assertAlmostEqual(r["root_bending_stress_Pa"] / 1e6, 41.6666666667, places=7)
        self.assertAlmostEqual(r["tip_deflection_m"] * 1000, 0.754830917874, places=9)
        self.assertAlmostEqual(r["mass_kg"], .1458)
        self.assertEqual(r["profile"][0]["deflection_m"], 0)
        self.assertAlmostEqual(r["profile"][-1]["deflection_m"], r["tip_deflection_m"])

    def test_beam_physical_scaling(self):
        c = case(1)
        a = cantilever(c)
        c["height_m"] *= 2
        b = cantilever(c)
        self.assertAlmostEqual(b["root_bending_stress_Pa"] / a["root_bending_stress_Pa"], .25)
        self.assertAlmostEqual(b["tip_deflection_m"] / a["tip_deflection_m"], .125)
        self.assertAlmostEqual(b["mass_kg"] / a["mass_kg"], 2)
        self.assertFalse(b["model_screen_passes"])

    def test_beam_zero_and_reversed_load(self):
        c = case(1)
        a = cantilever(c)
        c["tip_force_N"] *= -1
        b = cantilever(c)
        self.assertEqual(a["root_bending_stress_Pa"], b["root_bending_stress_Pa"])
        self.assertEqual(a["tip_deflection_m"], -b["tip_deflection_m"])
        c["tip_force_N"] = 0
        r = cantilever(c)
        self.assertTrue(r["passes"])
        self.assertIsNone(r["checks"]["bending_Pa"]["margin"])

    def test_shaft_pure_modes_and_diameter_scaling(self):
        c = case(2)
        c["torque_Nm"] = 0
        r = shaft(c)
        self.assertEqual(r["von_mises_Pa"], r["bending_stress_Pa"])
        self.assertEqual(r["twist_rad"], 0)
        c = case(2)
        c["bending_moment_Nm"] = 0
        r = shaft(c)
        self.assertAlmostEqual(r["von_mises_Pa"] / r["torsional_shear_Pa"], math.sqrt(3))
        c["diameter_m"] *= 2
        b = shaft(c)
        self.assertAlmostEqual(b["von_mises_Pa"] / r["von_mises_Pa"], 1 / 8)
        self.assertAlmostEqual(b["twist_rad"] / r["twist_rad"], 1 / 16)

    def test_bolt_force_and_moment_equilibrium(self):
        c = case(3)
        r = bolt_group(c)
        rows = r["bolts"]
        self.assertAlmostEqual(sum(x["force_x_N"] for x in rows), 300)
        self.assertAlmostEqual(sum(x["force_y_N"] for x in rows), -1000)
        cx, cy = r["centroid_xy_m"]
        moment = sum((x["x_m"]-cx)*x["force_y_N"] - (x["y_m"]-cy)*x["force_x_N"] for x in rows)
        self.assertAlmostEqual(moment, -120)

    def test_bolt_coordinate_origin_invariance(self):
        c = case(3)
        a = bolt_group(c)
        c["bolt_xy_m"] = [[x+4, y-3] for x, y in c["bolt_xy_m"]]
        x, y = c["load_point_xy_m"]
        c["load_point_xy_m"] = [x+4, y-3]
        b = bolt_group(c)
        for ra, rb in zip(a["bolts"], b["bolts"]):
            self.assertAlmostEqual(ra["force_N"], rb["force_N"])

    def test_centered_bolt_load_equal_sharing(self):
        c = case(3)
        c["load_point_xy_m"] = [0, 0]
        for row in bolt_group(c)["bolts"]:
            self.assertAlmostEqual(row["force_x_N"], 75)
            self.assertAlmostEqual(row["force_y_N"], -250)

    def test_actuator_moment_balance(self):
        c = case(4)
        r = actuator(c)
        ax, ay = c["anchor_xy_m"]
        for row in r["positions"]:
            theta = math.radians(row["angle_deg"])
            bx = c["arm_radius_m"] * math.cos(theta)
            by = c["arm_radius_m"] * math.sin(theta)
            force = row["signed_actuator_force_N"]
            fx = force * (ax-bx) / row["length_m"]
            fy = force * (ay-by) / row["length_m"]
            self.assertAlmostEqual(bx*fy-by*fx + c["resisting_moment_Nm"], 0)

    def test_dead_center_between_samples_detected(self):
        c = case(4)
        c.update(anchor_xy_m=[.1, 0], start_angle_deg=-5, stop_angle_deg=5, samples=2)
        r = actuator(c)
        self.assertTrue(r["singular"])
        self.assertFalse(r["passes"])
        self.assertIsNone(r["required_capacity_N"])
        self.assertEqual(len(r["positions"]), 3)
        self.assertAlmostEqual(r["min_length_m"], .04)

    def test_search_selection_and_infeasibility(self):
        c = case(5)
        r = optimize_bracket(c)
        feasible = [x for x in r["candidates"] if x["passes"]]
        self.assertEqual(r["candidate_count"], 60)
        self.assertEqual(r["best"]["mass_kg"], min(x["mass_kg"] for x in feasible))
        self.assertTrue(all(r["best"][k] <= 1 for k in ("strength_utilization", "deflection_utilization", "mass_utilization")))
        c["max_mass_kg"] = 1e-6
        r = optimize_bracket(c)
        self.assertIsNone(r["best"])
        self.assertFalse(r["passes"])

    def test_invalid_physical_inputs(self):
        for value in (0, -1, float("nan"), float("inf"), True, "0.1"):
            c = case(1)
            c["height_m"] = value
            with self.assertRaises(ValueError):
                cantilever(c)
        c = case(3)
        c["bolt_xy_m"] = [[0, 0], [0, 0]]
        with self.assertRaises(ValueError):
            bolt_group(c)

    def test_output_preserves_inputs_and_serializable_singularity(self):
        c = case(4)
        c.update(anchor_xy_m=[.1, 0], start_angle_deg=-5, stop_angle_deg=5, samples=2)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            source = p / "singular.json"
            source.write_text(json.dumps(c))
            run_file(source, p / "output")
            text = (p / "output" / "result.json").read_text()
            self.assertNotIn("Infinity", text)
            self.assertNotIn("NaN", text)
            self.assertEqual(json.loads(text)["inputs"], c)
            self.assertTrue((p / "output" / "positions.csv").exists())


if __name__ == "__main__":
    unittest.main()
