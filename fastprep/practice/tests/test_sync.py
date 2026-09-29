"""The background sync: new problems land whole, changed ones never lose their
statement mid-sync, vanished ones are kept and flagged, and the app picks all
of it up while it keeps serving.

Nothing here touches the network or the real bank: the unit tests use a fake
client, and the end-to-end test runs serve.py on a COPY of the bank against a
stand-in FastPrep upstream on localhost.
"""
import json, os, shutil, socket, sqlite3, subprocess, sys, tempfile, threading, time, unittest
import urllib.error, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))

import fastprep  # noqa: E402
import fpdb      # noqa: E402

BASE = "http://upstream.test"


def problem(pid, title="T", seen=("2026-09-01",), **extra):
    p = {"id": pid, "title": title, "company": "Acme", "companyId": "c1",
         "status": "published", "difficulty": "easy", "problemType": "OA",
         "problemTypes": ["OA"], "employmentTypes": ["INTERN"], "topics": ["array"],
         "targetRoles": [], "practiceFormat": "algorithm", "supportedLanguages": [],
         "url": None, "order": 1, "lastSeen": list(seen)}
    p.update(extra)
    return p


def detail(p, statement="<p>do it</p>"):
    return dict(p, problemStatement=statement, examples=[], functionName="f",
                starterCode="", sourceImages=[])


class FakeClient:
    """Serves an index and details from dicts; ids in `fail` raise."""

    def __init__(self, index, details, fail=()):
        self.index, self.details, self.fail = index, details, set(fail)
        self.calls = []

    def get_json(self, url):
        self.calls.append(url)
        if url == BASE + "/api/problems":
            return self.index
        pid = url.rsplit("/", 1)[1]
        if pid in self.fail:
            raise RuntimeError("HTTP 500")
        return self.details.get(pid)


