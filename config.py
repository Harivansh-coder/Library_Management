import os

# load .env file
from dotenv import load_dotenv

load_dotenv()

# Config class to store configuration variables
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'database.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'thisissecretforincasenotenv')
    JWT_ACCESS_TOKEN_EXPIRES = int(
        os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    RATELIMIT_DEFAULT = "30 per minute"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    JWT_ACCESS_TOKEN_EXPIRES = 3
    RATELIMIT_DEFAULT = "5 per minute"
