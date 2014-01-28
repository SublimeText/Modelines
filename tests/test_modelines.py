from sublime_unittest import TestCase
import sublime, os


class ModelinesTest(TestCase):
    def tearDown(self):
        if hasattr(self, 'tempfile'):
            if os.path.exists(self.tempfile):
                os.remove(self.tempfile)

    def _modeline_test(self, lines):
        import tempfile

        fd, self.tempfile = mkstemp()
        fd.write(lines)
        fd.close()

        view = sublime.active_window().open_file(self.tempfile)

        while view.is_loading():
            yield

        # here test view's settings

        # in the end remove tempfile

    def test_modelines_1(self):
        lines = ("# sublime:et:ai:ts=4:\n")
        self._modeline_test(lines)

    def _gen_raw_options_test(self, line, expected):
        from .. import sublime_modelines
        if isinstance(line, list):
            self.assertEquals([x for x in sublime_modelines.gen_raw_options(line)], expected)
        else:
            self.assertEquals([x for x in sublime_modelines.gen_raw_options([line])], expected)


    def test_gen_raw_options_vim_compatibility_1(self):
        self._gen_raw_options_test("# vim: set ai noet ts=4:", 

            [ ('auto_indent', '=', 'true'),
              ('translate_tabs_to_spaces', '=', 'false'),
              ('tab_size', '=', '4') ]
              )

    def test_gen_raw_options_vim_compatibility_2(self):
        self._gen_raw_options_test("# vim:ai:et:ts=4:", 
              [ ('auto_indent', '=', 'true'),
                ('translate_tabs_to_spaces', '=', 'true'),
                ('tab_size', '=', '4') ]
              )

    def test_gen_raw_options_vim_compatibility_3(self):
        self._gen_raw_options_test('# sublime:ai:et:ts=4:ignored_packages+="Makefile Improved":',
             [('auto_indent', '=', 'true'),
              ('translate_tabs_to_spaces', '=', 'true'),
              ('tab_size', '=', '4'),
              ('ignored_packages', '+=', '"Makefile Improved"')]
              )


    def test_gen_raw_options_vim_compatibility_4(self):
        self._gen_raw_options_test('# sublime:ai:et:ts=4:ignored_packages+=["Makefile Improved", "Vintage"]:',
             [('auto_indent', '=', 'true'),
              ('translate_tabs_to_spaces', '=', 'true'),
              ('tab_size', '=', '4'),
              ('ignored_packages', '+=', '["Makefile Improved", "Vintage"]')]
            )

    def test_gen_raw_options_vim_compatibility_5(self):
        #import spdb ; spdb.start()
        self._gen_raw_options_test(
            '# sublime: set color_scheme="Packages/Color Scheme - Default/Monokai.tmTheme":',
            [('color_scheme', '=', '"Packages/Color Scheme - Default/Monokai.tmTheme"')])


    def test_gen_raw_options(self):

        mdls = [
            "# sublime: foo bar",
            "# sublime: bar foo; foo bar",
            "# st: baz foob",
            "# st: fibz zap; zup blah",
        ]

        actual = [
            "foo bar",
            "bar foo",
            "foo bar",
            "baz foob",
            "fibz zap",
            "zup blah",
        ]
        self._gen_raw_options_test(mdls, actual)
