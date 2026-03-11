from typing import cast, Any, Optional

from unittest import TestCase
from unittest.mock import Mock

from sublime import View as SublimeView
from sublime import Window as SublimeWindow
from unittesting import DeferrableTestCase
import sublime

from ..app.modeline import Modeline
from ..app.modeline_instruction import ModelineInstruction
from ..app.modeline_instructions.set_view_setting import ModelineInstruction_SetViewSetting
from ..app.modeline_instructions_mapping import ModelineInstructionsMapping
from ..app.modeline_parsers.legacy_vim import ModelineParser_LegacyVIM
from ..plugin import do_modelines



class LegacyVIMModelineParsingTest(TestCase):
	
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
	
	def test_parsing_legacy_compatibility(self):
		# Note: The original test was more interesting.
		# It parsed multiple lines at once and verified the resulting instructions contained all of the instructions from all of the lines.
		# We have strayed too far from the original implementation for the test to make sense, so we do this middle ground instead.
		# We could also remove the test completely, I guess…
		for l, r in [
			("# sublime: foo bar",          Modeline([ModelineInstruction_SetViewSetting("foo",  "bar")])),
			("# sublime: bar foo; foo bar", Modeline([ModelineInstruction_SetViewSetting("bar",  "foo"), ModelineInstruction_SetViewSetting("foo", "bar")])),
			("# st: baz foob",              Modeline([ModelineInstruction_SetViewSetting("baz",  "foob")])),
			("# st: fibz zap; zup blah",    Modeline([ModelineInstruction_SetViewSetting("fibz", "zap"), ModelineInstruction_SetViewSetting("zup", "blah")])),
		]:
			self.__test_parsing("#", l, r)
	
	
	def __test_parsing(self, comment_char: str, line: str, expected: Modeline):
		parser = ModelineParser_LegacyVIM(ModelineInstructionsMapping())
		self.assertEqual(parser.parse_line(line, comment_char), expected)


class LegacyVIMModelineIntegrationTest(DeferrableTestCase):
	
	view: SublimeView
	window: SublimeWindow
	
	def setUp(self):
		# Make sure we have a window to work with.
		s = sublime.load_settings("Preferences.sublime-settings")
		s.set("close_windows_when_empty", False)
		
		# Set some plugin settings we require for the tests.
		s = sublime.load_settings("Sublime Modelines.sublime-settings")
		s.set("formats", ["classic+vim"])
		s.set("number_of_lines_to_check_from_beginning", 3)
		s.set("number_of_lines_to_check_from_end", 3)
		s.set("verbose", True)
		
		self.window = sublime.active_window()
		self.view = self.window.new_file()
		while self.view.is_loading():
			yield
	
	def tearDown(self):
		if self.view:
			self.view.set_scratch(True)
			self.window.focus_view(self.view)
			self.window.run_command("close_file")
	
	def test_modelines_1(self):
		self.view.run_command("insert", {"characters": "# sublime:noet:ai:ts=3:\n"})
		self.window.run_command("sublime_modelines_apply")
		self.assertEqual(self.view.settings().get("tab_size"), 3)
		self.assertEqual(self.view.settings().get("auto_indent"), True)
		self.assertEqual(self.view.settings().get("translate_tabs_to_spaces"), False)
		
		self.view.run_command("insert", {"characters": "# vim: ts=7:noai:et:\n"})
		self.window.run_command("sublime_modelines_apply")
		self.assertEqual(self.view.settings().get("tab_size"), 7)
		self.assertEqual(self.view.settings().get("auto_indent"), False)
		self.assertEqual(self.view.settings().get("translate_tabs_to_spaces"), True)
	
	def test_modelines_2(self):
		self.view.run_command("insert", {"characters": "# sublime:noet:ai:ts=3:\n"})
		self.window.run_command("sublime_modelines_apply")
		self.assertEqual(self.view.settings().get("tab_size"), 3)
		self.assertEqual(self.view.settings().get("auto_indent"), True)
		self.assertEqual(self.view.settings().get("translate_tabs_to_spaces"), False)
		
		self.view.run_command("insert", {"characters": "// vim: ts=7:noai:et:\n"})
		self.window.run_command("sublime_modelines_apply")
		self.assertEqual(self.view.settings().get("tab_size"), 3)
		self.assertEqual(self.view.settings().get("auto_indent"), True)
		self.assertEqual(self.view.settings().get("translate_tabs_to_spaces"), False)
		
		self.view.meta_info = Mock(return_value=[{"name": "TM_COMMENT_START", "value": "//"}])
		self.assertEqual(self.__find_comment_start(), "//")
		# Call `do_modelines` directly instead of running the `sublime_modelines_apply` command.
		# `do_modelines` is the underlying function that is called when running the command,
		#  however we need to pass our mocked view in order for the comment change to work.
		# I tried changing the comment start another way, but that does not seem possible.
		# Here’s a guy asking for something related <https://forum.sublimetext.com/t/7178>.
		do_modelines(self.view)
		self.assertEqual(self.view.settings().get("tab_size"), 7)
		self.assertEqual(self.view.settings().get("auto_indent"), False)
		self.assertEqual(self.view.settings().get("translate_tabs_to_spaces"), True)
	
	
	def __find_comment_start(self) -> Optional[str]:
		commentChar = ""
		try:
			for pair in cast(Any, self.view.meta_info("shellVariables", 0)):
				if pair["name"] == "TM_COMMENT_START":
					commentChar = pair["value"]
				if commentChar:
					break
		except TypeError:
			pass
		
		return commentChar
