from marshmallow import Schema
from stringcase import camelcase, snakecase


class SnakeCaseSchema(Schema):
    """A Schema that marshals data with camelCase keys into snake_case."""
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)
        field_obj.dump_to = snakecase(field_obj.data_key or field_name)
