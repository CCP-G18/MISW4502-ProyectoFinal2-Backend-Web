import pytest
from flask import Flask
from flask_jwt_extended import JWTManager
from app.controllers.user_controller import user_bp
from app.models.user_model import User
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


def test_get_users(mocker, client):
    mock_users = [User(name="Test1", lastname="User1", email="test1@example.com", password="123456"),
                  User(name="Test2", lastname="User2", email="test2@example.com", password="123456")]
    
    mocker.patch("app.services.user_service.UserService.get_all", return_value=mock_users)
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert len(data["data"]) == 2


def test_get_user(mocker, client):
    mock_user = User(name="Test", lastname="User", email="test@example.com", password="123456")
    
    mocker.patch("app.services.user_service.UserService.get_by_id", return_value=mock_user)
    mocker.patch("app.controllers.user_controller.jwt_required", lambda fn: fn)
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", return_value=None)
    mocker.patch("app.controllers.user_controller.get_jwt_identity", return_value=1)

    response = client.get("/users/1")
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["data"]["email"] == "test@example.com"


def test_get_user_not_found(mocker, client):
    # Mock de la función que debe lanzar un NotFoundError
    mocker.patch("app.services.user_service.UserService.get_by_id", side_effect=NotFoundError("Usuario no encontrado"))
    
    # Mock de Flask-JWT-Extended decoradores y métodos
    mocker.patch("app.controllers.user_controller.jwt_required", lambda fn: fn)
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", return_value=None)
    mocker.patch("app.controllers.user_controller.get_jwt_identity", return_value=99)

    # Ejecutar la solicitud
    response = client.get("/users/99")
    
    # Verificaciones
    assert response.status_code == 404
    data = response.get_json()
    assert data["status"] == "error"
    assert "Usuario no encontrado" in data["error"]



def test_create_user(mocker, client):
    mock_user = User(name="Test", lastname="User", email="test@example.com", password="123456")
    
    mocker.patch("app.services.user_service.UserService.create", return_value=mock_user)
    
    response = client.post("/users/", json={
        "name": "Test",
        "lastname": "User",
        "email": "test@example.com",
        "password": "123456"
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"
    assert data["data"]["email"] == "test@example.com"


def test_update_user_status(mocker, client):
    mock_user = User(name="Test", lastname="User", email="test@example.com", password="123456")
    
    # Mocks necesarios
    mocker.patch("app.services.user_service.UserService.update_status", return_value=mock_user)
    mocker.patch("app.controllers.user_controller.get_jwt_identity", return_value=1)
    mocker.patch("app.controllers.user_controller.jwt_required", lambda fn: fn)
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", return_value=None)
    
    response = client.patch("/users/", json={"status": "ACTIVE"})
    
    # Verificar respuesta
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["data"]["email"] == "test@example.com"



def test_ping(client):
    response = client.get("/users/ping")
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["message"] == "pong"
