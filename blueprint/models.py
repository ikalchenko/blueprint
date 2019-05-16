from .extensions import db


class BaseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now())


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)


class List(BaseModel):
    __tablename__ = 'lists'

    title = db.Column(db.String)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))


class Trip(BaseModel):
    __tablename__ = 'trips'


class Task(BaseModel):
    __tablename__ = 'tasks'


class Suggestion(BaseModel):
    __tablename__ = 'suggestions'
