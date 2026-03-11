from unittest import TestCase

from sublime import View as SublimeView
from sublime import Window as SublimeWindow
from unittesting import DeferrableTestCase
import sublime

from ..app.modeline import Modeline
from ..app.modeline_instruction import ModelineInstruction
from ..app.modeline_instructions.set_view_setting import ModelineInstruction_SetViewSetting
from ..app.modeline_parsers.sublime import ModelineParser_Sublime
from ..plugin import do_modelines



class SublimeModelineParsingTest(TestCase):
	
	def test_simple_case(self):
		self.__test_parsing(
			"# ~*~ sublime: setting1=key1 ~*~",
			Modeline([
				ModelineInstruction_SetViewSetting("setting1", "key1"),
			])
		)
	
	def test_two_settings(self):
		self.__test_parsing(
			"# ~*~ sublime: setting1=key1; setting2=key2 ~*~",
			Modeline([
				ModelineInstruction_SetViewSetting("setting1", "key1"),
				ModelineInstruction_SetViewSetting("setting2", "key2"),
			])
		)
	
	def test_weird_chars(self):
		self.__test_parsing(
			'# ~*~ sublime: setting1=key1; setting2=key2  ;	 setting3  =key;;3;  setting4 = " key4" ~*~',
			Modeline([
				ModelineInstruction_SetViewSetting("setting1", "key1"),
				ModelineInstruction_SetViewSetting("setting2", "key2"),
				ModelineInstruction_SetViewSetting("setting3", "key;3"),
				ModelineInstruction_SetViewSetting("setting4", " key4"),
			])
		)
	
	
	def __test_parsing(self, line: str, expected: Modeline):
		parser = ModelineParser_Sublime()
		self.assertEqual(parser.parse_line(line, None), expected)


class SublimeModelineIntegrationTest(DeferrableTestCase):
	
	view: SublimeView
	window: SublimeWindow
	
	def setUp(self):
		# Make sure we have a window to work with.
		s = sublime.load_settings("Preferences.sublime-settings")
		s.set("close_windows_when_empty", False)
		
		# Set some plugin settings we require for the tests.
		s = sublime.load_settings("Sublime Modelines.sublime-settings")
		s.set("formats", ["default"])
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
		self.view.run_command("insert", {"characters": "/* ~*~ sublime: tab_size=7; translate_tabs_to_spaces=true ~*~ */\n"})
		self.window.run_command("sublime_modelines_apply")
		self.assertEqual(self.view.settings().get("tab_size"), 7)
		self.assertEqual(self.view.settings().get("translate_tabs_to_spaces"), True)
		
		self.view.run_command("insert", {"characters": "/* ~*~ sublime: tab_size=3; translate_tabs_to_spaces=false ~*~ */\n"})
		self.window.run_command("sublime_modelines_apply")
		self.assertEqual(self.view.settings().get("tab_size"), 3)
		self.assertEqual(self.view.settings().get("translate_tabs_to_spaces"), False)
