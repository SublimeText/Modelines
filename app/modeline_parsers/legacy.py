from typing import final, List, Optional, Tuple

from sublime import View as SublimeView

from ..modeline_instruction import ModelineInstruction
from ..modeline_parser import ModelineParser



@final
class ModelineParser_Legacy(ModelineParser):
	
	def parse_line_raw(self, line: str, parser_data: object) -> Optional[List[Tuple[str, Optional[str], ModelineInstruction.ValueModifier]]]:
		raise Exception("Not Implemented")
	
	def parser_data_for_view(self, view: SublimeView) -> object:
		raise Exception("Not Implemented")
