from ..models import BaseModel
from ..extensions import db


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def to_dict(self):
        return {'user_id': self.id}

    def serialize(self):
        return {
            'id': self.user,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }
