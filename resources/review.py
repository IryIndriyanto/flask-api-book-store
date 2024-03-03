from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import ReviewModel
from schemas import ReviewSchema

blp = Blueprint("reviews", "reviews", description="Operations on reviews", url_prefix="reviews")


@blp.route('/')
class Books(MethodView):
    @blp.response(200, ReviewSchema(many=True))
    def get(self):
        return ReviewModel.get_reviews()

    @blp.arguments(ReviewSchema)
    @blp.response(200, ReviewSchema)
    def post(self, review_data):
        review = ReviewModel(**review_data)
        try:
            review.add_review()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the review.")

        return review


@blp.route('/<int:review_id>')
class Book(MethodView):
    @blp.response(200, ReviewSchema)
    def get(self, review_id):
        review = ReviewModel.get_review(review_id)
        return review

    @blp.arguments(ReviewSchema)
    @blp.response(200, ReviewSchema)
    def put(self, review_data, review_id):
        review = ReviewModel.get_review(review_id)
        try:
            review.update_review(review_data)
            return review
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the review.")

    def delete(self, review_id):
        review = ReviewModel.get_review(review_id)
        review.delete_review()
        return {"message": "Review deleted"}
