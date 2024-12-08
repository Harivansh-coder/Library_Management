import os

# load .env file
from dotenv import load_dotenv

load_dotenv()

# Config class to store configuration variables


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///library.db')  # Default to SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.getenv('JWT_SECRET')
    JWT_ACCESS_TOKEN_EXPIRES = int(
        os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
