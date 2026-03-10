# This can be removed when using Python >= 3.10.
from typing import List

from .modeline_instruction import ModelineInstruction



class Modeline:
	
	instructions: List[ModelineInstruction]
	
	def __init__(self, instructions: List[ModelineInstruction] = []):
		super().__init__()
		# We copy the list because otherwise the _default argument_ can get modified…
		self.instructions = instructions.copy()
	
	
	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Modeline):
			return False
		print(len(self.instructions))
		print(len(other.instructions))
		return (self.instructions == other.instructions)
	
	def __str__(self) -> str:
		# There is probably a more Pythonic way of doing this (map + join?), but this works.
		res = "Modeline:\n"
		for i in self.instructions:
			res += "   - " + i.__str__()
			res += "\n"
		return res
