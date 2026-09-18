"""End-to-end tests against a real server process.

Starts serve.py on a spare port with a throwaway progress database, so these
tests exercise the same entry point a user runs, and never touch the progress
file in the working tree. The problem bank is opened read-only.
"""
import json, os, socket, subprocess, sys, tempfile, time, unittest
import urllib.error, urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class ServerCase(unittest.TestCase):
    proc = None
    base = None
    tmp = None

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="fp-test-")
        port = free_port()
        cls.base = "http://127.0.0.1:%d" % port
        cls.proc = subprocess.Popen(
            [sys.executable, os.path.join(HERE, "serve.py"), "--port", str(port),
             "--progress-db", os.path.join(cls.tmp, "progress.db"), "--offline"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=HERE)
        for _ in range(100):
            try:
                urllib.request.urlopen(cls.base + "/api/health", timeout=1).read()
                return
            except Exception:
                time.sleep(0.1)
        raise RuntimeError("server did not start")

    @classmethod
    def tearDownClass(cls):
        if cls.proc:
            cls.proc.terminate()
            cls.proc.wait(timeout=10)

    # helpers
    def get(self, path):
        return json.load(urllib.request.urlopen(self.base + path, timeout=30))

    def post(self, path, obj):
        req = urllib.request.Request(self.base + path, json.dumps(obj).encode(),
                                     {"Content-Type": "application/json"})
        try:
            return json.load(urllib.request.urlopen(req, timeout=60)), 200
        except urllib.error.HTTPError as e:
            return json.load(e), e.code


class TestBrowsing(ServerCase):
    def test_health(self):
        h = self.get("/api/health")
        self.assertEqual(h["problems"], 3533)
        self.assertTrue(h["bank"].endswith("fastprep.db"))

    def test_oa_filter_uses_the_array_column(self):
        """1976, not 1959: the singular problemType is null for multi-stage rows."""
        self.assertEqual(self.get("/api/problems?stage=OA&limit=1")["total"], 1976)

    def test_recent_sort_puts_the_newest_sighting_first(self):
        first = self.get("/api/problems?sort=recent&limit=1")["items"][0]
        self.assertEqual(first["lastSeenMax"], "2026-09-18")

    def test_frequent_sort_is_monotonic(self):
        items = self.get("/api/problems?sort=frequent&limit=25")["items"]
        counts = [i["seenCount"] or 0 for i in items]
        self.assertEqual(counts, sorted(counts, reverse=True))
        self.assertEqual(counts[0], 13)

    def test_facets_have_counts(self):
        f = self.get("/api/facets")
        stages = {x["value"]: x["count"] for x in f["stage"]}
        self.assertEqual(stages["OA"], 1976)
        self.assertEqual(f["meta"]["total"], 3533)
        self.assertEqual(f["meta"]["withImages"], 1619)
        self.assertEqual({x["value"] for x in f["format"]}, {"algorithm", "tabular"})

    def test_filters_combine(self):
        a = self.get("/api/problems?stage=OA&difficulty=hard&limit=1")["total"]
        b = self.get("/api/problems?stage=OA&limit=1")["total"]
        c = self.get("/api/problems?difficulty=hard&limit=1")["total"]
        self.assertLess(a, min(b, c))

    def test_multiple_values_in_one_facet_are_or(self):
        easy = self.get("/api/problems?difficulty=easy&limit=1")["total"]
        hard = self.get("/api/problems?difficulty=hard&limit=1")["total"]
        both = self.get("/api/problems?difficulty=easy&difficulty=hard&limit=1")["total"]
        self.assertEqual(both, easy + hard)

    def test_date_window(self):
        res = self.get("/api/problems?seenFrom=2026-09-01&seenTo=2026-09-18&limit=200")
        self.assertTrue(res["total"] > 0)
        for item in res["items"]:
            self.assertTrue("2026-09-01" <= item["lastSeenMax"] <= "2026-09-18")

    def test_any_sighting_window_differs_from_newest_only(self):
        newest = self.get("/api/problems?seenFrom=2024-01-01&seenTo=2024-12-31&limit=1")["total"]
        anyseen = self.get("/api/problems?seenOnFrom=2024-01-01&seenOnTo=2024-12-31&limit=1")["total"]
        self.assertGreater(anyseen, newest)

    def test_search_finds_a_known_problem(self):
        res = self.get("/api/problems?q=deployment+window&sort=relevance&limit=5")
        self.assertIn("stripe-deployment-window-scheduler", [i["id"] for i in res["items"]])

    def test_paging(self):
        a = self.get("/api/problems?sort=title&limit=10&offset=0")["items"]
        b = self.get("/api/problems?sort=title&limit=10&offset=10")["items"]
        self.assertEqual(len(a), 10)
        self.assertFalse({i["id"] for i in a} & {i["id"] for i in b})

    def test_every_field_sorts_both_ways(self):
        fields = [f["key"] for f in self.get("/api/facets")["sorts"]]
        self.assertEqual(set(fields),
                         {"recent", "frequent", "difficulty", "title", "company", "default"})
        for key in fields:
            asc = self.get("/api/problems?sort=%s&dir=asc&limit=3" % key)
            desc = self.get("/api/problems?sort=%s&dir=desc&limit=3" % key)
            self.assertEqual(asc["direction"], "asc")
            self.assertEqual(desc["direction"], "desc")
            self.assertNotEqual([i["id"] for i in asc["items"]],
                                [i["id"] for i in desc["items"]], key)

    def test_title_sort_reverses(self):
        asc = self.get("/api/problems?sort=title&dir=asc&limit=1")["items"][0]["title"]
        desc = self.get("/api/problems?sort=title&dir=desc&limit=1")["items"][0]["title"]
        self.assertLess(asc.lower(), desc.lower())

    def test_unknown_values_sort_last_in_both_directions(self):
        for direction in ("asc", "desc"):
            top = self.get("/api/problems?sort=difficulty&dir=%s&limit=5" % direction)["items"]
            self.assertTrue(all(i["difficulty"] for i in top), direction)
        oldest = self.get("/api/problems?sort=recent&dir=asc&limit=1")["items"][0]
        self.assertEqual(oldest["lastSeenMax"], "2014-08-16")

    def test_legacy_sort_names_still_work(self):
        self.assertEqual(self.get("/api/problems?sort=hardest&limit=1")["direction"], "desc")
        self.assertEqual(self.get("/api/problems?sort=oldest&limit=1")["sort"], "recent")
        self.assertEqual(self.get("/api/problems?sort=rare&limit=1")["direction"], "asc")

    def test_unset_values_are_filterable(self):
        """76 problems have no difficulty, 1557 no platform - they must be findable."""
        self.assertEqual(self.get("/api/problems?difficulty=__unset__&limit=1")["total"], 76)
        self.assertEqual(self.get("/api/problems?platform=__unset__&limit=1")["total"], 1557)
        self.assertEqual(self.get("/api/problems?employment=__unset__&limit=1")["total"], 523)
        self.assertEqual(self.get("/api/problems?topic=__unset__&limit=1")["total"], 76)

    def test_unset_combines_with_named_values(self):
        hard = self.get("/api/problems?difficulty=hard&limit=1")["total"]
        both = self.get("/api/problems?difficulty=hard&difficulty=__unset__&limit=1")["total"]
        self.assertEqual(both, hard + 76)

    def test_facets_offer_the_unset_bucket(self):
        f = self.get("/api/facets")
        unset = [x for x in f["difficulty"] if x.get("unset")]
        self.assertEqual([x["count"] for x in unset], [76])

    def test_seen_count_range(self):
        lo = self.get("/api/problems?minSeen=5&limit=1")["total"]
        hi = self.get("/api/problems?maxSeen=1&limit=1")["total"]
        both = self.get("/api/problems?minSeen=3&maxSeen=5&limit=1")["total"]
        self.assertGreater(lo, 0)
        self.assertGreater(hi, 0)
        self.assertLess(both, lo + hi)
        for item in self.get("/api/problems?minSeen=3&maxSeen=5&limit=100")["items"]:
            self.assertTrue(3 <= (item["seenCount"] or 0) <= 5)

    def test_not_started_count_is_the_whole_bank_when_nothing_is_touched(self):
        f = self.get("/api/facets")
        self.assertEqual(f["progress"]["none"], f["meta"]["total"] -
                         sum(1 for _ in []))      # nothing touched in this fixture yet

    def test_index_html_is_bootstrapped(self):
        html = urllib.request.urlopen(self.base + "/?stage=OA", timeout=30).read().decode()
        self.assertIn("window.__BOOT__", html)
        self.assertIn('"total": 1976', html.replace('"total":1976', '"total": 1976'))


class TestDetail(ServerCase):
    def test_algorithm_problem(self):
        d = self.get("/api/problems/stripe-deployment-window-scheduler")
        self.assertEqual(d["practiceFormat"], "algorithm")
        self.assertEqual(len(d["cases"]), 2)
        self.assertEqual(d["functionName"], "scheduleDeploymentWindows")
        self.assertIn("<p>", d["problemStatement"])           # HTML, rendered by the page
        self.assertEqual(len(d["images"]), 2)
        self.assertEqual([l["id"] for l in d["languages"]], ["python", "java"])

    def test_tabular_problem(self):
        d = self.get("/api/problems/alarm-get-average-thermostat-temperature")
        self.assertEqual(d["practiceFormat"], "tabular")
        self.assertEqual(d.get("examples") or [], [])
        self.assertEqual([t["name"] for t in d["tabular"]["inputSchema"]], ["devices"])
        self.assertTrue(d["tabular"]["visibleCases"])
        ids = [l["id"] for l in d["languages"]]
        self.assertIn("sqlite", ids)
        self.assertIn("mysql", ids)

    def test_unknown_problem_is_404(self):
        with self.assertRaises(urllib.error.HTTPError) as cm:
            self.get("/api/problems/not-a-real-problem")
        self.assertEqual(cm.exception.code, 404)

    def test_every_lastseen_date_is_exposed(self):
        d = self.get("/api/problems/stripe-deployment-window-scheduler")
        self.assertGreaterEqual(len(d["lastSeen"]), 6)


class TestRunning(ServerCase):
    CORRECT = open(os.path.join(HERE, "tests", "fixtures", "stripe_solution.py")).read() \
        if os.path.exists(os.path.join(HERE, "tests", "fixtures", "stripe_solution.py")) else None

    def test_correct_solution_passes_every_visible_case(self):
        self.assertIsNotNone(self.CORRECT, "fixture missing")
        out, code = self.post("/api/run", {
            "problemId": "stripe-deployment-window-scheduler",
            "language": "python", "code": self.CORRECT})
        self.assertEqual(code, 200)
        self.assertEqual((out["passed"], out["total"]), (2, 2), out)
        self.assertIn("VISIBLE examples only", out["disclaimer"])

    def test_wrong_solution_fails_with_both_values(self):
        out, _ = self.post("/api/run", {
            "problemId": "stripe-deployment-window-scheduler", "language": "python",
            "code": "def scheduleDeploymentWindows(part, inputCsv):\n    return []\n"})
        self.assertEqual(out["passed"], 0)
        self.assertEqual(out["results"][0]["got"], "[]")
        self.assertNotEqual(out["results"][0]["expected"], "[]")

    def test_sql_runs_against_the_visible_cases(self):
        out, _ = self.post("/api/run", {
            "problemId": "alarm-get-average-thermostat-temperature", "language": "sqlite",
            "code": "SELECT room_name, AVG(temperature) AS average_temperature FROM devices "
                    "WHERE device_type='Thermostat' GROUP BY room_name HAVING COUNT(*) > 2"})
        self.assertEqual((out["passed"], out["total"]), (1, 1), out)

    def test_language_that_cannot_run_is_refused_not_faked(self):
        import languages
        if languages._HAS_JAVA:
            self.skipTest("a JDK is installed, so Java is genuinely runnable")
        out, code = self.post("/api/run", {
            "problemId": "stripe-deployment-window-scheduler", "language": "java",
            "code": "class X {}"})
        self.assertEqual(code, 400)
        self.assertIn("cannot be executed", out["error"])

    def test_unknown_language_is_refused(self):
        out, code = self.post("/api/run", {
            "problemId": "stripe-deployment-window-scheduler", "language": "cobol",
            "code": "x"})
        self.assertEqual(code, 400)


class TestProgress(ServerCase):
    PID = "amazon-word-ladder"

    def test_status_notes_and_bookmark_round_trip(self):
        out, _ = self.post("/api/progress/" + self.PID,
                           {"status": "solved", "bookmarked": True, "notes": "BFS"})
        self.assertEqual(out["status"], "solved")
        again = self.get("/api/problems/" + self.PID)["progress"]
        self.assertEqual((again["status"], again["bookmarked"], again["notes"]),
                         ("solved", True, "BFS"))

    def test_progress_filters_the_listing(self):
        self.post("/api/progress/" + self.PID, {"status": "review"})
        ids = [i["id"] for i in self.get("/api/problems?status=review&limit=50")["items"]]
        self.assertIn(self.PID, ids)
        self.assertNotIn(self.PID,
                         [i["id"] for i in self.get("/api/problems?status=solved&limit=50")["items"]])

    def test_running_records_a_submission_but_never_claims_solved(self):
        pid = "adobe-determine-edit-distance-in-word-ladder"
        code = ("from collections import deque\n"
                "def ladderLength(beginWord, endWord, wordList):\n"
                "    words = set(wordList)\n"
                "    if endWord not in words: return -1\n"
                "    if beginWord == endWord: return 0\n"
                "    q = deque([(beginWord, 0)]); seen = {beginWord}\n"
                "    while q:\n"
                "        w, d = q.popleft()\n"
                "        for i in range(len(w)):\n"
                "            for ch in 'abcdefghijklmnopqrstuvwxyz':\n"
                "                nxt = w[:i] + ch + w[i+1:]\n"
                "                if nxt == endWord: return d + 1\n"
                "                if nxt in words and nxt not in seen:\n"
                "                    seen.add(nxt); q.append((nxt, d + 1))\n"
                "    return -1\n")
        out, _ = self.post("/api/run", {"problemId": pid, "language": "python", "code": code})
        self.assertEqual((out["passed"], out["total"]), (3, 3), out)
        p = self.get("/api/problems/" + pid)["progress"]
        self.assertEqual(p["status"], "attempted")       # never auto-"solved"
        self.assertIn("python", p["submissions"])

    def test_bank_is_never_written(self):
        import fpdb
        before = os.path.getmtime(fpdb.DEFAULT_DB)
        self.post("/api/progress/" + self.PID, {"notes": "x" * 100})
        self.assertEqual(os.path.getmtime(fpdb.DEFAULT_DB), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
