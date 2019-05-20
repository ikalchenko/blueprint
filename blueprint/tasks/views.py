from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_jwt import protected, inject_user

from .models import Task
from .validators import NewTaskValidator
from ..trips.models import UsersTrip


class TasksView(HTTPMethodView):
    decorators = [protected(), inject_user()]

    async def post(self, request, trip_id, user):
        task_title = request.json.get('title')
        task_suggestion = request.json.get('converted_suggestion', None)
        task_importance = request.json.get('importance', 0)

        task_validator = NewTaskValidator(title=task_title)

        if not await task_validator.is_valid():
            return json({'status': 'failed validation',
                         'errors': task_validator.errors})

        users_trip = await UsersTrip.query.where(UsersTrip.user_id == user.id) \
            .where(UsersTrip.trip_id == int(trip_id)).gino.first()
        if not users_trip:
            return json({'status': 'not found'}, status=404)

        task = await Task.create(title=task_title,
                                 trip_id=int(trip_id),
                                 converted_suggestion=task_suggestion,
                                 importance=task_importance)

        return json(task.serialize())

    async def get(self, request, trip_id, user):
        users_trip = await UsersTrip.query.where(UsersTrip.user_id == user.id) \
            .where(UsersTrip.trip_id == int(trip_id)).gino.first()
        if not users_trip:
            return json({'status': 'not found'}, status=404)
        tasks = await Task.query.where(Task.trip_id == int(trip_id)).gino.all()
        return json({'tasks': [task.serialize() for task in tasks],
                     'suggestions': []})


class TaskDetailView(HTTPMethodView):
    decorators = [protected(), inject_user()]

    async def delete(self, request, trip_id, task_id, user):
        users_trip = await UsersTrip.query.where(UsersTrip.user_id == user.id) \
            .where(UsersTrip.trip_id == int(trip_id)).gino.first()
        if not users_trip:
            return json({'status': 'not found'}, status=404)
        await Task.delete.where(Task.id == int(task_id)).gino.status()
        return json({'status': 'deleted'})

    async def put(self, request, trip_id, task_id, user):
        new_title = request.json.get('title')
        new_suggestion = request.json.get('converted_suggestion', None)
        new_importance = request.json.get('importance', 0)

        task_validator = NewTaskValidator(title=new_title)

        if not await task_validator.is_valid():
            return json({'status': 'failed validation',
                         'errors': task_validator.errors})

        users_trip = await UsersTrip.query.where(UsersTrip.user_id == user.id) \
            .where(UsersTrip.trip_id == int(trip_id)).gino.first()

        if not users_trip:
            return json({'status': 'not found'}, status=404)

        task = await Task.get(int(task_id))
        await task.update(title=new_title,
                          trip_id=int(trip_id),
                          converted_suggestion=new_suggestion,
                          importance=new_importance).apply()
        return json({'status': 'modified',
                     'task': task.serialize()})
