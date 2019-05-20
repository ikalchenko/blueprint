from sanic.response import json
from simple_bcrypt import check_password_hash

from ..users.models import User


async def retrieve_user(request, payload, *args, **kwargs):
    if payload:
        user_id = payload.get('user_id', None)
        user = await User.get(user_id)
        return user
    else:
        return None


async def authenticate(request):
    reject_json = {'status': 'failed authentication',
                   'errors': 'Wrong email or password'}
    user_email = request.json.get('email')
    user_password = request.json.get('password')

    user = await User.query.where(User.email == user_email).gino.first()
    if not user or not check_password_hash(user.password, user_password):
        return json(reject_json)

    return user
