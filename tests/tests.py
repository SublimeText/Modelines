import unittest
import sys
import os

import mock

import sublime


sys.path.extend([".."])

sublime.packagesPath = mock.Mock()
sublime.packagesPath.return_value = "XXX"


import sublime_plugin
import sublime_modelines


def test_get_line_comment_char_Does_meta_info_GetCorrectArgs():
    view = mock.Mock()
    sublime_modelines.get_line_comment_char(view)

    actual = view.meta_info.call_args
    expected = (("shellVariables", 0), {})

    assert actual == expected

def test_get_line_comment_char_DoWeGetLineCommentCharIfExists():
    view = mock.Mock()
    view.meta_info.return_value = [{ "name": "TM_COMMENT_START", "value": "#"}]

    expected = "#"
    actual = sublime_modelines.get_line_comment_char(view)

    assert expected == actual

def test_get_line_comment_char_DoWeGetEmptyLineIfLineCommentCharDoesntExist():
    view = mock.Mock()
    view.meta_info.return_value = [{ "name": "NOT_TM_COMMENT_START", "value": "#"}]

    expected = ""
    actual = sublime_modelines.get_line_comment_char(view)

    assert expected == actual

def test_get_line_comment_char_ShouldReturnEmptyStringIfNoExtraVariablesExist():
    view = mock.Mock()
    view.meta_info.return_value = None

    expected = ""
    actual = sublime_modelines.get_line_comment_char(view)

    assert expected == actual

def test_build_modeline_prefix_AreDefaultsCorrect():
    actual = sublime_modelines.MODELINE_PREFIX_TPL % "TEST", sublime_modelines.DEFAULT_LINE_COMMENT
    expected = "%s\\s*(st|sublime): " % "TEST", "#"
    assert actual == expected

def test_BuildPrefixWithDynamicLineCommentChar():
    view = mock.Mock()
    view.meta_info.return_value = [{ "name": "TM_COMMENT_START", "value": "//"}]
    expected = "%s\\s*(st|sublime): " % "//"
    actual = sublime_modelines.build_modeline_prefix(view)
    assert actual == expected

def test_BuildPrefixWithDefaultLineCommentChar():
    view = mock.Mock()
    view.meta_info.return_value = None

    expected = "%s\\s*(st|sublime): " % "#"
    actual = sublime_modelines.build_modeline_prefix(view)

    assert expected == actual


def test_gen_modelines():
    # can't bother to test this now
    assert False

def test_gen_raw_options():
    mdls = [
        "# sublime: foo bar",
        "# sublime: bar foo; foo bar",
        "# st: baz foob",
        "# st: fibz zap; zup blah"
    ]

    actual = [
        "foo bar",
        "bar foo",
        "foo bar",
        "baz foob",
        "fibz zap",
        "zup blah",
    ]

    assert actual == [x for x in sublime_modelines.gen_raw_options(mdls)]

def test_gen_modeline_options():
    view = mock.Mock()
    set = view.settings().set

    gen_modelines = mock.Mock()
    gen_modelines.return_value = ["# sublime: foo bar",
                                  "# sublime: baz zoom"]

    gen_raw_options = mock.Mock()
    gen_raw_options.return_value = ["foo bar",
                                  "baz zoom"]

    sublime_modelines.gen_modelines = gen_modelines
    sublime_modelines.gen_raw_options = gen_raw_options

    actual = [x for x in sublime_modelines.gen_modeline_options(view)]
    assert [(set, "foo", "bar"), (set, "baz", "zoom")] == actual


# class TestCase_isModeline(unittest.TestCase):

#     def setUp(self):
#         self.view = mock.Mock()
#         self.regionLine = mock.Mock()
#         self.command = sublime_modelines.ExecuteSublimeTextModeLinesCommand()

#     def test_isModeline_EmptyLine(self):

#         self.regionLine.emtpy.return_value = True

#         expected = False
#         actual = self.command.isModeline(self.view, self.regionLine)

#         self.assertEquals(expected, actual)

#     def test_isModeline_BadPrefix(self):

#         self.view.substr.return_value = "NOT A MODELINE!"

#         expected = False
#         actual = self.command.isModeline(self.view, self.regionLine)

#         self.assertEquals(expected, actual)

#     def test_isModeline_Good_st_Style(self):

#         self.regionLine.empty.return_value = False
#         self.view.substr.return_value = "# st: A MODELINE!"

#         expected = True
#         actual = self.command.isModeline(self.view, self.regionLine)

#         self.assertEquals(expected, actual)

#     def test_isModeline_Good_sublime_Style(self):

#         self.regionLine.empty.return_value = False
#         self.view.substr.return_value = "# sublime: A MODELINE!"

#         expected = True
#         actual = self.command.isModeline(self.view, self.regionLine)

#         self.assertEquals(expected, actual)


# class TestCase_Other(unittest.TestCase):

#     def setUp(self):
#         self.view = mock.Mock()
#         self.view.substr.side_effect = lambda x: x
#         self.c = sublime_modelines.ExecuteSublimeTextModeLinesCommand()

#     def test_WellFormedOptionIsParsedCorrectly(self):

#         actual = self.c._extractOptions(self.view, "sublime: drawWhiteSpace all")
#         expected = (("drawWhiteSpace", "all"),)

#         self.assertEquals(expected, actual)

#     def test_MultipleOptionsAreParsedCorrectly(self):

#         actual = self.c._extractOptions(self.view, "sublime: drawWhiteSpace all; gutter false")
#         expected = (('drawWhiteSpace', 'all'), ('gutter', 'false'))

#         self.assertEquals(expected, actual)

#     def test_MultipleOptionsWithFalseSepAreParsedCorrectly(self):

#         actual = self.c._extractOptions(self.view, "sublime: drawWhiteSpace all; wordSeparators $%&:;")
#         expected = (('drawWhiteSpace', 'all'), ('wordSeparators', '$%&:;'))

#         self.assertEquals(expected, actual)

# if __name__ == "__main__":
#     unittest.main()
