from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def init_db(app):
  db.init_app(app)
  ma.init_app(app)

  with app.app_context():
    db.drop_all()
    db.create_all()