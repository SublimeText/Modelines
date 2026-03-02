from abc import ABC, abstractmethod



class ModelineInstruction(ABC):
	
	@abstractmethod
	def apply(self) -> None:
		pass
