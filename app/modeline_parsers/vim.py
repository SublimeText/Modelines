from typing import cast, final, List, Optional, Tuple

import re

from ..modeline_instruction import ModelineInstruction
from ..modeline_instructions_mapping import ModelineInstructionsMapping
from ..modeline_parser import ModelineParser



@final
class ModelineParser_VIM(ModelineParser):
	
	def __init__(self, mapping: ModelineInstructionsMapping):
		super().__init__()
		self.mapping = mapping
	
	
	def parse_line_raw(self, line: str, parser_data: object) -> Optional[List[Tuple[str, Optional[str], ModelineInstruction.ValueModifier]]]:
		match = self.__modeline_re.search(line)
		
		if match:
			modeline = "".join(m for m in match.groups() if m)
			matches = [self.__attr_kvp_re.match(attr) for attr in filter(bool, self.__attr_sep_re.split(modeline))]
			raw_attrs = [cast(Tuple[str, str], match.groups()) for match in filter(None, matches)]
			return [(
				raw_attr[0],
				raw_attr[1] or None, # If raw_attr.1 is empty we return None.
				ModelineInstruction.ValueModifier.NONE
			) for raw_attr in raw_attrs]
		
		return None
	
	
	__modeline_re = re.compile(r"""
		(?:^vim?                # begin line with either vi or vim
		   | \s(?:vim? | ex))   # … or white-space then vi, vim, or ex
		(?:\d*):                # optional version digits, closed with :
		\s*                     # optional white-space after ~vim700:
		(?:                     # alternation of type 1 & 2 modelines
		   (?:set?[ ])([^ ].*):.*$ # type 2: optional set or se, spc, opts, :
		   | (?!set?[ ])([^ ].*)$  # type 1: everything following
		)
	""", re.VERBOSE)
	
	__attr_sep_re = re.compile(r"[:\s]")
	__attr_kvp_re = re.compile(r"([^=]+)=?([^=]*)")
