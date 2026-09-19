"""Rules about the page that a Python test can still hold us to.

These exist because of a real bug: #study and #workspace were given `display`
in the stylesheet, which beats the browser's [hidden] rule, so toggling
`el.hidden` from JavaScript changed nothing visible. Every other pane in the
file had its own `[hidden]{display:none}` rule; the two new ones did not.
"""
import os, re, unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC = os.path.join(HERE, "static")


def read(name):
    with open(os.path.join(STATIC, name), encoding="utf-8") as fh:
        return fh.read()


class TestHiddenActuallyHides(unittest.TestCase):
    def test_a_global_rule_makes_hidden_win(self):
        css = read("styles.css")
        self.assertRegex(
            css, r"\[hidden\]\s*\{\s*display\s*:\s*none\s*!important",
            "without a global [hidden] rule, any element with its own display "
            "cannot be hidden from JavaScript")

    def test_every_toggled_element_has_a_display_rule_it_can_lose_to(self):
        """Whatever JS toggles must be an id the stylesheet does not re-show."""
        js = read("app.js") + read("study.js") + read("timer.js")
        css = read("styles.css")
        toggled = set(re.findall(r"\$\('#([a-zA-Z]+)'\)\.hidden\s*=", js))
        toggled |= set(re.findall(r"#([a-zA-Z]+)'\)\.hidden\s*=", js))
        self.assertTrue(toggled, "no hidden toggles found - did the app change?")
        for el in sorted(toggled):
            own = re.search(r"#%s\s*\{([^}]*)\}" % el, css)
            if own and re.search(r"display\s*:", own.group(1)):
                # it has a display of its own, so the global rule is the only
                # thing that can hide it
                self.assertRegex(css, r"\[hidden\]\s*\{\s*display\s*:\s*none\s*!important",
                                 "#%s sets display and would ignore [hidden]" % el)


class TestNoDanglingSelectors(unittest.TestCase):
    """Every $('#id') must be an id something actually creates.

    This exists because of a real bug: the interface rebuild left a second copy
    of runFuzz() behind that still reached for `#editorHost .results`, an id
    the new page does not have. Nothing complained until it ran.
    """

    SCRIPTS = ("app.js", "study.js", "timer.js")

    def known_ids(self):
        ids = set(re.findall(r'id="([\w-]+)"', read("index.html")))
        for name in self.SCRIPTS:                      # ids the scripts create
            js = read(name)
            ids |= set(re.findall(r"\.id = '([\w-]+)'", js))
        return ids

    def test_every_id_selector_resolves(self):
        ids = self.known_ids()
        for name in self.SCRIPTS:
            js = read(name)
            used = set(re.findall(r"\$\('#([\w-]+)'", js))
            used |= set(re.findall(r"getElementById\('([\w-]+)'\)", js))
            for el in sorted(used - ids):
                self.fail("%s reaches for #%s, which nothing creates" % (name, el))

    def test_no_function_is_defined_twice(self):
        """Two definitions means the first one is dead code that still reads."""
        for name in self.SCRIPTS:
            names = re.findall(r"^(?:async )?function ([A-Za-z_]\w*)",
                               read(name), re.M)
            dupes = sorted({n for n in names if names.count(n) > 1})
            self.assertFalse(dupes, "%s defines %s more than once" % (name, dupes))


class TestTimerWiring(unittest.TestCase):
    """The timer is one script talking to ids in the page; a typo in either is
    invisible until you click, so hold them to each other here."""

    def test_the_script_is_loaded_before_the_app(self):
        html = read("index.html")
        self.assertLess(html.index('src="timer.js"'), html.index('src="app.js"'),
                        "app.js calls Timer.wire() during boot")

    def test_every_id_the_timer_reaches_for_exists_in_the_page(self):
        html = read("index.html")
        wanted = set(re.findall(r"\$\('#([A-Za-z][\w-]*)'\)", read("timer.js")))
        self.assertIn("timerBtn", wanted, "did the timer stop using $('#...')?")
        for el in sorted(wanted):
            self.assertIn('id="%s"' % el, html, "timer.js reaches for #%s, "
                          "which the page does not have" % el)

    def test_the_app_wires_and_hooks_the_timer(self):
        js = read("app.js")
        self.assertIn("Timer.wire()", js)
        self.assertIn("Timer.onEscape()", js)
        self.assertIn("Timer.onProblemOpened()", js)

    def test_the_server_serves_the_script_under_a_mount_prefix(self):
        """ROUTES is how /site/timer.js is recognised behind a proxy."""
        with open(os.path.join(HERE, "serve.py"), encoding="utf-8") as fh:
            serve = fh.read()
        routes = re.search(r"ROUTES = \{(.*?)\}", serve, re.S).group(1)
        self.assertIn('"timer.js"', routes)


class TestPageWiring(unittest.TestCase):
    def test_study_script_is_loaded_before_the_app(self):
        html = read("index.html")
        self.assertLess(html.index('src="study.js"'), html.index('src="app.js"'),
                        "app.js calls Study.wire() during boot")

    def test_the_study_button_exists(self):
        self.assertIn('id="studyBtn"', read("index.html"))

    def test_the_study_space_does_not_reuse_the_topic_filter_key(self):
        """?topic= is a bank-tag filter; the study space must not collide."""
        js = read("app.js")
        self.assertIn("extra.study = state.topic", js)
        self.assertNotIn("extra.topic = state.topic", js)


if __name__ == "__main__":
    unittest.main()
