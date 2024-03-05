import os
from flask import Flask, jsonify
from flask_smorest import Api
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from db import db
from resources.book import blp as book_blueprint
from resources.user import blp as user_blueprint
from resources.review import blp as review_blueprint
from resources.auth import blp as auth_blueprint


def create_app(is_test_env=False):
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
    if is_test_env is True:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")

    db.init_app(app)
    Migrate(app, db)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "330864960365311445001535564788325620144"
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    v1_blueprints = [book_blueprint, user_blueprint, review_blueprint, auth_blueprint]
    for bp in v1_blueprints:
        bp.url_prefix = f"/v1/{bp.url_prefix}"
        api.register_blueprint(bp)

    v2_blueprints = []
    for bp in v2_blueprints:
        bp.url_prefix = f"/v2/{bp.url_prefix}"
        api.register_blueprint(bp)

    return app
