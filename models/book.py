from db import db
from flask_smorest import abort


class BookModel(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    author = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=3), nullable=False)
    year = db.Column(db.Integer, nullable=False)

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
        try:
            with db.session.begin():
                db.session.add(self)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_book(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update_book(self, book_data):
        try:
            for key, value in book_data.items():
                print('key:', key, 'value:', value)
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
