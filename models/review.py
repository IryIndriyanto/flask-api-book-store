from db import db
from models.common import CommonModel


class ReviewModel(CommonModel):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))

    book = db.relationship("BookModel", back_populates="books_review")
    user = db.relationship("UserModel", back_populates="books_review")
