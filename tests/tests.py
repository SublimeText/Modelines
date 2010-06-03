import unittest
import mock
import sublime

sublime.packagesPath = mock.Mock()
sublime.packagesPath.return_value = "XXX"

import sublimeplugin

# sublimeplugin.Plugin = mock.Mock()

import sublimemodelines

class TestCase_getLineCommentCharacter(unittest.TestCase):

    def setUp(self):
        self.view = mock.Mock()

    def test_AreWeCalling_metaInfo_WithCorrectArgs(self):

        sublimemodelines.getLineCommentCharacter(self.view)

        actual = self.view.metaInfo.call_args
        expected = (("shellVariables", 0), {})

        self.assertEquals(actual, expected)

    def test_DoWeGetLineCommentCharIfExists(self):
        self.view.metaInfo.return_value = [{ "name": "TM_COMMENT_START", "value": "#"}]

        expected = "#"
        actual = sublimemodelines.getLineCommentCharacter(self.view)

        self.assertEquals(expected, actual)

    def test_DoWeGetEmptyLineIfLineCommentCharDoesntExist(self):
        self.view.metaInfo.return_value = [{ "name": "NOT_TM_COMMENT_START", "value": "#"}]

        expected = ""
        actual = sublimemodelines.getLineCommentCharacter(self.view)

        self.assertEquals(expected, actual)

    def test_IfNoVariablesExistWeShouldReturnEmptyString(self):
        self.view.metaInfo.return_value = None

        expected = ""
        actual = sublimemodelines.getLineCommentCharacter(self.view)

        self.assertEquals(expected, actual)


class TestCase_buildModelinePrefix(unittest.TestCase):

    def setUp(self):
        self.view = mock.Mock()
        self.DEFAULT_LINE_CHAR = "#"
        self.DEFAULT_PREFIX_TEMPLATE = "%s\\s*(st|sublime): "

    def test_AreDefaultsCorrect(self):

        actual = sublimemodelines.SUBLIMETEXT_MODELINE_PREFIX_TPL % "TEST", sublimemodelines.DEFAULT_LINE_COMMENT
        expected = self.DEFAULT_PREFIX_TEMPLATE % "TEST", self.DEFAULT_LINE_CHAR

        self.assertEquals(actual, expected)

    def test_BuildPrefixWithDynamicLineCommentChar(self):

        self.view.metaInfo.return_value = [{ "name": "TM_COMMENT_START", "value": "//"}]

        expected = self.DEFAULT_PREFIX_TEMPLATE % "//"
        actual = sublimemodelines.buildModelinePrefix(self.view)

        self.assertEquals(expected, actual)

    def test_BuildPrefixWithDefaultLineCommentChar(self):

        self.view.metaInfo.return_value = None

        expected = "%s\\s*(st|sublime): " % self.DEFAULT_LINE_CHAR
        actual = sublimemodelines.buildModelinePrefix(self.view)

        self.assertEquals(expected, actual)


class TestCase_GettingModelines(unittest.TestCase):

    def setUp(self):
        self.view = mock.Mock()


    def test_getCandidatesBottom_TopRegionLargerThanBuffer(self):
        self.view.size.return_value = 100

        c = sublimemodelines.ExecuteSublimeTextModeLinesCommand()
        actual = c._getCandidatesBottom(self.view, 200)
        expected = []

        self.assertEquals(expected, actual)

    def test_getCandidatesBottom_MakeSureWeCall_sublime_Region_Correctly(self):

        self.view.size.return_value = 200
        sublime.Region = mock.Mock()

        c = sublimemodelines.ExecuteSublimeTextModeLinesCommand()
        c._getCandidatesBottom(self.view, 100)
        actual = sublime.Region.call_args
        expected = ((101, 200), {})

        self.assertEquals(expected, actual)


    def test_getCandidatesBottom_MakeSureWeReturnFrom_view_lines(self):

        self.view.size.return_value = 200
        sublime.Region = mock.Mock()

        self.view.lines.return_value = [1, 2]
        c = sublimemodelines.ExecuteSublimeTextModeLinesCommand()
        actual = c._getCandidatesBottom(self.view, 100)
        expected = [1, 2]

        self.assertEquals(expected, actual)


class TestCase_isModeline(unittest.TestCase):

    def setUp(self):
        self.view = mock.Mock()

    def test_isModeline_EmptyLine(self):

        regionLine = mock.Mock()
        regionLine.emtpy.return_value = True

        expected = False

        c = sublimemodelines.ExecuteSublimeTextModeLinesCommand()
        actual = c.isModeline(self.view, regionLine)

        self.assertEquals(expected, actual)


    def test_isModeline_BadPrefix(self):

        regionLine = mock.Mock()
        self.view.substr.return_value = "NOT A MODELINE!"

        expected = False

        c = sublimemodelines.ExecuteSublimeTextModeLinesCommand()
        actual = c.isModeline(self.view, regionLine)

        self.assertEquals(expected, actual)


    def test_isModeline_Good_st_Style(self):

        regionLine = mock.Mock()
        regionLine.empty.return_value = False
        self.view.substr.return_value = "# st: A MODELINE!"

        expected = True

        c = sublimemodelines.ExecuteSublimeTextModeLinesCommand()
        actual = c.isModeline(self.view, regionLine)

        self.assertEquals(expected, actual)

    def test_isModeline_Good_sublime_Style(self):

        regionLine = mock.Mock()
        regionLine.empty.return_value = False
        self.view.substr.return_value = "# sublime: A MODELINE!"

        expected = True

        c = sublimemodelines.ExecuteSublimeTextModeLinesCommand()
        actual = c.isModeline(self.view, regionLine)

        self.assertEquals(expected, actual)


if __name__ == "__main__":
    unittest.main()