import pytest
from app import create_app
from db import db


@pytest.fixture()
def test_app():
    app = create_app(is_test_env=True)
    app.config['TESTING'] = True

    yield app

    with app.app_context():
        db.drop_all()
