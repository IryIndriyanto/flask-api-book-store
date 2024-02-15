from db import db


class BookModel(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    author = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)

    @classmethod
    def get_books(cls):
        return cls.query.all()

    @classmethod
    def get_book(cls, book_id):
        return cls.query.get_or_404(book_id)

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
