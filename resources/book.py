from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import BookModel
from schemas import BookSchema

blp = Blueprint("books", "books", description="Operations on books", url_prefix="books")


@blp.route('/')
class Books(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        return BookModel.get_books()

    @blp.arguments(BookSchema)
    @blp.response(200, BookSchema)
    def post(self, book_data):
        # book = BookModel(title=book_data["title"], author=book_data["author"], price=book_data["price"])
        book = BookModel(**book_data)
        try:
            book.add_book()
        except IntegrityError:
            abort(400, message="A book with that title already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the book.")

        return book


@blp.route('/<int:book_id>')
class Book(MethodView):
    @blp.response(200, BookSchema)
    def get(self, book_id):
        book = BookModel.get_book(book_id)
        return book

    @blp.arguments(BookSchema)
    @blp.response(200, BookSchema)
    def put(self, book_data, book_id):
        print('here')
        book = BookModel.get_book(book_id)
        book.update_book(book_data)
        return book

    def delete(self, book_id):
        book = BookModel.get_book(book_id)
        book.delete_book()
        return {"message": "Book deleted"}
