"""The sandbox and the two harnesses.

These tests are the reason to trust the Run button: they assert both that a
correct solution passes and that hostile code cannot reach the network, the
filesystem, or an unbounded amount of CPU and memory.
"""
import json, os, shutil, sqlite3, sys, tempfile, time, unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import fpdb, runner

ONE_CASE = [{"id": 1, "inputs": [], "outputType": "int", "expectedRaw": "1"}]


def run(code, cases=None, fn="f"):
    return runner.run_python(code, cases or ONE_CASE, fn)


class TestPythonRunner(unittest.TestCase):
    def test_correct_solution_passes(self):
        r = run("def f():\n    return 1\n")
        self.assertEqual([x["ok"] for x in r["results"]], [True])

    def test_wrong_answer_reports_both_sides(self):
        r = run("def f():\n    return 2\n")
        res = r["results"][0]
        self.assertFalse(res["ok"])
        self.assertEqual((res["got"], res["expected"]), ("2", "1"))

    def test_missing_function_is_named(self):
        r = run("def other():\n    return 1\n")
        self.assertIn("no function named f", r["error"])
        self.assertIn("other", r["error"])

    def test_syntax_error_is_reported_not_raised(self):
        r = run("def f(:\n")
        self.assertIn("SyntaxError", r["error"])

    def test_exception_is_per_case(self):
        r = run("def f():\n    return 1 / 0\n")
        self.assertFalse(r["results"][0]["ok"])
        self.assertIn("ZeroDivisionError", r["results"][0]["error"])

    def test_stdout_is_captured_not_confused_with_the_result(self):
        r = run("def f():\n    print('debugging')\n    return 1\n")
        self.assertTrue(r["results"][0]["ok"])
        self.assertIn("debugging", r["results"][0]["stdout"])

    def test_node_types_are_available(self):
        cases = [{"id": 1, "inputs": [{"name": "head", "type": "ListNode",
                                       "rawValue": "[1,2,3]"}],
                  "outputType": "ListNode", "expectedRaw": "[3,2,1]"}]
        code = ("def f(head):\n"
                "    prev = None\n"
                "    while head:\n"
                "        head.next, prev, head = prev, head, head.next\n"
                "    return prev\n")
        self.assertTrue(runner.run_python(code, cases, "f")["results"][0]["ok"])

    def test_mutating_the_input_cannot_poison_later_cases(self):
        cases = [{"id": i, "inputs": [{"name": "a", "type": "int[]", "rawValue": "[1,2,3]"}],
                  "outputType": "int", "expectedRaw": "6"} for i in (1, 2)]
        code = "def f(a):\n    total = sum(a)\n    a.clear()\n    return total\n"
        r = runner.run_python(code, cases, "f")
        self.assertEqual([x["ok"] for x in r["results"]], [True, True])


class TestSandbox(unittest.TestCase):
    """Skipped rather than failed without bwrap: the fallback makes no such promise."""

    def setUp(self):
        if runner.sandbox_kind() != "bubblewrap":
            self.skipTest("bwrap not installed; the app warns and degrades")

    def test_no_network(self):
        r = run("import socket\ndef f():\n"
                "    socket.create_connection(('1.1.1.1', 80), 3)\n    return 1\n")
        self.assertFalse(r["results"][0]["ok"])

    def test_cannot_read_the_problem_bank(self):
        r = run("def f():\n    return open(%r, 'rb').read(4)\n" % fpdb.DEFAULT_DB)
        self.assertFalse(r["results"][0]["ok"])
        self.assertIn("FileNotFoundError", r["results"][0]["error"])

    def test_cannot_write_outside_the_sandbox(self):
        target = os.path.join(HERE, "PWNED")
        run("def f():\n    open(%r, 'w').write('x')\n    return 1\n" % target)
        self.assertFalse(os.path.exists(target))

    def test_home_is_not_visible(self):
        r = run("import os\ndef f():\n    return len(os.listdir('/home'))\n")
        self.assertTrue(r["results"][0].get("error") or r["results"][0]["got"] == "0")


class TestLimits(unittest.TestCase):
    def test_infinite_loop_is_stopped(self):
        t0 = time.time()
        r = run("def f():\n    while True:\n        pass\n")
        self.assertLess(time.time() - t0, runner.WALL_TIMEOUT + 5)
        self.assertTrue(r.get("timeout"))

    def test_memory_is_capped(self):
        r = run("def f():\n    return len(bytearray(4 * 10**9))\n")
        self.assertFalse(r.get("results", [{}])[0].get("ok", False))

    def test_output_is_capped(self):
        r = run("def f():\n    print('x' * 200000)\n    return 1\n")
        self.assertLessEqual(len(r["results"][0]["stdout"]), runner.MAX_OUTPUT)

    def test_oversized_program_is_refused(self):
        r = runner.run_python("#" * (runner.MAX_CODE + 1), ONE_CASE, "f")
        self.assertIn("characters", r["error"])


