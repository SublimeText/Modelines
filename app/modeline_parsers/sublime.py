from typing import final, List, Optional, Tuple

import re

from ..modeline_instruction import ModelineInstruction
from ..modeline_parser import ModelineParser



@final
class ModelineParser_Sublime(ModelineParser):
	
	def parse_line_raw(self, line: str) -> Optional[List[Tuple[str, Optional[str], ModelineInstruction.ValueModifier]]]:
		# Find the first and last `~*~` tokens in the line, if any.
		start = line.find(self.__token)
		if start == -1: return None
		end = line.rfind(self.__token)
		if end == start: return None
		line = line[start+len(self.__token):end].strip()
		
		# Verify the string between the two tokens starts with `sublime`.
		if not line.startswith(self.__prefix): return None
		line = line[len(self.__prefix):].strip()
		
		if not line.startswith(":"): return None
		line = line[1:].strip()
		
		def find_next_tuple() -> Optional[Tuple[str, Optional[str], ModelineInstruction.ValueModifier]]:
			nonlocal line
			
			if len(line) == 0:
				return None
			
			# Read line until the next `+=`, `-=` or `=`.
			match = self.__re__plus_minus_equal.search(line)
			if match is None:
				key = line; line = ""
				return (key, None, ModelineInstruction.ValueModifier.NONE)
			
			operator = line[match.start():match.end()]
			modifer: ModelineInstruction.ValueModifier
			if   operator ==  "=": modifer = ModelineInstruction.ValueModifier.NONE
			elif operator == "+=": modifer = ModelineInstruction.ValueModifier.ADD
			elif operator == "-=": modifer = ModelineInstruction.ValueModifier.REMOVE
			else: raise Exception("Internal error: Unknown operator.")
			
			key = line[:match.start()]
			line = line[match.end():]
			
			value: str = ""
			while idx := line.find(";") + 1: # +1: If not found, idx will be 0, and thus we will exit the loop.
				idx -= 1
				value += line[:idx]
				line = line[idx+1:]
				if len(line) > 0 and line[0] == ";":
					value += ";"
					line = line[1:]
				else:
					break
			else:
				value += line
				line = ""
			
			return (key, value, modifer)
		
		try:
			res: List[Tuple[str, Optional[str], ModelineInstruction.ValueModifier]] = []
			while tuple := find_next_tuple():
				res.append(tuple)
			return res
		except ValueError:
			return None
	
	def transform_key_postmapping(self, key: str) -> str:
		return super().transform_key_postmapping(key)
	
	__token = "~*~"
	__prefix = "sublime"
	
	__re__plus_minus_equal = re.compile(r"=|\+=|-=")

