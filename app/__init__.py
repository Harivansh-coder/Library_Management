# library management system app initialization
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    # Load configurations from config.py
    app.config.from_object('config.Config')
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    return app
