from sanic import Blueprint

from .views import AuthUserView

user_bp = Blueprint('authentication', url_prefix='/users')

user_bp.add_route(AuthUserView.as_view(), '/login')
user_bp.add_route(AuthUserView.as_view(), '/register')
