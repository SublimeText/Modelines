from typing import final

from sublime import View as SublimeView
from sublime_types import Value as SublimeValue

from ..modeline_instruction import ModelineInstruction



@final
class ModelineInstruction_CallViewFunction(ModelineInstruction):
	
	function_name: str
	function_arg: SublimeValue
	
	def __init__(self, function_name: str, function_arg: SublimeValue) -> None:
		super().__init__()
		self.function_name = function_name
		self.function_arg  = function_arg
	
	def apply(self, view: SublimeView) -> None:
		f = getattr(view, self.function_name)
		f(self.function_arg)
