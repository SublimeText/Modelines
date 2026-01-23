# This is the original test file before ST 3 compatibility was added.

from unittest import TestCase
import sublime

from Modelines import sublime_modelines



class MockView(sublime.View):
    
    comment_start_char = None
    latest_meta_info_call_args = None
    
    def set_comment_start_char(self, new_char):
        self.comment_start_char = new_char
    
    def meta_info(self, key, pt):
        res = None
        if key != "TM_COMMENT_START" or self.comment_start_char == None: res = super().meta_info(key, pt)
        else:                                                            res = self.comment_start_char
        self.latest_meta_info_call_args = ((key, pt), res)
        return res


class SublimeModelinesTest(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file(sublime.TRANSIENT, "")
        self.view.__class__ = MockView
        
        # Make sure we have a window to work with.
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")
    
    # This test is strange, but it relates to a previous version of Modelines checking the comment char to make it a part of the regex to detect modelines.
    # We do not do that anymore; let’s make sure of it!
    # (I like the mock thing I did, I don’t want to remove it…)
    def test_get_line_comment_char_does_not_call_meta_info(self):
        sublime_modelines.build_modeline_prefix(self.view)

        actual = self.view.latest_meta_info_call_args
        expected = None

        self.assertEqual(actual, expected)

    # def test_build_modeline_prefix_AreDefaultsCorrect(self):
    #     actual = sublime_modelines.MODELINE_PREFIX_TPL % "TEST", sublime_modelines.DEFAULT_LINE_COMMENT
    #     expected = "%s\\s*(st|sublime):" % "TEST", "#"
    #     self.assertEqual(actual, expected)


    # def test_BuildPrefixWithDynamicLineCommentDoubleSlash(self):
    #     self.view.set = [{"name": "TM_COMMENT_START", "value": "//"}]
    #     expected = "%s\\s*(st|sublime):" % "//"
    #     actual = sublime_modelines.build_modeline_prefix(self.view)
    #     assert actual == expected


    # def test_BuildPrefixWithDefaultLineCommentChar(self):
    #     #self.view.meta_info.return_value = None

    #     expected = "%s\\s*(st|sublime):" % "#"
    #     actual = sublime_modelines.build_modeline_prefix(self.view)

    #     self.assertEqual(actual, expected)


    # def test_gen_modelines(self):
    #     sublime.Region = mock.Mock()
    #     self.view.substr.side_effect = lambda x: x
    #     self.view.size.return_value = 0
    #     self.view.lines.return_value = [
    #                             "# sublime: hello world",
    #                             "# sublime: hi there; it's me",
    #                             "#sublime: some modeline",
    #                             "random stuff"
    #                         ]
    #     modelines = [
    #             "# sublime: hello world",
    #             "# sublime: hi there; it's me",
    #             "#sublime: some modeline"
    #         ] * 2 # the buffer is so small that there's overlap top/bottom modelines.

    #     self.assertEqual([l for l in sublime_modelines.gen_modelines(self.view)], modelines)


    # def test_gen_raw_options(self):
    #     mdls = [
    #         "# sublime: foo bar",
    #         "# sublime: bar foo; foo bar",
    #         "# st: baz foob",
    #         "# st: fibz zap; zup blah"
    #     ]

    #     actual = [
    #         "foo bar",
    #         "bar foo",
    #         "foo bar",
    #         "baz foob",
    #         "fibz zap",
    #         "zup blah",
    #     ]

    #     self.assertEqual([x for x in sublime_modelines.gen_raw_options(mdls)], actual)


    # def test_gen_modeline_options(self):
    #     set = self.view.settings().set

    #     gen_modelines = mock.Mock()
    #     gen_modelines.return_value = ["# sublime: foo bar",
    #                                   "# sublime: baz zoom"]

    #     gen_raw_options = mock.Mock()
    #     gen_raw_options.return_value = ["foo bar",
    #                                     "baz zoom"]

    #     sublime_modelines.gen_modelines = gen_modelines
    #     sublime_modelines.gen_raw_options = gen_raw_options

    #     actual = [x for x in sublime_modelines.gen_modeline_options(self.view)]
    #     self.assertEqual([(set, "foo", "bar"), (set, "baz", "zoom")], actual)


    # def test_is_modeline(self):
    #     sublime_modelines.build_modeline_prefix = mock.Mock(return_value="# sublime: ")
    #     self.view.substr.return_value = "# sublime: "  
    #     self.assertTrue(sublime_modelines.is_modeline(self.view, 0))


    def test_to_json_type(self):
        a = "1"
        b = "1.0"
        c = "false"
        d = "true"
        e = list()

        self.assertEqual(sublime_modelines.to_json_type(a), 1)
        self.assertEqual(sublime_modelines.to_json_type(b), 1.0)
        self.assertEqual(sublime_modelines.to_json_type(c), False)
        self.assertEqual(sublime_modelines.to_json_type(d), True)
        self.assertEqual(sublime_modelines.to_json_type(e), e)
