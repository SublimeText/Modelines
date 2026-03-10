# This can be removed when using Python >= 3.10.
from typing import List

from .modeline_instruction import ModelineInstruction



class Modeline:
	
	instructions: List[ModelineInstruction]
	
	def __init__(self, instructions: List[ModelineInstruction] = []):
		super().__init__()
		# We copy the list because otherwise the _default argument_ can get modified…
		self.instructions = instructions.copy()
