from unittest import TestCase

from ..app.modeline_instructions_mapping import ModelineInstructionsMapping



class InstructionsMappingTests(TestCase):
	
	def test_simple_case(self):
		mapping = ModelineInstructionsMapping({
			"to_map": {
				"key": "mapped",
			},
		})
		self.assertEqual(mapping.apply("to_map",   "val"), ("mapped",   "val"))
		self.assertEqual(mapping.apply("unmapped", "val"), ("unmapped", "val"))
	
	def test_unsupported_key(self):
		mapping = ModelineInstructionsMapping({
			"to_map": {
				"key": None,
			},
		})
		self.assertEqual(mapping.apply("to_map", "val"), None)
	
	def test_forced_value(self):
		mapping = ModelineInstructionsMapping({
			"to_map": {
				"key": "mapped",
				"value": 42
			},
		})
		self.assertEqual(mapping.apply("to_map", "val"), ("mapped", 42))
	
	def test_forced_value_none(self):
		# It is not possible to force a None value.
		# Makes sense, but is it _really_ what we want?
		# I’d say yes, probably.
		mapping = ModelineInstructionsMapping({
			"to_map": {
				"key": "mapped",
				"value": None
			},
		})
		self.assertEqual(mapping.apply("to_map", "val"), ("mapped", "val"))
	
	def test_mapped_value(self):
		mapping = ModelineInstructionsMapping({
			"to_map": {
				"key": "mapped",
				"value-mapping": {
					"v2m-1": "m-1",
					"v2m-2": None,
					"v2m-3": {"v": "m-3"},
				}
			},
		})
		self.assertEqual(mapping.apply("to_map", "v2m-0"), None)
		self.assertEqual(mapping.apply("to_map", "v2m-1"), ("mapped", "m-1"))
		self.assertEqual(mapping.apply("to_map", "v2m-2"), None)
		self.assertEqual(mapping.apply("to_map", "v2m-3"), ("mapped", {"v": "m-3"}))
	
	def test_mapped_value_with_default(self):
		mapping = ModelineInstructionsMapping({
			"to_map": {
				"key": "mapped",
				"value-mapping-default": 42,
				"value-mapping": {
					"v2m-1": "m-1",
					"v2m-2": None,
					"v2m-3": {"v": "m-3"},
				}
			},
		})
		self.assertEqual(mapping.apply("to_map", "v2m-0"), ("mapped", 42))
		self.assertEqual(mapping.apply("to_map", "v2m-1"), ("mapped", "m-1"))
		self.assertEqual(mapping.apply("to_map", "v2m-2"), None)
		self.assertEqual(mapping.apply("to_map", "v2m-3"), ("mapped", {"v": "m-3"}))
	
	def test_mapped_value_with_null_default(self):
		mapping = ModelineInstructionsMapping({
			"to_map": {
				"key": "mapped",
				"value-mapping-default": None,
				"value-mapping": {
					"v2m-1": "m-1",
					"v2m-2": None,
					"v2m-3": {"v": "m-3"},
				}
			},
		})
		self.assertEqual(mapping.apply("to_map", "v2m-0"), ("mapped", "v2m-0"))
		self.assertEqual(mapping.apply("to_map", "v2m-1"), ("mapped", "m-1"))
		self.assertEqual(mapping.apply("to_map", "v2m-2"), None)
		self.assertEqual(mapping.apply("to_map", "v2m-3"), ("mapped", {"v": "m-3"}))
		
	def test_mapped_value_long_form(self):
		mapping = ModelineInstructionsMapping({
			"to_map": {
				"key": "mapped",
				"value-transforms": [
					{
						"type": "map",
						"parameters": {
							"table": {
								"v2m-1": "m-1",
								"v2m-2": None,
								"v2m-3": {"v": "m-3"},
							}
						}
					}
				],
			},
		})
		self.assertEqual(mapping.apply("to_map", "v2m-0"), None)
		self.assertEqual(mapping.apply("to_map", "v2m-1"), ("mapped", "m-1"))
		self.assertEqual(mapping.apply("to_map", "v2m-2"), None)
		self.assertEqual(mapping.apply("to_map", "v2m-3"), ("mapped", {"v": "m-3"}))
	
	def test_mapped_value_long_form_with_default(self):
		mapping = ModelineInstructionsMapping({
			"to_map": {
				"key": "mapped",
				"value-transforms": [
					{
						"type": "map",
						"parameters": {
							"default": 42,
							"table": {
								"v2m-1": "m-1",
								"v2m-2": None,
								"v2m-3": {"v": "m-3"},
							}
						}
					}
				],
			},
		})
		self.assertEqual(mapping.apply("to_map", "v2m-0"), ("mapped", 42))
		self.assertEqual(mapping.apply("to_map", "v2m-1"), ("mapped", "m-1"))
		self.assertEqual(mapping.apply("to_map", "v2m-2"), None)
		self.assertEqual(mapping.apply("to_map", "v2m-3"), ("mapped", {"v": "m-3"}))
	
	def test_mapped_value_long_form_with_null_default(self):
		mapping = ModelineInstructionsMapping({
			"to_map": {
				"key": "mapped",
				"value-transforms": [
					{
						"type": "map",
						"parameters": {
							"default": None,
							"table": {
								"v2m-1": "m-1",
								"v2m-2": None,
								"v2m-3": {"v": "m-3"},
							}
						}
					}
				],
			},
		})
		self.assertEqual(mapping.apply("to_map", "v2m-0"), ("mapped", "v2m-0"))
		self.assertEqual(mapping.apply("to_map", "v2m-1"), ("mapped", "m-1"))
		self.assertEqual(mapping.apply("to_map", "v2m-2"), None)
		self.assertEqual(mapping.apply("to_map", "v2m-3"), ("mapped", {"v": "m-3"}))
