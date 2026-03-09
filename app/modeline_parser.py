# This can be removed when using Python >= 3.10 (for List at least; the rest idk).
from typing import final, List, Optional, Tuple

from abc import ABC, abstractmethod
import json

from .logger import Logger
from .modeline import Modeline
from .modeline_instruction import ModelineInstruction
from .modeline_instructions.set_view_setting import ModelineInstruction_SetViewSetting
from .modeline_instructions.call_view_function import ModelineInstruction_CallViewFunction
from .modeline_instructions_mapping import ModelineInstructionsMapping
from .utils import Utils



class ModelineParser(ABC):
	
	def __init__(self):
		super().__init__()
	
	# Concrete sub-classes should set the value of this variable if they have a custom mapping (e.g. for the vim format, “filetype” -> “x_syntax”).
	mapping = ModelineInstructionsMapping()
	
	@final
	def parse_line(self, line: str) -> Optional[Modeline]:
		instructions_raw: Optional[List[Tuple[str, Optional[str], ModelineInstruction.ValueModifier]]]
		try:
			instructions_raw = self.parse_line_raw(line)
			if instructions_raw is None:
				return None
		except Exception as e:
			Logger.warning(f"Got an exception while parsing raw modeline instructions from a line. This is an error in the concrete subclass: it should return None instead. -- line=“{line}”, error=“{e}”")
			return None
		
		res = Modeline()
		for key, raw_value, modifier in instructions_raw:
			try:
				# Let’s parse the value.
				# It should already be trimmed (`parse_line_raw` should do it).
				# See the Sublime settings file for the rules (and update it if they change).
				if not raw_value is None:
					if   j := self.__parse_jsonesque_str(raw_value): value = j
					elif raw_value == "true":                        value = True
					elif raw_value == "false":                       value = False
					elif i := Utils.as_int_or_none  (raw_value):     value = i
					elif f := Utils.as_float_or_none(raw_value):     value = f
					elif raw_value == "null":                        value = None
					else:                                            value = raw_value
				else:
					value = None # aka. raw_value
				
				# Apply the mapping to the key and value.
				key_value_pair = self.mapping.apply(key, value)
				if key_value_pair is None: continue # Unsupported key
				(key, value) = key_value_pair
				
				# Apply the post-mapping transform on the key.
				key = self.transform_key_postmapping(key)
				sublime_value = Utils.checked_cast_to_sublime_value(
					value,
					ValueError("Post-mapped value is invalid (not a SublimeValue).")
				)
				
				if key.endswith("()"): res.instructions.append(ModelineInstruction_CallViewFunction(key[:-2], sublime_value, modifier))
				else:                  res.instructions.append(ModelineInstruction_SetViewSetting  (key,      sublime_value, modifier))
			except Exception as e:
				Logger.warning(f"Failed converting modeline raw instruction to structured instruction. -- key=“{key}”, raw_value=“{raw_value}”, modifier=“{modifier}”, error=“{e}”")
		return res
	
	@abstractmethod
	def parse_line_raw(self, line: str) -> Optional[List[Tuple[str, Optional[str], ModelineInstruction.ValueModifier]]]:
		"""
		Abstract method whose concrete implementation should parse the given line as a dictionary of key/values if the line is a modeline.
		No parsing of any sort should be done on the key or value, including mappings; this will be handled by the `parse` function (which calls that function).
		If applicable, trimming should be done by this function though.
		"""
		pass
	
	def transform_key_postmapping(self, key: str) -> str:
		"""
		Gives an opportunity to concrete sub-classes to post-process the key after the mapping has been applied.
		This is used for instance by the VIM modeline parser class to implement Sublime commands with a prefix, bypassing the mapping.
		In practice this is very much useless and only there for full backward compatibility.
		"""
		return key
	
	
	# Parse strings that starts with either a double-quote (`"`), a brace (`{`) or a bracket (`[`) as a JSON string.
	@final
	def __parse_jsonesque_str(self, str: str) -> object:
		if not str.startswith('"') and not str.startswith('{') and not str.startswith('['):
			return None
		
		try:                                 return json.loads(str)
		except json.decoder.JSONDecodeError: return None
