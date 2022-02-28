

class Extractor:

    def __init__(self, schema: dict):
        self.schema = schema
        self._validate_schema()

    def extract(self, data: dict):
        pass

    def _validate_schema(self):
        self._require_dict(self.schema)

    @staticmethod
    def _require_dict(data):
        if not isinstance(data, dict):
            raise TypeError(f"Data should be a dictionary, not {type(data)}.")

    def _parse_schema(self):
        parsed_schema = {}
        for path, value in self._generate_paths(self.schema):
            if value[0] == "{":
                parsed_schema[value] = path
        return parsed_schema

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
