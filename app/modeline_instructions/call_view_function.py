from typing import final

from sublime import View as SublimeView
from sublime_types import Value as SublimeValue

from ..modeline_instruction import ModelineInstruction



@final
class ModelineInstruction_CallViewFunction(ModelineInstruction):
	
	function_name: str
	function_arg: SublimeValue
	
	def __init__(self, key: str, value: SublimeValue, modifier: ModelineInstruction.ValueModifier = ModelineInstruction.ValueModifier.NONE) -> None:
		super().__init__(key, value, modifier)
		
		if modifier != ModelineInstruction.ValueModifier.NONE:
			raise ValueError(f"Unsupported value modifier “{modifier}” for a call view function modeline instruction.")
		
		self.function_name = key
		self.function_arg  = value
	
	def apply(self, view: SublimeView) -> None:
		f = getattr(view, self.function_name)
		f(self.function_arg)
	
	
	def __str__(self) -> str:
		return f"ModelineInstruction: CallViewFunction: {self.function_name}()={self.function_arg}"
