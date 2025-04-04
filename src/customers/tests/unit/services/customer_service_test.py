import pytest
from unittest.mock import MagicMock, patch
from app.services.customer_service import CustomerService, is_valid_email, validate_uuid, is_valid_data
from app.models.customer_model import Customer
from app.exceptions.http_exceptions import BadRequestError, NotFoundError, UnauthorizedError, ForbiddenError


@pytest.fixture
def mock_customer_data():
     return Customer ({
        "identificationType": "CC",
        "identificationNumber": "123456789",
        "country": "Colombia",
        "city": "Bogotá",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez@example.com"
        }
    })

def test_validate_uuid():
    assert validate_uuid("4e49e816-e4b0-4d94-974b-8b35d905ae21") is True
    assert validate_uuid("invalid-uuid") is False

def test_is_valid_email():
    assert is_valid_email("test@example.com") is True
    assert is_valid_email("invalid-email") is False

def test_is_valid_data():
    assert is_valid_data("Colombia") is True
    assert is_valid_data("Bogotá") is True
    assert is_valid_data("12345") is False
    assert is_valid_data("Colombia123") is False

@patch("app.repositories.customer_repository.CustomerRepository.get_all")
def test_get_all_customers_success(mock_get_all):
    mock_customers = [
        Customer(
            identification_type="CC",
            identification_number=123456789,
            country="Colombia",
            city="Bogotá",
            address="Calle 123",
            user_id="4e49e816-e4b0-4d94-974b-8b35d905ae21"
        )
    ]
    mock_get_all.return_value = mock_customers

    result = CustomerService.get_all()
    assert len(result) == 1
    assert result[0].country == "Colombia"


@patch("app.repositories.customer_repository.CustomerRepository.get_all")
def test_get_all_customers_no_data(mock_get_all):
    mock_get_all.return_value = []

    with pytest.raises(ValueError, match="No hay clientes registrados"):
        CustomerService.get_all()

@patch("app.repositories.customer_repository.CustomerRepository.create")
@patch("app.services.customer_service.requests.post")
def test_create_customer_success(mock_post, mock_create, mock_customer_data):
    # Simular respuesta del servicio de usuarios
    mock_post.return_value = MagicMock(
        status_code=201,
        json=lambda: {"data": {"id": "4e49e816-e4b0-4d94-974b-8b35d905ae21"}}
    )

    # Simular creación del cliente
    mock_create.return_value = Customer(
        identification_type="CC",
        identification_number=123456789,
        country="Colombia",
        city="Bogotá",
        address="Calle 123",
        user_id="4e49e816-e4b0-4d94-974b-8b35d905ae21"
    )

    result = CustomerService.create(mock_customer_data)
    assert result.identification_type == "CC"
    assert result.country == "Colombia"

@patch("app.services.customer_service.requests.post")
def test_create_customer_user_service_error(mock_post, mock_customer_data):
    # Simular error del servicio de usuarios
    mock_post.return_value = MagicMock(
        status_code=400,
        json=lambda: {"error": "El email ya está registrado"}
    )

    with pytest.raises(BadRequestError, match="Error al crear el usuario: El email ya está registrado"):
        CustomerService.create(mock_customer_data)

def test_create_customer_missing_identification_type(mock_customer_data):
    mock_customer_data.pop("identificationType")

    with pytest.raises(BadRequestError, match="El tipo de identificación es requerido"):
        CustomerService.create(mock_customer_data)


def test_create_customer_invalid_identification_type(mock_customer_data):
    mock_customer_data["identificationType"] = "INVALID"

    with pytest.raises(BadRequestError, match="El tipo de identificación no es válido, debe ser CC, NIT, CE, DNI o PASSPORT"):
        CustomerService.create(mock_customer_data)


def test_create_customer_missing_user_data(mock_customer_data):
    mock_customer_data.pop("user")

    with pytest.raises(BadRequestError, match="Los datos del cliente son requeridos"):
        CustomerService.create(mock_customer_data)


def test_create_customer_invalid_email(mock_customer_data):
    mock_customer_data["user"]["email"] = "invalid-email"

    with pytest.raises(BadRequestError, match="El email no es válido"):
        CustomerService.create(mock_customer_data)