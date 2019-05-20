from ..users.models import User
from ..models import BaseModel
from ..extensions import db


class Trip(BaseModel):
    __tablename__ = 'trips'

    title = db.Column(db.String)
    country = db.Column(db.String)
    city = db.Column(db.String)
    date = db.Column(db.DateTime)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'country': self.country,
            'city': self.city,
            'date': self.date
        }


class UsersTrip(BaseModel):
    __tablename__ = 'users_trips'

    user_id = db.Column(None, db.ForeignKey('users.id'))
    trip_id = db.Column(None, db.ForeignKey('trips.id'))
    is_owner = db.Column(db.Boolean)

    async def serialize(self):
        user = await User.query.get(self.user_id)
        trip = await Trip.query.get(self.trip_id)
        return {
            'id': self.id,
            'user': user.serialize(),
            'trip': trip.serialize(),
            'is_owner': self.is_owner,
        }
