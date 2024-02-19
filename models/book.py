from db import db
from flask_smorest import abort


class BookModel(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    author = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=3), nullable=False)

    @classmethod
    def get_books(cls):
        # return sql.execute("SELECT * FROM books")
        return cls.query.all()

    @classmethod
    def get_book(cls, book_id):
        book = db.session.get(cls, book_id)
        if book is None:
            abort(404, message="Book not found")
        return book

    def add_book(self):
        db.session.add(self)
        db.session.commit()

    def delete_book(self):
        db.session.delete(self)
        db.session.commit()

    def update_book(self, book_data):
        for key, value in book_data.items():
            setattr(self, key, value)
        db.session.commit()
