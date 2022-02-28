from unittest import TestCase

from extractor import Extractor


class BasicExtractorTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.schema = {
            "x": {
                "a": "{x}",
                "b": "...",
                "c": "{a thing}"
            },
            "y": "{z}",
            "...": "..."
        }

    def test_initialize_extractor(self):
        extractor = Extractor(self.schema)
        self.assertIsInstance(extractor, Extractor)

    def test_schema_must_be_a_dict(self):
        with self.assertRaises(TypeError):
            Extractor("a string")
