import pytest
from unittest.mock import MagicMock, patch
from app.services.customer_service import CustomerService, validate_uuid, is_valid_data
from app.models.customer_model import Customer, DocumentTypeEnum
from app.exceptions.http_exceptions import BadRequestError
from flask import Flask


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

@patch("app.services.customer_service.requests.post")
def test_create_customer_user_service_error(mock_post, mock_customer):
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

@patch("app.repositories.customer_repository.CustomerRepository.get_all")
def test_get_all_customers_no_data(mock_get_all):
    mock_get_all.return_value = []

    with pytest.raises(ValueError, match="No hay clientes registrados"):
        CustomerService.get_all()

@patch("app.repositories.customer_repository.CustomerRepository.get_all")
@patch("app.services.customer_service.requests.get")
def test_get_all_customers_success(mock_requests_get, mock_get_all):
    mock_get_all.return_value = [
        Customer(
            identification_type="CC",
            identification_number=123456789,
            country="Colombia",
            city="Bogotá",
            address="Calle 123",
            user_id="7070484b-34aa-456d-bb51-3b0063a66662"
        ),
        Customer(
            identification_type="CC",
            identification_number=123456789,
            country="Colombia",
            city="Bogotá",
            address="Calle 123",
            user_id="a7f9baae-634d-4641-a3b9-02d4cf501130"
        )
    ]
    mock_requests_get.side_effect = [
        MagicMock(
            status_code=200,
            json=lambda: {
                "data": {
                    "name": "Juan",
                    "lastname": "Pérez",
                    "email": "juan.perez@example.com"
                }
            }
        ),
        MagicMock(
            status_code=200,
            json=lambda: {
                "data": {
                    "name": "Ana",
                    "lastname": "Lozano",
                    "email": "ana.lozano@example.com"
                }
            }
        )
    ]
    app = Flask(__name__)
    with app.test_request_context(headers={"Authorization": "Bearer test_token"}):
        result = CustomerService.get_all()

    assert len(result) == 2
    assert result[0]["name"] == "Juan Pérez"
    assert result[0]["email"] == "juan.perez@example.com"
    assert result[0]["identification_type"] == "CC"
    assert result[0]["identification_number"] == 123456789
    assert result[0]["country"] == "Colombia"
    assert result[0]["city"] == "Bogotá"
    assert result[0]["address"] == "Calle 123"

    assert result[1]["name"] == "Ana Lozano"
    assert result[1]["email"] == "ana.lozano@example.com"
    assert result[1]["identification_type"] == "CC"
    assert result[1]["identification_number"] == 123456789
    assert result[1]["country"] == "Colombia"
    assert result[1]["city"] == "Bogotá"
    assert result[1]["address"] == "Calle 123"

@patch("app.repositories.customer_repository.CustomerRepository.get_all")
@patch("app.services.customer_service.requests.get")
def test_get_all_customers_identification_type(mock_requests_get, mock_get_all):
    customer_enum = Customer(
        identification_type=DocumentTypeEnum.CC,
        identification_number=123456789,
        country="Colombia",
        city="Bogotá",
        address="Calle 123",
        user_id="7070484b-34aa-456d-bb51-3b0063a66662"
    )
    customer_str = Customer(
        identification_type="CC",
        identification_number=987654321,
        country="Colombia",
        city="Medellín",
        address="Carrera 45",
        user_id="a7f9baae-634d-4641-a3b9-02d4cf501130"
    )
    customer_invalid = Customer(
        identification_type=123,  # Tipo inválido
        identification_number=111222333,
        country="Colombia",
        city="Cali",
        address="Calle 10",
        user_id="c8d9b3f2-f8e8-4c8d-9b3f-2f8e8c8d9b3f"
    )
    mock_get_all.return_value = [customer_enum, customer_str, customer_invalid]
    mock_requests_get.side_effect = [
        MagicMock(
            status_code=200,
            json=lambda: {
                "data": {
                    "name": "Juan",
                    "lastname": "Pérez",
                    "email": "juan.perez@example.com"
                }
            }
        ),
        MagicMock(
            status_code=200,
            json=lambda: {
                "data": {
                    "name": "Ana",
                    "lastname": "Lozano",
                    "email": "ana.lozano@example.com"
                }
            }
        ),
        MagicMock(
            status_code=400,
            json=lambda: {"error": "Invalid user ID"}
        )
    ]

    app = Flask(__name__)
    with app.test_request_context(headers={"Authorization": "Bearer test_token"}):
        mock_get_all.return_value = [customer_enum, customer_str]
        result = CustomerService.get_all()
        assert len(result) == 2
        assert result[0]["identification_type"] == "CC"
        assert result[1]["identification_type"] == "CC"
        mock_get_all.return_value = [customer_invalid]
        with pytest.raises(BadRequestError, match="No se pudo obtener los datos del usuario con ID c8d9b3f2-f8e8-4c8d-9b3f-2f8e8c8d9b3f"):
            CustomerService.get_all()