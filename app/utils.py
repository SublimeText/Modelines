# This can be removed when using Python >= 3.10 (for List at least; the rest idk).
from typing import cast, Any, Dict, List, Optional, TypeVar

from sublime_types import Value as SublimeValue



class Utils:
	
	@staticmethod
	def is_dict_with_string_keys(variable: object) -> bool:
		"""Casts the given object to a dictionary with string keys; raises the given exception if the given object is not that."""
		return isinstance(variable, dict) and all(isinstance(elem, str) for elem in variable.keys())
	
	@staticmethod
	def checked_cast_to_string(variable: object, exception: Exception = ValueError("Given object is not a string.")) -> str:
		"""Casts the given object to a string; raises the given exception if the given object is not that."""
		if not isinstance(variable, str):
			raise exception
		return cast(str, variable)
	
	@staticmethod
	def checked_cast_to_optional_string(variable: object, exception: Exception = ValueError("Given object is not an optional string.")) -> Optional[str]:
		"""Casts the given object to an optional string; raises the given exception if the given object is not that."""
		if object is None:
			return None
		return Utils.checked_cast_to_string(variable, exception)
	
	@staticmethod
	def checked_cast_to_list_of_strings(variable: object, exception: Exception = ValueError("Given object is not a list of strings.")) -> List[str]:
		"""Casts the given object to a list of strings; raises the given exception if the given object is not that."""
		if not isinstance(variable, list) or not all(isinstance(elem, str) for elem in variable):
			raise exception
		return cast(List[str], variable)
	
	@staticmethod
	def checked_cast_to_dict_with_string_keys(variable: object, exception: Exception = ValueError("Given object is not a dictionary with string keys.")) -> Dict[str, object]:
		"""Casts the given object to a dictionary with string keys; raises the given exception if the given object is not that."""
		if not Utils.is_dict_with_string_keys(variable):
			raise exception
		return cast(Dict[str, object], variable)
	
	@staticmethod
	def checked_cast_to_list_of_dict_with_string_keys(variable: object, exception: Exception = ValueError("Given object is not a list of dictionaries with string keys.")) -> List[Dict[str, object]]:
		"""Casts the given object to a list of dictionaries with string keys; raises the given exception if the given object is not a that."""
		if not isinstance(variable, list) or not all(Utils.is_dict_with_string_keys(elem) for elem in variable):
			raise exception
		return cast(List[Dict[str, object]], variable)
	
	@staticmethod
	def checked_cast_to_dict_of_dict_with_string_keys(variable: object, exception: Exception = ValueError("Given object is not a dictionary with string keys of dictionaries with string keys.")) -> Dict[str, Dict[str, object]]:
		"""Casts the given object to a dictionary with string key of dictionaries with string keys; raises the given exception if the given object is not a that."""
		dict = Utils.checked_cast_to_dict_with_string_keys(variable, exception)
		if not all(Utils.is_dict_with_string_keys(elem) for elem in dict.values()):
			raise exception
		return cast(Dict[str, Dict[str, object]], variable)
	
	@staticmethod
	def checked_cast_to_sublime_value(variable: object, exception: Exception = ValueError("Given object is not a Sublime Value.")) -> SublimeValue:
		"""Casts the given object to a Sublime Value; raises the given exception if the given object is not that."""
		if variable is None:
			return cast(SublimeValue, variable)
		# I don’t think there is a way to automatically check all the elements of the Value union, so we do them manually.
		# We’ll have to manually update the checks when the Value type is updated in Sublime.
		# Note: We do None separately because NoneType causes issues w/ Python 3.8 apparently.
		for t in [bool, str, int, float, list, dict]:
			if isinstance(variable, t):
				return cast(SublimeValue, variable)
		raise exception
	
	@staticmethod
	def as_int_or_none(variable: str) -> Optional[int]:
		try:               return int(variable)
		except ValueError: return None
	
	@staticmethod
	def as_float_or_none(variable: str) -> Optional[float]:
		try:               return float(variable)
		except ValueError: return None
	
	K = TypeVar("K"); V = TypeVar("V")
	@staticmethod
	def merge(a: Dict[K, V], b: Dict[K, V], path=[]) -> Dict[K, V]:
		"""
		Merges b in a, in place, and returns a.
		From <https://stackoverflow.com/a/7205107>, modified (and not extensively tested…).
		"""
		for key in b:
			if key in a:
				if isinstance(a[key], dict) and isinstance(b[key], dict):
					Utils.merge(cast(Dict[object, object], a[key]), cast(Dict[object, object], b[key]), path + [str(key)])
				else:
					# Original SO source checked whether the values were the same; we do not care and just trump.
					a[key] = b[key]
			else:
				a[key] = b[key]
		return a
	
	def __new__(cls, *args, **kwargs):
		raise RuntimeError("Utils is static and thus cannot be instantiated.")
