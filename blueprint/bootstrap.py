import os

from sanic import Sanic
from .extensions import db
from .routes import root_bp
from .users.routes import user_bp


def run_app():
    app = Sanic('Blueprint')

    app.config.DB_HOST = os.getenv('DB_HOST')
    app.config.DB_PORT = os.getenv('DB_PORT')
    app.config.DB_USER = os.getenv('DB_USER')
    app.config.DB_PASSWORD = os.getenv('DB_PASSWORD')
    app.config.DB_DATABASE = os.getenv('DB_DATABASE')

    db.init_app(app)

    app.blueprint(user_bp)
    app.blueprint(root_bp)

    app.run(host='0.0.0.0', port=8080, debug=True)
