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
			def apply(self, value: Optional[object]) -> Optional[object]:
				pass
		
		
		class ValueTransformLowercase(ValueTransform):
			
			def __init__(self, parameters: Dict[str, object]) -> None:
				super().__init__(parameters)
			
			def apply(self, value: Optional[object]) -> Optional[object]:
				if not isinstance(value, str):
					Logger.warning(f"Skipping lowercase transform for value “{value}” because it is not a string.")
					return None
				return value.lower()
		
		
		class ValueTransformMapping(ValueTransform):
			
			mapping: Dict[str, object]
			# If there is no mapping for the given value, the default value is returned.
			default_on_no_mapping: Optional[object]
			
			def __init__(self, parameters: Dict[str, object]) -> None:
				super().__init__(parameters)
				
				if not "table" in parameters:
					raise ValueError("Mandatory parameter “table” not present for a “map” transform.")
				self.mapping = Utils.checked_cast_to_dict_with_string_keys(
					parameters["table"],
					ValueError("Invalid “table” value: not a dictionary with string keys.")
				)
				self.default_on_no_mapping = parameters.get("default")
			
			def apply(self, value: Optional[object]) -> Optional[object]:
				if not isinstance(value, str):
					Logger.warning(f"Skipping lowercase transform for value “{value}” because it is not a string.")
					return None
				return self.mapping.get(value, self.default_on_no_mapping)
		
		
		# This is `None` if the mapped instruction is unsupported (e.g. vim’s “softtab” which is unsupported in Sublime).
		# If this is `None`, all the other parameters should be ignored.
		key: Optional[str]
		# If this is set, the value for the mapped instruction should be unset, and will be overridden by this value.
		value: Optional[object]
		# These transforms will be applied to the value.
		value_transforms: List[ValueTransform]
		
		def __init__(self, raw_mapping_value: Dict[str, object]) -> None:
			super().__init__()
			
			key = raw_mapping_value["key"]
			if key is None:
				self.key = None
				self.value = None
				self.value_transforms = []
				return
			
			self.key = Utils.checked_cast_to_string(key, ValueError("Invalid “key” value: not a string."))
			# Note: We do not differentiate a None value and the absence of a value.
			self.value = raw_mapping_value.get("value")
			
			# Parse transforms shortcut (`value-mapping`).
			raw_value_transforms: List[Dict[str, object]]
			if "value-mapping" in raw_mapping_value:
				if "value-transforms" in raw_mapping_value:
					raise ValueError("“value-transforms” must not be in mapping if “value-mapping” exists.")
				
				raw_value_transforms = [{
					"type": "map",
					"parameters": {
						"table": Utils.checked_cast_to_dict_with_string_keys(
							raw_mapping_value["value-mapping"],
							ValueError("Invalid “value-mapping” value: not a dictionary with string keys.")
						),
						"default": raw_mapping_value.get("value-mapping-default")
					}
				}]
				
			else:
				raw_value_transforms = Utils.checked_cast_to_list_of_dict_with_string_keys(
					raw_mapping_value.get("value-transforms", []),
					ValueError("")
				)
			
			# Parse transforms from `raw_value_transforms`.
			self.value_transforms = []
			for raw_value_transform in raw_value_transforms:
				params: Dict[str, object] = Utils.checked_cast_to_dict_with_string_keys(
					raw_value_transform.get("parameters", {}),
					ValueError("Invalid “parameters” for a value transform: not a dictionary with string keys.")
				)
				# The match instruction has been added to Python 3.10 only.
				type = Utils.checked_cast_to_optional_string(raw_value_transform.get("type"))
				if   type == "lowercase": self.value_transforms.append(self.ValueTransformLowercase(params))
				elif type == "map":       self.value_transforms.append(self.ValueTransformMapping(params))
				else: raise ValueError("Invalid/unknown type for a value transform.")
		
		def __str__(self) -> str:
			return f"\tkey: {self.key}\n\tvalue: {self.value}\n\ttransforms_count: {len(self.value_transforms)}"
	
	
	mapping: Dict[str, MappingValue] = {}
	
	def __init__(self, raw_mapping_object: Dict[str, Dict[str, Optional[object]]] = {}) -> None:
		super().__init__()
		
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
	def apply(self, key: str, value: Optional[object]) -> Optional[Tuple[str, Optional[object]]]:
		mapping_value = self.mapping.get(key)
		if mapping_value is None: return (key, value)
		
		# If there is a None key in the mapping value, the key is unsupported: we return None.
		if mapping_value.key is None:
			return None
		key = mapping_value.key
		
		# Replace the value if the mapping has a forced value.
		if not mapping_value.value is None:
			if not value is None:
				Logger.warning(f"Replacing value “{value}” for key “{key}” with “{mapping_value.value}”: the key is mapped with a forced value.")
			value = mapping_value.value
		
		for transform in mapping_value.value_transforms:
			value = transform.apply(value)
