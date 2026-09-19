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
        js = read("app.js") + read("study.js")
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
