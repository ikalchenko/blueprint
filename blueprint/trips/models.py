from ..models import BaseModel


class Trip(BaseModel):
    __tablename__ = 'trips'


class UsersTrip(BaseModel):
    __tablename__ = 'users_trips'
