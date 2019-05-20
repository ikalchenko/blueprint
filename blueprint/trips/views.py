from datetime import datetime

from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_jwt.decorators import protected, inject_user

from .models import Trip, UsersTrip
from .validators import NewTripValidator


class TripsView(HTTPMethodView):
    decorators = [protected(), inject_user()]

    async def post(self, request, user):
        trip_title = request.json.get('title')
        trip_country = request.json.get('country')
        trip_city = request.json.get('city')
        trip_date = request.json.get('date')

        trip_validator = NewTripValidator(title=trip_title,
                                          city=trip_city,
                                          country=trip_country,
                                          date=trip_date)

        if not await trip_validator.is_valid():
            return json({'status': 'failed validation',
                         'errors': trip_validator.errors})
        trip = await Trip.create(title=trip_title,
                                 city=trip_city,
                                 country=trip_country,
                                 date=datetime.strptime(trip_date, '%Y-%m-%d').date())

        await UsersTrip.create(user_id=user.id,
                               trip_id=trip.id,
                               is_owner=True)
        return json(trip.serialize())

    async def get(self, request, user):
        trips = await UsersTrip.join(Trip).select(UsersTrip.user_id == user.id).gino.all()
        trips = [Trip(id=trip[4], title=trip[5], country=trip[6], city=trip[7], date=trip[8]) for trip in trips]
        return json([trip.serialize() for trip in trips])


class TripDetailView(HTTPMethodView):
    decorators = [protected(), inject_user()]

    async def get(self, request, trip_id, user):
        users_trip = await UsersTrip.query.where(UsersTrip.user_id == user.id)\
                                          .where(UsersTrip.trip_id == int(trip_id)).gino.first()
        if not users_trip:
            return json({'status': 'not found'}, status=404)
        trip = await Trip.get(int(trip_id))
        return json(trip.serialize())

    async def delete(self, request, trip_id, user):
        users_trip = await UsersTrip.query.where(UsersTrip.user_id == user.id)\
                                          .where(UsersTrip.trip_id == int(trip_id))\
                                          .where(UsersTrip.is_owner == True).gino.first()
        if not users_trip:
            return json({'status': 'not found'}, status=404)
        await Trip.delete.where(Trip.id == int(trip_id)).gino.status()
        return json({'status': 'deleted'})

    async def patch(self, request, trip_id, user):
        new_title = request.json.get('title')
        new_country = request.json.get('country')
        new_city = request.json.get('city')
        new_date = request.json.get('date')

        users_trip = await UsersTrip.query.where(UsersTrip.user_id == user.id) \
            .where(UsersTrip.trip_id == int(trip_id)).gino.first()
        if not users_trip:
            return json({'status': 'not found'}, status=404)
        trip = await Trip.get(int(trip_id))
        await trip.update(title=new_title, country=new_country, city=new_city,
                          date=datetime.strptime(new_date, '%Y-%m-%d').date()).apply()
        return json({'status': 'modified',
                     'trip': trip.serialize()})

