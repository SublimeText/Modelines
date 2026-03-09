from typing import final, List, Optional, Tuple

import re

from ..modeline_instruction import ModelineInstruction
from ..modeline_instructions_mapping import ModelineInstructionsMapping
from ..modeline_parser import ModelineParser



@final
class ModelineParser_Emacs(ModelineParser):
	
	def __init__(self, mapping: ModelineInstructionsMapping):
		super().__init__()
		self.mapping = mapping
	
	
	def parse_line_raw(self, line: str, parser_data: object) -> Optional[List[Tuple[str, Optional[str], ModelineInstruction.ValueModifier]]]:
		# From <https://github.com/kvs/STEmacsModelines/blob/0a5487831c6ee5cedb924be4f1c64aa7651a3464/EmacsModelines.py#L98-L135>.
		# We probably should rewrite this properly though…
		m = re.match(self.__modeline_re, line)
		if not m: return None
		
		res: List[Tuple[str, Optional[str], ModelineInstruction.ValueModifier]] = []
		
		modeline = m.group(1) # Original implementation had a lowercase here. It does not make sense though.
		for opt in modeline.split(";"):
			opt = opt.strip()
			if len(opt) == 0: continue
			
			opts = re.match(r"\s*(st-|sublime-text-|sublime-|sublimetext-)?(.+):\s*(.+)\s*", opt)
			if opts:
				key, value = (self.__sublime_prefix if opts.group(1) else "") + opts.group(2), opts.group(3)
				res.append((key, value, ModelineInstruction.ValueModifier.NONE))
			else:
				# Not a `key: value`-pair: we assume it’s a syntax-name.
				res.append(("syntax", opt.strip(), ModelineInstruction.ValueModifier.NONE))
		
		return res
	
	
	def transform_key_postmapping(self, key: str, parser_data: object) -> str:
		transformed = super().transform_key_postmapping(key, parser_data)
		if transformed.startswith(self.__sublime_prefix):
			transformed = transformed[len(self.__sublime_prefix):]
		return transformed
	
	
	__modeline_re = r".*-\*-\s*(.+?)\s*-\*-.*"
	__sublime_prefix = "sublimetext--"
