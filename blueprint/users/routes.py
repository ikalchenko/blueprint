from sanic import Blueprint

from .views import RegisterUserView

user_bp = Blueprint('users', url_prefix='/users')

user_bp.add_route(RegisterUserView.as_view(), '/register')
