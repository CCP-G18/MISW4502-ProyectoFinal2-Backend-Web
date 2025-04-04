import pytest
from flask import Flask
from flask_jwt_extended import JWTManager

# Importaciones del proyecto
from app.controllers.auth_controller import auth_bp
from app.models.user_model import User
from app.exceptions.http_exceptions import UnauthorizedError, NotFoundError

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "test-secret"
    app.config["TESTING"] = True
    JWTManager(app)
    app.register_blueprint(auth_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()


def test_login_success(mocker, client):
    # Crear un usuario real
    mock_user = User(
        name="Test",
        lastname="User",
        email="test@example.com",
        password="123456",
        role="admin",
    )

    # Mock del servicio y del token
    mocker.patch("app.services.user_service.UserService.check_credentials", return_value=mock_user)
    mocker.patch("app.controllers.auth_controller.create_access_token", return_value="fake-jwt-token")

    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "access_token" in data["data"]
    assert data["data"]["user"]["email"] == "test@example.com"


def test_login_unauthorized(mocker, client):
    mocker.patch("app.services.user_service.UserService.check_credentials", side_effect=UnauthorizedError("Credenciales inválidas"))

    response = client.post("/login", json={
        "email": "wrong@example.com",
        "password": "wrongpass"
    })

    assert response.status_code == 401
    data = response.get_json()
    assert data["status"] == "error"
    assert "error" in data


def test_verify_success(mocker, client):
    # Usuario simulado
    mock_user = User(
        name="Test",
        lastname="User",
        email="test@example.com",
        password="123456",
        role="admin",
    )

    # Mocks necesarios
    mocker.patch("app.controllers.auth_controller.jwt_required", lambda *args, **kwargs: lambda f: f)
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("app.controllers.auth_controller.get_jwt_identity", return_value=1)
    mocker.patch("app.services.user_service.UserService.get_by_id_and_status", return_value=mock_user)

    response = client.get("/verify", headers={"Authorization": "Bearer fake-token"})

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["data"]["email"] == "test@example.com"


def test_verify_user_not_found(mocker, client):
    mocker.patch("app.controllers.auth_controller.jwt_required", lambda *args, **kwargs: lambda f: f)
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("app.controllers.auth_controller.get_jwt_identity", return_value=99)
    mocker.patch("app.services.user_service.UserService.get_by_id_and_status", side_effect=NotFoundError("Usuario no encontrado"))

    response = client.get("/verify", headers={"Authorization": "Bearer fake-token"})

    assert response.status_code == 404
    data = response.get_json()
    assert data["status"] == "error"
    assert "error" in data
