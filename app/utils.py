# This can be removed when using Python >= 3.10 (for List at least; the rest idk).
from typing import cast, Dict, List



class Utils:
	
	@staticmethod
	def is_dict_with_string_keys(variable: object) -> bool:
		"""Casts the given object to a dictionary with string keys; raises the given exception if the given object is not that."""
		return isinstance(variable, dict) and all(isinstance(elem, str) for elem in variable.keys())
	
	@staticmethod
	def checked_cast_to_string(variable: object, exception: Exception = ValueError("Given object is not a string.")) -> str:
		"""Casts the given object to a string; raises the given exception if the given object is not that."""
		if not isinstance(object, str):
			raise exception
		return cast(str, object)
	
	@staticmethod
	def checked_cast_to_list_of_strings(variable: object, exception: Exception = ValueError("Given object is not a list of strings.")) -> List[str]:
		"""Casts the given object to a list of strings; raises the given exception if the given object is not that."""
		if not isinstance(variable, list) or not all(isinstance(elem, str) for elem in variable):
			raise exception
		return cast(List[str], object)
	
	@staticmethod
	def checked_cast_to_dict_with_string_keys(variable: object, exception: Exception = ValueError("Given object is not a dictionary with string keys.")) -> Dict[str, object]:
		"""Casts the given object to a dictionary with string keys; raises the given exception if the given object is not that."""
		if not Utils.is_dict_with_string_keys(object):
			raise exception
		return cast(Dict[str, object], object)
	
	@staticmethod
	def checked_cast_to_list_of_dict_with_string_keys(variable: object, exception: Exception = ValueError("Given object is not a list of dictionaries with string keys.")) -> List[Dict[str, object]]:
		"""Casts the given object to a list of dictionaries with string keys; raises the given exception if the given object is not a that."""
		if not isinstance(variable, list) or not all(Utils.is_dict_with_string_keys(elem) for elem in variable):
			raise exception
		return cast(List[Dict[str, object]], object)
	
	def __new__(cls, *args, **kwargs):
		raise RuntimeError("Utils is static and thus cannot be instantiated.")
