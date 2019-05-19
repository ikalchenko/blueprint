from sanic.response import json
from sanic_jwt import BaseEndpoint
from simple_bcrypt import generate_password_hash, check_password_hash

from ..users.validators import UserValidator
from ..users.models import User


class LoginUserView(BaseEndpoint):

    async def post(self, request):
        return json({'hello': 'world'})


class LogoutUserView(BaseEndpoint):

    async def post(self, request):
        pass


class RegisterUserView(BaseEndpoint):

    async def post(self, request):
        new_user_email = request.json.get('email')
        new_user_password = request.json.get('password')
        new_user_first_name = request.json.get('first_name')
        new_user_last_name = request.json.get('last_name')

        user_validator = UserValidator(first_name=new_user_first_name,
                                       last_name=new_user_last_name,
                                       email=new_user_email,
                                       password=new_user_password)

        if not user_validator.is_valid():
            return json({'status': 'failed validation',
                         'errors': user_validator.errors})

        user = User(first_name=new_user_first_name,
                    last_name=new_user_last_name,
                    email=new_user_email,
                    password=generate_password_hash(new_user_password))

        await user.save()
        return json({'status': 'created'}, status=201)
