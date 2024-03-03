from db import db
from flask_smorest import abort


class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    books_review = db.relationship("ReviewModel", back_populates="user")

    @classmethod
    def get_users(cls):
        return cls.query.all()

    @classmethod
    def get_user(cls, book_id):
        user = db.session.get(cls, book_id)
        if user is None:
            abort(404, message="User not found")
        return user

    def add_user(self):
        try:
            with db.session.begin():
                db.session.add(self)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_user(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update_user(self, user_data):
        try:
            for key, value in user_data.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
