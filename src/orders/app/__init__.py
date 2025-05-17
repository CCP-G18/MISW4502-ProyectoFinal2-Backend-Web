import os
from flask import Flask
from flask_cors import CORS
from app.core.config import Config
from app.core.routes import register_routes
from app.core.database import init_db
from app.core.jwt import init_jwt
from app.extensions import socketio
from apscheduler.schedulers.background import BackgroundScheduler
from app.jobs.auto_update_delivered_orders import auto_update_delivered_orders

def create_app(config = Config):
    allowed_origins = os.getenv("ALLOWED_ORIGINS").split(",")
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, resources={r"/*": {"origins": allowed_origins}})
    init_db(app)
    init_jwt(app)    
    register_routes(app)

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: auto_update_delivered_orders(app), 'interval', minutes=int(os.getenv("EXECUTION_MINUTES_JOB")))
    scheduler.start()
    socketio.init_app(app)
    
    return app