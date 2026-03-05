from typing import final, List, Optional, Tuple

from ..modeline_instruction import ModelineInstruction
from ..modeline_parser import ModelineParser



@final
class ModelineParser_Sublime(ModelineParser):
	
	def parse_line_raw(self, line: str) -> Optional[List[Tuple[str, Optional[str], ModelineInstruction.ValueModifier]]]:
		raise Exception("Not Implemented")
	
	
	def transform_key_postmapping(self, key: str) -> str:
		return super().transform_key_postmapping(key)
