from db import db
from models.common import CommonModel
from sqlalchemy import Enum


class UserModel(CommonModel):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(Enum("admin", "user", name="role_enum"), nullable=False)

    books_review = db.relationship("ReviewModel", back_populates="user")
