

class Extractor:

    def __init__(self, schema: dict):
        self._validate_raw_schema(schema)
        self.schema = schema.copy()
        self._parse_schema()
        self._validate_parsed_schema()

    def extract(self, data: dict):
        extracted_data = dict()
        for variable, path in self.schema.items():
            value = self._extract_a_path(data, path)
            extracted_data[variable] = value
        return extracted_data

    @classmethod
    def _extract_a_path(cls, data, keys):
        data = data.copy()
        for k in keys:
            data = data[k]
        return data


    def _validate_raw_schema(self, schema):
        self._require_dict(schema)

    @staticmethod
    def _require_dict(data):
        if not isinstance(data, dict):
            raise TypeError(f"Data should be a dictionary, not {type(data)}.")

    def _parse_schema(self):
        parsed_schema = {}
        for path, value in self._generate_paths(self.schema):
            if value[0] == "{":
                value = self._remove_tags(value)
                parsed_schema[value] = path
        self.schema = parsed_schema
        return parsed_schema

    @classmethod
    def _remove_tags(cls, value: str):
        return value.replace("{", "").replace("}", "")

    @classmethod
    def _generate_paths(cls, schema, path=None):
        if path is None:
            path = []
        for k, v in schema.items():
            new_path = path + [k]
            if isinstance(v, dict):
                for u in cls._generate_paths(v, new_path):
                    yield u
            else:
                yield new_path, v

    def _validate_parsed_schema(self):
        self._require_dict(self.schema)
