from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from models import ReviewModel
from schemas import ReviewSchema
from resources.auth import get_user_id

blp = Blueprint("reviews", "reviews", description="Operations on reviews", url_prefix="reviews")


@blp.route('/')
class Books(MethodView):
    @blp.response(200, ReviewSchema(many=True))
    def get(self):
        return ReviewModel.get_items()

    @blp.arguments(ReviewSchema)
    @blp.response(200, ReviewSchema)
    @jwt_required()
    def post(self, review_data):
        user_id = get_user_id()
        review = ReviewModel(**review_data, user_id=user_id)
        try:
            existing_review = ReviewModel.query.filter(
                ReviewModel.book_id == review.book_id,
                ReviewModel.user_id == user_id
            ).first()

            if existing_review:
                abort(400, message="You have already reviewed this book.")

            review.add_item()
        except SQLAlchemyError as e:
            print(e)
            abort(500, message="An error occurred while inserting the review.")

        return review


@blp.route('/<int:review_id>')
class Book(MethodView):
    @blp.response(200, ReviewSchema)
    def get(self, review_id):
        review = ReviewModel.get_item(review_id)
        return review

    @blp.arguments(ReviewSchema)
    @blp.response(200, ReviewSchema)
    def put(self, review_data, review_id):
        review = ReviewModel.get_item(review_id)
        try:
            review.update_item(review_data)
            return review
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the review.")

    def delete(self, review_id):
        review = ReviewModel.get_item(review_id)
        review.delete_item()
        return {"message": "Review deleted"}
