class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = 'super-secret'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