class TestSyncBank(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fp-sync-")
        self.conn = fastprep.connect(os.path.join(self.tmp, "b.db"))
        a, b = problem("a", "A"), problem("b", "B")
        client = FakeClient([a, b], {"a": detail(a), "b": detail(b)})
        fastprep.sync_bank(self.conn, client, workers=2, base=BASE)

    def tearDown(self):
        self.conn.close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def row(self, pid):
        return self.conn.execute("SELECT * FROM problems WHERE id=?", (pid,)).fetchone()

    def test_first_sync_stores_index_and_detail_together(self):
        for pid in ("a", "b"):
            r = self.row(pid)
            self.assertIsNotNone(r["detail_json"])
            self.assertEqual(r["detail_stale"], 0)

    def test_only_new_and_changed_problems_are_fetched(self):
        a, b, c = problem("a", "A"), problem("b", "B2"), problem("c", "C")
        client = FakeClient([a, b, c], {"b": detail(b), "c": detail(c)})
        s = fastprep.sync_bank(self.conn, client, workers=2, base=BASE)
        fetched = sorted(u.rsplit("/", 1)[1] for u in client.calls[1:])
        self.assertEqual(fetched, ["b", "c"])            # "a" is unchanged: no request
        self.assertEqual((s["added"], s["updated"]), (["c"], ["b"]))
        self.assertTrue(s["inSync"])
        self.assertEqual(json.loads(self.row("b")["detail_json"])["title"], "B2")

    def test_a_new_problem_whose_detail_fails_is_not_half_written(self):
        a, b, c = problem("a", "A"), problem("b", "B"), problem("c", "C")
        s = fastprep.sync_bank(self.conn, FakeClient([a, b, c], {}, fail={"c"}),
                               workers=1, base=BASE)
        self.assertIsNone(self.row("c"))                 # not there at all, rather than empty
        self.assertEqual(s["failed"], ["c"])
        self.assertFalse(s["inSync"])
        s = fastprep.sync_bank(self.conn, FakeClient([a, b, c], {"c": detail(c)}),
                               workers=1, base=BASE)
        self.assertEqual(s["added"], ["c"])               # and the next run picks it up
        self.assertTrue(s["inSync"])

    def test_a_changed_problem_keeps_its_statement_until_the_new_one_arrives(self):
        a2 = problem("a", "A2", seen=("2026-09-01", "2026-09-20"))
        s = fastprep.sync_bank(self.conn, FakeClient([a2, problem("b", "B")], {}, fail={"a"}),
                               workers=1, base=BASE)
        r = self.row("a")
        self.assertEqual(json.loads(r["detail_json"])["title"], "A")   # old, but present
        self.assertEqual(r["title"], "A")                               # row not half-updated
        self.assertEqual(s["failed"], ["a"])
        diff = fastprep.compare(self.conn, [a2, problem("b", "B")])
        self.assertEqual(diff["changed"], ["a"])                        # still owed

    def test_a_problem_gone_upstream_is_kept_and_flagged_then_unflagged(self):
        a, b = problem("a", "A"), problem("b", "B")
        s = fastprep.sync_bank(self.conn, FakeClient([a], {}), workers=1, base=BASE)
        self.assertEqual(s["delisted"], ["b"])
        self.assertIsNotNone(self.row("b")["delisted_at"])
        self.assertIsNotNone(self.row("b")["detail_json"])             # kept whole
        self.assertTrue(s["inSync"])
        s = fastprep.sync_bank(self.conn, FakeClient([a, b], {}), workers=1, base=BASE)
        self.assertEqual(s["relisted"], ["b"])
        self.assertIsNone(self.row("b")["delisted_at"])

    def test_compare_counts_without_writing(self):
        before = self.conn.total_changes
        diff = fastprep.compare(self.conn, [problem("a", "A"), problem("z", "Z")])
        self.assertEqual((diff["remote"], diff["local"]), (2, 2))
        self.assertEqual((diff["new"], diff["removed"]), (["z"], ["b"]))
        self.assertFalse(diff["inSync"])
        self.assertEqual(self.conn.total_changes, before)

    def test_screenshots_replaced_upstream_are_reported_appended_ones_are_not(self):
        a, b = problem("a", "A1"), problem("b", "B1")     # changed, so refetched
        imgs = lambda pid, n: ["/api/problem-source-images/%s/%d" % (pid, i) for i in range(n)]
        da, db = dict(detail(a), sourceImages=imgs("a", 2)), dict(detail(b), sourceImages=imgs("b", 2))
        fastprep.sync_bank(self.conn, FakeClient([a, b], {"a": da, "b": db}), base=BASE)
        a2, b2 = problem("a", "A2"), problem("b", "B2")
        da2 = dict(detail(a2), sourceImages=imgs("a", 3))                  # one appended
        db2 = dict(detail(b2), sourceImages=["/elsewhere/0"])               # replaced
        s = fastprep.sync_bank(self.conn, FakeClient([a2, b2], {"a": da2, "b": db2}), base=BASE)
        self.assertEqual(s["imagesReplaced"], ["b"])

    def test_forgetting_a_problems_screenshots_leaves_the_others(self):
        import images
        old = images.CACHE_DIR
        try:
            images.set_cache_dir(os.path.join(self.tmp, "img"))
            for name in ("b-0", "b-1", "b-1x-0", "bb-0"):
                open(os.path.join(images.CACHE_DIR, name), "wb").write(b"x")
            self.assertEqual(images.forget("b"), 2)
            self.assertEqual(sorted(os.listdir(images.CACHE_DIR)), ["b-1x-0", "bb-0"])
        finally:
            images.CACHE_DIR = old

    def test_first_indexed_at_survives_an_update(self):
        first = self.row("a")["first_indexed_at"]
        a2 = problem("a", "A2")
        fastprep.sync_bank(self.conn, FakeClient([a2, problem("b", "B")], {"a": detail(a2)}),
                           workers=1, base=BASE)
        self.assertEqual(self.row("a")["first_indexed_at"], first)

    def test_an_old_bank_is_migrated_in_place(self):
        path = os.path.join(self.tmp, "old.db")
        old = sqlite3.connect(path)
        # the schema as it was before delisting and staleness were tracked
        lines = [l for l in fastprep.SCHEMA.splitlines()
                 if "detail_stale" not in l and "delisted_at" not in l]
        old.executescript("\n".join(lines).replace("updated_at          TEXT,",
                                                     "updated_at          TEXT"))
        old.execute("INSERT INTO problems (id, title) VALUES ('x', 'X')")
        old.commit()
        old.close()
        conn = fastprep.connect(path)
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(problems)")}
        self.assertTrue({"detail_stale", "delisted_at"} <= cols)
        self.assertEqual(conn.execute("SELECT detail_stale FROM problems").fetchone()[0], 0)
        conn.close()


class TestReaderDuringSync(unittest.TestCase):
    """What the app's read-only Bank sees of a sync that is happening."""

    def test_new_problems_become_searchable_after_invalidate(self):
        tmp = tempfile.mkdtemp(prefix="fp-sync-")
        try:
            path = os.path.join(tmp, "b.db")
            conn = fastprep.connect(path)
            a = problem("a", "Alpha")
            fastprep.sync_bank(conn, FakeClient([a], {"a": detail(a)}), base=BASE)
            bank = fpdb.Bank(path)
            self.assertEqual(bank.query({"q": "Zebra"})["total"], 0)
            z = problem("z", "Zebra crossing")
            fastprep.sync_bank(conn, FakeClient([a, z], {"z": detail(z)}), base=BASE)
            self.assertEqual(bank.query({})["total"], 2)       # plain reads: immediately
            bank.invalidate()
            self.assertEqual([i["id"] for i in bank.query({"q": "Zebra"})["items"]], ["z"])
            self.assertEqual(bank.detail("z")["title"], "Zebra crossing")
            conn.close(); bank.conn.close()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_an_index_only_row_is_served_not_a_500(self):
        tmp = tempfile.mkdtemp(prefix="fp-sync-")
        try:
            path = os.path.join(tmp, "b.db")
            conn = fastprep.connect(path)
            fastprep.upsert_index(conn, [problem("a", "Alpha")])
            bank = fpdb.Bank(path)
            d = bank.detail("a")
            self.assertEqual((d["id"], d["title"]), ("a", "Alpha"))
            conn.close(); bank.conn.close()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------ end to end
def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    return port


class Upstream:
    """A stand-in for www.fastprep.io's two public endpoints."""

    def __init__(self, index, details):
        self.index, self.details, self.hits = index, details, []
        outer = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                outer.hits.append(self.path)
                if self.path == "/api/problems":
                    body = outer.index
                else:
                    body = outer.details.get(self.path.rsplit("/", 1)[1])
                if body is None:
                    self.send_response(404); self.send_header("Content-Length", "0")
                    self.end_headers(); return
                raw = json.dumps(body).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers(); self.wfile.write(raw)

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = "http://127.0.0.1:%d" % self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def close(self):
        self.httpd.shutdown(); self.httpd.server_close()


class TestSyncEndToEnd(unittest.TestCase):
    """serve.py on a copy of the bank, syncing from a fake upstream."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="fp-sync-e2e-")
        cls.db = os.path.join(cls.tmp, "fastprep.db")
        src = sqlite3.connect("file:%s?mode=ro" % fpdb.DEFAULT_DB, uri=True)
        dst = sqlite3.connect(cls.db)
        src.backup(dst)
        src.close(); dst.close()
        conn = fastprep.connect(cls.db)          # migrate the copy, as a sync would
        # a few hundred problems are plenty here, and keep the topic re-filing
        # (a minute of CPU over the whole bank) to a couple of seconds
        conn.execute("DELETE FROM problems WHERE id NOT IN "
                     "(SELECT id FROM problems ORDER BY id LIMIT 300)")
        conn.commit()
        rows = list(conn.execute(
            "SELECT id, index_json, detail_json FROM problems WHERE delisted_at IS NULL "
            "ORDER BY id"))
        cls.before = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
        conn.close()

        index = [json.loads(r["index_json"]) for r in rows]
        details = {r["id"]: json.loads(r["detail_json"]) for r in rows}
        cls.gone = index.pop()["id"]                                  # removed upstream
        cls.changed = index[0]["id"]
        index[0] = dict(index[0], lastSeen=list(index[0]["lastSeen"]) + ["2026-09-28"])
        details[cls.changed] = dict(details[cls.changed],
                                    lastSeen=index[0]["lastSeen"])
        cls.new_ids = []
        for n in range(2):
            pid = "zz-synctest-quokka-%d" % n
            p = problem(pid, "Quokka Counting %d" % n, seen=("2026-09-28",))
            index.append(p)
            details[pid] = detail(p, "<p>Count the quokkas in the grid.</p>")
            cls.new_ids.append(pid)
        cls.upstream = Upstream(index, details)

        with open(os.path.join(cls.tmp, "all_problems.json"), "w") as f:
            f.write("[]")
        cls.topic_index = os.path.join(cls.tmp, "INDEX.json")
        import topics
        shutil.copy(topics.INDEX_PATH, cls.topic_index)
        port = free_port()
        cls.base = "http://127.0.0.1:%d" % port
        env = dict(os.environ, FASTPREP_BASE=cls.upstream.url)
        cls.proc = subprocess.Popen(
            [sys.executable, os.path.join(HERE, "serve.py"), "--port", str(port),
             "--db", cls.db, "--progress-db", os.path.join(cls.tmp, "p.db"),
             "--sync-interval", "3600", "--topic-index", cls.topic_index],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=HERE, env=env)
        for _ in range(150):
            try:
                urllib.request.urlopen(cls.base + "/api/health", timeout=1).read()
                break
            except Exception:
                time.sleep(0.1)
        else:
            raise RuntimeError("server did not start")

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate(); cls.proc.wait(timeout=10)
        cls.upstream.close()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def get(self, path):
        return json.load(urllib.request.urlopen(self.base + path, timeout=30))

    def sync_now(self):
        req = urllib.request.Request(self.base + "/api/sync", b"{}", method="POST",
                                     headers={"Content-Type": "application/json"})
        r = urllib.request.urlopen(req, timeout=30)
        self.assertEqual(r.status, 202)
        for _ in range(600):
            s = self.get("/api/sync")
            if not s["running"] and s["phase"] == "idle" and s["lastCheck"]:
                return s
            time.sleep(0.1)
        self.fail("sync did not finish")

    def test_sync_pulls_new_problems_into_the_running_app(self):
        s = self.sync_now()
        r = s["lastResult"]
        self.assertIsNone(s["lastError"])
        self.assertEqual((r["added"], r["updated"], r["delisted"]), (2, 1, 1), r)
        self.assertTrue(r["inSync"])
        self.assertEqual(r["progressOrphans"], 0)
        self.assertEqual(sorted(r["addedIds"]), self.new_ids)

        # only the two new problems and the changed one were fetched in detail
        details = [h for h in self.upstream.hits if h != "/api/problems"]
        self.assertEqual(sorted(details), sorted(
            "/api/problems/" + i for i in self.new_ids + [self.changed]))

        # the app serves them without a restart: count, detail, search, sort
        self.assertEqual(self.get("/api/health")["problems"], self.before + 2)
        d = self.get("/api/problems/" + self.new_ids[0])
        self.assertIn("quokkas", d["problemStatement"])
        self.assertTrue(d["addedAt"])
        hits = self.get("/api/problems?q=quokka&limit=5")["items"]
        self.assertEqual(sorted(i["id"] for i in hits), self.new_ids)
        top = self.get("/api/problems?sort=added&limit=2")["items"]
        self.assertEqual(sorted(i["id"] for i in top), self.new_ids)
        self.assertIn("2026-09-28", self.get("/api/problems/" + self.changed)["lastSeen"])

        # removed upstream: still openable, and says so
        gone = self.get("/api/problems/" + self.gone)
        self.assertTrue(gone["delistedAt"])
        self.assertGreaterEqual(self.get("/api/facets")["meta"]["delisted"], 1)

        # the JSON copy of the bank matches the database row for row
        with open(os.path.join(self.tmp, "all_problems.json")) as f:
            export = json.load(f)
        conn = sqlite3.connect(self.db)
        self.assertEqual(len(export), conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0])
        self.assertEqual({p["id"] for p in export},
                         {r[0] for r in conn.execute("SELECT id FROM problems")})
        conn.close()

        # the study space filed them: its problem count is the bank's
        self.assertEqual(self.get("/api/topics")["problems"], self.before + 2)
        with open(self.topic_index) as f:
            self.assertIn(self.new_ids[0], json.load(f)["byProblem"])

        # and a second look finds nothing to do: one index request, no details
        self.upstream.hits.clear()
        r = self.sync_now()["lastResult"]
        self.assertEqual((r["added"], r["updated"], r["delisted"]), (0, 0, 0))
        self.assertEqual(self.upstream.hits, ["/api/problems"])

    def test_status_is_reported_in_health(self):
        s = self.get("/api/health")["sync"]
        self.assertTrue(s["enabled"])
        self.assertEqual(s["upstream"], self.upstream.url)


class TestSyncOff(unittest.TestCase):
    def test_offline_means_no_sync(self):
        port = free_port()
        tmp = tempfile.mkdtemp(prefix="fp-sync-off-")
        proc = subprocess.Popen(
            [sys.executable, os.path.join(HERE, "serve.py"), "--port", str(port),
             "--offline", "--progress-db", os.path.join(tmp, "p.db")],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=HERE)
        base = "http://127.0.0.1:%d" % port
        try:
            for _ in range(150):
                try:
                    urllib.request.urlopen(base + "/api/health", timeout=1).read(); break
                except Exception:
                    time.sleep(0.1)
            s = json.load(urllib.request.urlopen(base + "/api/sync", timeout=10))
            self.assertEqual((s["enabled"], s["reason"]), (False, "--offline"))
            req = urllib.request.Request(base + "/api/sync", b"{}", method="POST")
            with self.assertRaises(urllib.error.HTTPError) as cm:
                urllib.request.urlopen(req, timeout=10)
            self.assertEqual(cm.exception.code, 409)
        finally:
            proc.terminate(); proc.wait(timeout=10)
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
