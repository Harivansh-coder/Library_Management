# library management system app initialization
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize the database, marshmallow and jwt manager
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

# Rate limit configuration
limiter = Limiter(key_func=get_remote_address)


def create_app(config_name=None):
    app = Flask(__name__)

    # config in case of testing
    if config_name == "testing":
        app.config.from_object('config.TestingConfig')

    # Load configurations from config.py
    app.config.from_object('config.Config')
    # Rate limit configuration
    limiter.init_app(app)

    # Importing routes
    from app.routes import routes
    app.register_blueprint(routes)
    # Initialize the database, marshmallow and jwt manager

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    return app
