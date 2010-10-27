import unittest
import mock
import sublime
import sys

sys.path.extend("..")

sublime.packagesPath = mock.Mock()
sublime.packagesPath.return_value = "XXX"

import sublimeplugin
import sublimemodelines

def test_getLineCommentCharacter_Does_metaInfo_GetCorrectArgs():
    view = mock.Mock()
    sublimemodelines.getLineCommentCharacter(view)

    actual = view.metaInfo.call_args
    expected = (("shellVariables", 0), {})

    assert actual == expected

def test_getLineCommentCharacter_DoWeGetLineCommentCharIfExists():
    view = mock.Mock()
    view.metaInfo.return_value = [{ "name": "TM_COMMENT_START", "value": "#"}]

    expected = "#"
    actual = sublimemodelines.getLineCommentCharacter(view)

    assert expected == actual

def test_getLineCommentCharacter_DoWeGetEmptyLineIfLineCommentCharDoesntExist():
    view = mock.Mock()
    view.metaInfo.return_value = [{ "name": "NOT_TM_COMMENT_START", "value": "#"}]

    expected = ""
    actual = sublimemodelines.getLineCommentCharacter(view)

    assert expected == actual

def test_getLineCommentCharacter_ShouldReturnEmptyStringIfNoExtraVariablesExist():
    view = mock.Mock()
    view.metaInfo.return_value = None

    expected = ""
    actual = sublimemodelines.getLineCommentCharacter(view)

    assert expected == actual

# class TestCase_buildModelinePrefix(unittest.TestCase):

#     def setUp(self):
#         self.view = mock.Mock()
#         self.DEFAULT_LINE_CHAR = "#"
#         self.DEFAULT_PREFIX_TEMPLATE = "%s\\s*(st|sublime): "

#     def test_AreDefaultsCorrect(self):

#         actual = sublimemodelines.SUBLIMETEXT_MODELINE_PREFIX_TPL % "TEST", sublimemodelines.DEFAULT_LINE_COMMENT
#         expected = self.DEFAULT_PREFIX_TEMPLATE % "TEST", self.DEFAULT_LINE_CHAR

#         self.assertEquals(actual, expected)

#     def test_BuildPrefixWithDynamicLineCommentChar(self):

#         self.view.metaInfo.return_value = [{ "name": "TM_COMMENT_START", "value": "//"}]

#         expected = self.DEFAULT_PREFIX_TEMPLATE % "//"
#         actual = sublimemodelines.buildModelinePrefix(self.view)

#         self.assertEquals(expected, actual)

#     def test_BuildPrefixWithDefaultLineCommentChar(self):

#         self.view.metaInfo.return_value = None

#         expected = "%s\\s*(st|sublime): " % self.DEFAULT_LINE_CHAR
#         actual = sublimemodelines.buildModelinePrefix(self.view)

#         self.assertEquals(expected, actual)


# class TestCase_GettingModelines(unittest.TestCase):

#     def setUp(self):
#         self.view = mock.Mock()
#         self.command = sublimemodelines.ExecuteSublimeTextModeLinesCommand()
#         self.sublime = sublime
#         self.sublime.Region = mock.Mock()

#     def test_getCandidatesBottom_TopRegionLargerThanBuffer(self):
#         self.view.size.return_value = 100

#         actual = self.command._getCandidatesBottom(self.view, 200)
#         expected = []

#         self.assertEquals(expected, actual)

#     def test_getCandidatesBottom_MakeSureWeCall_sublime_Region_Correctly(self):

#         self.view.size.return_value = 200

#         self.command._getCandidatesBottom(self.view, 100)
#         actual = self.sublime.Region.call_args
#         expected = ((101, 200), {})

#         self.assertEquals(expected, actual)


#     def test_getCandidatesBottom_MakeSureWeReturnFrom_view_lines(self):

#         self.view.size.return_value = 200

#         self.view.lines.return_value = [1, 2]
#         actual = self.command._getCandidatesBottom(self.view, 100)
#         expected = [1, 2]

#         self.assertEquals(expected, actual)

#     def test_getCandidatesTop_MakeSureWeGetCorrectDefaultBottomBoundary(self):

#         self.view.size.return_value = 5000

#         self.command._getCandidatesTop(self.view)

#         actual = self.view.fullLine.call_args
#         expected = ((4000,), {})

#         self.assertEquals(expected, actual)

#     def test_getCandidatesTop_MakeSureWeReturnFrom_view_lines(self):

#         self.view.size.return_value = 5000

#         self.view.lines.return_value = [1, 2]

#         actual = self.command._getCandidatesTop(self.view)
#         expected = [1, 2]

#         self.assertEquals(expected, actual)

# class TestCase_isModeline(unittest.TestCase):

#     def setUp(self):
#         self.view = mock.Mock()
#         self.regionLine = mock.Mock()
#         self.command = sublimemodelines.ExecuteSublimeTextModeLinesCommand()

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
#         self.c = sublimemodelines.ExecuteSublimeTextModeLinesCommand()

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
