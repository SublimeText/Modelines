# This can be removed when using Python >= 3.10 (for List at least; the rest idk).
from typing import final, List, Optional, Tuple

from abc import ABC, abstractmethod
from enum import Enum
import json

from .modeline import Modeline
from .modeline_instructions_mapping import ModelineInstructionsMapping
from .utils import Utils



class ModelineParser(ABC):
	
	class ValueModifier(str, Enum):
		NONE   = ""
		ADD    = "+"
		REMOVE = "-"
	
	def __init__(self):
		super().__init__()
	
	# Concrete sub-classes should set the value of this variable if they have a custom mapping (e.g. for the vim format, “filetype” -> “x_syntax”).
	mapping = ModelineInstructionsMapping()
	
	@final
	def parse_line(self, line: str) -> Optional[Modeline]:
		instructions = self.parse_line_raw(line)
		if instructions is None:
			return None
		
		for key, value, modifier in instructions:
			# Let’s parse the value.
			# See the Sublime settings file for the rules (and update it if they change).
			if not value is None:
				if   j:= self.__parse_jsonesque_str(value): value = j
				elif value == "true":                       value = True
				elif value == "false":                      value = False
				elif i := Utils.as_int_or_none  (value):    value = i
				elif f := Utils.as_float_or_none(value):    value = f
				elif value == "null":                       value = None
			
			# Apply the mapping to the key and value.
			key_value = self.mapping.apply(key, value)
			if key_value is None: return None # Unsupported key
			(key, value) = key_value
			
			# Apply the post-mapping transform on the key.
			key = self.transform_key_post_mapping(key)
	
	@abstractmethod
	def parse_line_raw(self, line: str) -> Optional[List[Tuple[str, Optional[str], ValueModifier]]]:
		"""
		Abstract method whose concrete implementation should parse the given line as a dictionary of key/values if the line is a modeline.
		No parsing of any sort should be done on the key or value, including mappings; this will be handled by the `parse` function (which calls that function).
		"""
		pass
	
	def transform_key_post_mapping(self, key: str) -> str:
		"""
		Gives an opportunity to concrete sub-classes to post-process the key after the mapping has been applied.
		This is used for instance by the VIM modeline parser class to implement Sublime commands with a prefix.
		"""
		return key
	
	
	# Parse strings that starts with either a double-quote (`"`), a brace (`{`) or a bracket (`[`) as a JSON string.
	def __parse_jsonesque_str(self, str: str) -> Optional[object]:
		if not str.startswith('"') and not str.startswith('{') and not str.startswith('['):
			return None
		
		try:                                 return json.loads(str)
		except json.decoder.JSONDecodeError: return None
