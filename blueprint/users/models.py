from ..models import BaseModel
from ..extensions import db


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
