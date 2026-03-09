from typing import cast, final, Any, Generator, List, Optional, Tuple

from sublime import View as SublimeView
import re

from ..modeline_instruction import ModelineInstruction
from ..modeline_instructions_mapping import ModelineInstructionsMapping
from ..modeline_parser import ModelineParser
from ..utils import Utils



@final
class ModelineParser_Legacy(ModelineParser):
	
	def __init__(self):
		super().__init__()
		self.mapping.mapping["x_syntax"] = ModelineInstructionsMapping.MappingValue({"key": "syntax"})
	
	
	def parse_line_raw(self, line: str, parser_data: object) -> Optional[List[Tuple[str, Optional[str], ModelineInstruction.ValueModifier]]]:
		modeline_prefix_re = Utils.checked_cast_to_string(parser_data, ValueError("Parser called with invalid parser data."))
		if not re.match(modeline_prefix_re, line):
			return None
		
		res: List[Tuple[str, Optional[str], ModelineInstruction.ValueModifier]] = []
		for opt in self.__gen_raw_options(line):
			name, _, value = opt.partition(" ")
			res.append((name.rstrip(":"), value.rstrip(";"), ModelineInstruction.ValueModifier.NONE))
		return res
	
	
	def parser_data_for_view(self, view: SublimeView) -> object:
		line_comment = self.__get_line_comment_char_re(view).lstrip() or self.__DEFAULT_LINE_COMMENT
		return (self.__MODELINE_PREFIX_TPL % line_comment)
	
	
	__MODELINE_PREFIX_TPL = "%s\\s*(st|sublime): "
	__DEFAULT_LINE_COMMENT = "#"
	__MULTIOPT_SEP = "; "
	
	
	def __is_modeline(self, prefix, line):
		return bool(re.match(prefix, line))
	
	def __gen_raw_options(self, raw_modeline: str) -> Generator[str, None, None]:
		opt = raw_modeline.partition(":")[2].strip()
		if self.__MULTIOPT_SEP in opt:
			for subopt in (s for s in opt.split(self.__MULTIOPT_SEP)):
				yield subopt
		else:
			yield opt
	
	def __get_line_comment_char_re(self, view: SublimeView):
		commentChar = ""
		commentChar2 = ""
		try:
			for pair in cast(Any, view.meta_info("shellVariables", 0)):
				if pair["name"] == "TM_COMMENT_START":
					commentChar = pair["value"]
				if pair["name"] == "TM_COMMENT_START_2":
					commentChar2 = pair["value"]
				if commentChar and commentChar2:
					break
		except TypeError:
			pass
		
		if not commentChar2:
			return re.escape(commentChar.strip())
		else:
			return "(" + re.escape(commentChar.strip()) + "|" + re.escape(commentChar2.strip()) + ")"
