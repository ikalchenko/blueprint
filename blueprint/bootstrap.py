import os

from sanic import Sanic
from sanic_jwt import Initialize
from .extensions import db
from .routes import root_bp
from .users.routes import user_bp
from .users.views import authenticate
from .tasks.routes import task_bp
from .trips.routes import trip_bp


class BlueprintAppRunner:
    def __init__(self):
        self.app = Sanic('Blueprint')
        self.db = db
        self._init_config()
        self._init_db()
        self._init_auth()
        self._init_routes()

    def _init_config(self):
        self.app.config.DB_HOST = os.getenv('DB_HOST')
        self.app.config.DB_PORT = os.getenv('DB_PORT')
        self.app.config.DB_USER = os.getenv('DB_USER')
        self.app.config.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.app.config.DB_DATABASE = os.getenv('DB_DATABASE')
        self.app.config.SANIC_JWT_SECRET = os.getenv('JWT_SECRET')

    def _init_db(self):
        self.db.init_app(self.app)

    def _init_auth(self):
        Initialize(self.app, authenticate=authenticate)

    def _init_routes(self):
        self.app.blueprint(user_bp)
        self.app.blueprint(task_bp)
        self.app.blueprint(trip_bp)
        self.app.blueprint(root_bp)

    def run(self):
        self.app.run(host='0.0.0.0', port=8080, debug=True)
