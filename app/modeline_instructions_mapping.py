# This can be removed when using Python >= 3.10 (for List at least; the rest idk).
from typing import Dict, List, Optional, Tuple

from abc import ABC, abstractmethod

from .logger import Logger
from .utils import Utils



class ModelineInstructionsMapping:
	
	class MappingValue:
		
		class ValueTransform(ABC):
			
			@abstractmethod
			def __init__(self, parameters: Dict[str, object]) -> None:
				pass
			
			@abstractmethod
			def apply(self, value: object) -> object:
				pass
		
		
		class ValueTransformLowercase(ValueTransform):
			
			def __init__(self, parameters: Dict[str, object]) -> None:
				super().__init__(parameters)
			
			def apply(self, value: object) -> object:
				if not isinstance(value, str):
					Logger.warning(f"Skipping lowercase transform for value “{value}” because it is not a string.")
					return None
				return value.lower()
		
		
		class ValueTransformMapping(ValueTransform):
			
			class __PassthroughMapping:
				"""
				Internal marker class set in the default value variable for a mapping,
				 to signify the source value should be used when there is no mapping for the value.
				"""
				pass
			
			class UnsupportedValue:
				"""
				Internal marker class set in the default value variable for a mapping,
				 to signify the value is unsupported.
				
				Note:
				This marker is public because we need it when converting the short mapping syntax to the full one,
				 which is done outside of this class.
				"""
				pass
				
			def __init__(self, parameters: Dict[str, object]) -> None:
				super().__init__(parameters)
				
				if not "table" in parameters:
					raise ValueError("Mandatory parameter “table” not present for a “map” transform.")
				self.mapping = Utils.checked_cast_to_dict_with_string_keys(
					parameters["table"],
					ValueError("Invalid “table” value: not a dictionary with string keys.")
				)
				# If there is no mapping for the given value, the default value is returned,
				#  unless no default is specified, in which case the original value is returned.
				# The “no default” case is represented by the `__NoDefaultValue()` value.
				self.default_on_no_mapping = parameters.get("default", self.UnsupportedValue()) or self.__PassthroughMapping()
			
			def apply(self, value: object) -> object:
				if not isinstance(value, str):
					Logger.warning(f"Skipping mapping transform for value “{value}” because it is not a string.")
					return None
				ret = self.mapping.get(value, self.default_on_no_mapping)
				if isinstance(ret, self.__PassthroughMapping): return value
				if isinstance(ret, self.UnsupportedValue): return None
				return ret
		
		
		def __init__(self, raw_mapping_value: Dict[str, object]) -> None:
			super().__init__()
			
			# This is `None` if the mapped instruction is unsupported (e.g. vim’s “softtab” which is unsupported in Sublime).
			# If this is `None`, all the other parameters should be ignored.
			key = raw_mapping_value["key"]
			if key is None:
				self.key = None
				self.value = None
				self.value_transforms = []
				return
			
			self.key = Utils.checked_cast_to_string(key, ValueError("Invalid “key” value: not a string."))
			# If this is set, the value for the mapped instruction should be unset, and will be overridden by this value.
			# Note: We do not differentiate a None value and the absence of a value.
			self.value = raw_mapping_value.get("value")
			
			# Parse transforms shortcut (`value-mapping`).
			raw_value_transforms: List[Dict[str, object]] = Utils.checked_cast_to_list_of_dict_with_string_keys(
				raw_mapping_value.get("value-transforms", []),
				ValueError("")
			)
			if "value-mapping" in raw_mapping_value:
				raw_value_transforms.append({
					"type": "map",
					"parameters": {
						"table": Utils.checked_cast_to_dict_with_string_keys(
							raw_mapping_value["value-mapping"],
							ValueError("Invalid “value-mapping” value: not a dictionary with string keys.")
						),
						# If we want a “pass-through” mapping for unmapped values, we have to go through the verbose syntax:
						#  using “value-mapping” the default default value is always “unsupported.”
						"default": raw_mapping_value.get("value-mapping-default", self.ValueTransformMapping.UnsupportedValue())
					}
				})
			
			# Parse transforms from `raw_value_transforms`.
			# These transforms will be applied to the value.
			self.value_transforms = []
			for raw_value_transform in raw_value_transforms:
				params: Dict[str, object] = Utils.checked_cast_to_dict_with_string_keys(
					raw_value_transform.get("parameters", {}),
					ValueError("Invalid “parameters” for a value transform: not a dictionary with string keys.")
				)
				# The “match” instruction has been added to Python 3.10.
				# We use `if elif else` instead.
				type = Utils.checked_cast_to_optional_string(raw_value_transform.get("type"))
				if   type == "lowercase": self.value_transforms.append(self.ValueTransformLowercase(params))
				elif type == "map":       self.value_transforms.append(self.ValueTransformMapping(params))
				else: raise ValueError("Invalid/unknown type for a value transform.")
		
		def __str__(self) -> str:
			return f"\tkey: {self.key}\n\tvalue: {self.value}\n\ttransforms_count: {len(self.value_transforms)}"
	
	
	def __init__(self, raw_mapping_object: Dict[str, Dict[str, Optional[object]]] = {}) -> None:
		super().__init__()
		
		self.mapping = {}
		for key, val in raw_mapping_object.items():
			# We must silently skip None values as these are valid overrides for user mappings, to remove a specific mapping.
			if val is None: continue
			
			try:
				aliases = Utils.checked_cast_to_list_of_strings(
					val.get("aliases", []),
					ValueError("Invalid “aliases” value: not a list of strings.")
				)
				
				val = ModelineInstructionsMapping.MappingValue(val)
				for key in [key] + aliases:
					self.mapping[key] = val
				
			except ValueError as e:
				Logger.warning(f"Skipping invalid mapping value for key “{key}”: “{e}”.")
	
	def __str__(self) -> str:
		# There is probably a more Pythonic way of doing this (map + join?), but this works.
		res = ""
		for k, v in self.mapping.items():
			res += k + ":\n" + v.__str__()
			res += "\n"
		return res
	
	# Returns `None` if the mapping tells the key is unsupported.
	def apply(self, key: str, value: object) -> Optional[Tuple[str, object]]:
		mapping_value = self.mapping.get(key)
		# If the mapping value is None, we return the unmodified source.
		# If there is a None key in the mapping value, the key is unsupported: we return None.
		if mapping_value is None: return (key, value)
		if mapping_value.key is None: return None
		
		key = mapping_value.key
		
		# Replace the value if the mapping has a forced value.
		if not mapping_value.value is None:
			if not value is None:
				Logger.warning(f"Replacing value “{value}” for key “{key}” with “{mapping_value.value}”: the key is mapped with a forced value.")
			value = mapping_value.value
		
		for transform in mapping_value.value_transforms:
			value = transform.apply(value)
			if value is None:
				return None
		
		return (key, value)
