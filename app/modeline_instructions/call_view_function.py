from typing import Final, FrozenSet, final

from sublime import View as SublimeView
from sublime_types import Value as SublimeValue

from ..modeline_instruction import ModelineInstruction



# Modeline content comes from the file being opened, so the function name in “name()=argument” is attacker-controlled:
#  an unbounded getattr() over the view exposes every method, including run_command(), which runs an arbitrary command.
# Only the methods a modeline has a reason to call are allowed, and all of them change the buffer’s own state and nothing else.
ALLOWED_VIEW_FUNCTIONS: Final[FrozenSet[str]] = frozenset({
	"set_encoding",
	"set_line_endings",
	"set_name",
	"set_read_only",
	"set_scratch",
	"set_syntax_file",
})


@final
class ModelineInstruction_CallViewFunction(ModelineInstruction):
	
	def __init__(self, key: str, value: SublimeValue, modifier: ModelineInstruction.ValueModifier = ModelineInstruction.ValueModifier.NONE) -> None:
		super().__init__(key, value, modifier)
		
		if modifier != ModelineInstruction.ValueModifier.NONE:
			raise ValueError(f"Unsupported value modifier “{modifier}” for a call view function modeline instruction.")
		
		self.function_name = key
		self.function_arg  = value
	
	def apply(self, view: SublimeView) -> None:
		if self.function_name not in ALLOWED_VIEW_FUNCTIONS:
			raise ValueError(f"Refusing to call view function “{self.function_name}”: it is not in the allowlist ({', '.join(sorted(ALLOWED_VIEW_FUNCTIONS))}).")
		f = getattr(view, self.function_name)
		f(self.function_arg)
	
	
	def __eq__(self, other: object):
		if not isinstance(other, ModelineInstruction_CallViewFunction):
			return False
		return (self.function_name == other.function_name and
				  self.function_arg  == other.function_arg)
	
	def __str__(self) -> str:
		return f"ModelineInstruction: CallViewFunction: {self.function_name}()={self.function_arg}"
