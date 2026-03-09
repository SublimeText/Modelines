from typing import final, List, Optional, Tuple

from sublime import View as SublimeView

from ..modeline_instruction import ModelineInstruction
from ..modeline_parser import ModelineParser



@final
class ModelineParser_LegacyVIM(ModelineParser):
	
	def parse_line_raw(self, line: str, view: SublimeView) -> Optional[List[Tuple[str, Optional[str], ModelineInstruction.ValueModifier]]]:
		raise Exception("Not Implemented")
	
	
	def transform_key_postmapping(self, key: str, view: SublimeView) -> str:
		return super().transform_key_postmapping(key, view)
