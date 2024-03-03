from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    price = fields.Float(required=True)
    year = fields.Int(required=True)
    user_review = fields.List(fields.Nested(UserSchema()), dump_only=True)
