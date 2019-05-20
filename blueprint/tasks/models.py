from ..models import BaseModel
from ..extensions import db


class Task(BaseModel):
    __tablename__ = 'tasks'

    title = db.Column(db.String)
    converted_suggestion = db.Column(None, db.ForeignKey('suggestions.id'))
    trip_id = db.Column(None, db.ForeignKey('trips.id'))
    importance = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'trip_id': self.trip_id,
            'importance': self.importance
        }


class Suggestion(BaseModel):
    __tablename__ = 'suggestions'

    title = db.Column(db.String)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title
        }
