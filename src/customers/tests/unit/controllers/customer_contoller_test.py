import pytest
from flask import Flask
from flask_jwt_extended import JWTManager

from app.controllers.customer_controller import customer_bp
from app.exceptions.http_exceptions import BadRequestError

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "test-secret"
    app.config["TESTING"] = True
    JWTManager(app)
    app.register_blueprint(customer_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_customer_success(mocker, client):
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": "123456789",
        "country": "Colombia",
        "city": "Bogotá",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez@example.com",
            "password": "123456",
            "role": "customer"
        }
    }
    mocker.patch("app.services.customer_service.CustomerService.create", return_value=None)

    response = client.post("/customers/", json=customer_data)

    customer_data["user"].pop("password", None)

    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"
    assert data["data"] == customer_data

def test_create_customer_bad_request_identificationType(mocker, client):
    # Datos simulados para el request (falta campo identificationType)
    customer_data = {
        "identificationNumber": 123456789,
        "country": "Estados Unidos",
        "city": "New York",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez18@example.com",
            "password": "123456"
        }
    }

    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("El tipo de identificación es requerido"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "El tipo de identificación es requerido" in data["error"]

def test_create_customer_bad_request_identificationType_invalid(mocker, client):
    # Datos simulados para el request (campo identificationType inválido)
    customer_data = {
        "identificationType": "INVALID_TYPE",
        "identificationNumber": 123456789,
        "country": "Estados Unidos",
        "city": "New York",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez18@example.com",
            "password": "123456"
        }
    }

    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("El tipo de identificación no es válido, debe ser CC, NIT, CE, DNI o PASSPORT"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "El tipo de identificación no es válido, debe ser CC, NIT, CE, DNI o PASSPORT" in data["error"]

def test_create_customer_bad_request_identificationNumber(mocker, client):
    # Datos simulados para el request (falta campo identificationNumber)
    customer_data = {
        "identificationType": "CC",        
        "country": "Estados Unidos",
        "city": "New York",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez18@example.com",
            "password": "123456"
        }
    }

    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("El número de identificación es requerido"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "El número de identificación es requerido" in data["error"]

def test_create_customer_bad_request_identificationNumber_invalid(mocker, client):
    # Datos simulados para el request (campo identificationNumber inválido)
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": "123456789M",
        "country": "Estados Unidos",
        "city": "New York",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez18@example.com",
            "password": "123456"
        }
    }

    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("El número de identificación no es válido, debe ser un valor numerico"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "El número de identificación no es válido, debe ser un valor numerico" in data["error"]

def test_create_customer_bad_request_country(mocker, client):
    # Datos simulados para el request (falta campo country)
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": 123456789,
        "city": "New York",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez18@example.com",
            "password": "123456"
        }
    }
    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("El país es requerido"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "El país es requerido" in data["error"]

def test_create_customer_bad_request_country_invalid(mocker, client):
    # Datos simulados para el request (campo country inválido)
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": "123456789M",
        "country": "Estados-Unidos",
        "city": "New York",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez18@example.com",
            "password": "123456"
        }
    }
   
    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("El país debe contener solo letras y espacios"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "El país debe contener solo letras y espacios" in data["error"]

def test_create_customer_bad_request_city(mocker, client):
    # Datos simulados para el request (falta campo city)
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": 123456789,
        "country": "Estados Unidos",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez18@example.com",
            "password": "123456"
        }
    }

    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("La ciudad es requerida"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "La ciudad es requerida" in data["error"]

def test_create_customer_bad_request_city_invalid(mocker, client):
    # Datos simulados para el request (campo city inválido)
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": "123456789M",
        "country": "Estados Unidos",
        "city": "New--York",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez18@example.com",
            "password": "123456"
        }
    }

    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("La ciudad debe contener solo letras y espacios"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "La ciudad debe contener solo letras y espacios" in data["error"]

def test_create_customer_bad_request_address(mocker, client):
    # Datos simulados para el request (falta address city)
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": 123456789,
        "country": "Estados Unidos",
        "city": "New York",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez18@example.com",
            "password": "123456"
        }
    }

    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("La dirección es requerida"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "La dirección es requerida" in data["error"]

def test_create_customer_bad_request_user(mocker, client):
    # Datos simulados para el request (falta address user)
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": 123456789,
        "country": "Estados Unidos",
        "city": "New York",
        "address": "Calle 123"
    }

    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("Los datos del cliente son requeridos"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "Los datos del cliente son requeridos" in data["error"]

def test_create_customer_bad_request_name(mocker, client):
    # Datos simulados para el request (falta el campo "name")
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": 123456789,
        "country": "Colombia",
        "city": "Bogotá",
        "address": "Calle 123",
        "user": {
            "lastname": "Pérez",
            "email": "juan.perez@example.com",
            "password": "123456"
        }
    }

    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("El nombre del cliente es requerido"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "El nombre del cliente es requerido" in data["error"]

def test_create_customer_missing_lastname(mocker, client):
    # Datos simulados para el request (falta el campo "lastname")
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": 123456789,
        "country": "Colombia",
        "city": "Bogotá",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "email": "juan.perez@example.com",
            "password": "123456"
        }
    }

    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("El apellido del cliente es requerido"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "El apellido del cliente es requerido" in data["error"]

def test_create_customer_bad_request_password(mocker, client):
    # Datos simulados para el request (falta el campo "password")
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": 123456789,
        "country": "Colombia",
        "city": "Bogotá",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez@example.com"
        }
    }

    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("La contraseña es requerida"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "La contraseña es requerida" in data["error"]

def test_create_customer_bad_request_email(mocker, client):
    # Datos simulados para el request (falta el campo "email")
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": 123456789,
        "country": "Colombia",
        "city": "Bogotá",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "password": "123456"
        }
    }

    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("El email es requerido"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "El email es requerido" in data["error"]

def test_create_customer_bad_request_invalid_email(mocker, client):
    # Datos simulados para el request (email inválido)
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": 123456789,
        "country": "Colombia",
        "city": "Bogotá",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "invalid-email",
            "password": "123456"
        }
    }

    mocker.patch("app.services.customer_service.CustomerService.create", side_effect=BadRequestError("El email no es válido"))

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "El email no es válido" in data["error"]         

