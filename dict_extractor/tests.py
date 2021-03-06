from unittest import TestCase

from .extractor import Extractor


class ExtractorInstantiationTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.schema = {
            "x": {
                "a": "{{x}}",
                "b": "...",
                "c": "{{a thing}}"
            },
            "y": "{{z}}",
            "...": "..."
        }

    def test_initialize_extractor(self):
        extractor = Extractor(self.schema)
        self.assertIsInstance(extractor, Extractor)

    def test_schema_must_be_a_dict(self):
        with self.assertRaises(TypeError):
            Extractor("a string")

    def test_empty_schema_throws_exception(self):
        with self.assertRaises(ValueError):
            Extractor({})

    def test_schema_without_braises_raises_exception(self):
        with self.assertRaises(ValueError):
            Extractor({"a": "b"})

    def test_does_not_all_duplicate_keys(self):
        bad_schema = self.schema.copy()
        bad_schema["zz"] = "{{z}}"
        with self.assertRaises(ValueError):
            Extractor(bad_schema)


class SchemaParserTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.schema = {
            "x": {
                "a": "{{x}}",
                "b": "...",
                "c": "{{a thing}}"
            },
            "y": "{{z}}",
            "...": "..."
        }

    def test_parses_to_list_of_keys(self):
        extractor = Extractor(self.schema)
        parsed = extractor.tags
        self.assertEqual(
            {
                "x": ["x", "a"],
                "a thing": ["x", "c"],
                "z": ["y"]
            },
            parsed
        )

    def test_generate_paths(self):
        paths = Extractor._generate_paths_to_all_values(self.schema)
        self.assertEqual(len(list(paths)), 5)


class ExtractDataTests(TestCase):

    @classmethod
    def setUpClass(cls):
        schema = {
            "x": {
                "a": "{{x}}",
                "b": "...",
                "c": "{{a thing}}"
            },
            "y": "{{z}}",
            "...": "..."
        }
        cls.extractor = Extractor(schema)
        cls.test_data = {
            "something": "a",
            "x": {
                "a": "the x variable",
                "c": "a thing variable",
                "b": "anything",
                "d": "nothing"
            },
            "y": "the z variable",
            "z": {
                "a": "sdfasdf"
            }
        }

    def test_extract_test_data(self):
        extracted_data = self.extractor.extract(self.test_data)
        self.assertEqual(
            {
                "x": "the x variable",
                "a thing": "a thing variable",
                "z": "the z variable"
            },
            extracted_data
        )

    def test_extract_defaults_to_none(self):
        missing_data = self.test_data.copy()
        del missing_data["y"]
        extracted_data = self.extractor.extract(missing_data)
        self.assertEqual(
            {
                "x": "the x variable",
                "a thing": "a thing variable",
                "z": None
            },
            extracted_data
        )
