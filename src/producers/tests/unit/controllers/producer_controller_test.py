import pytest
from flask import Flask
from flask_jwt_extended import JWTManager
from app.controllers.producer_controller import user_bp
from app.exceptions.http_exceptions import NotFoundError, BadRequestError


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "test-secret"
    app.config["TESTING"] = True
    JWTManager(app)
    app.register_blueprint(user_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()