"""Whole-bank sweep: every example in every problem must parse and round-trip.

This is the test that found the Java `long` suffix (9000606388L) and that keeps
the parser honest as the bank grows: `python3 fastprep.py sync` can add new
types and new value dialects at any time.
"""
import collections, json, os, sqlite3, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import parsing

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "fastprep.db")


def problems(fmt="algorithm"):
    c = sqlite3.connect("file:%s?mode=ro" % os.path.abspath(DB), uri=True)
    return c.execute("select id, detail_json from problems where practice_format=?", (fmt,))


class TestCorpus(unittest.TestCase):
    def test_every_example_parses(self):
        bad = []
        n_in = n_out = 0
        for pid, j in problems():
            for ex in json.loads(j).get("examples") or []:
                for item in ex.get("inputText") or []:
                    n_in += 1
                    try:
                        parsing.parse_value(item.get("inputValue"), item.get("inputType"))
                    except Exception as e:
                        bad.append((pid, "in", item.get("inputType"), item.get("inputValue"), str(e)))
                n_out += 1
                try:
                    parsing.parse_value(ex.get("outputText"), ex.get("outputType"))
                except Exception as e:
                    bad.append((pid, "out", ex.get("outputType"), ex.get("outputText"), str(e)))
        self.assertEqual(bad[:5], [], "%d of %d values failed to parse" % (len(bad), n_in + n_out))
        self.assertGreater(n_in, 13000)

    def test_expected_output_compares_equal_to_itself(self):
        """The comparator must accept the bank's own expected answer."""
        bad = []
        n = 0
        for pid, j in problems():
            for ex in json.loads(j).get("examples") or []:
                t, raw = ex.get("outputType"), ex.get("outputText")
                try:
                    value = parsing.parse_value(raw, t)
                except Exception:
                    continue
                n += 1
                ok, got_s, exp_s = parsing.compare_output(value, raw, t)
                if not ok:
                    bad.append((pid, t, raw, got_s, exp_s))
        self.assertEqual(bad[:5], [], "%d expected outputs did not equal themselves" % len(bad))
        self.assertGreater(n, 7000)

    def test_type_coverage(self):
        """Every declared type in the bank is one this module models."""
        types = collections.Counter()
        for pid, j in problems():
            for ex in json.loads(j).get("examples") or []:
                for item in ex.get("inputText") or []:
                    types[item.get("inputType")] += 1
                types[ex.get("outputType")] += 1
        unknown = []
        for t in types:
            b = parsing.base_type(t)
            if b not in (parsing.INT_TYPES | parsing.REAL_TYPES | parsing.BOOL_TYPES |
                         parsing.CHAR_TYPES | parsing.STR_TYPES | parsing.NODE_TYPES |
                         {"Integer", "Long", "Double", "Float", "Boolean", "Character"}):
                unknown.append((t, b, types[t]))
        self.assertEqual(unknown, [], "unmodelled types: %r" % (unknown,))


if __name__ == "__main__":
    unittest.main(verbosity=2)
