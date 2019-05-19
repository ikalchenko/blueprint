from .extensions import db


class BaseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # date_created = db.Column(db.DateTime, server_default=db.func.now())
    # date_modified = db.Column(db.DateTime, server_default=db.func.now())

    def serialize(self):
        pass
