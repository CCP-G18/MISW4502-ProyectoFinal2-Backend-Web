import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False