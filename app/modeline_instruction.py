from abc import ABC, abstractmethod

from enum import Enum
from sublime import View as SublimeView
from sublime_types import Value as SublimeValue



class ModelineInstruction(ABC):
	
	class ValueModifier(str, Enum):
		NONE   = ""
		ADD    = "+"
		REMOVE = "-"
	
	@abstractmethod
	def __init__(self, key: str, value: SublimeValue, modifier: ValueModifier = ValueModifier.NONE) -> None:
		pass
	
	@abstractmethod
	def apply(self, view: SublimeView) -> None:
		pass
