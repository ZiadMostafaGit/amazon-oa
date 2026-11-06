"""The repair layer: a fixes/<id>.json is validated, and lands in the problem payload."""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fixes  # noqa: E402

GOOD = {
    "pattern": "knapsack",
    "why": "Each package is taken or not under a weight cap: 0/1 knapsack on weight.",
    "hints": ["What is limited?", "Take-or-skip per item.", "dp over capacity, O(n*W)."],
    "pitfalls": ["capacity 0"],
    "statement": "<p>clear</p>",
    "by": "claude", "at": "2026-11-06",
}


class FixValidation(unittest.TestCase):
    def test_good_repair_passes(self):
        self.assertEqual(fixes.problems(dict(GOOD), {"knapsack"}), [])

    def test_missing_file_is_reported(self):
        self.assertEqual(fixes.problems(None), ["no repair file"])

    def test_bad_fields_are_named(self):
        bad = dict(GOOD, hints=["only one"], pattern="not-a-chapter", statement="plain text", extra=1)
        errs = " | ".join(fixes.problems(bad, {"knapsack"}))
        for needle in ("hints", "not a study chapter", "statement must be HTML", "unknown fields"):
            self.assertIn(needle, errs)


class FixLoading(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old_dir, self.old_khatt = fixes.DIR, fixes.KHATT
        fixes.DIR = self.tmp.name
        fixes.KHATT = os.path.join(self.tmp.name, "khatt.json")

    def tearDown(self):
        fixes.DIR, fixes.KHATT = self.old_dir, self.old_khatt
        self.tmp.cleanup()

    def test_get_strips_unknown_fields_and_rejects_paths(self):
        with open(os.path.join(self.tmp.name, "p1.json"), "w") as f:
            json.dump(dict(GOOD, junk=True), f)
        got = fixes.get("p1")
        self.assertEqual(got["pattern"], "knapsack")
        self.assertNotIn("junk", got)
        self.assertIsNone(fixes.get("../p1"))
        self.assertIsNone(fixes.get("missing"))

    def test_khatt_slot(self):
        with open(fixes.KHATT, "w") as f:
            json.dump({"p1": {"week": 20, "day": "Sun", "label": "2-D DP"}}, f)
        self.assertEqual(fixes.khatt_for("p1")["week"], 20)
        self.assertIsNone(fixes.khatt_for("p2"))
        self.assertEqual(fixes.khatt_ids(), ["p1"])


if __name__ == "__main__":
    unittest.main()
