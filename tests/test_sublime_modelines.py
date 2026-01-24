# This is the original test file before ST 3 compatibility was added.

from unittest import TestCase
from unittest.mock import Mock
import sublime

from Modelines import sublime_modelines



class SublimeModelinesTest(TestCase):
    
    # This test is strange, but it relates to a previous version of Modelines 
    #  that used to check the comment char to make it a part of the regex to detect modelines.
    # We do not do that anymore; let’s make sure of it!
    def test_get_line_comment_char_does_not_call_meta_info(self):
        view = Mock()
        sublime_modelines.build_modeline_prefix(view)
        
        actual = view.meta_info.call_args
        expected = None
        
        self.assertEqual(actual, expected)
    
    def test_gen_modelines(self):
        # Override the builtin Sublime Region class (with a backup, we restore it at the end of the test).
        originalRegion = sublime.Region
        sublime.Region = Mock()
        
        view = Mock()
        view.substr.side_effect = lambda x: x
        view.size.return_value = 0
        view.lines.return_value = [
            "# sublime: hello world",
            "# sublime: hi there; it's me",
            "#sublime: some modeline",
            "random stuff"
        ]
        modelines = [
            "# sublime: hello world",
            "# sublime: hi there; it's me",
            "#sublime: some modeline"
        ] * 2 # The buffer is so small the top/bottom modelines overlap.
        
        self.assertEqual([l for l in sublime_modelines.gen_modelines(view)], modelines)
        
        # Restore the Region class.
        sublime.Region = originalRegion
    
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
        self.assertEqual([x for x in sublime_modelines.gen_raw_options(mdls)], actual)
    
    def test_gen_modeline_options(self):
        view = Mock()
        set = view.settings().set
        
        gen_modelines = Mock()
        gen_modelines.return_value = [
            "# sublime: foo bar",
            "# sublime: baz zoom",
        ]
        
        gen_raw_options = Mock()
        gen_raw_options.return_value = [
            "foo bar",
            "baz zoom",
        ]
        
        original_gen_modelines   = sublime_modelines.gen_modelines
        original_gen_raw_options = sublime_modelines.gen_raw_options
        sublime_modelines.gen_modelines   = gen_modelines
        sublime_modelines.gen_raw_options = gen_raw_options
        
        actual = [x for x in sublime_modelines.gen_modeline_options(view)]
        self.assertEqual([(set, "foo", "bar"), (set, "baz", "zoom")], actual)
        
        sublime_modelines.gen_modelines   = original_gen_modelines
        sublime_modelines.gen_raw_options = original_gen_raw_options
    
    def test_is_modeline(self):
        self.assertTrue(sublime_modelines.is_modeline("# sublime: ", "# sublime: "))
    
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
