from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import UserModel
from schemas import UserSchema

blp = Blueprint("users", "users", description="Operations on users", url_prefix="users")


@blp.route('/')
class Users(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.get_users()

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, user_data):
        user = UserModel(**user_data)
        try:
            user.add_user()
        except IntegrityError:
            abort(400, message="A user with that username already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while add the user.")

        return user


@blp.route('/<int:book_id>')
class Book(MethodView):
    @blp.response(200, UserSchema)
    def get(self, book_id):
        user = UserModel.get_user(book_id)
        return user

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.get_user(user_id)
        try:
            user.update_user(user_data)
            return user
        except IntegrityError:
            abort(400, message="A user with that username already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while add the user.")

    def delete(self, book_id):
        user = UserModel.get_user(book_id)
        user.delete_user()
        return {"message": "User deleted"}
