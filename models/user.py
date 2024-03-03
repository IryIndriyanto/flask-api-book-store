from db import db
from models.common import CommonModel


class UserModel(CommonModel):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    books_review = db.relationship("ReviewModel", back_populates="user")
