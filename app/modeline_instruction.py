from abc import ABC, abstractmethod

from enum import Enum
import sublime



class ModelineInstruction(ABC):
	
	class ValueModifier(str, Enum):
		NONE   = ""
		ADD    = "+"
		REMOVE = "-"
	
	@abstractmethod
	def apply(self, view: sublime.View) -> None:
		pass
