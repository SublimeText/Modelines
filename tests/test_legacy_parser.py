from unittest import TestCase
from unittest.mock import Mock
import re

from ..app.modeline import Modeline
from ..app.modeline_instructions.set_view_setting import ModelineInstruction_SetViewSetting
from ..app.modeline_parsers.legacy import ModelineParser_Legacy



class LegacyModelineParsingTest(TestCase):
	
	def test_parsing_data_retrieval(self):
		"""Checks whether we retrieve the correct comment char."""
		parser = ModelineParser_Legacy()
		
		# Note for the tests in this method: retrieving the comment char is a private method in the parser,
		#  so we check the final parser data, which are the full modeline prefix regex.
		
		view = Mock()
		view.meta_info = Mock(return_value=[{"name": "TM_COMMENT_START", "value": "#"}])
		self.assertEqual(parser.parser_data_for_view(view), "%s\\s*(st|sublime): " % re.escape("#"))
		
		view.meta_info = Mock(return_value=[{"name": "TM_COMMENT_START", "value": "//"}])
		self.assertEqual(parser.parser_data_for_view(view), "%s\\s*(st|sublime): " % re.escape("//"))
		
		view.meta_info = Mock(return_value=[{"name": "TM_COMMENT_START", "value": "/* "}])
		self.assertEqual(parser.parser_data_for_view(view), "%s\\s*(st|sublime): " % re.escape("/*"))
		
		view.meta_info = Mock(return_value=[{"name": "NOT_TM_COMMENT_START", "value": "//"}])
		self.assertEqual(parser.parser_data_for_view(view), "%s\\s*(st|sublime): " % re.escape("#")) # `#` is the default comment start (set in the parser).
		
		view.meta_info = Mock(return_value=None)
		self.assertEqual(parser.parser_data_for_view(view), "%s\\s*(st|sublime): " % re.escape("#")) # `#` is the default comment start (set in the parser).
	
	def test_simple_case(self):
		self.__test_parsing(
			"#",
			"# sublime: setting1 key1",
			Modeline([
				ModelineInstruction_SetViewSetting("setting1", "key1"),
			])
		)
	
	def test_two_settings(self):
		self.__test_parsing(
			";",
			"; sublime: setting1 key1; setting2 key2",
			Modeline([
				ModelineInstruction_SetViewSetting("setting1", "key1"),
				ModelineInstruction_SetViewSetting("setting2", "key2"),
			])
		)
	
	def test_weird_chars(self):
		self.__test_parsing(
			"dnl",
			'dnl st: setting1 key1; setting2 key2  ; 	setting3   key;3;  setting4  " key4"',
			Modeline([
				ModelineInstruction_SetViewSetting("setting1", "key1"),
				ModelineInstruction_SetViewSetting("setting2", "key2"),
				ModelineInstruction_SetViewSetting("setting3", "key;3"),
				ModelineInstruction_SetViewSetting("setting4", " key4"),
			])
		)
	
	
	def __test_parsing(self, comment_char: str, line: str, expected: Modeline):
		view = Mock()
		parser = ModelineParser_Legacy()
		view.meta_info = Mock(return_value=[{"name": "TM_COMMENT_START", "value": comment_char}])
		#print(parser.parse_line(line, parser.parser_data_for_view(view)))
		self.assertEqual(parser.parse_line(line, parser.parser_data_for_view(view)), expected)

# Note: We don’t do another integration test as we have done it in the Sublime parser test (and the legacy+vim one).
