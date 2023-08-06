class AbstractSerializer:

    @classmethod
    def init(cls, data):
        return {}

    @classmethod
    def apply(cls, result, key, value, data):
        result[key] = value

    @classmethod
    def serialize(cls, data):
        return data
