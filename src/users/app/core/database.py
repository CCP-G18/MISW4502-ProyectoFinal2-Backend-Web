import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import inspect, text

db = SQLAlchemy()
ma = Marshmallow()

def init_db(app):
    db.init_app(app)
    ma.init_app(app)
    
    with app.app_context():
        db.create_all()
        inspector = inspect(db.engine)
        if "users" in inspector.get_table_names():
            result = db.session.execute(text("SELECT COUNT(*) FROM users")).scalar()
            if result == 0:
                base_dir = os.path.dirname(__file__)
                sql_file = os.path.join(base_dir, "data.sql")
                if os.path.exists(sql_file):
                    with open(sql_file, "r") as f:
                        sql_statements = f.read()
                        db.session.execute(text(sql_statements))
                        db.session.commit()
                    print("Datos iniciales insertados correctamente en la base de datos.")