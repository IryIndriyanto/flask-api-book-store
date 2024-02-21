from unittest.mock import patch

import pytest

from resources.book import Books, Book
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError


@pytest.fixture
def data():
    book = {
        "title": "Harry Potter 1",
        "author": "Rowling",
        "price": 150
    }
    yield book


# POST /v1/books/

def test_post_books(test_app, data):
    with test_app.test_request_context(json=data):
        response = Books.post(None)
        assert response.status_code == 200
        assert response.get_json() == {
            'id': 1,
            **data
        }


def test_post_books_integrity_error(test_app, data):
    with test_app.test_request_context(json=data):
        with pytest.raises(BadRequest):
            Books.post(None)
            Books.post(None)


@patch('models.book.BookModel.add_book')
def test_post_books_sql_error(mock_add_book, test_app, data):
    with test_app.test_request_context(json=data):
        with pytest.raises(InternalServerError):
            mock_add_book.side_effect = SQLAlchemyError
            Books.post(None)


# GET /v1/books/

def test_get_books_empty(test_app):
    with test_app.test_request_context():
        response = Books.get(None)
        assert response.status_code == 200
        assert response.get_json() == []


def test_get_books(test_app, data):
    with test_app.test_request_context(json=data):
        book = Books.post(data)
        response = Books.get(book)
        assert response.status_code == 200
        assert response.get_json() == [
            {
                "id": 1,
                **data
            }
        ]


# GET /v1/books/{book_id}

def test_get_book(test_app, data):
    with test_app.test_request_context(json=data):
        book = Books.post(data)
        response = Book.get(book, book_id=1)
        assert response.status_code == 200
        assert response.get_json() == {
            'id': 1,
            **data
        }


def test_get_book_not_found(test_app):
    with test_app.test_request_context():
        with pytest.raises(NotFound):
            Book.get(None, book_id=1)


# DELETE /v1/books/{book_id}

def test_delete_book(test_app, data):
    with test_app.test_request_context(json=data):
        book = Books.post(data)
        response = Book.delete(book, 1)
        assert response == {"message": "Book deleted"}


def test_delete_book_not_found(test_app):
    with test_app.test_request_context():
        with pytest.raises(NotFound):
            Book.delete(None, 1)


# PUT /v1/books/{book_id}

def test_put_book(test_app, data):
    with test_app.test_request_context(json=data):
        Books.post(data)
        response = Book.put(book_data={
            **data,
            "title": "New Harry Potter",
        }, book_id=1)
        assert response.status_code == 200
        assert response.get_json() == {
            'id': 1,
            **data,
            "title": "New Harry Potter"
        }


def test_put_book_not_found(test_app, data):
    with test_app.test_request_context(json=data):
        with pytest.raises(NotFound):
            Book.put(data, book_id=1)


def test_put_books_integrity_error(test_app, data):
    book_2 = {
        "title": "Harry Potter 2",
        "author": "Rowling",
        "price": 150
    }
    with test_app.test_request_context(json=data):
        Books.post(data)
    with test_app.test_request_context(json=book_2):
        with pytest.raises(BadRequest):
            Books.post(book_2)
            response = Book.put(book_2, book_id=1)


@patch('resources.book.BookModel.update_book')
def test_put_books_sql_error(mock_update_book, test_app, data):
    with test_app.test_request_context(json=data):
        mock_update_book.side_effect = SQLAlchemyError
        with pytest.raises(InternalServerError):
            Books.post(data)
            Book.put(data, book_id=1)
