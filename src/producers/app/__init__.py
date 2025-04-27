import os
from flask import Flask, request, make_response
from flask_cors import CORS
from app.core.config import Config
from app.core.routes import register_routes
from app.core.database import init_db
from app.core.jwt import init_jwt

def create_app(config = Config):
    allowed_origins = os.getenv("ALLOWED_ORIGINS").split(",")
    print("Allowed origins:", allowed_origins)
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, resources={r"/*": {"origins": allowed_origins}})

    @app.before_request
    def handle_options_requests():
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Authorization,Content-Type'
            return response

    init_db(app)
    init_jwt(app)
    register_routes(app)

    return app