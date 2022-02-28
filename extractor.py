

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
