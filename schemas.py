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
    books_review = fields.List(fields.Nested("ReviewUserSchema"), dump_only=True)


class UserSchema(PlainUserSchema):
    books_review = fields.List(fields.Nested("ReviewBookSchema"), dump_only=True)


class PlainReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    comment = fields.Str(required=True)
    rating = fields.Int(required=True)


class ReviewUserSchema(PlainReviewSchema):
    user = fields.Nested(PlainUserSchema(), dump_only=True)


class ReviewBookSchema(PlainReviewSchema):
    book = fields.Nested(PlainBookSchema(), dump_only=True)


class ReviewSchema(PlainReviewSchema):
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    book = fields.Nested(PlainBookSchema(), dump_only=True)
