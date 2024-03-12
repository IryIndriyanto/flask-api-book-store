from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required
from passlib.hash import pbkdf2_sha256
from functools import wraps
from sqlalchemy import select
from db import db

from models import UserModel
from schemas import UserSchema, PlainUserSchema

blp = Blueprint("auth", "auth", description="Operations on auth", url_prefix="auth")


@blp.route("/register-jwt")
class UserRegister(MethodView):
    @blp.arguments(PlainUserSchema)
    @blp.response(200, PlainUserSchema)
    def post(self, user_data):
        try:
            user = UserModel(
                username=user_data["username"],
                password=pbkdf2_sha256.hash(user_data["password"]),
                role="user"
            )

            user.add_item()
        except IntegrityError:
            abort(400, message="A user with that username already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while add the user.")

        return user


@blp.route("/login-jwt")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = db.session.execute(select(UserModel).where(UserModel.username == user_data["username"])).first()[0]
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity={"id": user.id, "role": user.role}, fresh=True)
            refresh_token = create_refresh_token(identity={"id": user.id, "role": user.role})
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/refresh-jwt")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


def admin_required(role_required="admin"):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            jwt = get_jwt()
            if jwt.get("sub").get("role") != role_required:
                abort(401, message=f"{role_required.capitalize()} privilege required.")
            return func(*args, **kwargs)

        return wrapper

    return decorator


# def admin_required(func):
#     @wraps(func)
#     @jwt_required()
#     def wrapper(*args, **kwargs):
#         jwt = get_jwt()
#         if not jwt.get("sub").get("role") == "admin":
#             abort(401, message="Admin privilege required.")
#         return func(*args, **kwargs)
#
#     return wrapper

def get_user_id():
    jwt = get_jwt()
    return jwt.get("sub").get("id")
