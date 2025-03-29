import pytest
from unittest.mock import MagicMock, patch
from app.services.user_service import UserService, is_valid_email, validate_uuid
from app.models.user_model import User, StatusEnum
from app.exceptions.http_exceptions import BadRequestError, NotFoundError, UnauthorizedError, ForbiddenError


@pytest.fixture
def mock_user():
    return User(
        name="Test",
        lastname="User",
        email="test@example.com",
        password="123456"
    )


def test_validate_uuid():
    assert validate_uuid("4e49e816-e4b0-4d94-974b-8b35d905ae21") is True
    assert validate_uuid("invalid-uuid") is False


def test_is_valid_email():
    assert is_valid_email("test@example.com") is True
    assert is_valid_email("invalid-email") is False


@patch("app.repositories.user_repository.UserRepository.get_all")
def test_get_all_success(mock_get_all, mock_user):
    mock_get_all.return_value = [mock_user]
    result = UserService.get_all()
    assert len(result) == 1


@patch("app.repositories.user_repository.UserRepository.get_all")
def test_get_all_no_users(mock_get_all):
    mock_get_all.return_value = []
    with pytest.raises(ValueError, match="No hay usuarios registrados"):
        UserService.get_all()


@patch("app.repositories.user_repository.UserRepository.get_by_id")
def test_get_by_id_success(mock_get_by_id, mock_user):
    mock_get_by_id.return_value = mock_user
    result = UserService.get_by_id("4e49e816-e4b0-4d94-974b-8b35d905ae21")
    assert result == mock_user


@patch("app.repositories.user_repository.UserRepository.get_by_id")
def test_get_by_id_not_found(mock_get_by_id):
    mock_get_by_id.return_value = None
    with pytest.raises(NotFoundError, match="Usuario no encontrado"):
        UserService.get_by_id("4e49e816-e4b0-4d94-974b-8b35d905ae21")


@patch("app.repositories.user_repository.UserRepository.get_by_id")
def test_get_by_id_and_status_success(mock_get_by_id, mock_user):
    mock_user.status = StatusEnum.ACTIVE
    mock_get_by_id.return_value = mock_user
    result = UserService.get_by_id_and_status("4e49e816-e4b0-4d94-974b-8b35d905ae21")
    assert result == mock_user


@patch("app.repositories.user_repository.UserRepository.get_by_id")
def test_get_by_id_and_status_blocked(mock_get_by_id, mock_user):
    mock_user.status = StatusEnum.BLOCKED
    mock_get_by_id.return_value = mock_user
    with pytest.raises(ForbiddenError, match="Tu cuenta ha sido bloqueada. Contacta al soporte del G18 para más información."):
        UserService.get_by_id_and_status("4e49e816-e4b0-4d94-974b-8b35d905ae21")


@patch("app.repositories.user_repository.UserRepository.get_by_email")
def test_get_by_email_success(mock_get_by_email, mock_user):
    mock_get_by_email.return_value = mock_user
    result = UserService.get_by_email("test@example.com")
    assert result == mock_user


@patch("app.repositories.user_repository.UserRepository.get_by_email")
def test_get_by_email_invalid_email(mock_get_by_email):
    with pytest.raises(BadRequestError, match="El email no es válido"):
        UserService.get_by_email("invalid-email")


@patch("app.repositories.user_repository.UserRepository.create")
@patch("app.repositories.user_repository.UserRepository.get_by_email", return_value=None)
def test_create_user_success(mock_get_by_email, mock_create, mock_user):
    mock_create.return_value = mock_user
    result = UserService.create({
        "name": "Test",
        "lastname": "User",
        "email": "test@example.com",
        "password": "123456"
    })
    assert result == mock_user


@patch("app.repositories.user_repository.UserRepository.get_by_id")
@patch("app.repositories.user_repository.UserRepository.update")
def test_update_user_status_success(mock_update, mock_get_by_id, mock_user):
    mock_get_by_id.return_value = mock_user
    result = UserService.update_status("4e49e816-e4b0-4d94-974b-8b35d905ae21", {"status": "ACTIVE"})
    assert result == mock_user


@patch("app.repositories.user_repository.UserRepository.get_by_email")
@patch("app.repositories.user_repository.UserRepository.get_by_username")
def test_check_credentials_success(mock_get_by_email, mock_get_by_username, mock_user):
    mock_user.check_password = MagicMock(return_value=True)
    mock_get_by_email.return_value = None
    mock_get_by_username.return_value = mock_user
    result = UserService.check_credentials({"username": "testuser", "password": "123456"})
    assert result == mock_user


@patch("app.repositories.user_repository.UserRepository.get_by_email")
@patch("app.repositories.user_repository.UserRepository.get_by_username")
def test_check_credentials_invalid(mock_get_by_email, mock_get_by_username):
    mock_get_by_email.return_value = None
    mock_get_by_username.return_value = None
    with pytest.raises(UnauthorizedError, match="Credenciales inválidas"):
        UserService.check_credentials({"username": "invaliduser", "password": "wrongpassword"})
