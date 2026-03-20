from typing import final

from os import path
from sublime import View as SublimeView
from sublime_types import Value as SublimeValue
import sublime

from ..logger import Logger
from ..modeline_instruction import ModelineInstruction



@final
class ModelineInstruction_SetViewSetting(ModelineInstruction):
	
	def __init__(self, key: str, value: SublimeValue, modifier: ModelineInstruction.ValueModifier = ModelineInstruction.ValueModifier.NONE) -> None:
		super().__init__(key, value, modifier)
		self.setting_name = key
		self.setting_value = value
		self.setting_modifier = modifier
	
	def apply(self, view: SublimeView) -> None:
		settings = view.settings()
		
		# Process setting value for special `syntax` case.
		# Note <https://github.com/kvs/STEmacsModelines/blob/0a5487831c6ee5cedb924be4f1c64aa7651a3464/EmacsModelines.py#L40> might be a better algorithm.
		# Among other things, it allows users to have a custom mapping of syntaxes, which we don’t.
		if (self.setting_name == "syntax" and
			 isinstance(self.setting_value, str) and
			 not self.setting_value.endswith("tmLanguage") and
			 not self.setting_value.endswith("sublime-syntax") and
			 not "/" in self.setting_value and
			 hasattr(sublime, "find_resources")
			):
			# We modify the value to find the proper file (this avoids specifying `Swift.tmLanguage`; instead we can use `Swift`).
			# TODO: Case-insensitive search.
			candidates = sublime.find_resources(f"{self.setting_value}.sublime-syntax") + sublime.find_resources(f"{self.setting_value}.tmLanguage")
			if len(candidates) > 0:
				# Note: We only use the basename of the found resource.
				# For some (unknown) reason, using the full path and the basename does not yield the same results,
				#  even when there is only one possible alternative!
				self.setting_value = path.basename(path.normpath(candidates[0]))
		
		new_setting_value: SublimeValue
		# The “match” instruction has been added to Python 3.10.
		# We use `if elif else` instead.
		if self.setting_modifier == ModelineInstruction.ValueModifier.NONE:
			new_setting_value = self.setting_value
			
		elif self.setting_modifier == ModelineInstruction.ValueModifier.ADD:
			# We’re told to add the given value(s) to the current value.
			# We can do this only if the current value is a list.
			# (Technically we could probably imagine rules for strings, dictionaries, etc., but they would be a stretch; let’s stay simple.)
			current_value = settings.get(self.setting_name, [])
			if isinstance(current_value, list):
				if isinstance(self.setting_value, list): new_setting_value = current_value +  self.setting_value
				else:                                    new_setting_value = current_value + [self.setting_value]
			else:
				# If the current value is not a known type, we fail.
				# Note current_value should never be None as we ask for an empty list for the default value.
				raise ValueError("Cannot add value to a non list setting.")
			
		elif self.setting_modifier == ModelineInstruction.ValueModifier.REMOVE:
			# We’re told to remove the given value(s) to the current value.
			# We can do this only if the current value is a list.
			# (Technically we could probably imagine rules for strings, dictionaries, etc., but they would be a stretch; let’s stay simple.)
			current_value = settings.get(self.setting_name)
			if current_value is None:
				new_setting_value = None
			elif isinstance(current_value, list):
				if isinstance(self.setting_value, list): new_setting_value = [v for v in current_value if not v in self.setting_value]
				else:                                    new_setting_value = [v for v in current_value if not v == self.setting_value]
			else:
				# If the current value is not a known type, we fail.
				raise ValueError("Cannot remove value to a non list setting.")
			
		else:
			Logger.error(f"Unknown setting modifier “{self.setting_modifier}” when applying a `SetViewSetting` modeline instruction.")
			raise Exception("Unknown setting modifier.")
		
		settings.set(self.setting_name, new_setting_value)
	
	
	def __eq__(self, other: object):
		if not isinstance(other, ModelineInstruction_SetViewSetting):
			return False
		return (self.setting_name     == other.setting_name     and
				  self.setting_value    == other.setting_value    and
				  self.setting_modifier == other.setting_modifier)
	
	def __str__(self) -> str:
		return f"ModelineInstruction: SetViewSetting: {self.setting_name}{self.setting_modifier}={self.setting_value}"
