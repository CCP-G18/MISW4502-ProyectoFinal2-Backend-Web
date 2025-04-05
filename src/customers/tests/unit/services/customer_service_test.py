import pytest
from unittest.mock import MagicMock, patch
from app.services.customer_service import CustomerService, validate_uuid, is_valid_data
from app.models.customer_model import Customer
from app.exceptions.http_exceptions import BadRequestError


@pytest.fixture
def mock_customer_data():
    return Customer(
        identification_type="CC",
        identification_number=123456789,
        country="Colombia",
        city="Bogotá",
        address="Calle 123",
        user_id="4e49e816-e4b0-4d94-974b-8b35d905ae21"
    )

@pytest.fixture
def mock_customer():
    return  {
        "identificationType": "CC",
        "identificationNumber": 123456789,
        "country": "Estados Unidos",
        "city": "New York",
        "address": "Calle 123",
        "user": {
            "name": "123",
            "lastname": "Pérez",
            "email": "juan.perez18@example.com",
            "password": "123456"
        }
    }
     
def test_validate_uuid():
    assert validate_uuid("4e49e816-e4b0-4d94-974b-8b35d905ae21") is True
    assert validate_uuid("invalid-uuid") is False

def test_is_valid_data():
    assert is_valid_data("Colombia") is True
    assert is_valid_data("Bogotá") is True
    assert is_valid_data("12345") is False
    assert is_valid_data("Colombia123") is False

@patch("app.repositories.customer_repository.CustomerRepository.get_all")
def test_get_all_customers_success(mock_get_all):
    mock_customers = {
        "code": 200,
        "data": [
            {
                "address": "Calle 123",
                "city": "Bogotá",
                "country": "Colombia",
                "created_at": "2025-04-03T22:30:52.658277",
                "id": "d3c14118-be62-4084-865d-01c1599bd024",
                "identification_number": 123456789,
                "identification_type": "CC",
                "updated_at": "2025-04-03T22:30:52.658277",
                "user_id": "7070484b-34aa-456d-bb51-3b0063a66662"
            },
            {
                "address": "Calle 123",
                "city": "Bogotá",
                "country": "Colombia",
                "created_at": "2025-04-03T22:48:29.275242",
                "id": "a49b48ee-d845-4e10-b9e7-dfc5a75af22d",
                "identification_number": 123456789,
                "identification_type": "CC",
                "updated_at": "2025-04-03T22:48:29.275242",
                "user_id": "a7f9baae-634d-4641-a3b9-02d4cf501130"
            }
        ],
        "message": "Todos los clientes han sido obtenidos",
        "status": "success"
    }
    mock_get_all.return_value = mock_customers

    result = CustomerService.get_all()
    assert len(result) == 4


@patch("app.repositories.customer_repository.CustomerRepository.get_all")
def test_get_all_customers_no_data(mock_get_all):
    mock_get_all.return_value = []

    with pytest.raises(ValueError, match="No hay clientes registrados"):
        CustomerService.get_all()

@patch("app.services.customer_service.requests.post")
def test_create_customer_user_service_error(mock_post, mock_customer):
    # Simular error del servicio de usuarios
    mock_post.return_value = MagicMock(
        status_code=400,
        json=lambda: {"error": "El email ya está registrado"}
    )

    with pytest.raises(BadRequestError, match="Error al crear el usuario: El email ya está registrado"):
        CustomerService.create(mock_customer)

def test_create_customer_missing_identification_type(mock_customer):
    mock_customer.pop("identificationType")

    with pytest.raises(BadRequestError, match="El tipo de identificación es requerido"):
        CustomerService.create(mock_customer)


def test_create_customer_invalid_identification_type(mock_customer):
    mock_customer["identificationType"] = "INVALID"

    with pytest.raises(BadRequestError, match="El tipo de identificación no es válido, debe ser CC, NIT, CE, DNI o PASSPORT"):
        CustomerService.create(mock_customer)

def test_create_customer_missing_identification_number(mock_customer):
    mock_customer.pop("identificationNumber")

    with pytest.raises(BadRequestError, match="El número de identificación es requerido"):
        CustomerService.create(mock_customer)


def test_create_customer_invalid_identification_type(mock_customer):
    mock_customer["identificationNumber"] = "INVALID"

    with pytest.raises(BadRequestError, match="El número de identificación no es válido, debe ser un valor numerico"):
        CustomerService.create(mock_customer)        

def test_create_customer_missing_country(mock_customer):
    mock_customer.pop("country")

    with pytest.raises(BadRequestError, match="El país es requerido"):
        CustomerService.create(mock_customer)

def test_create_customer_invalid_country(mock_customer):
    mock_customer["country"] = "Colombia123"

    with pytest.raises(BadRequestError, match="El país debe contener solo letras y espacios"):
        CustomerService.create(mock_customer)

def test_create_customer_missing_city(mock_customer):
    mock_customer.pop("city")

    with pytest.raises(BadRequestError, match="La ciudad es requerida"):
        CustomerService.create(mock_customer)

def test_create_customer_invalid_city(mock_customer):
    mock_customer["city"] = "Bogotá123"

    with pytest.raises(BadRequestError, match="La ciudad debe contener solo letras y espacios"):
        CustomerService.create(mock_customer)

def test_create_customer_missing_address(mock_customer):
    mock_customer.pop("address")

    with pytest.raises(BadRequestError, match="La dirección es requerida"):
        CustomerService.create(mock_customer)

def test_create_customer_missing_user_data(mock_customer):
    mock_customer.pop("user")

    with pytest.raises(BadRequestError, match="Los datos del cliente son requeridos"):
        CustomerService.create(mock_customer)