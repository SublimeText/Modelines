# This is the test file that was added with ST3+vim compatibility (heavily edited).
from tempfile import mkstemp
from unittest import TestCase
import sublime, os, sys

from ..app.modeline import Modeline
from ..app.modeline_instruction import ModelineInstruction
from ..app.modeline_instructions.set_view_setting import ModelineInstruction_SetViewSetting
from ..app.modeline_instructions_mapping import ModelineInstructionsMapping
from ..app.modeline_parsers.legacy_vim import ModelineParser_LegacyVIM



class ModelinesTest(TestCase):
	
	def tearDown(self):
		if hasattr(self, "tempfile"):
			if os.path.exists(self.tempfile):
				os.remove(self.tempfile)
	
	def _modeline_test(self, lines):
		fd, self.tempfile = mkstemp()
		os.write(fd, lines)
		os.close(fd)
		
		view = sublime.active_window().open_file(self.tempfile)
		
		while view.is_loading():
			yield
		
		# here test view’s settings
		
		# in the end remove tempfile
	
	#def test_modelines_1(self):
	#	lines = ("# sublime:et:ai:ts=4:\n")
	#	self._modeline_test(lines)
	
	def test_parsing_vim_compatibility_1(self):
		self.__test_parsing(
			"#",
			"# vim: set ai noet ts=4:", 
			Modeline([
				ModelineInstruction_SetViewSetting("ai",   True),
				ModelineInstruction_SetViewSetting("noet", True),
				ModelineInstruction_SetViewSetting("ts",   4),
			])
		)
	
	def test_parsing_vim_compatibility_2(self):
		self.__test_parsing(
			"#",
			"# vim:ai:et:ts=4:", 
			Modeline([
				ModelineInstruction_SetViewSetting("ai", True),
				ModelineInstruction_SetViewSetting("et", True),
				ModelineInstruction_SetViewSetting("ts", 4),
			])
		)
	
	def test_parsing_vim_compatibility_3(self):
		self.__test_parsing(
			"#",
			'# sublime:ai:et:ts=4:ignored_packages+="Makefile Improved":',
			Modeline([
				ModelineInstruction_SetViewSetting("ai",               True),
				ModelineInstruction_SetViewSetting("et",               True),
				ModelineInstruction_SetViewSetting("ts",               4),
				ModelineInstruction_SetViewSetting("ignored_packages", "Makefile Improved", ModelineInstruction.ValueModifier.ADD),
			])
		)
	
	def test_parsing_vim_compatibility_4(self):
		self.__test_parsing(
			"#",
			'# sublime:ai:et:ts=4:ignored_packages+=["Makefile Improved", "Vintage"]:',
			Modeline([
				ModelineInstruction_SetViewSetting("ai",               True),
				ModelineInstruction_SetViewSetting("et",               True),
				ModelineInstruction_SetViewSetting("ts",               4),
				ModelineInstruction_SetViewSetting("ignored_packages", ["Makefile Improved", "Vintage"], ModelineInstruction.ValueModifier.ADD),
			])
		)
	
	def test_parsing_vim_compatibility_5(self):
		self.__test_parsing(
			"#",
			'# sublime: set color_scheme="Packages/Color Scheme - Default/Monokai.tmTheme":',
			Modeline([ModelineInstruction_SetViewSetting("color_scheme", "Packages/Color Scheme - Default/Monokai.tmTheme")])
		)
	
	#def test_parsing(self):
	#	mdls = [
	#		"# sublime: foo bar",
	#		"# sublime: bar foo; foo bar",
	#		"# st: baz foob",
	#		"# st: fibz zap; zup blah",
	#	]
	#	actual = [
	#		"foo bar",
	#		"bar foo",
	#		"foo bar",
	#		"baz foob",
	#		"fibz zap",
	#		"zup blah",
	#	]
	#	self.__test_parsing(mdls, actual)
	
	
	def __test_parsing(self, comment_char: str, line: str, expected: Modeline):
		parser = ModelineParser_LegacyVIM(ModelineInstructionsMapping())
		self.assertEqual(parser.parse_line(line, comment_char), expected)
