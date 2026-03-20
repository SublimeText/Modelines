from typing import final, Dict

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
		
		if (self.setting_name == "syntax"):
			# Process setting value for special `syntax` case:
			#  we modify the value to find the proper file (this avoids specifying `Swift.tmLanguage`; instead we can use `Swift`, or even `swift`).
			self.setting_value = self.syntax_for(self.setting_value)
		
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
	
	
	# Initially I was using `find_resources` to find the exact file for a given syntax.
	# The problem with this approach is the search is not case-insensitive (at least on a case-sensitive fs, not sure on a ci one).
	# I then tried to generate a case-insensitive glob to use in `find_resources`.
	# This probably should work, but the documentation of `find_resources` seems to be lying: it does not support actual glob.
	# It supports the `*`, yes, but not `[]`, AFAICT.
	# So we resort to finding *all* the known syntaxes and indexing them on their lowercased base name.
	#
	# For reference here’s the code with the conversion to glob:
	# ```
	# case_insensitive_glob_value_chars = [
	#    c if not c.isalpha() else f"[{c.lower()}{c.upper()}]"
	#    for c in list(glob_escape(self.setting_value))
	# ]
	# case_insensitive_glob_value = "".join(case_insensitive_glob_value_chars)
	# candidates = sublime.find_resources(f"{case_insensitive_glob_value}.sublime-syntax") + sublime.find_resources(f"{case_insensitive_glob_value}.tmLanguage")
	# ```
	__known_syntaxes: Dict[str, str] = {}
	@staticmethod
	def syntax_for(setting_value: SublimeValue) -> SublimeValue:
		if (isinstance(setting_value, str) and
			 not setting_value.endswith("tmLanguage") and
			 not setting_value.endswith("sublime-syntax") and
			 not "/" in setting_value and
			 hasattr(sublime, "find_resources")
			):
			
			# If there is already a value for the given setting, we return it.
			# _Technically_ we should make sure the value still exists, but let’s be optimistic.
			if ret := ModelineInstruction_SetViewSetting.__known_syntaxes.get(setting_value.lower()):
				return ret
			
			# If there are no values for the given settings, we refresh the full known syntaxes dictionary and try again.
			Logger.debug("Re-computing full list of known syntaxes.")
			ModelineInstruction_SetViewSetting.__known_syntaxes = {}
			for s in sublime.find_resources("*.tmLanguage") + sublime.find_resources("*.sublime-syntax"):
				base = path.basename(path.normpath(s))
				ModelineInstruction_SetViewSetting.__known_syntaxes[path.splitext(base)[0].lower()] = base
			
			return ModelineInstruction_SetViewSetting.__known_syntaxes.get(setting_value.lower(), setting_value)
