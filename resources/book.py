from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import BookModel
from schemas import BookSchema

blp = Blueprint("books", "books", description="Operations on books", url_prefix="/books")


@blp.route('/')
class Book(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        return BookModel.query.all()

    @blp.arguments(BookSchema)
    @blp.response(200, BookSchema)
    def post(self, book_data):
        # book = BookModel(title=book_data["title"], author=book_data["author"], price=book_data["price"])
        book = BookModel(**book_data)
        try:
            db.session.add(book)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A book with that title already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the book.")

        return book


@blp.route('/<int:book_id>')
class Book(MethodView):
    @blp.response(200, BookSchema)
    def get(self, book_id):
        book = BookModel.query.get_or_404(book_id)
        return book

    @blp.arguments(BookSchema)
    @blp.response(200, BookSchema)
    def put(self, book_data, book_id):
        book = BookModel.query.get_or_404(book_id)
        # book.title = book_data["title"]
        # book.author = book_data["author"]
        # book.price = book_data["price"]

        BookModel.query.filter_by(id=book_id).update(book_data)
        db.session.commit()
        return book

    def delete(self, book_id):
        book = BookModel.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted"}
