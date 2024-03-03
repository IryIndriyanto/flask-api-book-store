from db import db
from models.common import CommonModel


class BookModel(CommonModel):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    author = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=3), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    books_review = db.relationship("ReviewModel", back_populates="book")
