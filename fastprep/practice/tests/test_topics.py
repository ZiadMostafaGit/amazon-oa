"""The study space: the canon, the mapping, the renderer and the endpoints."""
import json, os, re, sys, unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "tools"))

import mdlite
import topics as topics_mod
from canon import CANON, by_slug


class TestCanon(unittest.TestCase):
    def test_one_hundred_and_fifty_topics(self):
        self.assertEqual(len(CANON), 150)

    def test_slugs_are_unique_and_url_safe(self):
        slugs = [c[1] for c in CANON]
        self.assertEqual(len(slugs), len(set(slugs)))
        for s in slugs:
            self.assertRegex(s, r"^[a-z0-9-]+$")

    def test_every_cross_reference_resolves(self):
        known = {c[1] for c in CANON}
        for c in CANON:
            for ref in c[5] + c[6]:
                self.assertIn(ref, known, "%s -> %s" % (c[1], ref))

    def test_patterns_compile(self):
        for c in CANON:
            for p in c[4]:
                re.compile(p)

    def test_no_topic_points_at_itself(self):
        for c in CANON:
            self.assertNotIn(c[1], c[5] + c[6])


class TestIndex(unittest.TestCase):
    """The mapping is generated; these are the properties it must keep."""
    @classmethod
    def setUpClass(cls):
        cls.idx = topics_mod.index()

    def test_every_canon_topic_is_indexed(self):
        self.assertEqual(len(self.idx["topics"]), len(CANON))
        self.assertEqual({t["slug"] for t in self.idx["topics"]},
                         {c[1] for c in CANON})

    def test_ranked_by_use_with_craft_last(self):
        real = [t for t in self.idx["topics"] if t["kind"] != "craft"]
        counts = [t["count"] for t in real]
        self.assertEqual(counts, sorted(counts, reverse=True))
        ranks = [t["rank"] for t in self.idx["topics"]]
        self.assertEqual(ranks, list(range(1, len(ranks) + 1)))

    def test_rare_means_no_problems(self):
        for t in self.idx["topics"]:
            if t["rare"]:
                self.assertEqual(t["count"], 0)
                self.assertNotEqual(t["kind"], "craft")
            elif t["kind"] != "craft":
                self.assertGreater(t["count"], 0)

    def test_counts_match_the_problem_lists(self):
        for t in self.idx["topics"]:
            self.assertEqual(t["count"], len(t["problems"]))

    def test_problem_links_are_capped_and_real(self):
        known = {c[1] for c in CANON}
        for pid, slugs in self.idx["byProblem"].items():
            self.assertLessEqual(len(slugs), 6)
            for s in slugs:
                self.assertIn(s, known)

    def test_a_known_problem_maps_where_it_should(self):
        links = self.idx["byProblem"].get("amazon-stock-span") or []
        self.assertIn("monotonic-stack", links)


class TestRenderer(unittest.TestCase):
    def render(self, src):
        return mdlite.render(src)

    def test_headings_get_anchors(self):
        out = self.render("# T\n\n## The idea\n")
        self.assertIn('<h2 id="the-idea">', out["html"])
        self.assertEqual([t["text"] for t in out["toc"]], ["T", "The idea"])

    def test_script_and_handlers_cannot_get_through(self):
        out = self.render('<svg viewBox="0 0 1 1" onclick="x()"><rect/></svg>\n'
                          '\n<script>bad()</script>\n')
        self.assertNotIn("onclick", out["html"])
        self.assertNotIn("<script>", out["html"])
        self.assertIn("&lt;script&gt;", out["html"])

    def test_runnable_blocks_are_marked(self):
        out = self.render("```python run\nprint(1)\n```\n\n```python\nx\n```\n")
        self.assertEqual([s["run"] for s in out["snippets"]], [True, False])
        self.assertIn('class="snippet runnable"', out["html"])

    def test_check_splits_on_the_dash(self):
        out = self.render(":::check\nQuestion?\n--\nAnswer.\n:::\n")
        self.assertEqual(out["checks"], 1)
        self.assertIn("Question?", out["html"])
        self.assertIn('class="a" hidden', out["html"])

    def test_topic_links(self):
        out = mdlite.render("See [[binary-search|it]].", lambda s: "?study=" + s)
        self.assertIn('href="?study=binary-search"', out["html"])
        self.assertIn(">it</a>", out["html"])

    def test_code_is_not_reformatted(self):
        out = self.render("`a**b**c` and **real** bold\n")
        self.assertIn("<code>a**b**c</code>", out["html"])
        self.assertIn("<strong>real</strong>", out["html"])

    def test_tables_and_lists(self):
        out = self.render("| a | b |\n| --- | --- |\n| 1 | 2 |\n\n- one\n- two\n")
        self.assertIn("<th>a</th>", out["html"])
        self.assertIn("<li>one</li>", out["html"])


class TestArticles(unittest.TestCase):
    """Whatever is written must stay loadable and self-consistent."""
    def test_every_article_renders_and_links_resolve(self):
        known = {c[1] for c in CANON}
        d = os.path.join(HERE, "topics", "articles")
        if not os.path.isdir(d):
            self.skipTest("no articles yet")
        names = [f[:-3] for f in os.listdir(d) if f.endswith(".md")]
        for slug in names:
            self.assertIn(slug, known, "%s is not a canon topic" % slug)
            a = topics_mod.article(slug)
            self.assertTrue(a["html"])
            # the closing ]] matters: a matrix literal like [[1, 2], [3, 4]]
            # is prose, not a broken link
            for m in re.finditer(r"\[\[([a-z0-9-]+)(?:\|[^\]]+)?\]\]", a["source"]):
                self.assertIn(m.group(1), known, "%s links to %s" % (slug, m.group(1)))

    def test_listing_counts_articles(self):
        out = topics_mod.listing()
        self.assertEqual(out["withArticles"],
                         sum(1 for t in out["topics"] if t["hasArticle"]))


if __name__ == "__main__":
    unittest.main()
