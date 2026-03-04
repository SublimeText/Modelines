from typing import final

from sublime import View as SublimeView
from sublime_types import Value as SublimeValue

from ..modeline_instruction import ModelineInstruction



@final
class ModelineInstruction_SetViewSetting(ModelineInstruction):
	
	setting_name: str
	setting_value: SublimeValue
	setting_modifier: ModelineInstruction.ValueModifier
	
	def __init__(self, key: str, value: SublimeValue, modifier: ModelineInstruction.ValueModifier) -> None:
		super().__init__(key, value, modifier)
		self.setting_name = key
		self.setting_value = value
		self.setting_modifier = modifier
	
	def apply(self, view: SublimeView) -> None:
		view.settings().set(self.setting_name, self.setting_value)
