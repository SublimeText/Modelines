from abc import ABC, abstractmethod

import sublime



class ModelineInstruction(ABC):
	
	@abstractmethod
	def apply(self, view: sublime.View) -> None:
		pass