def test_create_customer_user_service_error(mocker, client):
    # Datos simulados para el request
    customer_data = {
        "identificationType": "CC",
        "identificationNumber": 123456789,
        "country": "Colombia",
        "city": "Bogotá",
        "address": "Calle 123",
        "user": {
            "name": "Juan",
            "lastname": "Pérez",
            "email": "juan.perez@example.com",
            "password": "123456"
        }
    }

    user_service_error_response = {
        "code": 400,
        "error": "El email no es válido",
        "status": "error"
    }
 
    mocker.patch(
        "app.services.customer_service.requests.post",
        return_value=mocker.Mock(
            status_code=400,
            json=lambda: user_service_error_response
        )
    )

    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert data["error"] == "Error al crear el usuario: El email no es válido"  

def test_get_customers_success(mocker, client):
    # Datos simulados para los clientes
    mock_customers = {
        "code": 200,
        "data": [
            {
                "id": "d3c14118-be62-4084-865d-01c1599bd024",
                "address": "Calle 123",
                "city": "Bogotá",
                "country": "Colombia",      
                "identification_number": 123456789,
                "identification_type": "CC",
                "name": "Ana Villanueva",                
                "email": "ana.villanueva@example.com",  
                "created_at": "2025-04-03T22:30:52.658277",
                "updated_at": "2025-04-03T22:30:52.658277"
            },
            {
                "id": "a49b48ee-d845-4e10-b9e7-dfc5a75af22d",
                "address": "Calle 123",
                "city": "Bogotá",
                "country": "Colombia",
                "name": "Ana Lozano",
                "email": "ana.lozano@example.com",                
                "identification_number": 123456789,
                "identification_type": "CC",
                "created_at": "2025-04-03T22:48:29.275242",
                "updated_at": "2025-04-03T22:48:29.275242",
                
            }
        ],
        "message": "Todos los clientes han sido obtenidos",
        "status": "success"
    }

    mocker.patch("app.services.customer_service.CustomerService.get_all", return_value=mock_customers)

    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)

    response = client.get("/customers/")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert len(data["data"]) == 4

def test_get_customers_no_data(mocker, client):
    mocker.patch("app.services.customer_service.CustomerService.get_all", side_effect=ValueError("No hay clientes registrados"))
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)

    response = client.get("/customers/")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["data"] == []
    assert "No hay clientes registrados" in data["message"]

def test_ping(client):
    response = client.get("/customers/ping")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["message"] == "pong"