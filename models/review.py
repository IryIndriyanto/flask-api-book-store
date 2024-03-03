from db import db
from flask_smorest import abort


class ReviewModel(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))

    book = db.relationship("BookModel", back_populates="books_review")
    user = db.relationship("UserModel", back_populates="books_review")

    @classmethod
    def get_reviews(cls):
        return cls.query.all()

    @classmethod
    def get_review(cls, review_id):
        review = db.session.get(cls, review_id)
        if review is None:
            abort(404, message="Review not found")
        return review

    def add_review(self):
        try:
            with db.session.begin():
                db.session.add(self)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_review(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update_review(self, review_data):
        try:
            for key, value in review_data.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
