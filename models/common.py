from db import db
from flask_smorest import abort


class CommonModel(db.Model):
    __abstract__ = True

    @classmethod
    def get_items(cls):
        return cls.query.all()

    @classmethod
    def get_item(cls, item_id):
        item = db.session.get(cls, item_id)
        if item is None:
            abort(404, message="Item not found")
        return item

    def add_item(self):
        try:
            with db.session.begin():
                db.session.add(self)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_item(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update_item(self, item_data):
        try:
            for key, value in item_data.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
