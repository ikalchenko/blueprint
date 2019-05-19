from sanic import Blueprint

from .views import LoginUserView, RegisterUserView, LogoutUserView

user_bp = Blueprint('authentication', url_prefix='/users')

user_bp.add_route(LoginUserView.as_view(), '/login')
user_bp.add_route(LogoutUserView.as_view(), '/login')
user_bp.add_route(RegisterUserView.as_view(), '/register')
