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


def pytest_funcarg__view(request):
    view = mock.Mock()
    return view


def test_get_line_comment_char_Does_meta_info_GetCorrectArgs(view):
    sublime_modelines.get_line_comment_char(view)

    actual = view.meta_info.call_args
    expected = (("shellVariables", 0), {})

    assert actual == expected


def test_get_line_comment_char_DoWeGetLineCommentCharIfExists(view):
    view.meta_info.return_value = [{ "name": "TM_COMMENT_START", "value": "#"}]

    expected = "#"
    actual = sublime_modelines.get_line_comment_char(view)

    assert expected == actual


def test_get_line_comment_char_DoWeGetEmptyLineIfLineCommentCharDoesntExist(view):
    view.meta_info.return_value = [{ "name": "NOT_TM_COMMENT_START", "value": "#"}]

    expected = ""
    actual = sublime_modelines.get_line_comment_char(view)

    assert expected == actual


def test_get_line_comment_char_ShouldReturnEmptyStringIfNoExtraVariablesExist(view):
    view.meta_info.return_value = None

    expected = ""
    actual = sublime_modelines.get_line_comment_char(view)

    assert expected == actual


def test_build_modeline_prefix_AreDefaultsCorrect():
    actual = sublime_modelines.MODELINE_PREFIX_TPL % "TEST", sublime_modelines.DEFAULT_LINE_COMMENT
    expected = "%s\\s*(st|sublime): " % "TEST", "#"
    assert actual == expected


def test_BuildPrefixWithDynamicLineCommentChar(view):
    view.meta_info.return_value = [{ "name": "TM_COMMENT_START", "value": "//"}]
    expected = "%s\\s*(st|sublime): " % "//"
    actual = sublime_modelines.build_modeline_prefix(view)
    assert actual == expected


def test_BuildPrefixWithDefaultLineCommentChar(view):
    view.meta_info.return_value = None

    expected = "%s\\s*(st|sublime): " % "#"
    actual = sublime_modelines.build_modeline_prefix(view)

    assert expected == actual


def test_gen_modelines(view):
    sublime.Region = mock.Mock()
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
        ] * 2 # the buffer is so small that there's overlap top/bottom modelines.

    assert modelines == [l for l in sublime_modelines.gen_modelines(view)]


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


def test_gen_modeline_options(view):
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


def test_is_modeline(view):
    sublime_modelines.build_modeline_prefix = mock.Mock(return_value="# sublime: ")
    view.substr.return_value = "# sublime: "  
    assert sublime_modelines.is_modeline(view, 0)


def test_to_json_type():
    a = "1"
    b = "1.0"
    c = "false"
    d = "true"
    e = list()

    assert sublime_modelines.to_json_type(a) == 1
    assert sublime_modelines.to_json_type(b) == 1.0
    assert sublime_modelines.to_json_type(c) == False
    assert sublime_modelines.to_json_type(d) == True
    assert sublime_modelines.to_json_type(e) == e