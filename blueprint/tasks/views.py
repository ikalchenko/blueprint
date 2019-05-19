from sanic.response import json
from sanic.views import HTTPMethodView
from simple_bcrypt import generate_password_hash, check_password_hash

from ..users.validators import NewUserValidator
from ..users.models import User


async def authenticate(request):
    reject_json = {'status': 'failed authentication',
                   'errors': 'Wrong email or password'}
    user_email = request.json.get('email')
    user_password = request.json.get('password')

    user = await User.query.where(User.email == user_email).gino.first()
    if not user or not check_password_hash(user.password, user_password):
        return json(reject_json)

    return user


class RegisterUserView(HTTPMethodView):

    async def post(self, request):
        new_user_email = request.json.get('email')
        new_user_password = request.json.get('password')
        new_user_first_name = request.json.get('first_name')
        new_user_last_name = request.json.get('last_name')

        user_validator = NewUserValidator(first_name=new_user_first_name,
                                          last_name=new_user_last_name,
                                          email=new_user_email,
                                          password=new_user_password)

        if not await user_validator.is_valid():
            return json({'status': 'failed validation',
                         'errors': user_validator.errors})

        await User.create(first_name=new_user_first_name,
                          last_name=new_user_last_name,
                          email=new_user_email,
                          password=generate_password_hash(new_user_password))

        return json({'status': 'created'}, status=201)
