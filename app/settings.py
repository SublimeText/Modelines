from enum import Enum
import sublime

from .logger import Logger



class ModelineFormat(str, Enum):
	CLASSIC   = "classic"
	DELIMITED = "delimited"


class Settings:
	"""
	A class that gives convenient access to the settings for our plugin.
	
	Creating an instance of this class will load the settings.
	"""
	
	def __init__(self):
		super().__init__()
		self.settings = sublime.load_settings("Sublime Modelines.sublime-settings")
	
	def modelines_formats(self):
		default_for_syntax_error = [ModelineFormat.CLASSIC]
		
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
