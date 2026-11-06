"""The roadmap: well formed, every rung solid, the KHATT plan drawn from it, and served."""
import importlib.util
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import fixes  # noqa: E402
import fpdb  # noqa: E402
import roadmap_view  # noqa: E402
import topics  # noqa: E402

_spec = importlib.util.spec_from_file_location("roadmap_tool", os.path.join(HERE, "tools", "roadmap.py"))
roadmap_tool = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(roadmap_tool)


class FakeProgress:
    def __init__(self, marks):
        self.marks = marks

    def all(self):
        return self.marks


@unittest.skipUnless(os.path.exists(roadmap_view.PATH_JSON), "no roadmap/ROADMAP.json")
class Roadmap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.load(open(roadmap_view.PATH_JSON))
        cls.bank = fpdb.Bank()
        try:
            cls.verified = {k for k, v in json.load(open(os.path.join(HERE, "solutions", "VERIFIED.json")))["problems"].items() if v.get("ok")}
        except (OSError, ValueError):
            cls.verified = set()

    def test_tree_is_ordered_prerequisites_first(self):
        order = {n["id"]: n["order"] for n in self.data["nodes"]}
        for n in self.data["nodes"]:
            for p in n["parents"]:
                self.assertLess(order[p], order[n["id"]], "%s needs %s" % (n["id"], p))
        self.assertEqual(roadmap_tool.order()[0], "arrays-hashing")

    def test_every_rung_exists_once_and_is_solid(self):
        seen = set()
        for n in self.data["nodes"]:
            self.assertTrue(n["ladder"], n["id"])
            for it in n["ladder"]:
                pid = it["id"]
                self.assertNotIn(pid, seen, pid)
                seen.add(pid)
                self.assertIsNotNone(self.bank.detail(pid), pid)
                self.assertIn(it["level"], ("core", "practice", "stretch"), pid)
                self.assertTrue(it.get("teaches"), pid)
                self.assertIn(pid, self.verified, "%s has no verified reference" % pid)
                self.assertEqual(fixes.problems(fixes.get(pid)), [], pid)

    def test_khatt_weeks_start_with_the_head_of_each_ladder(self):
        khatt = json.load(open(fixes.KHATT))
        for n in self.data["nodes"]:
            mine = [pid for pid, v in khatt.items() if v.get("node") == n["id"] and v["week"] in n["weeks"]]
            heads = [it["id"] for it in n["ladder"][:len(mine)]]
            self.assertEqual(sorted(mine), sorted(heads), n["id"])

    def test_listing_counts_progress_and_picks_next(self):
        first = self.data["nodes"][0]["ladder"]
        out = roadmap_view.listing(self.bank, FakeProgress({first[0]["id"]: {"status": "solved"}}), topics)
        self.assertEqual(out["solved"], 1)
        self.assertEqual(out["next"]["id"], first[1]["id"])
        self.assertTrue(out["nodes"][0]["unlocked"])

    def test_position_has_neighbours_and_the_technique(self):
        lad = self.data["nodes"][1]["ladder"]
        pos = roadmap_view.position(lad[1]["id"], self.bank)
        self.assertEqual(pos["prev"]["id"], lad[0]["id"])
        self.assertEqual(pos["next"]["id"], lad[2]["id"])
        self.assertEqual(pos["teaches"], lad[1]["teaches"])
        self.assertIsNone(roadmap_view.position("no-such-problem"))


if __name__ == "__main__":
    unittest.main()
