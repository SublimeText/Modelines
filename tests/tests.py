import unittest
import mock
import sublime

sublime.packagesPath = mock.Mock()
sublime.packagesPath.return_value = "XXX"

import sublimeplugin

sublimeplugin.Plugin = mock.Mock()

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


if __name__ == "__main__":
    unittest.main()