# This can be removed when using Python >= 3.10.
from typing import List, NewType, Tuple

from enum import Enum
import sublime

from .logger import Logger
from .modeline_instructions_mapping import ModelineInstructionsMapping
from .modeline_parser import ModelineParser
from .modeline_parsers.emacs import ModelineParser_Emacs
from .modeline_parsers.legacy import ModelineParser_Legacy
from .modeline_parsers.legacy_vim import ModelineParser_LegacyVIM
from .modeline_parsers.sublime import ModelineParser_Sublime
from .modeline_parsers.vim import ModelineParser_VIM
from .utils import Utils



class ModelineFormat(str, Enum):
	DEFAULT    = "default"
	VIM        = "vim"
	EMACS      = "emacs"
	LEGACY     = "classic"
	LEGACY_VIM = "classic+vim"
	
	# Forward declare Settings because we use it in ModelineFormat (and reciprocally).
	Settings = NewType("Settings", None)
	
	def get_parser_with_data(self, settings: Settings, view: sublime.View) -> Tuple[ModelineParser, object]:
		def add_data(parser: ModelineParser) -> Tuple[ModelineParser, object]:
			return (parser, parser.parser_data_for_view(view))
		# The “match” instruction has been added to Python 3.10.
		# We use `if elif else` instead.
		if   self == ModelineFormat.DEFAULT:    return add_data(ModelineParser_Sublime())
		elif self == ModelineFormat.VIM:        return add_data(ModelineParser_VIM(settings.vimMapping()))
		elif self == ModelineFormat.EMACS:      return add_data(ModelineParser_Emacs(settings.emacsMapping()))
		elif self == ModelineFormat.LEGACY:     return add_data(ModelineParser_Legacy())
		elif self == ModelineFormat.LEGACY_VIM: return add_data(ModelineParser_LegacyVIM(settings.vimMapping()))
		else: raise Exception("Internal error: Unknown parser ID.")


class Settings:
	"""
	A class that gives convenient access to the settings for our plugin.
	
	Creating an instance of this class will load the settings.
	"""
	
	def __init__(self):
		super().__init__()
		self.settings = sublime.load_settings("Sublime Modelines.sublime-settings")
	
	def modelines_formats(self) -> List[ModelineFormat]:
		default_for_syntax_error = [ModelineFormat.DEFAULT]
		
		raw_formats = self.settings.get("formats")
		if not isinstance(raw_formats, list):
			Logger.warning("Did not get an array in the settings for the “formats” key.")
			return default_for_syntax_error
		
		formats = []
		for raw_format in raw_formats:
			if not isinstance(raw_format, str):
				Logger.warning("Found an invalid value (not a string) in the “formats” key. Returning the default modeline formats.")
				return default_for_syntax_error
			
			try:
				formats.append(ModelineFormat(raw_format))
			except ValueError:
				Logger.warning("Found an invalid value (unknown format) in the “formats” key. Skipping this value.")
		
		return formats
	
	def apply_on_load(self) -> bool:
		raw_value = self.settings.get("apply_on_load")
		if not isinstance(raw_value, bool):
			Logger.warning("Did not get a bool in the settings for the apply_on_load key.")
			return False
		return raw_value
	
	def apply_on_save(self) -> bool:
		raw_value = self.settings.get("apply_on_save")
		if not isinstance(raw_value, bool):
			Logger.warning("Did not get a bool in the settings for the apply_on_save key.")
			return False
		return raw_value
	
	def number_of_lines_to_check_from_beginning(self) -> int:
		raw_value = self.settings.get("number_of_lines_to_check_from_beginning")
		if not isinstance(raw_value, int):
			Logger.warning("Did not get an int in the settings for the number_of_lines_to_check_from_beginning key.")
			return 5
		return raw_value
	
	def number_of_lines_to_check_from_end(self) -> int:
		raw_value = self.settings.get("number_of_lines_to_check_from_end")
		if not isinstance(raw_value, int):
			Logger.warning("Did not get an int in the settings for the number_of_lines_to_check_from_end key.")
			return 5
		return raw_value
	
	def vimMapping(self) -> ModelineInstructionsMapping:
		raw_value = Utils.checked_cast_to_dict_with_string_keys(
			self.settings.get("vim_mapping"),
			ValueError("Invalid “vim_mapping” setting value: not a dict with string keys.")
		)
		raw_value_user = Utils.checked_cast_to_dict_with_string_keys(
			self.settings.get("vim_mapping_user"),
			ValueError("Invalid “vim_mapping_user” setting value: not a dict with string keys.")
		)
		raw_value = Utils.checked_cast_to_dict_of_dict_with_string_keys(
			Utils.merge(raw_value, raw_value_user),
			ValueError("Invalid “vim_mapping” or “vim_mapping_user”: the resulting merged dictionary is not a dictionary with string keys of dictionary with string keys.")
		)
		return ModelineInstructionsMapping(raw_value)
	
	def emacsMapping(self) -> ModelineInstructionsMapping:
		raw_value = Utils.checked_cast_to_dict_with_string_keys(
			self.settings.get("emacs_mapping"),
			ValueError("Invalid “emacs_mapping” setting value: not a dict with string keys.")
		)
		raw_value_user = Utils.checked_cast_to_dict_with_string_keys(
			self.settings.get("emacs_mapping_user"),
			ValueError("Invalid “emacs_mapping_user” setting value: not a dict with string keys.")
		)
		raw_value = Utils.checked_cast_to_dict_of_dict_with_string_keys(
			Utils.merge(raw_value, raw_value_user),
			ValueError("Invalid “emacs_mapping” or “emacs_mapping_user”: the resulting merged dictionary is not a dictionary with string keys of dictionary with string keys.")
		)
		return ModelineInstructionsMapping(raw_value)
	
	def verbose(self) -> bool:
		raw_value = self.settings.get("verbose")
		if not isinstance(raw_value, bool):
			Logger.warning("Did not get a bool in the settings for the verbose key.")
			return False
		return raw_value
	
	def log_to_tmp(self) -> bool:
		raw_value = self.settings.get("log_to_tmp")
		if not isinstance(raw_value, bool):
			Logger.warning("Did not get a bool in the settings for the log_to_tmp key.")
			return False
		return raw_value
