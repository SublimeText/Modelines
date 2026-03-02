# This can be removed when using Python >= 3.10 (for List at least; the rest idk).
from typing import final, Dict, Optional

from abc import ABC, abstractmethod

from .modeline import Modeline
from .modeline_instructions_mapping import ModelineInstructionsMapping



class ModelineParser(ABC):
	
	def __init__(self):
		super().__init__()
	
	# Concrete sub-classes should set the value of this variable if they have a custom mapping (e.g. for the vim format, “filetype” -> “x_syntax”).
	mapping = ModelineInstructionsMapping()
	
	@final
	def parse(self, line: str) -> Optional[Modeline]:
		instructions = self.parseRaw(line)
		if instructions is None:
			return None
		
		for key, val in instructions.items():
			
			raise RuntimeError("Not Implemented")
	
	@abstractmethod
	def parseRaw(self, line: str) -> Optional[Dict[str, str]]:
		"""
		Abstract method whose concrete implementation should parse the given line as a dictionary of key/values if the line is a modeline.
		No parsing of any sort should be done on the key or value, including mappings; this will be handled by the `parse` function (which calls that function).
		"""
		pass
