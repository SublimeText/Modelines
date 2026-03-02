# This can be removed when using Python >= 3.10 (for List at least; the rest idk).
from typing import cast, Dict, List, TypeVar



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
	
	@staticmethod
	def checked_cast_to_dict_of_dict_with_string_keys(variable: object, exception: Exception = ValueError("Given object is not a dictionary with string keys of dictionaries with string keys.")) -> Dict[str, Dict[str, object]]:
		"""Casts the given object to a dictionary with string key of dictionaries with string keys; raises the given exception if the given object is not a that."""
		dict = Utils.checked_cast_to_dict_with_string_keys(variable, exception)
		if not all(Utils.is_dict_with_string_keys(elem) for elem in dict.values()):
			raise exception
		return cast(Dict[str, Dict[str, object]], variable)
	
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
