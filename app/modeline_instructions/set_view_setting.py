from typing import final

from sublime import View as SublimeView
from sublime_types import Value as SublimeValue

from ..modeline_instruction import ModelineInstruction



@final
class ModelineInstruction_SetViewSetting(ModelineInstruction):
	
	setting_name: str
	setting_value: SublimeValue
	
	def __init__(self, setting_name: str, setting_value: SublimeValue) -> None:
		super().__init__()
		self.setting_name  = setting_name
		self.setting_value = setting_value
	
	def apply(self, view: SublimeView) -> None:
		view.settings().set(self.setting_name, self.setting_value)
