import os
from flask import Flask
from flask_smorest import Api
from dotenv import load_dotenv

from db import db

from resources.book import blp as book_blueprint


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    # OpenAPI Config
    app.config["API_TITLE"] = "Book Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Database Config
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api = Api(app)
    api.register_blueprint(book_blueprint)

    return app
