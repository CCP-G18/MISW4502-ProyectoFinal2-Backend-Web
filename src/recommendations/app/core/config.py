import os
from datetime import timedelta

class Config:
  SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_DB_URI')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)