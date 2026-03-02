# This can be removed when using Python >= 3.10.
from typing import List

from enum import Enum
import sublime

from .logger import Logger



class ModelineFormat(str, Enum):
	DEFAULT = "default"
	LEGACY  = "classic"
	VIM     = "vim"
	EMACS   = "emacs"


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
	
	
	def __settings_getdict(self, key: str) -> Optional[Dict[str, object]]:
		"""
		Get the dictionary value for the setting for the given key, if it is dict like.
		The whole thing is probably slow af but I don’t know how to do better, nor do I really care tbh.
		"""
		setting_value = self.settings.get(key)
		
		# Check if value is dict-like (has “items” function).
		# From <https://stackoverflow.com/a/5268474>.
		items_attr = getattr(setting_value, "items", None)
		if not callable(items_attr):
			return None
		
		ret: Dict[str, object] = {}
		for k, v in cast(Dict[str, object], setting_value).items():
			ret[k] = v
