from unittest import TestCase

from ..app.modeline import Modeline
from ..app.modeline_instructions.set_view_setting import ModelineInstruction_SetViewSetting
from ..app.modeline_instructions_mapping import ModelineInstructionsMapping
from ..app.modeline_parsers.emacs import ModelineParser_Emacs



class VIMModelineParsingTests(TestCase):
	
	def test_simple_case(self):
		self.__test_parsing(
			"# -*- setting1:key1 -*-",
			Modeline([
				ModelineInstruction_SetViewSetting("setting1", "key1"),
			])
		)
	
	def test_two_settings(self):
		self.__test_parsing(
			"/* -*- setting1:key1; setting2 -*- */",
			Modeline([
				ModelineInstruction_SetViewSetting("setting1", "key1"),
				ModelineInstruction_SetViewSetting("syntax", "setting2"),
			])
		)
	
	def test_weird_chars(self):
		self.__test_parsing(
			'dnl -*-setting1:key1; setting2:key2  ; 	 setting3:key3;;;  setting4:" key4"-*-',
			Modeline([
				ModelineInstruction_SetViewSetting("setting1", "key1"),
				ModelineInstruction_SetViewSetting("setting2", "key2"),
				ModelineInstruction_SetViewSetting("setting3", "key3"),
				ModelineInstruction_SetViewSetting("setting4", " key4"),
			])
		)
	
	
	def __test_parsing(self, line: str, expected: Modeline):
		parser = ModelineParser_Emacs(ModelineInstructionsMapping())
		print(parser.parse_line(line, None))
		self.assertEqual(parser.parse_line(line, None), expected)

# Note: We don’t do another integration test as we have done it in the Sublime parser test (and the legacy+vim one).