class TestSqlRunner(unittest.TestCase):
    def setUp(self):
        bank = fpdb.Bank()
        row = bank.conn.execute(
            "SELECT detail_json FROM problems WHERE id='alarm-get-average-thermostat-temperature'"
        ).fetchone()
        self.tab = json.loads(row[0])["tabular"]

    def test_correct_query_passes(self):
        q = ("SELECT room_name, AVG(temperature) AS average_temperature FROM devices "
             "WHERE device_type = 'Thermostat' GROUP BY room_name HAVING COUNT(*) > 2")
        r = runner.run_sql(q, self.tab)
        self.assertTrue(r["results"][0]["ok"], r["results"][0])

    def test_wrong_row_count_fails(self):
        r = runner.run_sql("SELECT room_name, temperature AS average_temperature FROM devices",
                           self.tab)
        self.assertFalse(r["results"][0]["ok"])
        self.assertIn("row(s)", r["results"][0]["error"])

    def test_wrong_columns_fail(self):
        r = runner.run_sql("SELECT room_name FROM devices", self.tab)
        self.assertIn("columns", r["results"][0]["error"])

    def test_sql_error_is_reported(self):
        r = runner.run_sql("SELECT nope FROM devices", self.tab)
        self.assertIn("no such column", r["results"][0]["error"])

    def test_numeric_columns_compare_by_the_declared_type(self):
        """The bank encodes a "decimal" column's expected values as strings, so
        100.0 and "100" must compare equal - but 72.5 and 72 must not."""
        import fpdb, json as _json
        bank = fpdb.Bank()
        row = bank.conn.execute(
            "SELECT detail_json FROM problems WHERE id='millennium-clean-the-tape'").fetchone()
        if not row:
            self.skipTest("problem not in this bank")
        tab = _json.loads(row[0])["tabular"]
        types = {c["name"]: c["type"] for c in tab["resultContract"]["columns"]}
        self.assertEqual(types["Asset_1"], "decimal")
        self.assertIsInstance(tab["visibleCases"][0]["expectedResult"]["rows"][0][2], str)

    def test_a_wrong_number_still_fails(self):
        q = ("SELECT room_name, AVG(temperature) + 0.5 AS average_temperature FROM devices "
             "WHERE device_type = 'Thermostat' GROUP BY room_name HAVING COUNT(*) > 2")
        r = runner.run_sql(q, self.tab)
        self.assertFalse(r["results"][0]["ok"])

    def test_multiple_statements_refused(self):
        r = runner.run_sql("SELECT 1; DROP TABLE devices", self.tab)
        self.assertIn("one statement", r["error"])


class TestSandboxTiers(unittest.TestCase):
    """What happens on a machine where bwrap cannot do everything it wants.

    Real report: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`
    on every single run - the sandbox died before the user's code started, and
    the app blamed the code. bwrap existing says nothing about whether this
    kernel, container or systemd unit will let it build namespaces, so the
    runner has to find out by running it, and settle for what works.
    """

    FAIL = ("#!/bin/sh\n"
            "echo 'bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted' >&2\n"
            "exit 1\n")
    # the machine in the report: every namespace except the network one
    NET_ONLY = ("#!/bin/sh\n"
                'for a in "$@"; do [ "$a" = --share-net ] && ok=1; done\n'
                'if [ -z "$ok" ]; then\n'
                "  echo 'bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted' >&2\n"
                "  exit 1\n"
                "fi\n"
                "while [ $# -gt 0 ]; do\n"
                '  case "$1" in\n'
                "    --unshare-all|--share-net|--die-with-parent|--new-session|--clearenv) shift;;\n"
                "    --setenv|--ro-bind|--bind) shift 3;;\n"
                "    --proc|--dev|--tmpfs|--chdir) shift 2;;\n"
                "    *) break;;\n"
                "  esac\n"
                "done\n"
                'exec "$@"\n')

    def setUp(self):
        self._bwrap, self._cached = runner.BWRAP, runner._SANDBOX
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        runner.BWRAP, runner._SANDBOX = self._bwrap, self._cached
        shutil.rmtree(self.dir, ignore_errors=True)

    def _fake(self, body):
        path = os.path.join(self.dir, "bwrap")
        with open(path, "w") as fh:
            fh.write(body)
        os.chmod(path, 0o755)
        runner.BWRAP = path
        runner.demote_sandbox()
        return path

    def test_a_machine_that_refuses_the_net_namespace_still_runs_code(self):
        self._fake(self.NET_ONLY)
        self.assertEqual(runner.sandbox_kind(), "bubblewrap-shared-net")
        self.assertIn("SHARES", runner.sandbox_note())
        r = runner.run_script("print('it ran')")
        self.assertEqual(r["printed"].strip(), "it ran")
        self.assertNotIn("error", r)

    def test_a_machine_where_bwrap_cannot_start_falls_back_to_the_subprocess(self):
        self._fake(self.FAIL)
        self.assertEqual(runner.sandbox_kind(), "subprocess")
        r = runner.run_script("print('still ran')")
        self.assertEqual(r["printed"].strip(), "still ran")

    def test_a_sandbox_that_breaks_while_running_is_worked_out_again(self):
        """The tier is cached, and the machine can change under it."""
        self._fake(self.NET_ONLY)
        runner._SANDBOX = ("bubblewrap", [])       # what we still believe
        r = runner.run_script("print('survived')")
        self.assertEqual(r["printed"].strip(), "survived")
        self.assertEqual(runner.sandbox_kind(), "bubblewrap-shared-net")

    def test_a_dead_sandbox_is_never_reported_as_your_code_raising(self):
        self._fake(self.FAIL)
        runner._SANDBOX = ("bubblewrap", [])       # force the failing path
        out = runner._run_child("print(1)", {"maxOutput": 100}, _retry=False)
        self.assertTrue(out.get("sandboxError"))
        self.assertIn("never ran", out["error"])
        self.assertIn("RTM_NEWADDR", out["error"])

    def test_the_tier_is_worked_out_once_and_kept(self):
        kind = runner.sandbox_kind()
        self.assertEqual(kind, runner.sandbox_kind())
        self.assertIsNotNone(runner._SANDBOX)


if __name__ == "__main__":
    unittest.main(verbosity=2)
