# This can be removed when using Python >= 3.10.
from typing import List

from .modeline_instruction import ModelineInstruction



class Modeline:
	
	instructions: List[ModelineInstruction]
	
	def __init__(self):
		super().__init__()
