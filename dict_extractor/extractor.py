from functools import reduce


class Extractor:

    def __init__(self, schema: dict):
        self._validate_raw_schema(schema)
        self.tags = self._identify_tags(schema)
        self._validate_parsed_tags()

    def extract(self, data: dict) -> dict:
        extracted_data = dict()
        for variable, path in self.tags.items():
            value = self._extract_a_path(data, path)
            extracted_data[variable] = value
        return extracted_data

    @classmethod
    def _extract_a_path(cls, data, keys):
        return reduce(lambda d, k: d.get(k), keys, data)

    @classmethod
    def _identify_tags(cls, schema: dict) -> dict:
        parsed_schema = dict()
        for value, path in cls._generate_paths_to_all_values(schema):
            if cls._is_value_a_tag(value):
                value = cls._remove_tags(value)
                cls._check_for_existing_key(value, parsed_schema)
                parsed_schema[value] = path

        return parsed_schema

    @classmethod
    def _generate_paths_to_all_values(cls, schema, path=None):
        """Generator objects of unique paths to each value in the original schema"""
        if path is None:
            path = []
        for k, v in schema.items():
            new_path = path + [k]
            if isinstance(v, dict):
                for result in cls._generate_paths_to_all_values(v, new_path):
                    yield result
            else:
                yield v, new_path

    @staticmethod
    def _is_value_a_tag(value: str):
        return value[0] == "{" and value[-1] == "}"

    @classmethod
    def _check_for_existing_key(cls, key, schema):
        if key in schema.keys():
            raise ValueError(f"Cannot have a duplicated target.")

    @staticmethod
    def _remove_tags(value: str):
        return value.replace("{", "").replace("}", "")

    @classmethod
    def _validate_raw_schema(cls, schema):
        cls._require_dict(schema)
        if len(schema) == 0:
            raise ValueError("Dictionary must not be empty.")

    def _validate_parsed_tags(self):
        self._require_dict(self.tags)
        if len(self.tags) == 0:
            raise ValueError("Schema dictionary must include braced variables.")
        return self

    @staticmethod
    def _require_dict(data):
        if not isinstance(data, dict):
            raise TypeError(f"Data should be a dictionary, not {type(data)}.")
