import pytest
from app import create_app
from db import db


@pytest.fixture()
def test_app():
    app = create_app(test_config=True)
    app.config['TESTING'] = True
    yield app


@pytest.fixture(autouse=True)
def run_around_tests(test_app):
    # Code that will run before your test
    # print("Before test")

    yield

    # Code that will run after your test
    with test_app.app_context():
        db.drop_all()
        db.create_all()

    # print("After test")
