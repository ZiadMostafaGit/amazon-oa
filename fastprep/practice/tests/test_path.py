"""The DSA path: PATH.json is well formed, agrees with the KHATT map, and is served."""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import fixes  # noqa: E402
import fpdb  # noqa: E402
import path as path_mod  # noqa: E402
import solutions  # noqa: E402


class FakeProgress:
    def __init__(self, marks):
        self.marks = marks

    def all(self):
        return self.marks


@unittest.skipUnless(os.path.exists(path_mod.PATH_JSON), "no path/PATH.json")
class PathData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.load(open(path_mod.PATH_JSON))
        cls.bank = fpdb.Bank()

    def stages(self):
        return [s for ph in self.data["phases"] for s in ph["stages"]]

    def test_every_problem_exists_and_appears_once(self):
        seen = set()
        for s in self.stages():
            for pid in s["plan"] + s["more"]:
                self.assertIsNotNone(self.bank.detail(pid), pid)
                self.assertNotIn(pid, seen, pid)
                seen.add(pid)

    def test_plan_problems_are_scheduled_in_their_week(self):
        khatt = json.load(open(fixes.KHATT))
        for s in self.stages():
            for pid in s["plan"]:
                self.assertIn(pid, khatt, pid)
                self.assertEqual(khatt[pid]["week"], s["week"], pid)

    def test_weeks_increase_and_oa_core_comes_first(self):
        weeks = [s["week"] for s in self.stages()]
        self.assertEqual(weeks, sorted(weeks))
        self.assertEqual(self.data["phases"][0]["title"], "OA core")

    def test_listing_counts_progress_and_picks_next(self):
        first = self.stages()[0]["plan"]
        marks = {first[0]: {"status": "solved"}}
        out = path_mod.listing(self.bank, FakeProgress(marks), fixes, solutions)
        self.assertEqual(out["planSolved"], 1)
        self.assertEqual(out["next"]["id"], first[1])
        st = out["phases"][0]["stages"][0]
        self.assertEqual(st["solved"], 1)
        self.assertEqual(st["plan"][0]["status"], "solved")

    def test_position_has_neighbours(self):
        s = self.stages()[1]
        pos = path_mod.position(s["plan"][1], self.bank)
        self.assertEqual(pos["stage"], s["slug"])
        self.assertEqual(pos["prev"]["id"], s["plan"][0])
        self.assertEqual(pos["next"]["id"], s["plan"][2])
        self.assertTrue(pos["inPlan"])
        self.assertIsNone(path_mod.position("no-such-problem"))


if __name__ == "__main__":
    unittest.main()
