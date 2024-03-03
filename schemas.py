from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)


class PlainBookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    price = fields.Float(required=True)
    year = fields.Int(required=True)


class BookSchema(PlainBookSchema):
    users_review = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)


class UserSchema(PlainUserSchema):
    books_review = fields.List(fields.Nested(PlainBookSchema()), dump_only=True)
